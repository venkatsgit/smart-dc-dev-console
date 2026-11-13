"""
Load GGES fault/symptom/edge tables from sgp7_dev and render a knowledge-graph image.

Usage:
  python render_gges_graph.py
  python render_gges_graph.py --out gges_fault_symptom_graph.jpg

Reads DB settings from env vars (or defaults matching SGP7 .devenv):
  PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import psycopg2
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch


DEFAULT_OUT = Path(__file__).resolve().parent / "gges_fault_symptom_graph.jpg"


def get_connection():
    return psycopg2.connect(
        host=os.getenv("PGHOST", "c.kdch-sg-aiml-postgresql-dev-02.postgres.database.azure.com"),
        port=os.getenv("PGPORT", "5432"),
        user=os.getenv("PGUSER", "kdchdb005"),
        password=os.getenv("PGPASSWORD", "2Tc2AUypdnFr"),
        dbname=os.getenv("PGDATABASE", "citus"),
        sslmode=os.getenv("PGSSLMODE", "require"),
    )


def load_graph_data(conn):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, name
            FROM sgp7_dev.gges_fault_nodes
            ORDER BY id
            """
        )
        faults = [{"id": r[0], "name": r[1]} for r in cur.fetchall()]

        cur.execute(
            """
            SELECT id, name, sensor_id, direction, formula_description
            FROM sgp7_dev.gges_symptom_nodes
            ORDER BY id
            """
        )
        symptoms = [
            {
                "id": r[0],
                "name": r[1],
                "sensor_id": r[2],
                "direction": r[3],
                "formula_description": r[4],
            }
            for r in cur.fetchall()
        ]

        cur.execute(
            """
            SELECT fault_id, symptom_id, relation_type, weight
            FROM sgp7_dev.gges_edges
            ORDER BY fault_id, relation_type, weight DESC
            """
        )
        edges = [
            {
                "fault_id": r[0],
                "symptom_id": r[1],
                "relation_type": r[2],
                "weight": float(r[3]),
            }
            for r in cur.fetchall()
        ]

    return faults, symptoms, edges


def build_graph(faults, symptoms, edges) -> nx.MultiDiGraph:
    G = nx.MultiDiGraph()
    for f in faults:
        G.add_node(f["id"], node_type="fault", label=f"{f['id']}\n{f['name']}")
    for s in symptoms:
        kind = "direct" if s["sensor_id"] else "derived"
        arrow = "↑" if s["direction"] == 1 else "↓"
        sensor_bit = s["sensor_id"] or "derived"
        G.add_node(
            s["id"],
            node_type="symptom",
            kind=kind,
            label=f"{s['id']} {arrow}\n{sensor_bit}",
        )
    for e in edges:
        G.add_edge(
            e["fault_id"],
            e["symptom_id"],
            relation=e["relation_type"],
            weight=e["weight"],
        )
    return G


def layout_positions(faults, symptoms):
    """Two-column layout: faults left, symptoms right."""
    pos = {}
    n_f = max(len(faults), 1)
    n_s = max(len(symptoms), 1)
    for i, f in enumerate(faults):
        y = 1.0 - (i + 0.5) / n_f
        pos[f["id"]] = (0.12, y)
    for i, s in enumerate(symptoms):
        y = 1.0 - (i + 0.5) / n_s
        pos[s["id"]] = (0.78, y)
    return pos


