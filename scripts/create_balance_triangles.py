import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np

# Create a figure with multiple subplots for balance theory triangles
fig = plt.figure(figsize=(16, 10))

def draw_triangle(ax, title, labels, edges, subtitle=""):
    """
    Draw a triangle with labeled vertices and signed edges.
    
    labels: dict with keys 'top', 'left', 'right'
    edges: dict with tuples as keys (e.g., ('top', 'left')) and '+' or '-' as values
    """
    # Triangle vertices
    vertices = {
        'top': (0.5, 0.85),
        'left': (0.15, 0.25),
        'right': (0.85, 0.25)
    }
    
    # Draw edges with colors
    edge_pairs = [
        ('top', 'left'),
        ('top', 'right'),
        ('left', 'right')
    ]
    
    for v1, v2 in edge_pairs:
        x_vals = [vertices[v1][0], vertices[v2][0]]
        y_vals = [vertices[v1][1], vertices[v2][1]]
        
        sign = edges.get((v1, v2), edges.get((v2, v1), '+'))
        color = 'green' if sign == '+' else 'red'
        linewidth = 3
        
        # Draw line
        ax.plot(x_vals, y_vals, color=color, linewidth=linewidth, zorder=1)
        
        # Add sign label at midpoint
        mid_x = (vertices[v1][0] + vertices[v2][0]) / 2
        mid_y = (vertices[v1][1] + vertices[v2][1]) / 2
        
        # Offset the label slightly
        if v1 == 'left' and v2 == 'right':
            mid_y -= 0.05
        elif v1 == 'top' and v2 == 'left':
            mid_x -= 0.05
        else:
            mid_x += 0.05
            
        ax.text(mid_x, mid_y, sign, fontsize=18, fontweight='bold', 
                color=color, ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=color, linewidth=2))
    
    # Draw vertices as circles
    for pos_name, (x, y) in vertices.items():
        circle = plt.Circle((x, y), 0.08, color='lightblue', ec='black', linewidth=2, zorder=2)
        ax.add_patch(circle)
        
        # Add labels
        label = labels[pos_name]
        if pos_name == 'top':
            y_offset = 0.12
        else:
            y_offset = -0.12
        ax.text(x, y + y_offset, label, fontsize=14, ha='center', va='center', fontweight='bold')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title(title, fontsize=16, fontweight='bold', pad=10)
    if subtitle:
        ax.text(0.5, 0.05, subtitle, fontsize=11, ha='center', style='italic', color='gray')

# 1. General structure
ax1 = fig.add_subplot(2, 3, 1)
draw_triangle(
    ax1,
    "General Structure",
    {'top': 'Subject', 'left': 'Model', 'right': 'Object'},
    {('top', 'left'): '+/-', ('left', 'right'): '+/-', ('top', 'right'): '+/-'},
    "Subject's relation to Model and Object"
)

# 2. Stable: All positive (+ + +)
ax2 = fig.add_subplot(2, 3, 2)
draw_triangle(
    ax2,
    "Stable: All Positive (+ + +)",
    {'top': 'Subject', 'left': 'Model', 'right': 'Object'},
    {('top', 'left'): '+', ('left', 'right'): '+', ('top', 'right'): '+'},
    "I like my model; my model likes X; I like X"
)

# 3. Stable: Two negative (+ - -)
ax3 = fig.add_subplot(2, 3, 3)
draw_triangle(
    ax3,
    "Stable: Us vs Them (+ - -)",
    {'top': 'Subject', 'left': 'Model', 'right': 'Object'},
    {('top', 'left'): '+', ('left', 'right'): '-', ('top', 'right'): '-'},
    "My ally and I both dislike X"
)

# 4. Unstable: Two positive, one negative (+ + -)
ax4 = fig.add_subplot(2, 3, 4)
draw_triangle(
    ax4,
    "Unstable: Conflicted (+ + -)",
    {'top': 'Subject', 'left': 'Model', 'right': 'Object'},
    {('top', 'left'): '+', ('left', 'right'): '+', ('top', 'right'): '-'},
    "I like my model; my model likes X; but I dislike X"
)

# 5. Unstable: All negative (- - -)
ax5 = fig.add_subplot(2, 3, 5)
draw_triangle(
    ax5,
    "Unstable: All Negative (- - -)",
    {'top': 'Subject', 'left': 'Model', 'right': 'Object'},
    {('top', 'left'): '-', ('left', 'right'): '-', ('top', 'right'): '-'},
    "Everyone hates everyone"
)

# 6. Trump-Coke example (unstable)
ax6 = fig.add_subplot(2, 3, 6)
draw_triangle(
    ax6,
    "Trump-Coke Example (Unstable)",
    {'top': 'Liberal', 'left': 'Trump', 'right': 'Diet Coke'},
    {('top', 'left'): '-', ('left', 'right'): '+', ('top', 'right'): '?'},
    "Liberal dislikes Trump; Trump likes Diet Coke; Liberal must choose"
)

plt.suptitle("Balance Theory: Stable and Unstable Triads", fontsize=20, fontweight='bold', y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('balance_theory_triangles.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Saved balance_theory_triangles.png")

# Create a second figure showing the resolution options for the Trump-Coke example
fig2, axes = plt.subplots(1, 3, figsize=(18, 6))

# Option 1: Liberal switches to negative on Coke (stable + - -)
draw_triangle(
    axes[0],
    "Option 1: Boycott Coke",
    {'top': 'Liberal', 'left': 'Trump', 'right': 'Diet Coke'},
    {('top', 'left'): '-', ('left', 'right'): '+', ('top', 'right'): '-'},
    "Liberal stops drinking Diet Coke → Stable (+ - -)"
)

# Option 2: Coke distances from Trump (stable + - -)
draw_triangle(
    axes[1],
    "Option 2: Coke Distances from Trump",
    {'top': 'Liberal', 'left': 'Trump', 'right': 'Diet Coke'},
    {('top', 'left'): '-', ('left', 'right'): '-', ('top', 'right'): '+'},
    "Coke denounces Trump → Stable (+ - -)"
)

# Option 3: Liberal switches to positive on Trump (stable all +)
draw_triangle(
    axes[2],
    "Option 3: Liberal Changes View of Trump",
    {'top': 'Liberal', 'left': 'Trump', 'right': 'Diet Coke'},
    {('top', 'left'): '+', ('left', 'right'): '+', ('top', 'right'): '+'},
    "Liberal starts liking Trump → Stable (+ + +) [Unlikely!]"
)

plt.suptitle("Resolving the Trump-Diet Coke Imbalance", fontsize=20, fontweight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('trump_coke_resolution.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Saved trump_coke_resolution.png")

print("Triangle illustrations created successfully!")
