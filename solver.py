from TSP import Map, SimulatedAnnealing, Animator
from absl import app, flags
from sklearn.cluster import SpectralClustering
import numpy as np
from matplotlib import pyplot as plt
import copy

FLAGS = flags.FLAGS

flags.DEFINE_integer('width', 10, 'width of the map')
flags.DEFINE_integer('height', 5, 'height of the map')
flags.DEFINE_integer('nodes_num', 50, 'number of nodes on the map')
flags.DEFINE_float('temp', 100, 'initial temperature')
flags.DEFINE_float('temp_rate', 0.996, 'rate at which to decrease the temperature')
flags.DEFINE_integer('max_iter', 5500, 'maximum number of iterations to anneal')
flags.DEFINE_integer('num_clusters', None, 'number of clusters (up to 7)')

def process_clusters(num_clusters, points, max_iter, width, height, temp, temp_rate):
    costs_matrix = np.zeros((num_clusters, max_iter))
    x_nodes = []
    y_nodes = []
    for i in range(num_clusters):
        cluster_points = points[np.where(points[:,-1]==i)]
        if i == 0:
            trained_model = optimize_submap(cluster_points, width, height, temp, temp_rate, max_iter)
        else: # don't keep origin node for the rest of the clusters 
            trained_model = optimize_submap(cluster_points, width, height, temp, temp_rate, max_iter, keep_origin=False)
        x_nodes.append(trained_model.map.x_nodes)
        y_nodes.append(trained_model.map.y_nodes)

        animator = Animator(trained_model.history, return_node=False)
        animator.animate('cluster_{}.mp4'.format(i))

        for t in range(len(trained_model.history)):
            costs_matrix[i, t] = trained_model.history[t][1]

    print('Saved cluster animations')
    return costs_matrix.sum(axis=0), np.concatenate(x_nodes), np.concatenate(y_nodes)

def optimize_submap(cluster_points, width, height, temp, temp_rate, max_iter, keep_origin=True):
    # given points belonging to one cluster, creates a submap and applies the Simulated Annealing algorithm 
    x_nodes = np.expand_dims(cluster_points[:,0], 0).T
    y_nodes = np.expand_dims(cluster_points[:,1], 0).T
    submap = Map(width, height, cluster_points.shape[0], x_nodes, y_nodes)

    model = SimulatedAnnealing(submap, temp, temp_rate, max_iter, return_node=False, keep_origin=keep_origin)
    model.anneal()
    return model

def visualize_clusters(points, width, height, num_clusters):
    fig = plt.figure(figsize=(5.2,3.2))
    plt.xlim(0,width)
    plt.ylim(0,height)
    colors = ['b', 'g', 'c', 'm', 'y', 'k', 'w']
    for i in range(1,points.shape[0]):
        plt.plot(points[i,0], points[i,1], '.', color=colors[int(points[i,-1])])
    plt.plot(points[0,0], points[0,1], 'o', color='r')
    plt.savefig('clusters_init.png')
    plt.close(fig)

def plot_costs(costs, name):
    fig = plt.figure(figsize=(5.2,3.2))
    plt.plot(costs)
    plt.xlabel('Iterations')
    plt.ylabel('Cost')
    plt.savefig(name)
    plt.close(fig)

def cluster(random_map, num_clusters):
    points = np.concatenate([random_map.x_nodes, random_map.y_nodes],axis=1)
    clusters = SpectralClustering(n_clusters=num_clusters, assign_labels="discretize").fit(points)
    points = np.concatenate([points, clusters.labels_.reshape(points.shape[0],1)],axis=1)
    return points

def main(_):
    width = FLAGS.width
    height = FLAGS.height
    nodes_num = FLAGS.nodes_num
    temp = FLAGS.temp
    temp_rate = FLAGS.temp_rate
    max_iter = FLAGS.max_iter 
    num_clusters = FLAGS.num_clusters

    np.random.seed(0)
    
    random_map = Map(width, height, nodes_num)
    random_map.visualize(show_path=False, save_name='initial_map.png')
    
    # optimize the whole map 
    model = SimulatedAnnealing(copy.deepcopy(random_map), temp, temp_rate, max_iter)
    model.anneal()
    animator = Animator(model.history)
    animator.animate('whole_map.mp4')
    costs = []
    for t in range(len(model.history)):
        costs.append(model.history[t][1])
    
    plot_costs(costs, 'costs.png')
    
    if num_clusters:
        # clusterize into submap and optimize each 
        points = cluster(random_map, num_clusters)
        visualize_clusters(points, width, height, num_clusters)

        costs, x_nodes, y_nodes = process_clusters(num_clusters, points, max_iter, width, height, temp, temp_rate)

        final_map = Map(width, height, nodes_num, x_nodes, y_nodes)
        final_perm = np.hstack([final_map.x_nodes, final_map.y_nodes])
        final_cost = SimulatedAnnealing(final_perm, 0, temp_rate, max_iter).cost(final_perm, True)
        final_map.visualize(final_cost, 0, save_name='cluster_map.png')
        plot_costs(costs, 'cluster_costs.png')

if __name__ == '__main__':
    app.run(main)

