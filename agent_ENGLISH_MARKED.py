"""
agent.py - International Student Agent Class
"""

import mesa
import numpy as np


class InternationalStudent(mesa.Agent):
    """An international student agent on campus."""
    
    def __init__(self, unique_id, model, x, y, country="Unknown", culture_vector=None, vision=2, social_capacity=5):
        """Initialize an international student agent."""
        super().__init__(unique_id=unique_id, model=model)
        
        self.x = x
        self.y = y
        self.country = country
        self.age = 0
        self.semester = 1
        
        if culture_vector is None:
            self.culture = np.random.randint(0, 2, 5)
        else:
            self.culture = culture_vector
        
        self.vision = vision
        self.social_capacity = social_capacity
        self.friends = set()
        self.social_connection = 0.3
        self.academic_performance = 0.6
        self.language_proficiency = np.random.uniform(0.4, 0.9)
        
        self.stress_level = 0.3
        self.isolation = 0.0
        self.homesickness = 0.3
        self.psychological_health = 0.8
        
        self.conflicts_this_week = 0
        self.total_conflicts = 0
        self.interaction_count = 0
        self.cultural_exchanges = 0
    
    def step(self):
        self.interact_with_neighbors()
        self.update_psychological_health()
        self.check_dropout()
        self.age += 1
        self.conflicts_this_week = 0
        self.interaction_count = 0
    
    def interact_with_neighbors(self):
        neighbors = self._get_neighbors_in_vision()
        if len(neighbors) == 0:
            self.isolation += 0.05
            self.social_connection -= 0.02
            return
        for neighbor in neighbors:
            distance = self.culture_distance(neighbor)
            if distance < 0.3:
                self._friendly_interaction(neighbor)
            elif distance > 0.7:
                self._conflict_interaction(neighbor)
            self.interaction_count += 1
    
    def _friendly_interaction(self, neighbor):
        self.social_connection = min(1.0, self.social_connection + 0.1)
        neighbor.social_connection = min(1.0, neighbor.social_connection + 0.1)
        self.isolation = max(0.0, self.isolation - 0.05)
        neighbor.isolation = max(0.0, neighbor.isolation - 0.05)
        if len(self.friends) < self.social_capacity:
            if neighbor.unique_id not in self.friends:
                self.friends.add(neighbor.unique_id)
                neighbor.friends.add(self.unique_id)
        if np.random.random() < 0.3:
            idx = np.random.randint(0, len(self.culture))
            self.culture[idx] = neighbor.culture[idx]
            self.cultural_exchanges += 1
        self.stress_level = max(0.0, self.stress_level - 0.05)
        neighbor.stress_level = max(0.0, neighbor.stress_level - 0.05)
    
    def _conflict_interaction(self, neighbor):
        self.conflicts_this_week += 1
        self.total_conflicts += 1
        neighbor.conflicts_this_week += 1
        neighbor.total_conflicts += 1
        self.stress_level = min(1.0, self.stress_level + 0.1)
        neighbor.stress_level = min(1.0, neighbor.stress_level + 0.1)
        self.isolation = min(1.0, self.isolation + 0.1)
        neighbor.isolation = min(1.0, neighbor.isolation + 0.1)
        self.social_connection = max(0.0, self.social_connection - 0.1)
        neighbor.social_connection = max(0.0, neighbor.social_connection - 0.1)
        self.homesickness = min(1.0, self.homesickness + 0.05)
        neighbor.homesickness = min(1.0, neighbor.homesickness + 0.05)
    
    def _get_neighbors_in_vision(self):
        neighbors = []
        for agent in self.model.schedule.agents:
            if agent is self:
                continue
            dist = abs(self.x - agent.x) + abs(self.y - agent.y)
            if dist <= self.vision:
                neighbors.append(agent)
        return neighbors
    
    def culture_distance(self, other):
        if len(self.culture) == 0:
            return 0.0
        diff = np.sum(self.culture != other.culture)
        return diff / len(self.culture)
    
    def update_psychological_health(self):
        self.psychological_health = 0.5
        self.psychological_health += self.social_connection * 0.3
        self.psychological_health += self.academic_performance * 0.1
        self.psychological_health -= self.isolation * 0.2
        self.psychological_health -= self.stress_level * 0.3
        self.psychological_health -= self.homesickness * 0.1
        self.psychological_health = max(0.0, min(1.0, self.psychological_health))
    
    def check_dropout(self):
        if self.psychological_health < 0.2:
            self.model.dropout_count += 1
            self.model.schedule.remove(self)
            self.model.grid.remove_agent(self)
        elif self.academic_performance < 0.3 and self.stress_level > 0.8:
            self.model.dropout_count += 1
            self.model.schedule.remove(self)
            self.model.grid.remove_agent(self)