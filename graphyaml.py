from __future__ import print_function

import yaml
import uuid
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
  trace( 'DUMP: ', node, graph.node[node])
  for e in graph.out_edges(node, data=True):
    trace( '  EDGE: ', e)
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

  # assume toplevel is an anonymous dict
  ## for k in data:
  ##  traverse(graph, data[k], k)
  traverse(graph, data)

  return graph


#
# data is a list, dict, or stringlike object
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

      # build edges to each new node
      ### for node in g:
      ###   trace( "adding edge {0} -> {1}".format(graph.node[key_id], graph.node[node]))
      ###   graph.add_edge(key_id, node)
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
      # trace( "before: {0}".format(graph.nodes()))
      graph.add_nodes_from(g.nodes(data=True))
      graph.add_edges_from(g.edges(data=True))
      # trace( "after: {0}".format(graph.nodes()))

      ### for node in g:
        ### trace( "for node: {0} {1}".format(node, graph.node[node]))
        ### trace( "adding edge {0} -> {1}".format(list_id, node)    # graph.node[node]))
        ### graph.add_edge(list_id, node)
      graph.add_edge(list_id, _root)
      trace( "returning from list: {0}".format(g.nodes()))

  else:
    # assume string-like...
    graph.add_node(node_id, {'type':'VALUE', 'value':data})
    trace( "added value node {0}".format(graph.node[node_id]))

  trace( "added node {0}".format(graph.node[node_id]))
  return node_id


def fake():
  g = nx.DiGraph()
  g.add_node(0)

  g.add_node(1, {'type':'LIST', 'value':'top-list'})
  g.add_node(10, {'type':'ELEMENT', 'value':'FroBozz'})
  g.add_node(11, {'type':'ELEMENT', 'value':'Foobar'})
  g.add_edge(0, 1)
  g.add_edge(1, 10)
  g.add_edge(1, 11)

  g.add_node(2, {'type':'DICT', 'value':'top-dict'})
  g.add_node(20, {'type':'ELEMENT', 'key':'Dog'})
  g.add_node(21, {'type':'ELEMENT', 'key':'Cat'})
  g.add_node(22, {'type':'ELEMENT', 'key':'Lizard'})

  g.add_node(200, {'type':'VALUE', 'value':'Sparky'})
  g.add_node(201, {'type':'VALUE', 'value':'Whiskers'})

  g.add_node(300, {'type':'LIST', 'value':''})
  g.add_node(202, {'type':'VALUE', 'value':'Eliza'})
  g.add_node(203, {'type':'VALUE', 'value':'Waldo'})
  g.add_node(204, {'type':'VALUE', 'value':'Wanda'})

  g.add_edge(0, 2)
  g.add_edge(2, 20)
  g.add_edge(2, 21)
  g.add_edge(2, 22)
  g.add_edge(20, 200)
  g.add_edge(21, 201)
  g.add_edge(22, 300)
  g.add_edge(300, 202)
  g.add_edge(300, 203)
  g.add_edge(300, 204)

  return g

#
# main begins
#
tracelevel = 0
write_file = None

data = None
with open('catalog.json') as f:
  data = yaml.load(f)
  trace( data)
G = toplevel_traverse(data)
### G = fake()

dump_graph(G)

l = {}
for t in G.nodes(data=True):
  _node = t[0]
  _data = t[1]
  G.node[_node]['label'] = getlabel(_data)

# for n in G.nodes():
  ## trace( "making label", getlabel(G.node[n]))
#  G.node[n]['label'] = getlabel(G.node[n])

trace( "made labels", l)

if write_file:
  with open("out.dot", "w") as f:
    f.write(str(nx.to_agraph(G)))

print nx.to_agraph(G)

"""
pos = nx.spring_layout(G)
nx.draw(G, pos)
nx.draw_networkx_labels(G, pos, labels = l)
mpl.show()
"""

"""
"""
