import json
import uuid
import sys 
import networkx as nx
import matplotlib.pyplot as mpl


def getlabel(node):
  l = ""
  try:
    l = l + node['type'] + ' '
  except:
    l = l + "NOTYPE" + ' '

  try:
    l = l + node['value'] 
  except:
    l = l + "no-value"
    
  return l


def dump_graph(g):
  dump(g, 0)

#
# n is a node...
#
def dump(graph, node):
  print 'DUMP: ', node, graph.node[node]
  for e in graph.out_edges(node, data=True):
    print '  EDGE: ', e
  for e in graph.out_edges(node, data=True):
    dump(graph, e[1])


# probably broken now
def _dump(g):

  if type(g) == nx.classes.digraph.DiGraph:
    for n in g.nodes():
      print "node: {0}".format(g.node[n])

      ## for e in graph.out_edges():
        ##print "edge: {0}".format(e)

        # print("  successors({1}): {0}".format(node.successors(n), n))
        ##print("dump edge: {0}->{1}".format(getlabel(e[0]), getlabel(e[1])))
        # dump(e[1])
  else:
    print(getlabel(g))
    # print("unknown: {0}".format(type(node)))
    


#
# return a directed graph containing a root node 
#
def splain(graph, data):

  print "Splain({1}): {0}".format(type(data), graph)

  label = str(uuid.uuid1())
  g = nx.DiGraph()

  if type(data) is dict:
    graph.add_node(label, element_type='DICT')

    for key in data:
      keylabel = "{0}_DICT_{1}".format(label, key)
      graph.add_edge(label, keylabel)

      splain(g, data[key])
      graph.add_nodes_from(g)
      for n in g:
        graph.add_edge(keylabel, n)

  elif type(data) is list:
    graph.add_node(label, element_type='LIST')

    n = 0
    for element in data:
      listlabel = "{0}_LIST_{1}".format(label, n)
      n = n + 1
      graph.add_edge(label, listlabel)

      splain(g, element)
      graph.add_nodes_from(g)
      for n in g:
        graph.add_edge(listlabel, n)

  else:
    graph.add_node(label, element_type='VALUE')
    graph.add_node(label, element_value=data )
    print "DEBUG: {0}".format(graph.node[label])

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
  g.add_node(20, {'type':'MAPPING', 'key':'Dog'})
  g.add_node(21, {'type':'MAPPING', 'key':'Cat'})
  g.add_node(22, {'type':'MAPPING', 'key':'Lizard'})

  g.add_node(200, {'type':'VALUE', 'value':'Sparky'})
  g.add_node(201, {'type':'VALUE', 'value':'Whiskers'})

  g.add_node(300, {'type':'LIST', 'value':'_anonymous_'})
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
G = fake()

dump_graph(G)

l = {}
for n in G.nodes():
  G.node[n]['label'] = getlabel(G.node[n])
print l

with open("out.dot", "w") as f:
  f.write(str(nx.to_agraph(G)))

"""
pos = nx.spring_layout(G)
nx.draw(G, pos)
nx.draw_networkx_labels(G, pos, labels = l)
mpl.show()
"""

"""
with open('catalog.json') as f:
  data = json.load(f)
  print data
"""
