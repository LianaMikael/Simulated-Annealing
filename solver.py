from TSP import Map, SimulatedAnnealing
from absl import app, flags

FLAGS = flags.FLAGS

flags.DEFINE_integer('width', 10, 'width of the map')
flags.DEFINE_integer('height', 5, 'height of the map')
flags.DEFINE_integer('nodes_num', 20, 'number of nodes on the map')

def main(_):
    width = FLAGS.width
    height = FLAGS.height
    nodes_num = FLAGS.nodes_num

    random_map = Map(width, height, nodes_num)
    s = SimulatedAnnealing(random_map, 0.8, 0.9, 1000).anneal()
    random_map.visualize()

if __name__ == '__main__':
    app.run(main)

