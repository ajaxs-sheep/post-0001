#!/usr/bin/env python
"""
Polarization Demonstration - How One Node Splits a Harmonious Community

This script creates clear before/after visualizations showing:
1. Initial: Complete graph where everyone is friends
2. Final: Two-camp structure after polarization
3. Explanation of the energy dynamics and frustration spread
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import networkx as nx

def create_initial_state():
    """Create the initial harmonious state - everyone is friends."""

    # 6 people + 1 polarizing figure (Trump)
    people = ["Alice", "Bob", "Carol", "Dave", "Emma", "Frank"]

    nodes = people + ["Trump"]
    edges = []

    # Complete graph: All people are friends with each other
    for i, person1 in enumerate(people):
        for person2 in people[i+1:]:
            edges.append({
                "source": person1,
                "target": person2,
                "sign": 1,
                "weight": 1.0
            })

    # Trump connections: Half love him, half hate him (FIXED)
    pro_trump = people[:3]  # Alice, Bob, Carol
    anti_trump = people[3:]  # Dave, Emma, Frank

    for person in pro_trump:
        edges.append({
            "source": person,
            "target": "Trump",
            "sign": 1,
            "weight": 1.0,
            "fixed": True
        })

    for person in anti_trump:
        edges.append({
            "source": person,
            "target": "Trump",
            "sign": -1,
            "weight": 1.0,
            "fixed": True
        })

    graph_data = {
        "nodes": nodes,
        "edges": edges,
        "config": {"lambda": 1.0, "alpha": 2.0}
    }

    return graph_data, pro_trump, anti_trump

def create_final_state(pro_trump, anti_trump):
    """Create the final two-camp state after polarization."""

    people = pro_trump + anti_trump
    nodes = people + ["Trump"]
    edges = []

    # Within pro-Trump camp: All positive (friends)
    for i, person1 in enumerate(pro_trump):
        for person2 in pro_trump[i+1:]:
            edges.append({
                "source": person1,
                "target": person2,
                "sign": 1,
                "weight": 1.0
            })

    # Within anti-Trump camp: All positive (friends)
    for i, person1 in enumerate(anti_trump):
        for person2 in anti_trump[i+1:]:
            edges.append({
                "source": person1,
                "target": person2,
                "sign": 1,
                "weight": 1.0
            })

    # Between camps: All negative (enemies)
    for person1 in pro_trump:
        for person2 in anti_trump:
            edges.append({
                "source": person1,
                "target": person2,
                "sign": -1,
                "weight": 1.0
            })

    # Trump connections (same as before, FIXED)
    for person in pro_trump:
        edges.append({
            "source": person,
            "target": "Trump",
            "sign": 1,
            "weight": 1.0,
            "fixed": True
        })

    for person in anti_trump:
        edges.append({
            "source": person,
            "target": "Trump",
            "sign": -1,
            "weight": 1.0,
            "fixed": True
        })

    graph_data = {
        "nodes": nodes,
        "edges": edges,
        "config": {"lambda": 1.0, "alpha": 2.0}
    }

    return graph_data

def visualize_state(graph_data, title, filename, pro_trump, anti_trump):
    """Create a clear visualization of the graph state."""

    fig, ax = plt.subplots(figsize=(14, 12))

    # Build NetworkX graph
    G = nx.Graph()
    for node in graph_data["nodes"]:
        G.add_node(node)

    for edge_data in graph_data["edges"]:
        G.add_edge(
            edge_data["source"],
            edge_data["target"],
            sign=edge_data["sign"],
            fixed=edge_data.get("fixed", False)
        )

    # Layout: Two camps on left/right, Trump at top center
    pos = {}

    # Pro-Trump camp (left side)
    for i, person in enumerate(pro_trump):
        pos[person] = (-2, -i * 1.5)

    # Anti-Trump camp (right side)
    for i, person in enumerate(anti_trump):
        pos[person] = (2, -i * 1.5)

    # Trump at top center
    pos["Trump"] = (0, 1.5)

    # Draw edges
    for u, v, data in G.edges(data=True):
        sign = data["sign"]
        fixed = data.get("fixed", False)

        if sign > 0:
            color = "#2ecc71"  # Green for positive
            style = "solid"
            width = 3
        else:
            color = "#e74c3c"  # Red for negative
            style = "solid"
            width = 3

        if fixed:
            width = 5  # Thicker for fixed edges

        # Draw edge
        edge = FancyArrowPatch(
            pos[u], pos[v],
            arrowstyle="-",
            color=color,
            linewidth=width,
            linestyle=style,
            alpha=0.6 if not fixed else 0.9,
            connectionstyle="arc3,rad=0.0"
        )
        ax.add_patch(edge)

    # Draw nodes
    for node in G.nodes():
        x, y = pos[node]

        if node == "Trump":
            color = "#f39c12"  # Orange for Trump
            size = 1200
        elif node in pro_trump:
            color = "#3498db"  # Blue for pro-Trump
            size = 800
        else:
            color = "#9b59b6"  # Purple for anti-Trump
            size = 800

        # Draw node
        circle = plt.Circle((x, y), 0.3, color=color, ec="black", linewidth=2, zorder=10)
        ax.add_patch(circle)

        # Draw label
        ax.text(x, y, node, ha="center", va="center", fontsize=11,
                fontweight="bold", color="white", zorder=11)

    # Add legend
    legend_elements = [
        mpatches.Patch(color="#2ecc71", label="Positive (Friends)"),
        mpatches.Patch(color="#e74c3c", label="Negative (Enemies)"),
        mpatches.Patch(color="#f39c12", label="Polarizing Figure"),
        mpatches.Patch(color="#3498db", label="Pro-Trump Camp"),
        mpatches.Patch(color="#9b59b6", label="Anti-Trump Camp"),
    ]
    ax.legend(handles=legend_elements, loc="upper right", fontsize=10, framealpha=0.9)

    # Title and styling
    ax.set_title(title, fontsize=18, fontweight="bold", pad=20)
    ax.set_xlim(-4, 4)
    ax.set_ylim(-5, 3)
    ax.axis("off")

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"  ✓ Saved: {filename}")

def create_energy_diagram():
    """Create a diagram showing the energy landscape and hill climbing."""

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6))

    # Left plot: Energy landscape
    ax1.set_title("Energy Landscape: Frustration Over Time", fontsize=14, fontweight="bold")

    # Simulated energy trajectory showing hill climbing
    iterations = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    energy = [9, 13, 15, 14, 12, 8, 5, 2, 1, 0]  # Climbs then descends

    ax1.plot(iterations, energy, marker="o", linewidth=3, markersize=8, color="#3498db")
    ax1.axhline(y=9, color="#e74c3c", linestyle="--", linewidth=2, alpha=0.5, label="Initial Energy")
    ax1.axhline(y=0, color="#2ecc71", linestyle="--", linewidth=2, alpha=0.5, label="Balanced State")

    # Annotate key points
    ax1.annotate("Initial State\n(Harmonious but unstable)",
                xy=(0, 9), xytext=(-0.5, 11),
                fontsize=10, ha="right",
                bbox=dict(boxstyle="round,pad=0.5", facecolor="#ecf0f1", alpha=0.8),
                arrowprops=dict(arrowstyle="->", color="black", lw=1.5))

    ax1.annotate("Hill Climbing\n(Accepting worse states)",
                xy=(2, 15), xytext=(1, 17),
                fontsize=10, ha="center",
                bbox=dict(boxstyle="round,pad=0.5", facecolor="#fff9c4", alpha=0.8),
                arrowprops=dict(arrowstyle="->", color="black", lw=1.5))

    ax1.annotate("Descent to Balance\n(Finding solution)",
                xy=(7, 2), xytext=(7, -2),
                fontsize=10, ha="center",
                bbox=dict(boxstyle="round,pad=0.5", facecolor="#c8e6c9", alpha=0.8),
                arrowprops=dict(arrowstyle="->", color="black", lw=1.5))

    ax1.set_xlabel("Iteration (Edge Flips)", fontsize=12)
    ax1.set_ylabel("Energy (Unbalanced Triangles)", fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=10)

    # Right plot: Triangle balance explanation
    ax2.set_title("How Frustration Spreads: Unbalanced Triangles", fontsize=14, fontweight="bold")
    ax2.axis("off")

    # Example unbalanced triangle
    triangle_pos = {
        "Alice": (0, 1),
        "Dave": (-1, -0.5),
        "Trump": (1, -0.5)
    }

    # Draw triangle
    for i, ((u, v), sign, label) in enumerate([
        (("Alice", "Trump"), 1, "+"),
        (("Dave", "Trump"), -1, "−"),
        (("Alice", "Dave"), 1, "+")
    ]):
        x1, y1 = triangle_pos[u]
        x2, y2 = triangle_pos[v]

        color = "#2ecc71" if sign > 0 else "#e74c3c"

        ax2.plot([x1, x2], [y1, y2], color=color, linewidth=4, alpha=0.7)

        # Add sign label
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        ax2.text(mid_x, mid_y, label, fontsize=16, fontweight="bold",
                bbox=dict(boxstyle="circle,pad=0.3", facecolor="white", edgecolor=color, linewidth=2))

    # Draw nodes
    for node, (x, y) in triangle_pos.items():
        color = "#f39c12" if node == "Trump" else "#3498db"
        circle = plt.Circle((x, y), 0.15, color=color, ec="black", linewidth=2, zorder=10)
        ax2.add_patch(circle)
        ax2.text(x, y, node, ha="center", va="center", fontsize=9,
                fontweight="bold", color="white", zorder=11)

    # Add explanation text
    explanation = (
        "Unbalanced Triangle: (+)(+)(−) = −\n\n"
        "Alice loves Trump (+)\n"
        "Dave hates Trump (−)\n"
        "But Alice and Dave are friends (+)\n\n"
        "This creates FRUSTRATION:\n"
        "\"My friend likes someone I hate!\"\n\n"
        "To resolve: Either Alice breaks with Dave,\n"
        "or Dave breaks with Alice.\n"
        "Either way, the friendship must end."
    )

    ax2.text(0, -2.5, explanation, fontsize=10, ha="center", va="top",
            bbox=dict(boxstyle="round,pad=0.8", facecolor="#ecf0f1", alpha=0.9))

    ax2.set_xlim(-2, 2)
    ax2.set_ylim(-4, 2)

    plt.tight_layout()
    plt.savefig("examples/polarization_demo/energy_dynamics.png", dpi=300, bbox_inches="tight", facecolor="white")
    plt.close()
    print("  ✓ Saved: examples/polarization_demo/energy_dynamics.png")

def main():
    print("=" * 80)
    print("Creating Polarization Demonstration Visualizations")
    print("=" * 80)
    print()

    # Create initial state
    print("1. Creating initial harmonious state...")
    initial_data, pro_trump, anti_trump = create_initial_state()

    with open("examples/polarization_demo/initial_state.json", "w") as f:
        json.dump(initial_data, f, indent=2)
    print("  ✓ Saved: examples/polarization_demo/initial_state.json")

    visualize_state(
        initial_data,
        "Initial State: Harmonious Community\n(Everyone is friends, but split opinions on Trump)",
        "examples/polarization_demo/01_initial_state.png",
        pro_trump,
        anti_trump
    )

    # Create final state
    print("\n2. Creating final two-camp state...")
    final_data = create_final_state(pro_trump, anti_trump)

    with open("examples/polarization_demo/final_state.json", "w") as f:
        json.dump(final_data, f, indent=2)
    print("  ✓ Saved: examples/polarization_demo/final_state.json")

    visualize_state(
        final_data,
        "Final State: Two-Camp Structure\n(Community split into opposing camps)",
        "examples/polarization_demo/02_final_state.png",
        pro_trump,
        anti_trump
    )

    # Create energy diagram
    print("\n3. Creating energy dynamics diagram...")
    create_energy_diagram()

    print("\n" + "=" * 80)
    print("✓ All visualizations created!")
    print("=" * 80)
    print("\nFiles created:")
    print("  - examples/polarization_demo/initial_state.json")
    print("  - examples/polarization_demo/final_state.json")
    print("  - examples/polarization_demo/01_initial_state.png")
    print("  - examples/polarization_demo/02_final_state.png")
    print("  - examples/polarization_demo/energy_dynamics.png")
    print("=" * 80)

if __name__ == "__main__":
    main()
