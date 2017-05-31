from __future__ import print_function

import yaml
import uuid
import argparse
import sys 
import networkx as nx
import matplotlib.pyplot as mpl


def trace(*s):
  if trace_level > 0:
    print("".join(map(str, s)))


def getlabel(node):
  trace( "getlabel: {0}".format(dict(node)))

  l = ""
  
  try:
    t = node['type'] 
  except:
    t = None

  try:
    k = node['key'] 
  except:
    k = None

  try:
    v = str(node['value'])
  except:
    v = None
  

  if t:
    l = l + "{0} ".format(t)

  if k:
    l = l + "[{0}]".format(k)

  if v:
    l = l + v

  trace( "label", l)
  return l


def dump_graph(g):
  dump(g, 0)


#
# n is a node...
#
def dump(graph, node):
  print( 'DUMP: ', node, graph.node[node])
  for e in graph.out_edges(node, data=True):
    print( '  EDGE: ', e)
  for e in graph.out_edges(node, data=True):
    dump(graph, e[1])


#
# Assume that toplevel object is always a dict
# Returns the graph
#
def toplevel_traverse(data):

  trace( "toplevel_traverse({0} [{1}])".format(data, type(data)))

  # failure conditions
  if data is None:
    raise "toplevel object is None"
  ### if type(data) is not dict: 
  ###  raise "toplevel object isn't a dict"

  # seed the graph
  graph = nx.DiGraph()
  graph.add_node(0)
  _root = traverse(graph, data)
  graph.add_edge(0, _root)

  return graph


#
# data is a list, dict, or stringlike 
#
def traverse(graph, data, name=''):

  trace( "traverse({0}, {1}, {2} [{3}])".format(graph, data, type(data), name))

  node_id = str(uuid.uuid1())

  if type(data) is dict:
    graph.add_node(node_id, {'type':'DICT', 'value':name})

    for key in data:
      trace( "traverse key {0}".format(key))

      key_id = "{0}_DICT_{1}".format(node_id, key)
      graph.add_node(key_id, {'type':'KEY', 'key':key})
      graph.add_edge(node_id, key_id)
      trace( "added key node {0}".format(graph.node[key_id]))

      g = nx.DiGraph()
      trace( "about to traverse {0} [{1}]".format(data[key], type(data[key])))
      _root = traverse(g, data[key])
      graph.add_nodes_from(g.nodes(data=True))
      graph.add_edges_from(g.edges(data=True))

      # build edge from current root to the new root
      graph.add_edge(key_id, _root)

      trace( "returning from dict: {0}".format(g))

  elif type(data) is list:
    graph.add_node(node_id, {'type':'LIST', 'value':name, 'top':'yes'})

    n = 0
    for element in data:
      list_id = "{0}_LIST_{1}".format(node_id, n)
      graph.add_node(list_id, {'type':'ELEMENT', 'value':n})
      n = n + 1
      graph.add_edge(node_id, list_id)

      g = nx.DiGraph()
      _root = traverse(g, element)
      graph.add_nodes_from(g.nodes(data=True))
      graph.add_edges_from(g.edges(data=True))

      graph.add_edge(list_id, _root)

      trace( "returning from list: {0}".format(g.nodes()))

  else:
    # assume string-like...
    graph.add_node(node_id, {'type':'VALUE', 'value':data})
    trace( "added value node {0}".format(graph.node[node_id]))

  trace( "added node {0}".format(graph.node[node_id]))
  return node_id


#
# main begins
#
arg_ns = None
arg_p = argparse.ArgumentParser(description='yaml to dot')
arg_p.add_argument('input_file', nargs='?', type=argparse.FileType('r'), 
                   default=sys.stdin)
arg_p.add_argument('-o', '--output-file', action='store', type=argparse.FileType('w'),
                   default=sys.stdout, required=False)
arg_p.add_argument('-t', '--trace', action='count', required=False)
arg_p.add_argument('-g', '--graph-debug', action='store_true', required=False)
try:
  arg_ns = arg_p.parse_args()
except IOError as ioe:
  print(ioe, file=sys.stderr)
  sys.exit(1)
  
print("===args")
print(arg_ns.input_file)
print(arg_ns.output_file)
print(arg_ns.trace)
print(arg_ns.graph_debug)
print("===end args")

input_file = arg_ns.input_file
output_file = arg_ns.output_file
trace_level = arg_ns.trace
graph_debug = arg_ns.graph_debug

data = None

# assume input_file is already open...
data = yaml.load(input_file)

# with open(input_file, "r") as f:
#   data = yaml.load(f)
#   trace( data)

trace(data)
G = toplevel_traverse(data)

if graph_debug:
    dump_graph(G)

l = {}
for t in G.nodes(data=True):
  _node = t[0]
  _data = t[1]
  G.node[_node]['label'] = getlabel(_data)
trace( "made labels", l)

dot = str(nx.to_agraph(G))

# assume output_file is already open...
output_file.write(dot)

# with open(output_file, "w") as f:
#     f.write(dot)


# if write_file:
#   with open("out.dot", "w") as f:
#     f.write(dot)
# else:
#   print(dot)

"""
l = {}
for t in G.nodes(data=True):
  _node = t[0]
  _data = t[1]
  G.node[_node]['label'] = getlabel(_data)

trace( "made labels", l)


pos = nx.spring_layout(G)
nx.draw(G, pos)
nx.draw_networkx_labels(G, pos, labels = l)
mpl.show()
"""
