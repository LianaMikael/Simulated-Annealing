# Simulated Annealing with Clustering

In this project, I implement the Simulated Annealing algorithm for the Travelling Salesman Problem (TSP) and explore whether clustering can help to improve the solution. 

![](https://github.com/LianaMikael/Simulated-Annealing/blob/master/TSP.gif)

## Travelling Salesman Problem

Suppose we wish to travel to a set of cities and return to the original city. Given only the locations of those cities (and therefore, distances between each pair),the goal is to find the shortest path to visit each of them once and return back. 

**Key observations**
- TSP can be modelles as an undirected graph since for each two cities *A* and *B*, the distance from *A* to *B* is equal to the distance from *B* to *A*.
- Each possible path is a permutation of the order of the cities, thus, a brute-force solution requires factorial runtime. (Some algorithms finding the exact solution reduce the time complexity to exponential)

## Simulated Annealing 

Simulated Annealing is an interative optimisation algorithm that estimates the global minimum or maximum value of a function when multiple local minima are available, beign particulary useful for intractavle problems like TSP.

**Hence, Simulated Annealing does not guarantee that the resulting path of TSP will be the most optimal, rather, it finds suboptimal solution that will work for most practical use cases.** 

It can be considered as an extention to the Metropolis-Hastings algorithm (check my explanation and implementation [here](https://github.com/LianaMikael/MCMC-to-Decrypt-Messages)).

**Procedure**
- Start from a random path and compute it's total cost comprised of the sum of Euclidean distances between two consecutive cities. 
- Propose a new path by swaping two randomly chosen cities and compute the corresponding total cost.
- The key is to propose new paths at each iteration and decide whether to accept or reject them, slowly converging to an acceptable solution. 
- If the cost of the new candidate is lower than the current cost, then we accept it with a probability of 1. If the cost of the new candidate is higher, then we accept it with an *acceptance probability* defined as:

- Continue until the temperature cools down to 0 or the pre-defined maximum number of iterations is reached.

## Clustering Example 

Clustering involves separating points into groups that are closer to each other. For example, we can clusterize a TSP map with 50 cities as follows:

![](https://github.com/LianaMikael/Simulated-Annealing/blob/master/outputs/clusters_init.png)

Here we performed Spectral clustering with 2 clusters. There are many clustering techniques, more information with comparison between different methods can be found in this [scikit-learn documentation](https://scikit-learn.org/stable/modules/clustering.html)

In this project, I propose to first clusterize given points in the TSP map, apply the Sumlated Annealing algorithm to each cluster and then connect the obtained paths to a single path. 

![](https://github.com/LianaMikael/Simulated-Annealing/blob/master/outputs/cluster_0.gif) ![](https://github.com/LianaMikael/Simulated-Annealing/blob/master/outputs/cluster_1.gif)

Final output obtained:

![](https://github.com/LianaMikael/Simulated-Annealing/blob/master/outputs/cluster_map.png)

For comparison, we perform Simulated Annealing for the whole map at once:

![](https://github.com/LianaMikael/Simulated-Annealing/blob/master/outputs/whole_map.gif)

The figure on the left shows costs for the case without clustering and the figure on the right shows costs with clustering:

![](https://github.com/LianaMikael/Simulated-Annealing/blob/master/outputs/costs.png) ![](https://github.com/LianaMikael/Simulated-Annealing/blob/master/outputs/cluster_costs.png)