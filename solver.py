from TSP import Map
from absl import app, flags

FLAGS = flags.FLAGS

flags.DEFINE_integer('width', 10, 'width of the map')
flags.DEFINE_integer('height', 5, 'height of the map')
flags.DEFINE_integer('nodes_num', 5, 'number of nodes on the map')

def main(_):
    width = FLAGS.width
    height = FLAGS.height
    nodes_num = FLAGS.nodes_num

    random_map = Map(width, height, nodes_num)
    random_map.visualize()

if __name__ == '__main__':
    app.run(main)

