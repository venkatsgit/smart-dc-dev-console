import numpy as np
import networkx as nx
from typing import Dict, List, Tuple, Any

class ChillerGGESEngine:
    """
    Chiller Graph-Grounded Evidence Scoring (GGES) Engine.
    
    This engine implements a physics-informed diagnostic logic that converts 
    sensor deviations (z-scores) into directional symptoms and evaluates 
    competing fault hypotheses using a knowledge graph.
    """

    def __init__(self, beta: float = 2.0, gamma: float = 0.5, theta_min: float = 0.5, 
                 tau_weak: float = 0.3, tau_strong: float = 1.5):
        """
        Initialize the GGES Engine with thermodynamic hyperparameters.
        
        Args:
            beta: Bonus multiplier for 'distinguishes' edges (discriminative symptoms).
            gamma: Penalty multiplier for 'contradictory' physical evidence.
            theta_min: Minimum confidence threshold for a valid diagnosis.
            tau_weak: Noise floor threshold (z-score multiplier for activation start).
            tau_strong: Strong evidence threshold (z-score multiplier for 100% activation).
            
        Note: If using p997 (3-sigma) as a reference, tau_weak=0.3 corresponds to 0.9 sigma,
        and tau_strong=1.5 corresponds to 4.5 sigma.
        """
        self.beta = beta
        self.gamma = gamma
        self.theta_min = theta_min
        self.tau_weak = tau_weak
        self.tau_strong = tau_strong
        
        # Initialize Directed Multigraph
        # Edge Direction: [Fault] --(indicates)--> [Symptom]
        # This represents physical causality (The Fault causes the Symptom).
        self.G = nx.MultiDiGraph()
        self.faults = []
        self.symptoms = {}
        
        self._build_demo_graph()

    def _build_demo_graph(self):
        """
        Builds a demonstration graph representing a subset of ASHRAE chiller faults.
        Focuses on demonstrating:
        1. 'indicates' edges (supporting evidence)
        2. 'distinguishes' edges (bonus for unique symptoms)
        3. Penalty logic (handled during scoring for opposite sensor directions)
        """
        
        # 1. Fault Nodes
        self.faults = ["NC", "ROC", "RCWF"]
        # NC: Non-Condensable Gases (Unseen)
        # ROC: Refrigerant Overcharge (Known)
        # RCWF: Reduced Condenser Water Flow (Unseen)
        
        for f in self.faults:
            self.G.add_node(f, node_type="Fault")

        # 2. Symptom Nodes & Physical Directions (+1: rise, -1: drop)
        # Format: symptom_id: (sensor_name, direction)
        self.symptoms = {
            "PRC_rise": ("PRC", +1),    # Condenser Pressure
            "TRCsub_rise": ("TRCsub", +1), # Liquid Subcooling
            "TRdis_rise": ("TRdis", +1),   # Discharge Temperature
            "FWC_drop": ("FWC", -1),       # Condenser Water Flow
            "fdir_flooding": ("fdir", -1), # Flooding indicator (e.g. ROC)
        }

        for s_name, (sensor, direction) in self.symptoms.items():
            self.G.add_node(s_name, node_type="Symptom", sensor=sensor, direction=direction)

        # 3. Edges (indicates vs distinguishes)
        
        # --- NC (Non-Condensable Gases) ---
        # High pressure and high subcooling indicate NC
        self.G.add_edge("NC", "PRC_rise", relation="indicates", weight=8.0)
        self.G.add_edge("NC", "TRCsub_rise", relation="indicates", weight=6.0)
        # discharge temperature rise is a KEY discriminator between NC and ROC
        self.G.add_edge("NC", "TRdis_rise", relation="indicates", weight=8.0)
        self.G.add_edge("NC", "TRdis_rise", relation="distinguishes") 

        # --- ROC (Refrigerant Overcharge) ---
        # Similar to NC, it shows high pressure and high subcooling
        self.G.add_edge("ROC", "PRC_rise", relation="indicates", weight=8.0)
        self.G.add_edge("ROC", "TRCsub_rise", relation="indicates", weight=8.0)
        # But ROC is characterized by flooding (fdir-)
        self.G.add_edge("ROC", "fdir_flooding", relation="indicates", weight=6.0)

        # --- RCWF (Reduced Condenser Water Flow) ---
        # Characterized by flow drop and pressure rise
        self.G.add_edge("RCWF", "FWC_drop", relation="indicates", weight=10.0)
        self.G.add_edge("RCWF", "PRC_rise", relation="indicates", weight=7.0)

    def symptom_activation(self, sensor_z_scores: Dict[str, float]) -> Dict[str, Dict[str, Any]]:
        """
        Converts raw z-scores into normalized symptom activations.
        """
        active_symptoms = {}
        for node, attrs in self.G.nodes(data=True):
            if attrs.get("node_type") != "Symptom":
                continue
            
            sensor = attrs["sensor"]
            expected_dir = attrs["direction"]
            z = sensor_z_scores.get(sensor, 0.0)
            
            # a_s > 0: Supportive (sensor moved in expected direction)
            # a_s < 0: Contradictory (sensor moved in opposite direction)
            a_s = expected_dir * z
            
            # Piecewise linear activation [0, 1]
            mag = abs(a_s)
            if mag < self.tau_weak:
                conf = 0.0
            elif mag >= self.tau_strong:
                conf = 1.0
            else:
                conf = (mag - self.tau_weak) / (self.tau_strong - self.tau_weak)
            
            active_symptoms[node] = {
                "conf": conf,
                "supportive": (a_s > 0),
                "raw_z": z
            }
        return active_symptoms

    def diagnose(self, sensor_z_scores: Dict[str, float]) -> Dict[str, Any]:
        """
        Evaluates the knowledge graph to diagnose the most likely fault.
        """
        sal = self.symptom_activation(sensor_z_scores)
        scores = {}

        for f in self.faults:
            support_score = 0.0
            distinguish_bonus = 0.0
            contradict_penalty = 0.0
            
            # Look at all outgoing edges from the fault node
            for _, symptom_node, data in self.G.out_edges(f, data=True):
                s_info = sal.get(symptom_node, {"conf": 0.0, "supportive": True})
                conf = s_info["conf"]
                
                if conf == 0:
                    continue
                
                relation = data.get("relation")
                
                if relation == "indicates":
                    weight = data.get("weight", 1.0)
                    if s_info["supportive"]:
                        support_score += weight * conf
                    else:
                        # Apply penalty for contradictory evidence
                        contradict_penalty += self.gamma * (weight * conf)
                        
                elif relation == "distinguishes":
                    # Distinguishing bonus only applies if symptom is supportive
                    if s_info["supportive"]:
                        distinguish_bonus += self.beta * conf
            
            scores[f] = support_score + distinguish_bonus - contradict_penalty

        # Find the best fault
        top_fault = max(scores, key=scores.get)
        top_score = scores[top_fault]
        
        verdict = top_fault if top_score >= self.theta_min else "Unresolved"
        
        return {
            "verdict": verdict,
            "top_score": round(top_score, 2),
            "all_scores": {k: round(v, 2) for k, v in scores.items()},
            "active_symptoms": {k: v for k, v in sal.items() if v["conf"] > 0}
        }

