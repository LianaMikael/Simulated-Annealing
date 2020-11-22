from TSP import Map, SimulatedAnnealing
from absl import app, flags

FLAGS = flags.FLAGS

flags.DEFINE_integer('width', 10, 'width of the map')
flags.DEFINE_integer('height', 5, 'height of the map')
flags.DEFINE_integer('nodes_num', 20, 'number of nodes on the map')
flags.DEFINE_float('temp', 1000, 'initial temperature')
flags.DEFINE_float('temp_rate', 0.95, 'rate at which to decrease the temperature')
flags.DEFINE_integer('max_iter', 5000, 'maximum number of iterations to anneal')

def main(_):
    width = FLAGS.width
    height = FLAGS.height
    nodes_num = FLAGS.nodes_num
    temp = FLAGS.temp
    temp_rate = FLAGS.temp_rate
    max_iter = FLAGS.max_iter 

    random_map = Map(width, height, nodes_num)
    random_map.visualize()
    SimulatedAnnealing(random_map, temp, temp_rate, max_iter).anneal()

if __name__ == '__main__':
    app.run(main)

