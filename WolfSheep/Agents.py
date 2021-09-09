from mesa import Agent, Model

class RandomWalker(Agent) :
    def __init__(self, unique_id: int, model: Model, pos: tuple) -> None:
        super().__init__(unique_id, model)

        self.pos = pos

    def random_move(self) :
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

class Sheep(RandomWalker):
    def __init__(self, unique_id: int, model: Model, pos: tuple) -> None:
        super().__init__(unique_id, model, pos)

    def reproduce(self) :
        if self.model.sheep_reproduction_chance > self.random.random() :
            self.model.new_agent(Sheep, self.pos)

    def step(self):
        '''
        This method should move the Sheep using the `random_move()` method implemented earlier, then conditionally reproduce.
        '''
        self.random_move()
        self.reproduce()

class Wolf(RandomWalker) :
    def __init__(self, unique_id: int, model: Model, pos: tuple) -> None:
        super().__init__(unique_id, model, pos)

        self.meals = 0
    
    def die(self) :
        if self.model.wolf_death_chance > self.random.random() :
            self.model.remove_agent(self)

    def reproduce(self) :
        self.model.new_agent(Wolf, self.pos)

    def eat_sheep(self) :
        this_cell = self.model.grid.get_cell_list_contents(self.pos)
        sheep = [obj for obj in this_cell if obj.__class__.__name__ == 'Sheep']
        if len(sheep) > 0 :
            meal = self.random.choice(sheep)
            self.model.remove_agent(meal)
            self.reproduce()
            self.meals += 1

    def step(self):
        '''
        This method should move the wolf, then check for sheep on its location, 
        eat the sheep if it is there and reproduce, and finally conditionally die.
        '''        
        self.random_move()
        self.eat_sheep()
        self.die()