if __name__ == "__main__":
    engine = ChillerGGESEngine()
    
    print("--- Scenario 1: Non-Condensable Gases (NC) ---")
    # NC symptoms: PRC rise, TRCsub rise, TRdis rise. 
    # TRdis rise is the discriminator.
    z_nc = {
        "PRC": 2.0,    # Strong rise
        "TRCsub": 1.8, # Strong rise
        "TRdis": 2.2,  # Strong rise (NC bonus!)
        "FWC": 0.0,    # Normal
        "fdir": 0.0    # Normal
    }
    result_nc = engine.diagnose(z_nc)
    print(f"Verdict: {result_nc['verdict']} (Score: {result_nc['top_score']})")
    print(f"All Scores: {result_nc['all_scores']}")
    
    print("\n--- Scenario 2: Refrigerant Overcharge (ROC) ---")
    # ROC symptoms: PRC rise, TRCsub rise, fdir flooding.
    z_roc = {
        "PRC": 2.0,
        "TRCsub": 1.8,
        "TRdis": 0.0,   # TRdis doesn't rise in ROC
        "fdir": -2.0    # Flooding (Strong ROC indicator)
    }
    result_roc = engine.diagnose(z_roc)
    print(f"Verdict: {result_roc['verdict']} (Score: {result_roc['top_score']})")
    print(f"All Scores: {result_roc['all_scores']}")

    print("\n--- Scenario 3: Contradictory Evidence ---")
    # Suppose PRC drops when it should rise for NC
    z_contra = {
        "PRC": -2.0,   # CONTRADICTION for all faults in our demo
        "TRdis": 2.0
    }
    result_contra = engine.diagnose(z_contra)
    print(f"Verdict: {result_contra['verdict']} (Score: {result_contra['top_score']})")
    print(f"All Scores: {result_contra['all_scores']}")
