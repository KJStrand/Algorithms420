# Kaden Strand - CS 420 Algorithms Honors Project 
# Program to find outerplanar embedding of graph

import copy

adjList = []

def graph_input():
	num_vertices = input("Enter number of vertices: ")
	global adjList
	adjList = [None] * num_vertices
	for i in range(num_vertices):
		print "Enter vertex connections for node %d: " %i
		s = raw_input()
		connections = map(int, s.split())
		adjList[i] = connections
	
def printAdjList(inputList):
	print ""
	n = len(inputList)
	for v in range(0,n):
		print "%d:" %v , inputList[v]

def ensureCyclicTriangle(adjacency_List, outerEdgeIndex):
	n = len(adjacency_List)
	for v in range(0,n):
		currentList = adjacency_List[v]
		if currentList is not None:
			A = currentList[0]
			B = currentList[1]
			adjacency_List[A][0] = B
			adjacency_List[A][1] = v
			adjacency_List[B][0] = v
			adjacency_List[B][1] = A
			outerEdgeIndex[v]=B
			outerEdgeIndex[A]=v
			outerEdgeIndex[B]=A
			return True
	return False


#Every outerplanar graph has at least 1 vertex of degree 2
def findPlanarEmbedding(adjacency_List, outerEdgeIndex):
	#reduceGraph = copy.deepcopy(adjacency_List)
	reduceGraph = adjacency_List
	if isTriangle(reduceGraph):
		ensureCyclicTriangle(reduceGraph, outerEdgeIndex)
		return True
	else:
		reduceResult = performTwoReduction(reduceGraph)
		if reduceResult:
			print reduceResult
			#printAdjList(reduceGraph)
			findPlanarEmbedding(reduceGraph, outerEdgeIndex)
			buildEdge(reduceResult, reduceGraph, outerEdgeIndex)
			print "reduceGraph after building edge:"
			printAdjList(reduceGraph)

def buildEdge(reduceResult, reduceGraph, outerEdgeIndex):
	v = reduceResult[0]
	nodeA = reduceResult[1]
	nodeB = reduceResult[2]
	edgeAdded = reduceResult[3]

	print "---"
	print reduceResult
	#print reduceGraph[nodeA]
	#print reduceGraph[nodeB]
	print outerEdgeIndex
	print "+++"
	printAdjList(reduceGraph)
	print "*****"
	insertIndexA = reduceGraph[nodeA].index(nodeB) # before
	insertIndexB = reduceGraph[nodeB].index(nodeA) # after
	if outerEdgeIndex[nodeA] is nodeB:
		if not edgeAdded:
			reduceGraph[nodeA].insert(insertIndexA, v)  #Add after cyclic ordering, if line did exist
			reduceGraph[nodeB].insert(insertIndexB+1, v) #Add before cyclic ordering, if line did exist
		else:
			reduceGraph[nodeA][insertIndexA] = v
			reduceGraph[nodeB][insertIndexB] = v
		outerEdgeIndex[nodeA]= v
		outerEdgeIndex[v]= nodeB
		reduceGraph[v] = [nodeB, nodeA]
	else:
		if not edgeAdded:
			reduceGraph[nodeA].insert(insertIndexA+1, v)  #Add after cyclic ordering, if line did exist
			reduceGraph[nodeB].insert(insertIndexB, v)
		else:
			reduceGraph[nodeA][insertIndexA] = v
			reduceGraph[nodeB][insertIndexB] = v
		outerEdgeIndex[nodeB]= v
		outerEdgeIndex[v]= nodeA
		reduceGraph[v] = [nodeA, nodeB]
	print "After2 building edge:"
	printAdjList(reduceGraph)
	print "End"
	
			
def performTwoReduction(adjacency_List):
	n = len(adjacency_List)
	for v in range(0,n):
		if adjacency_List[v] is not None and len(adjacency_List[v]) is 2:
			nodeA = adjacency_List[v][0] 
			nodeB = adjacency_List[v][1] 
			adjacency_List[v] = None
			adjacency_List[nodeA].remove(v)
			adjacency_List[nodeB].remove(v)
			# We add the new edges to A and B, if they do not already exist
			edgeAdded = False
			if nodeB not in adjacency_List[nodeA]:
				adjacency_List[nodeA] = adjacency_List[nodeA] + [nodeB]
				edgeAdded = True
			if nodeA not in adjacency_List[nodeB]:
				adjacency_List[nodeB] = adjacency_List[nodeB] + [nodeA]
				edgeAdded = True
			#The graph is two reducible, so we return the node we removed, 
			#the two connected nodes, and whether or not we created a new line
			return (v, nodeA, nodeB, edgeAdded)
	#If we never find an adjacency list of size two, then the graph is not two  reducible
	return False
		
def isTriangle(adjacency_List):
	n = len(adjacency_List)
	count = 0
	for v in range(0,n):
		currentList = adjacency_List[v]
		if currentList is not None:
			count = count + 1
			if count > 3:
				return False
			nodeA = currentList[0]
			nodeB = currentList[1]
			if v not in adjacency_List[nodeA] and v not in adjacency_List[nodeB]:
				return False
	if count is 3:
		return True
	return False

if __name__ == '__main__':
   graph = graph_input()
   printAdjList(adjList)
   outerEdgeIndex = [None]*len(adjList)
   print ""
   findPlanarEmbedding(adjList, outerEdgeIndex)
   #printAdjList(adjList)
