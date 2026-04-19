#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gui.py - Interactive GUI for International Students Cultural Segregation Model

Standalone GUI that works with the current Mesa version.
Uses matplotlib animation to show agents moving on the grid in real-time.

USAGE:
    python3 gui.py

FEATURES:
- Real-time visualization of 100 student agents on a 50x50 grid
- Color-coded agents: Red = Traditional culture, Blue = Modern culture
- Size-coded agents: Large = Socially connected, Small = Isolated
- 6 real-time charts:
  1. Conflicts per week
  2. Isolation index
  3. Social connection
  4. Diversity vs Clustering
  5. Friendships (total + cross-cultural, separate y-axes for clarity)
  6. Population & Health (separate y-axes for proper scaling)
- Interactive controls: Play, Pause, Reset

This GUI demonstrates the MODIFICATION (conflict mechanism) by showing
how same-culture students cluster together over time due to cultural conflict.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
from matplotlib.lines import Line2D
from model_ENGLISH_MARKED import CampusModel


class CampusGUI:
    """Interactive GUI for visualizing the International Students Model."""
    
    def __init__(self, num_students=100, max_steps=200):
        """Initialize the GUI."""
        self.max_steps = max_steps
        self.current_step = 0
        self.is_running = True
        self.num_students = num_students
        
        # Create the model
        np.random.seed(42)
        self.model = CampusModel(num_students=num_students)
        
        # Data tracking for charts
        self.steps_history = []
        self.conflicts_history = []
        self.isolation_history = []
        self.social_connection_history = []
        self.diversity_history = []
        self.clustering_history = []
        self.total_friendships_history = []
        self.cross_friendships_history = []
        self.total_students_history = []
        self.health_history = []
        
        # Setup the figure
        self._setup_figure()
        
    def _setup_figure(self):
        """Create the figure with all panels."""
        self.fig = plt.figure(figsize=(18, 10))
        self.fig.suptitle('International Students Cultural Segregation Model', 
                          fontsize=14, fontweight='bold')
        
        # Left: Campus grid (spans all 3 rows, 2 cols wide)
        self.ax_grid = plt.subplot2grid((3, 4), (0, 0), rowspan=3, colspan=2)
        self.ax_grid.set_xlim(-1, 51)
        self.ax_grid.set_ylim(-1, 51)
        self.ax_grid.set_aspect('equal')
        self.ax_grid.set_xlabel("X position")
        self.ax_grid.set_ylabel("Y position")
        self.ax_grid.grid(True, alpha=0.3)
        
        # Right: 6 charts in a 3x2 grid
        self.ax_conflicts = plt.subplot2grid((3, 4), (0, 2))
        self.ax_isolation = plt.subplot2grid((3, 4), (0, 3))
        self.ax_social = plt.subplot2grid((3, 4), (1, 2))
        self.ax_diversity = plt.subplot2grid((3, 4), (1, 3))
        self.ax_friendships = plt.subplot2grid((3, 4), (2, 2))
        self.ax_population = plt.subplot2grid((3, 4), (2, 3))
        
        plt.tight_layout(rect=[0, 0.05, 1, 0.96])
        
        # Control buttons
        self.ax_pause = plt.axes([0.35, 0.01, 0.08, 0.035])
        self.btn_pause = Button(self.ax_pause, 'Pause')
        self.btn_pause.on_clicked(self._toggle_pause)
        
        self.ax_reset = plt.axes([0.47, 0.01, 0.08, 0.035])
        self.btn_reset = Button(self.ax_reset, 'Reset')
        self.btn_reset.on_clicked(self._reset)
        
        # Status text
        self.status_text = self.fig.text(0.6, 0.02, '', fontsize=9, fontweight='bold')
    
    def _toggle_pause(self, event):
        """Pause/Resume animation."""
        self.is_running = not self.is_running
        self.btn_pause.label.set_text('Play' if not self.is_running else 'Pause')
    
    def _reset(self, event):
        """Reset simulation."""
        self.current_step = 0
        self.is_running = True
        self.btn_pause.label.set_text('Pause')
        
        np.random.seed(42)
        self.model = CampusModel(num_students=self.num_students)
        
        self.steps_history = []
        self.conflicts_history = []
        self.isolation_history = []
        self.social_connection_history = []
        self.diversity_history = []
        self.clustering_history = []
        self.total_friendships_history = []
        self.cross_friendships_history = []
        self.total_students_history = []
        self.health_history = []
    
    def _draw_agents(self):
        """Draw all agents on the grid."""
        self.ax_grid.clear()
        
        self.ax_grid.set_xlim(-1, 51)
        self.ax_grid.set_ylim(-1, 51)
        self.ax_grid.set_aspect('equal')
        self.ax_grid.set_xlabel("X position")
        self.ax_grid.set_ylabel("Y position")
        self.ax_grid.grid(True, alpha=0.3)
        self.ax_grid.set_title(
            f"Campus Grid - Week {self.current_step} | Students: {self.model.schedule.get_agent_count()} | Dropouts: {self.model.dropout_count}",
            fontsize=11, fontweight='bold'
        )
        
        for agent in self.model.schedule.agents:
            culture_mean = sum(agent.culture) / len(agent.culture)
            
            if culture_mean < 0.5:
                color = (0.85, 0.25 + 0.5*culture_mean, 0.25 + 0.5*culture_mean)
            else:
                color = (0.85 - 0.6*(culture_mean - 0.5)*2, 0.5, 0.85)
            
            size = 30 + agent.social_connection * 200
            alpha = max(0.4, 1.0 - 0.4 * agent.isolation)
            
            self.ax_grid.scatter(
                agent.x, agent.y, s=size, c=[color], alpha=alpha,
                edgecolors='black', linewidth=0.3
            )
        
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', label='Traditional Culture',
                   markerfacecolor='red', markersize=10),
            Line2D([0], [0], marker='o', color='w', label='Modern Culture',
                   markerfacecolor='blue', markersize=10),
            Line2D([0], [0], marker='o', color='w', label='Connected (large)',
                   markerfacecolor='gray', markersize=14),
            Line2D([0], [0], marker='o', color='w', label='Isolated (small)',
                   markerfacecolor='gray', markersize=6),
        ]
        self.ax_grid.legend(handles=legend_elements, loc='upper right', fontsize=8)
    
    def _draw_charts(self):
        """Update all 6 charts."""
        # Clear all charts
        for ax in [self.ax_conflicts, self.ax_isolation, self.ax_social,
                   self.ax_diversity, self.ax_friendships, self.ax_population]:
            ax.clear()
            ax.grid(True, alpha=0.3)
            ax.tick_params(axis='both', which='major', labelsize=7)
            ax.set_xlabel("Week", fontsize=7)
        
        if not self.steps_history:
            return
        
        # Chart 1: Conflicts
        self.ax_conflicts.set_title("Conflicts per Week", fontsize=9, fontweight='bold')
        self.ax_conflicts.plot(self.steps_history, self.conflicts_history, 
                                'r-', linewidth=2)
        
        # Chart 2: Isolation
        self.ax_isolation.set_title("Average Isolation", fontsize=9, fontweight='bold')
        self.ax_isolation.plot(self.steps_history, self.isolation_history, 
                                'orange', linewidth=2)
        self.ax_isolation.set_ylim(0, max(0.6, max(self.isolation_history) * 1.1))
        
        # Chart 3: Social Connection
        self.ax_social.set_title("Social Connection", fontsize=9, fontweight='bold')
        self.ax_social.plot(self.steps_history, self.social_connection_history, 
                             'g-', linewidth=2)
        self.ax_social.set_ylim(0, 1)
        
        # Chart 4: Diversity vs Clustering
        self.ax_diversity.set_title("Diversity vs Clustering", fontsize=9, fontweight='bold')
        self.ax_diversity.plot(self.steps_history, self.diversity_history, 
                                'gold', linewidth=2, label='Diversity')
        self.ax_diversity.plot(self.steps_history, self.clustering_history, 
                                'brown', linewidth=2, label='Clustering')
        self.ax_diversity.legend(fontsize=7, loc='best')
        self.ax_diversity.set_ylim(0, 1.1)
        
        # Chart 5: Friendships - DUAL AXIS for proper scaling
        # Total friendships on left (large numbers)
        # Cross-cultural on right (small numbers)
        self.ax_friendships.set_title("Friendships", fontsize=9, fontweight='bold')
        line1 = self.ax_friendships.plot(self.steps_history, self.total_friendships_history, 
                                           'b-', linewidth=2, label='Total')
        self.ax_friendships.set_ylabel('Total', color='b', fontsize=7)
        self.ax_friendships.tick_params(axis='y', labelcolor='b', labelsize=7)
        
        ax_f2 = self.ax_friendships.twinx()
        line2 = ax_f2.plot(self.steps_history, self.cross_friendships_history, 
                            'purple', linewidth=2, label='Cross-Cultural')
        ax_f2.set_ylabel('Cross-Cultural', color='purple', fontsize=7)
        ax_f2.tick_params(axis='y', labelcolor='purple', labelsize=7)
        
        # Combined legend
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        self.ax_friendships.legend(lines, labels, fontsize=7, loc='center right')
        
        # Chart 6: Population & Health - FIXED DUAL AXIS
        # Students on left y-axis (0-100 range)
        # Health on right y-axis (0-1 range) 
        self.ax_population.set_title("Population & Health", fontsize=9, fontweight='bold')
        line1 = self.ax_population.plot(self.steps_history, self.total_students_history, 
                                           'b-', linewidth=2, label='Students')
        self.ax_population.set_ylabel('# Students', color='b', fontsize=7)
        self.ax_population.tick_params(axis='y', labelcolor='b', labelsize=7)
        self.ax_population.set_ylim(0, 110)
        
        ax_p2 = self.ax_population.twinx()
        line2 = ax_p2.plot(self.steps_history, self.health_history, 
                            'g-', linewidth=2, label='Health')
        ax_p2.set_ylabel('Health Index', color='g', fontsize=7)
        ax_p2.tick_params(axis='y', labelcolor='g', labelsize=7)
        ax_p2.set_ylim(0, 1)
        
        # Combined legend
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        self.ax_population.legend(lines, labels, fontsize=7, loc='center right')
    
    def _collect_metrics(self):
        """Collect all metrics from the model."""
        agents = self.model.schedule.agents
        if len(agents) == 0:
            return {
                'conflicts': 0, 'isolation': 0, 'social': 0,
                'diversity': 0, 'clustering': 0, 'total_friends': 0,
                'cross_friends': 0, 'total_students': 0, 'health': 0
            }
        
        conflicts = sum([a.conflicts_this_week for a in agents])
        isolation = np.mean([a.isolation for a in agents])
        social = np.mean([a.social_connection for a in agents])
        diversity = self.model._calculate_cultural_diversity()
        clustering = self.model._calculate_clustering_coefficient()
        total_friends = sum([len(a.friends) for a in agents]) // 2
        cross_friends = self.model._count_cross_cultural_friendships()
        total_students = self.model.schedule.get_agent_count()
        health = np.mean([a.psychological_health for a in agents])
        
        return {
            'conflicts': conflicts, 'isolation': isolation, 'social': social,
            'diversity': diversity, 'clustering': clustering, 
            'total_friends': total_friends, 'cross_friends': cross_friends,
            'total_students': total_students, 'health': health
        }
    
    def update(self, frame):
        """Update function for animation."""
        if not self.is_running:
            return
        
        if self.current_step >= self.max_steps:
            self.status_text.set_text(f'Simulation complete! {self.current_step} weeks elapsed.')
            self.is_running = False
            return
        
        self.model.step()
        self.current_step += 1
        
        m = self._collect_metrics()
        self.steps_history.append(self.current_step)
        self.conflicts_history.append(m['conflicts'])
        self.isolation_history.append(m['isolation'])
        self.social_connection_history.append(m['social'])
        self.diversity_history.append(m['diversity'])
        self.clustering_history.append(m['clustering'])
        self.total_friendships_history.append(m['total_friends'])
        self.cross_friendships_history.append(m['cross_friends'])
        self.total_students_history.append(m['total_students'])
        self.health_history.append(m['health'])
        
        self._draw_agents()
        self._draw_charts()
        
        self.status_text.set_text(
            f'Week: {self.current_step}/{self.max_steps} | '
            f'Conflicts: {m["conflicts"]} | Clustering: {m["clustering"]:.3f} | '
            f'Friendships: {m["total_friends"]} | Health: {m["health"]:.3f}'
        )
    
    def run(self):
        """Start the animation."""
        print("\n" + "="*70)
        print("INTERNATIONAL STUDENTS MODEL - INTERACTIVE GUI")
        print("="*70)
        print("\nStarting GUI...")
        print("Watch how students cluster by culture over time!")
        print("Use the Pause/Reset buttons to control the simulation.")
        print("\nTo close: Close the window or press Ctrl+C\n")
        
        self._draw_agents()
        
        self.anim = FuncAnimation(
            self.fig, self.update, 
            interval=200,
            cache_frame_data=False,
            save_count=self.max_steps
        )
        
        plt.show()


def main():
    """Launch the GUI."""
    gui = CampusGUI(num_students=100, max_steps=200)
    gui.run()


if __name__ == "__main__":
    main()