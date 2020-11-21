import numpy as np
from matplotlib import pyplot as plt

class Map:
    def __init__(self, width, height, nodes_num):
        self.width = width
        self.height = height
        self.nodes_num = nodes_num 

        self.x_nodes = np.random.rand(self.nodes_num) * self.width
        self.y_nodes = np.random.rand(self.nodes_num) * self.height

    def visualize(self):
        plt.title('Map')
        plt.xlim(0,self.width)
        plt.ylim(0,self.height)
        plt.plot(self.x_nodes, self.y_nodes, '.')
        plt.show()
    