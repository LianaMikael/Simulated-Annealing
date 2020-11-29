from TSP import Map, SimulatedAnnealing
from absl import app, flags
from sklearn.cluster import SpectralClustering
import numpy as np
from matplotlib import pyplot as plt

FLAGS = flags.FLAGS

flags.DEFINE_integer('width', 10, 'width of the map')
flags.DEFINE_integer('height', 5, 'height of the map')
flags.DEFINE_integer('nodes_num', 20, 'number of nodes on the map')
flags.DEFINE_float('temp', 100, 'initial temperature')
flags.DEFINE_float('temp_rate', 0.998, 'rate at which to decrease the temperature')
flags.DEFINE_integer('max_iter', 3000, 'maximum number of iterations to anneal')
flags.DEFINE_integer('num_clusters', 2, 'number of clusters ')

def process_submap(cluster_points, width, height, temp, temp_rate, max_iter):
    # given points belonging to one cluster, creates a submap and applies the Simulated Annealing algorithm 
    x_nodes = cluster_points[:,0].reshape(cluster_points[:,0].shape[0],1)
    y_nodes = cluster_points[:,1].reshape(cluster_points[:,1].shape[0],1)
    submap = Map(width, height, cluster_points.shape[0], x_nodes, y_nodes)

    model = SimulatedAnnealing(submap, temp, temp_rate, max_iter)
    model.anneal()
    return model

def visualize_clusters(points, width, height, num_clusters):
    plt.xlim(0,width)
    plt.ylim(0,height)
    colors = ['b', 'g', 'c', 'm', 'y', 'k', 'w']
    for i in range(1,points.shape[0]):
        plt.plot(points[i,0], points[i,1], '.', color=colors[int(points[i,-1])])
    plt.plot(points[0,0], points[0,1], 'o', color='r')
    plt.show()

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
    random_map.visualize(show_path=False, show_each=True)

    points = cluster(random_map, num_clusters)
    visualize_clusters(points, width, height, num_clusters)

    # for each cluster perform Simulated Annealing 
    for i in range(num_clusters):
        cluster_points = points[np.where(points[:,-1]==i)]
        trained_model = process_submap(cluster_points, width, height, temp, temp_rate, max_iter)
        trained_model.animate('cluster_{}.mp4'.format(i))


if __name__ == '__main__':
    app.run(main)