def render_graph(G, faults, symptoms, edges, out_path: Path):
    pos = layout_positions(faults, symptoms)
    fig, ax = plt.subplots(figsize=(16, 10), dpi=160)
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.05, 1.12)
    ax.axis("off")
    ax.set_title(
        "GGES Fault–Symptom Knowledge Graph (loaded from sgp7_dev tables)",
        fontsize=16,
        fontweight="bold",
        color="#1f3a5f",
        pad=18,
    )

    # Column headers
    ax.text(0.12, 1.05, "Fault Nodes", ha="center", fontsize=12, fontweight="bold", color="#1f3a5f")
    ax.text(0.78, 1.05, "Symptom Nodes", ha="center", fontsize=12, fontweight="bold", color="#1f3a5f")

    # Draw edges first
    for e in edges:
        x1, y1 = pos[e["fault_id"]]
        x2, y2 = pos[e["symptom_id"]]
        is_dist = e["relation_type"] == "distinguishes"
        color = "#2e7d32" if is_dist else "#4a6fa5"
        style = (0, (4, 3)) if is_dist else "solid"
        lw = 2.0 if is_dist else 1.3
        ax.annotate(
            "",
            xy=(x2 - 0.07, y2),
            xytext=(x1 + 0.07, y1),
            arrowprops=dict(
                arrowstyle="-|>",
                color=color,
                lw=lw,
                linestyle=style,
                connectionstyle="arc3,rad=0.05",
            ),
        )
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2
        if is_dist:
            label = "distinguishes"
        else:
            label = f"indicates w={e['weight']:g}"
        ax.text(mx, my + 0.008, label, fontsize=6.5, color=color, ha="center", va="bottom", alpha=0.9)

    # Draw fault boxes
    for f in faults:
        x, y = pos[f["id"]]
        box = FancyBboxPatch(
            (x - 0.07, y - 0.035),
            0.14,
            0.07,
            boxstyle="round,pad=0.008,rounding_size=0.02",
            linewidth=1.5,
            edgecolor="#1f3a5f",
            facecolor="#d6e4f5",
        )
        ax.add_patch(box)
        ax.text(x, y, f"{f['id']}\n{f['name']}", ha="center", va="center", fontsize=7.5, color="#102a43")

    # Draw symptom boxes
    for s in symptoms:
        x, y = pos[s["id"]]
        is_direct = bool(s["sensor_id"])
        face = "#e8f5e9" if is_direct else "#fff3e0"
        edge = "#2e7d32" if is_direct else "#ef6c00"
        arrow = "↑" if s["direction"] == 1 else "↓"
        sensor_bit = s["sensor_id"] or "derived formula"
        box = FancyBboxPatch(
            (x - 0.09, y - 0.028),
            0.18,
            0.056,
            boxstyle="round,pad=0.006,rounding_size=0.015",
            linewidth=1.3,
            edgecolor=edge,
            facecolor=face,
        )
        ax.add_patch(box)
        ax.text(
            x,
            y,
            f"{s['id']} {arrow}\n{sensor_bit}",
            ha="center",
            va="center",
            fontsize=7,
            color="#102a43",
        )

    legend = [
        Line2D([0], [0], color="#4a6fa5", lw=2, label="indicates (weight w0)"),
        Line2D([0], [0], color="#2e7d32", lw=2, linestyle=(0, (4, 3)), label="distinguishes (beta bonus)"),
        Line2D([0], [0], marker="s", color="w", markerfacecolor="#e8f5e9",
               markeredgecolor="#2e7d32", markersize=10, label="direct sensor symptom"),
        Line2D([0], [0], marker="s", color="w", markerfacecolor="#fff3e0",
               markeredgecolor="#ef6c00", markersize=10, label="derived symptom"),
    ]
    ax.legend(handles=legend, loc="lower center", ncol=4, frameon=False, fontsize=9, bbox_to_anchor=(0.5, -0.02))

    counts = f"Faults: {len(faults)}  |  Symptoms: {len(symptoms)}  |  Edges: {len(edges)}"
    ax.text(0.5, -0.04, counts, ha="center", fontsize=9, color="#486581")

    out_path = Path(out_path)
    fig.tight_layout()
    fig.savefig(out_path, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return out_path


def main():
    parser = argparse.ArgumentParser(description="Render GGES graph from sgp7_dev tables")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="Output image path (.jpg/.png)")
    args = parser.parse_args()

    conn = get_connection()
    try:
        faults, symptoms, edges = load_graph_data(conn)
    finally:
        conn.close()

    if not faults or not symptoms:
        raise SystemExit("No fault/symptom rows found in sgp7_dev.gges_* tables.")

    G = build_graph(faults, symptoms, edges)
    out = render_graph(G, faults, symptoms, edges, args.out)

    print(f"Loaded {len(faults)} faults, {len(symptoms)} symptoms, {len(edges)} edges")
    print("Symptoms:")
    for s in symptoms:
        kind = "direct" if s["sensor_id"] else "derived"
        print(f"  - {s['id']:14} [{kind:7}] dir={s['direction']:+d}  {s['sensor_id'] or '-'}")
    print(f"Wrote: {out}")


if __name__ == "__main__":
    main()
