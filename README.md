# Simulated Annealing with Clustering

In this project, I implement the Simulated Annealing algorithm Travelling Salesman Problem (TSP) and explore whether clustering can help to improve the solution. 

## Travelling Salesman Problem

Suppose we wish to travel to a set of cities and return to the original city. Given only the locations of those cities (and therefore, distances between each pair),the goal is to find the shortest path to visit each of them once and return back. 

**Key observations**
- TSP can be modelles as an undirected graph since for each two cities *A* and *B*, the distance from *A* to *B* is equal to the distance from *B* to *A*.
- Each possible path is a permutation of the order of the cities, thus, a brute-force solution requires factorial runtime. (Some algorithms finding the exact solution reduce the time complexity to exponential)

## Simulated Annealing 

Simulated Annealing is an interative optimisation algorithm that estimates the global minimum or maximum value of a function when multiple local minima are available, beign particulary useful for intractavle problems like TSP. 
**Hence, Simulated Annealing does not guarantee that the resulting path of TSP will be the most optimal, rather, it finds suboptimal solution that will work for most practical use cases.** 
It can be considered as an extention to the Metropolis-Hastings algorithm (check my explanation and implementation here).

**Procedure**
- Start from a random path and compute it's total cost comprised of the sum of Euclidean distances between two consecutive cities. 
- Propose a new path by swaping two randomly chosen cities and compute the corresponding total cost.
- The key is to propose new paths at each iteration and decide whether to accept or reject them, slowly converging to an acceptable solution. 
- If the cost of the new candidate is lower than the current cost, then we accept it with a probability of 1. If the cost of the new candidate is higher, then we accept it with an *acceptance probability* defined as:

- Continue until the temperature cools down to 0 or the pre-defined maximum number of iterations is reached.