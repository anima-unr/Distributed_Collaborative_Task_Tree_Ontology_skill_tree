#!/usr/bin/env python

import sys
import re
import collections

def main_reorder() :
  NodeDict = dict()
  NodeIndex = dict()
  nodeString = ""
  node = ""

  infilestream = open('outputnew.txt', 'r')

  for line in infilestream:
    if re.match(r'ROOT*|THEN*|AND*|OR*|WHILE*|PLACE*', line):
      if nodeString != "":
        NodeDict[node] = nodeString
      nodeString =""
      node = re.sub(r':', "", line.strip())
      numb = re.search(r'...$', node).group()
      NodeIndex[numb] = node
    nodeString += '  ' + line 
  NodeDict[node] = nodeString
  NodeIndex = collections.OrderedDict(sorted(NodeIndex.items())) 
  infilestream.close()



  listString = ("NodeList: [")
  nodeString= "Nodes: \n"
  for key, val in NodeIndex.items():
    nodeString += NodeDict[val]
    listString += "'"+ val +"'" + ", "
  listString = re.sub (r'..$', ' ]\n', listString)

  outfilestream = open('output.yaml', 'w')
  outfilestream.write(listString)
  outfilestream.write(nodeString)
  outfilestream.close()

if __name__ == '__main__':

  main()