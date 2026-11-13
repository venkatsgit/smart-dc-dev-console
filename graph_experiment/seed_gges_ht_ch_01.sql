-- Seed data for GGES Knowledge Graph - HT-CH-01 (Asset C_100)
-- Grounded in ASHRAE RP-1043 and Asset-Specific Sensors from sgp7_dev

-- 1. Insert Fault Nodes
INSERT INTO gges_fault_nodes (id, name, description, affected_sensors) VALUES
('CF', 'Condenser Fouling', 'Condenser fouling reduces heat-transfer efficiency by adding thermal resistance to the tubes, increasing approach temperature.', ARRAY['CH-CWS-FLOW', 'CH-CON-RFT-PRES', 'CH-OIL-DIS-TEMP', 'CH-CON-APPROACH-TEMP']),
('RL', 'Refrigerant Leak', 'Refrigerant mass loss causes starvation of the evaporator, leading to low pressure and high superheat.', ARRAY['CH-EVA-RFT-PRES', 'CH-EVA-RFT-TEMP', 'CH-OIL-DIS-TEMP']),
('ROC', 'Refrigerant Overcharge', 'Excess refrigerant causes condenser flooding, increasing subcooling and condensing pressure.', ARRAY['CH-CON-RFT-PRES', 'CH-OIL-DIS-TEMP', 'CH-KW-COMBINED']),
('RCWF', 'Reduced Condenser Water Flow', 'Condenser water flow is reduced by pump or blockage faults, leading to poor heat rejection and high discharge pressure.', ARRAY['CH-CWS-FLOW', 'CH-CON-RFT-PRES', 'CH-OIL-DIS-TEMP']),
('REWF', 'Reduced Evaporator Water Flow', 'Evaporator water flow is reduced by pump or valve faults, reducing cooling capacity and evaporator pressure.', ARRAY['CH-CHWR-FLOW', 'CH-EVA-RFT-PRES', 'CH-KW-COMBINED']),
('NC', 'Non-Condensable Gases', 'Non-condensible gases (like air) trapped in the condenser increase pressure and discharge temperature without flooding.', ARRAY['CH-CON-RFT-PRES', 'CH-OIL-DIS-TEMP', 'CH-KW-COMBINED'])
ON CONFLICT (id) DO UPDATE SET 
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    affected_sensors = EXCLUDED.affected_sensors;

-- 2. Insert Symptom Nodes (Total 14 as per Paper)
INSERT INTO gges_symptom_nodes (id, name, sensor_id, direction, formula_logic, formula_description) VALUES
-- Direct Sensors
('PRC_rise', 'Condenser Pressure Rise', 'C_100_2410', 1, 'z_score(CH-CON-RFT-PRES) > tau_strong', 'Rise in Condenser Refrigerant Pressure (CH-CON-RFT-PRES)'),
('PRE_drop', 'Evaporator Pressure Drop', 'C_100_2405', -1, 'z_score(CH-EVA-RFT-PRES) < -tau_strong', 'Drop in Evaporator Refrigerant Pressure (CH-EVA-RFT-PRES)'),
('TRdis_rise', 'Discharge Temperature Rise', 'C_100_2414', 1, 'z_score(CH-OIL-DIS-TEMP) > tau_strong', 'Rise in Compressor Discharge Temperature (using CH-OIL-DIS-TEMP as proxy)'),
('Tsuc_rise', 'Suction Temperature Rise', 'C_100_2403', 1, 'z_score(CH-EVA-RFT-TEMP) > tau_strong', 'Rise in Suction Temperature (using CH-EVA-RFT-TEMP as proxy)'),
('Tsuc_drop', 'Suction Temperature Drop', 'C_100_2403', -1, 'z_score(CH-EVA-RFT-TEMP) < -tau_strong', 'Drop in Suction Temperature (using CH-EVA-RFT-TEMP as proxy)'),
('FWC_drop', 'Condenser Flow Drop', 'C_100_2029', -1, 'z_score(CH-CWS-FLOW) < -tau_strong', 'Drop in Condenser Water Flow (CH-CWS-FLOW)'),
('FWE_drop', 'Evaporator Flow Drop', 'C_100_2028', -1, 'z_score(CH-CHWR-FLOW) < -tau_strong', 'Drop in Chilled Water Flow (CH-CHWR-FLOW)'),
('kW_rise', 'Compressor Power Rise', 'C_100_2919_MD', 1, 'z_score(CH-KW-COMBINED) > tau_strong', 'Rise in Compressor Power (CH-KW-COMBINED)'),

