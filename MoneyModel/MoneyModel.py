from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner
from Agents import MoneyAgent, SpatialMoneyAgent
import matplotlib.pyplot as plt
import numpy as np

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
            a = SpatialMoneyAgent(i, self)
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