from mesa import Agent, Model
from mesa.space import NetworkGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from Agents import State, Person

class NetworkModel(Model) :
    """Network model containing N nodes, all filled with an agent"""
    def __init__( self
                , N: int = 10
                , initial_outbreak_size: int = 1
                , avg_node_degree: float = 3.
                , ptrans: float = 0.5
                , progression_period: int = 3
                , progression_sd: int = 2
                , death_rate: float = 0.02
                , recovery_days: int = 20
                , recovery_sd: int = 7) -> None:
        
        self.initial_outbreak_size = initial_outbreak_size
        self.recovery_days = recovery_days
        self.recovery_sd = recovery_sd
        self.ptrans = ptrans
        self.progression_period = progression_period
        self.progression_sd = progression_sd
        self.death_rate = death_rate

        # network params
        self.n_nodes = N
        prob = avg_node_degree / self.n_nodes
        self.G = nx.erdos_renyi_graph(n=self.n_nodes, p=prob)
        self.grid = NetworkGrid(self.G)

        self.schedule = RandomActivation(self)
        self.running = True
        self.datacollector = DataCollector(
            agent_reporters={"State": "state"})

        # init agents
        for i, node in enumerate(self.G.nodes(), 1) :
            a = Person(i, self, int(self.random.normalvariate(20,40)))
            self.schedule.add(a)
            self.grid.place_agent(a, node)

            infected = np.random.choice([0,1], p=[0.99, .01])
            if infected == 1 :
                a.state = State.INFECTED
                a.recovery_time = self.get_recovery_time()

    def step(self) :
        self.datacollector.collect(self)
        self.schedule.step()

    def plot_grid(self, fig, title='') :
        """Plots the network graph"""
        graph = self.G
        pos = nx.spring_layout(graph, iterations=5, seed=8)
        plt.clf()
        ax = fig.add_subplot()
        nx.draw(graph, pos, node_size=100, edge_color='gray')

    def get_recovery_time(self) :
        return int(self.random.normalvariate(self.recovery_days, self.recovery_sd))

    def run_model(self, N: int = 200) :
        for _ in range(N) :
            self.step()