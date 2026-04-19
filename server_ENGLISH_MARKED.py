"""
server.py - Mesa Visualization Server

Provides a web interface to observe the Cultural Segregation Model in real-time.

MODIFICATION SUMMARY:
- Displays cultural background using color gradient (red=traditional, blue=modern)
- Size of agents represents social connection (large=many friends, small=isolated)
- Charts show the impact of the conflict mechanism:
  * Conflict and isolation trends
  * Friendship network changes
  * Cultural diversity decline
  * Psychological health deterioration
"""

from mesa.visualization import VisualizationServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from model_ENGLISH_MARKED import CampusModel
from agent_ENGLISH_MARKED import InternationalStudent


def agent_draw(agent):
    """
    Define how agents are rendered on the canvas.
    
    🔴 MODIFICATION: Visualization designed to show the effects of conflict:
    - Color: Represents cultural background (red=traditional, blue=modern)
    - Size: Represents social connection (large=connected, small=isolated)
    - Opacity: Represents isolation (darker=more isolated)
    
    This makes it easy to see segregation happening in real-time.
    """
    if agent is None:
        return
    
    # Color based on cultural characteristics
    culture_mean = sum(agent.culture) / len(agent.culture)  # Range: 0-1
    
    # Size based on social connection
    size = 5 + agent.social_connection * 5
    
    # Color gradient: Red (traditional) → Blue (modern)
    if culture_mean < 0.5:
        # Red side (traditional)
        r = 200
        g = int(100 + 100 * culture_mean / 0.5)
        b = int(100 + 100 * culture_mean / 0.5)
    else:
        # Blue side (modern)
        r = int(200 - 100 * (culture_mean - 0.5) / 0.5)
        g = int(150 - 50 * (culture_mean - 0.5) / 0.5)
        b = 200
    
    # Opacity based on isolation (isolated students appear faded)
    opacity = 1.0 - 0.3 * agent.isolation
    
    return {
        "shape": "circle",
        "color": f"rgba({r},{g},{b},{opacity})",
        "size": size,
    }


# ==================== VISUALIZATION COMPONENTS ====================

# Canvas to display campus grid
campus_canvas = CanvasGrid(
    agent_draw,
    50,      # Grid width
    50,      # Grid height
    500,     # Canvas width (pixels)
    500      # Canvas height (pixels)
)

# 🔴 MODIFICATION: Chart 1 - Shows impact of conflict mechanism
conflict_chart = ChartModule(
    [
        {"Label": "Total_Conflicts_Per_Week", "Color": "Red"},
        {"Label": "Average_Isolation", "Color": "Orange"},
        {"Label": "Average_Stress", "Color": "Pink"},
    ],
    data_collector_name="datacollector",
    canvas_height=200,
    canvas_width=500,
)

# 🔴 MODIFICATION: Chart 2 - Shows friendship network changes
friendship_chart = ChartModule(
    [
        {"Label": "Average_Social_Connection", "Color": "Green"},
        {"Label": "Total_Friendships", "Color": "Blue"},
        {"Label": "Cross_Cultural_Friendships", "Color": "Purple"},
    ],
    data_collector_name="datacollector",
    canvas_height=200,
    canvas_width=500,
)

# 🔴 MODIFICATION: Chart 3 - Shows cultural diversity decline
diversity_chart = ChartModule(
    [
        {"Label": "Cultural_Diversity", "Color": "Gold"},
        {"Label": "Cultural_Clustering", "Color": "Brown"},
    ],
    data_collector_name="datacollector",
    canvas_height=200,
    canvas_width=500,
)

# 🔴 MODIFICATION: Chart 4 - Shows psychological health and dropouts
health_chart = ChartModule(
    [
        {"Label": "Total_Students", "Color": "Blue"},
        {"Label": "Dropouts", "Color": "Black"},
        {"Label": "Average_Psychological_Health", "Color": "Green"},
    ],
    data_collector_name="datacollector",
    canvas_height=200,
    canvas_width=500,
)


# ==================== MODEL PARAMETERS ====================

model_params = {
    "num_students": {
        "type": "SliderInt",
        "value": 100,
        "label": "Number of Students:",
        "min": 20,
        "max": 300,
        "step": 10,
    },
    "width": 50,
    "height": 50,
    "culture_dim": 5,
    "similarity_threshold": {
        "type": "Slider",
        "value": 0.3,
        "label": "Friendship Threshold (distance < this = friendly):",
        "min": 0.1,
        "max": 0.5,
        "step": 0.05,
    },
    "conflict_threshold": {
        "type": "Slider",
        "value": 0.7,
        "label": "Conflict Threshold (distance > this = conflict):",
        "min": 0.5,
        "max": 0.9,
        "step": 0.05,
    },
}


# ==================== START SERVER ====================

if __name__ == "__main__":
    server = VisualizationServer(
        model_class=CampusModel,
        model_params=model_params,
        name="International Students Cultural Segregation Model",
    )
    
    print("=" * 70)
    print("🌍 INTERNATIONAL STUDENTS MODEL - VISUALIZATION SERVER")
    print("=" * 70)
    print("\n✨ Server is running!")
    print("📍 Open your browser to: http://localhost:8521")
    print("\n📊 Charts explain the modification:")
    print("  1. Conflict Chart: Shows how conflicts decrease as segregation")
    print("     completes (students stop interacting with different cultures)")
    print("\n  2. Friendship Chart: Shows how cross-cultural friendships decline")
    print("     due to conflict avoidance")
    print("\n  3. Diversity Chart: Shows how cultural diversity decreases")
    print("     due to clustering")
    print("\n  4. Health Chart: Shows psychological health decline and dropouts")
    print("     caused by isolation and stress")
    print("\n🎨 Visual indicators:")
    print("  - RED students: Traditional cultural background")
    print("  - BLUE students: Modern cultural background")
    print("  - Large circles: Highly connected students")
    print("  - Small circles: Isolated students")
    print("  - Bright colors: Socially active")
    print("  - Faded colors: Isolated")
    print("\n⚙️  Adjustable parameters:")
    print("  - Similarity Threshold: Make it harder/easier to be friends")
    print("  - Conflict Threshold: Make conflicts more/less likely")
    print("\n💡 Hypothesis to observe:")
    print("  H1: Similar cultures form friendships early")
    print("  H2: Different cultures experience conflict and isolation")
    print("  H3: Conflict leads to segregation and clustering")
    print("  H4: Overall cultural diversity declines")
    print("\nPress Ctrl+C to stop the server\n")
    
    server.launch()
