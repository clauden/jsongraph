import json, inspect


def splain(indent, data):
  if type(data) is dict:
    for key in data:
      print "%s%s = " % (indent, key), 
      splain(indent + '>', data[key])
  elif type(data) is list:
    for element in data:
      splain(indent + '>', element)
  else:
    # print "not dict, but {1}: {0}".format(data, type(data))
    print "%s" % (data)

with open('catalog.json') as f:
  data = json.load(f)
  splain('', data)


  if type(data) is dict:
    for k in data:
      print(k)
      for y in data[k]:
        print(y)
    
