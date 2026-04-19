"""
model.py - Campus Model for International Students
"""

import mesa
from mesa import Model
from mesa.space import MultiGrid
import mesa.time as time
from mesa.datacollection import DataCollector
import numpy as np
from agent_ENGLISH_MARKED import InternationalStudent


class CampusModel(Model):
    """A model representing a multicultural university campus."""
    
    def __init__(self, num_students=100, width=50, height=50, 
                 culture_dim=5, similarity_threshold=0.3, conflict_threshold=0.7):
        super().__init__()
        
        self.num_students = num_students
        self.width = width
        self.height = height
        self.culture_dim = culture_dim
        self.grid = MultiGrid(width, height, torus=True)
        self.schedule = time.RandomActivation(self)
        self.countries = ['China', 'India', 'Korea', 'Vietnam', 'Japan',
                         'Brazil', 'Mexico', 'Nigeria', 'Pakistan', 'Indonesia']
        self.dropout_count = 0
        self.current_step = 0
        
        self._create_students()
        
        self.datacollector = DataCollector(
            model_reporters={
                "Total_Students": lambda m: m.schedule.get_agent_count(),
                "Dropouts": lambda m: m.dropout_count,
                "Total_Conflicts_Per_Week": lambda m: sum([a.conflicts_this_week for a in m.schedule.agents]),
                "Average_Isolation": lambda m: np.mean([a.isolation for a in m.schedule.agents]) if m.schedule.get_agent_count() > 0 else 0,
                "Average_Stress": lambda m: np.mean([a.stress_level for a in m.schedule.agents]) if m.schedule.get_agent_count() > 0 else 0,
                "Average_Social_Connection": lambda m: np.mean([a.social_connection for a in m.schedule.agents]) if m.schedule.get_agent_count() > 0 else 0,
                "Cultural_Diversity": lambda m: m._calculate_cultural_diversity(),
                "Cultural_Clustering": lambda m: m._calculate_clustering_coefficient(),
                "Total_Friendships": lambda m: sum([len(a.friends) for a in m.schedule.agents]) // 2 if m.schedule.get_agent_count() > 0 else 0,
                "Cross_Cultural_Friendships": lambda m: m._count_cross_cultural_friendships(),
                "Average_Psychological_Health": lambda m: np.mean([a.psychological_health for a in m.schedule.agents]) if m.schedule.get_agent_count() > 0 else 0,
            }
        )
    
    def _create_students(self):
        agent_id = 1
        for i in range(self.num_students):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            country = self.random.choice(self.countries)
            culture = np.random.randint(0, 2, self.culture_dim)
            vision = self.random.randint(1, 4)
            
            student = InternationalStudent(
                unique_id=agent_id,
                model=self, 
                x=x, 
                y=y, 
                country=country,
                culture_vector=culture, 
                vision=vision, 
                social_capacity=5
            )
            
            self.grid.place_agent(student, (x, y))
            self.schedule.add(student)
            
            agent_id += 1
    
    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        self.current_step += 1
    
    def _calculate_cultural_diversity(self):
        if self.schedule.get_agent_count() == 0:
            return 0.0
        
        all_values = []
        for agent in self.schedule.agents:
            for bit in agent.culture:
                all_values.append(bit)
        
        if len(all_values) == 0:
            return 0.0
        
        proportion_1 = np.mean(all_values)
        proportion_0 = 1 - proportion_1
        
        diversity = 0.0
        if 0 < proportion_0 < 1:
            diversity -= proportion_0 * np.log2(proportion_0)
        if 0 < proportion_1 < 1:
            diversity -= proportion_1 * np.log2(proportion_1)
        
        return min(1.0, diversity)
    
    def _calculate_clustering_coefficient(self):
        if self.schedule.get_agent_count() == 0:
            return 0.0
        
        clustering_scores = []
        for agent in self.schedule.agents:
            neighbors = agent._get_neighbors_in_vision()
            if len(neighbors) == 0:
                clustering_scores.append(0.0)
                continue
            
            similarities = [1 - agent.culture_distance(neighbor) for neighbor in neighbors]
            clustering_scores.append(np.mean(similarities))
        
        return np.mean(clustering_scores) if clustering_scores else 0.0
    
    def _count_cross_cultural_friendships(self):
        cross_cultural_count = 0
        counted_pairs = set()
        
        for agent in self.schedule.agents:
            for friend_id in agent.friends:
                pair = tuple(sorted([agent.unique_id, friend_id]))
                if pair in counted_pairs:
                    continue
                counted_pairs.add(pair)
                
                friend = None
                for other_agent in self.schedule.agents:
                    if other_agent.unique_id == friend_id:
                        friend = other_agent
                        break
                
                if friend and agent.culture_distance(friend) > 0.3:
                    cross_cultural_count += 1
        
        return cross_cultural_count