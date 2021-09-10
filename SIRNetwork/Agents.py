from mesa import Agent, Model
import numpy as np

class State :
    SUSCEPTIBLE = 0
    INFECTED = 1
    REMOVED = 2

class Person(Agent) :
    def __init__(self, unique_id: int, model: Model, age: int) -> None:
        super().__init__(unique_id, model)

        self.age = age
        self.state = State.SUSCEPTIBLE
        self.infection_time = 0

    def move(self) :
        """Move agent through network"""
        possible_steps = [ node for node in self.model.grid.get_neighbors(self.pos, include_center=False) 
                           if self.model.grid.is_cell_empty(node)]
        
    def status(self) :
        """Check status of infected agent"""
        if self.state == State.INFECTED :
            drate = self.model.death_rate
            alive = np.random.choice([0,1], p=[drate, 1-drate])
            if alive == 0 :
                self.model.schedule.remove(self)
            t = self.model.schedule.time - self.infection_time
            if t >= self.recovery_time :
                self.state = State.REMOVED

    def contact(self) :
        """Find closest contact and infect"""

        nearby_nodes = self.model.grid.get_neighbors(self.pos, include_center=False)
        sus_neighbors = [ agent for agent in self.model.grid.get_cell_list_contents(nearby_nodes)
                          if agent.state == State.SUSCEPTIBLE]

        for a in sus_neighbors :
            if self.random.random() < self.model.ptrans :
                a.state = State.INFECTED
                a.recovery_time = self.model.get_recovery_time()
    
    def step(self) :
        self.status()
        self.move()
        self.contact()

    
    