-- Derived / Complex Symptoms
('TRCsub_rise', 'Subcooling Rise', NULL, 1, 'z_score(SaturationTemp(PRC) - LiquidTemp) > tau_strong', 'Rise in Subcooling (Calculated from Pressure and Temperature)'),
('TRCsub_drop', 'Subcooling Drop', NULL, -1, 'z_score(SaturationTemp(PRC) - LiquidTemp) < -tau_strong', 'Drop in Subcooling (Calculated from Pressure and Temperature)'),
('fdir_starve', 'Starvation Indicator (fdir+)', NULL, 1, 'z_Tsuc - (z_TRdis^2 + z_TRCsub^2) > 0', 'Positive fdir: Suction Temp Rise > High-Side Rise (Starvation Pattern)'),
('fdir_flood', 'Flooding Indicator (fdir-)', NULL, -1, 'z_Tsuc - (z_TRdis^2 + z_TRCsub^2) < 0', 'Negative fdir: Suction Temp Drop > High-Side Rise (Flooding Pattern)'),
('Qbal_error', 'Heat Balance Residual', NULL, 1, 'abs(Q_evap + kW - Q_cond) > threshold', 'Thermodynamic inconsistency in Heat Balance (Q_evap + kW - Q_cond)'),
('flow_collapse', 'Total Flow Collapse', NULL, -1, 'z_FWC < -2.0 AND z_FWE < -2.0', 'Simultaneous drop in both water loops (Pump/System Failure)')
ON CONFLICT (id) DO UPDATE SET 
    name = EXCLUDED.name,
    sensor_id = EXCLUDED.sensor_id,
    direction = EXCLUDED.direction,
    formula_logic = EXCLUDED.formula_logic,
    formula_description = EXCLUDED.formula_description;

-- 3. Insert Edges (Expert Weights from SSRN-7656122 Table 6 & GGES Logic)
INSERT INTO gges_edges (fault_id, symptom_id, relation_type, weight) VALUES
-- NC (Non-Condensable Gases)
('NC', 'PRC_rise', 'indicates', 8.0),
('NC', 'TRdis_rise', 'indicates', 8.0),
('NC', 'TRdis_rise', 'distinguishes', 1.0),
('NC', 'TRCsub_rise', 'indicates', 6.0),
('NC', 'fdir_flood', 'indicates', 4.0),

-- ROC (Refrigerant Overcharge)
('ROC', 'PRC_rise', 'indicates', 8.0),
('ROC', 'TRCsub_rise', 'indicates', 8.0),
('ROC', 'fdir_flood', 'indicates', 6.0),

-- RCWF (Reduced Condenser Water Flow)
('RCWF', 'FWC_drop', 'indicates', 10.0),
('RCWF', 'FWC_drop', 'distinguishes', 1.0),
('RCWF', 'PRC_rise', 'indicates', 7.0),
('RCWF', 'TRdis_rise', 'indicates', 6.0),

-- REWF (Reduced Evaporator Water Flow)
('REWF', 'FWE_drop', 'indicates', 10.0),
('REWF', 'FWE_drop', 'distinguishes', 1.0),
('REWF', 'PRE_drop', 'indicates', 6.0),
('REWF', 'kW_rise', 'indicates', 4.0),

-- CF (Condenser Fouling)
('CF', 'FWC_drop', 'indicates', 7.0),
('CF', 'PRC_rise', 'indicates', 8.0),
('CF', 'TRdis_rise', 'indicates', 7.0),
('CF', 'Qbal_error', 'indicates', 8.0),

-- RL (Refrigerant Leak)
('RL', 'PRE_drop', 'indicates', 10.0),
('RL', 'Tsuc_rise', 'indicates', 8.0),
('RL', 'Tsuc_rise', 'distinguishes', 1.0),
('RL', 'TRCsub_drop', 'indicates', 8.0),
('RL', 'fdir_starve', 'indicates', 6.0)
ON CONFLICT (fault_id, symptom_id, relation_type) DO UPDATE SET 
    weight = EXCLUDED.weight;
