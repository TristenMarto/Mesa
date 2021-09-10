from mesa import Agent, Model

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
        self.wealth = wealth
    
    def move_agent(self) :
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def give_money(self) :
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1 :
            other = self.random.choice(cellmates)
            other.wealth += 1 
            self.wealth -= 1

    def step(self) :
        self.move_agent()
        if self.wealth > 0 :
            self.give_money()

