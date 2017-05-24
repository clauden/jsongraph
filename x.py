import json
import uuid
import networkx as nx
import matplotlib.pyplot as mpl

def dump(node):
  print ("dump {0}".format(node))

  #if type(node) == unicode or type(node) == str:
  
  if hasattr(node, 'value'):
    print node['value']
  else:
    print "anonymous"

  if type(node) == nx.classes.digraph.DiGraph:
    for n in node.nodes():
      print("  successors({1}): {0}".format(node.successors(n), n))
      dump(n)

  # else:
  #  print("unknown: {0}".format(type(node)))


#
# return a directed graph containing a root node 
#
def splain(data):

  print "splain: {0}".format(type(data))

  label = str(uuid.uuid1())
  graph = nx.DiGraph(value=label)
  # graph.add_node(label)

  if type(data) is dict:
    for key in data:
      # print "%s%s = " % (indent, key), 
      subgraph = splain(data[key])
      graph.add_node(key)
      graph.add_node(subgraph)
      graph.add_edge(label, key)
      graph.add_edge(key, subgraph)
  elif type(data) is list:
    for element in data:
      subgraph = splain(element)
      # graph.add_node(subgraph)          # add_edge does it automatically?
      graph.add_edge(label,  subgraph)
  else:
    # print "not dict, but {1}: {0}".format(data, type(data))
    # print "%s" % (data)
    graph.add_node(label, value=data)      # assume add_node quietly adds value attribute

  print "returning {0}".format(graph.nodes())
  return graph


#
# main begins
#
with open('catalog.json') as f:
  data = json.load(f)

  g = splain(data)
  print g.nodes()
  print ("DUMPIN")
  dump(g)
  nx.write_edgelist(g, 'edges.txt')

  # l = {}
  # for u, v, data in g.edges(data=True):
  #   l[(u,v)] = data['type']
  if False:
    pos = nx.spring_layout(g)
    nx.draw(g, pos)
    nx.draw_networkx_edge_labels(g, pos) # , edge_labels=l)
    mpl.show()
  
  if False:
    nx.write_dot(g, 'out.dot')


  if False:
    if type(data) is dict:
      for k in data:
        print(k)
        for y in data[k]:
          print(y)
    
