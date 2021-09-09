from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner
from typing import Callable
import matplotlib.pyplot as plt
import numpy as np

class MoneyAgent(Agent) :
    def __init__(self, unique_id: int, model: Model, wealth: int = 1) -> None:
        super().__init__(unique_id, model)
        self.wealth = wealth

    def step(self) :
        if self.wealth == 0 :
            return

        other_agent = self.random.choice(self.model.schedule.agents)
        other_agent.wealth += 1 
        self.wealth -= 1

class SpatialMoneyAgent(Agent) :
    def __init__(self, unique_id: int, model: Model, wealth: int = 1) -> None:
        super().__init__(unique_id, model)
        self.weath = wealth
    
    def move_agent(self) :
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def give_money(self) :
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates > 1) :
            other = self.random.choice(cellmates)
            other.wealth += 1 
            self.wealth -= 1

    def step(self) :
        self.move()
        if self.wealth > 0 :
            self.give_money()

class MoneyModel(Model) :
    def __init__(self, N: int) -> None:
        self.n_agents = N
        self.schedule = RandomActivation(self)

        for i in range(self.n_agents) :
            a = MoneyAgent(i, self)
            self.schedule.add(a)

    def step(self) :
        self.schedule.step()

    def run(self, n: int) :
        for _ in range(n) :
            self.step()

class SpatialMoneyModel(Model) :
    def __init__(self, N: int, width: int, height: int) -> None:
        self.n_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True

        for i in range(self.n_agents) :
            a = MoneyAgent(i, self)
            self.schedule.add(a)

            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        self.datacollector = DataCollector(model_reporters={'Gini': compute_gini}, agent_reporters={'Wealth': 'wealth'})

    def step(self) :
        self.datacollector.collect(self)
        self.schedule.step()

    def run(self, n: int) :
        for _ in range(n) :
            self.step()

    def get_agent_distribution(self) :
        agent_counts = np.zeros((self.grid.width, self.grid.height))
        for cell in self.grid.coord_iter():
            cell_content, x, y = cell
            agent_count = len(cell_content)
            agent_counts[x][y] = agent_count

        return agent_counts
        
def compute_gini(model):
    agent_wealths = [agent.wealth for agent in model.schedule.agents]
    x = sorted(agent_wealths)
    N = model.n_agents
    B = sum( xi * (N-i) for i,xi in enumerate(x) ) / (N*sum(x))
    return (1 + (1/N) - 2*B)