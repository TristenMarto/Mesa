from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from MoneyModel import SpatialMoneyModel

def agent_portrayal(agent) :
    portrayal =  {
          "Shape" : "circle" 
        , "Filled" : "true"
        , "r" : 0.5
    }

    if agent.wealth > 0 :
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    else :
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2

    return portrayal

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
model_params = {
      "N" : 100
    , "width" : 10
    , "height" : 10
}

chart = ChartModule([{"Label" : "Gini",
                      "Color" : "Black"}], data_collector_name='datacollector')

server = ModularServer(SpatialMoneyModel, [grid, chart], "Money Model", model_params)
server.launch()