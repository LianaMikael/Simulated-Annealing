import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation 
import copy
class Map:
    # creates a random map of cities
    # the first node is assumed to be the origin
    # the order of nodes assumes the initial randomly chosen path 
    def __init__(self, width, height, nodes_num, x_nodes=None, y_nodes=None):
        self.width = width
        self.height = height
        self.nodes_num = nodes_num 

        if x_nodes is not None and y_nodes is not None:
            self.x_nodes = x_nodes
            self.y_nodes = y_nodes
        else:
            self.x_nodes = np.random.rand(self.nodes_num,1) * self.width
            self.y_nodes = np.random.rand(self.nodes_num,1) * self.height

    def visualize(self, cost=None, temp=None, show_path=True, return_node=True, save_name=None):
        plt.clf()
        plt.title('Map')
        plt.xlim(0,self.width)
        plt.ylim(0,self.height)

        if show_path:
            for i in range(self.nodes_num):
                plt.plot(self.x_nodes[i:i+2], self.y_nodes[i:i+2], 'bo-')
            if return_node:
                # return back to original node
                plt.plot([self.x_nodes[-1],self.x_nodes[0]],[self.y_nodes[-1],self.y_nodes[0]], 'bo-')

            if cost and temp:
            # visualize the total cost 
                plt.text(1, 4.6, 'cost: {:.2f}'.format(cost), color='r')
                plt.text(1, 4.4, 'temp: {:.2f}'.format(temp), color='r')

        plt.plot(self.x_nodes[0], self.y_nodes[0], 'o', color='r')
        plt.plot(self.x_nodes[1:], self.y_nodes[1:], '.')

        if save_name:
            plt.savefig(save_name)
            #plt.close(fig)
        else:
            plt.show()

    
class SimulatedAnnealing:
    def __init__(self, TSP_map, temp, rate, max_iter, return_node=True, keep_origin=True):
        self.map = TSP_map
        self.temp = temp
        self.rate = rate
        self.max_iter = max_iter 
        self.history = None
        self.return_node = return_node
        self.keep_origin = keep_origin

    def anneal(self):
        curr_permutation = np.hstack([self.map.x_nodes, self.map.y_nodes])
        candidate_maps = []
        curr_cost = self.cost(curr_permutation, self.return_node)

        for _ in range(self.max_iter):
            
            new_permutation = self.create_neighbour_path(curr_permutation, self.keep_origin)
            new_cost = self.cost(new_permutation, self.return_node)

            if new_cost < curr_cost:
                curr_permutation = new_permutation
                curr_cost = new_cost
                self.map.x_nodes = new_permutation[:,0]
                self.map.y_nodes = new_permutation[:,1]

            elif np.random.random() < self.acceptance_prob(curr_cost, new_cost):
                curr_permutation = new_permutation
                curr_cost = new_cost
                self.map.x_nodes = new_permutation[:,0]
                self.map.y_nodes = new_permutation[:,1]

            candidate_maps.append((copy.deepcopy(self.map), curr_cost, self.temp))
            self.temp *= self.rate 

        self.history = candidate_maps

    def acceptance_prob(self, curr_cost, new_cost):
        # calculates the acceptance probability 
        return np.exp(-np.abs(new_cost - curr_cost) / self.temp)

    @staticmethod
    def create_neighbour_path(curr_permutation, keep_origin=True):
        # swaps two randomly chosen nodes 
        # Keep the origin for the cluster that contains it 
        if keep_origin:
            start_idx = 1 
        else:
            start_idx = 0

        idx_1 = np.random.randint(start_idx, len(curr_permutation))
        idx_2 = np.random.randint(start_idx, len(curr_permutation))

        while (idx_1 == idx_2): 
            idx_2 = np.random.randint(start_idx, len(curr_permutation))

        new_permutation = curr_permutation.copy()
        new_permutation[[idx_1, idx_2]] = new_permutation[[idx_2, idx_1]]

        return new_permutation

    @staticmethod
    def Euclidean(coord1, coord2):
        return np.linalg.norm(coord1 - coord2)

    @classmethod
    def cost(cls, permutation, return_node=True): 
        # calculates the cost of a given permutation
        # uses l2 norm (Euclidean) as the distance function
        dist = 0
        for i in range(len(permutation)-1):
            dist += cls.Euclidean(permutation[i], permutation[i+1])
        if return_node:
            dist += cls.Euclidean(permutation[-1], permutation[0])
        return dist 

class Animator:
    # given a history of maps, costs and temperatures, creates an animation 
    def __init__(self, history, return_node=True):
        self.history = history
        self.return_node = return_node

    def update_animation(self, i):
        self.history[i][0].visualize(self.history[i][1], self.history[i][2], return_node=self.return_node, save_name='current.png')

    def animate(self, name):
        fig = plt.figure(figsize=(5.2,3.2))
        self.animator = animation.FuncAnimation(fig, self.update_animation, frames = len(self.history), interval=10)
        self.animator.save(name,  writer = 'ffmpeg')
        plt.close(fig)
