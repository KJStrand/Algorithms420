# Kaden Strand - CS 420 Algorithms Honors Project 
# Program to find outerplanar embedding of graph, using dictionary for expected O(n) time

import Queue

#Holds vertices with degree 2; this program does not use clean/dirty edges
twoCleanQueue = Queue.Queue()

class Vertex:
	
	def __init__(self, vertexNumber):
		self.vertexNumber = vertexNumber
		self.edges = EdgeDoubleList()
		self.numCleanEdges = 0
		self.outerEdge = None
		
	def __str__(self):
		return ( "Vertex " + str(self.vertexNumber) + ": "
		+ "Edges: " + str(self.edges) )
		#+ "Vertex cleanEdges:" + " " + str(self.numCleanEdges) )
		
class Edge:
	
	def __init__(self, parentVertex, toVertex, clean):
		self.edgeParentVertexNum = parentVertex
		self.edgeToVertexNum = toVertex
		self.clean = clean
		self.isOuter = False
		self.sisterEdge = None
		self.next = None
		self.prev = None
		
	def __str__(self):
		return str(self.edgeToVertexNum)

class EdgeDoubleList(object):
 
	head = None
	tail = None
	numEdges = 0 
 
	def append(self, addEdge):
		if self.head is None:
			#print "Adding " + str(addEdge) + " to " + str(addEdge.edgeParentVertexNum)
			self.head = self.tail = addEdge
			addEdge.next = addEdge
			addEdge.prev = addEdge
			self.numEdges = self.numEdges + 1
		else:
			self.addAfter(self.head, addEdge)
			
			
	def addBefore(self, edgeInList, edgeToAdd):
		#print "Adding " + str(edgeToAdd) +" before " + str(edgeInList) + " to vertex " + str(edgeInList.edgeParentVertexNum)
		edgeToAdd.next = edgeInList
		edgeToAdd.prev = edgeInList.prev
		edgeInList.prev.next = edgeToAdd
		edgeInList.prev = edgeToAdd
		self.numEdges = self.numEdges + 1
		#print str(self)
		#print "done adding before"
		
	def addAfter(self, edgeInList, edgeToAdd):
		#print "Adding " + str(edgeToAdd) +" after " + str(edgeInList) + " to vertex " + str(edgeInList.edgeParentVertexNum)
		edgeToAdd.next = edgeInList.next
		edgeToAdd.prev = edgeInList
		edgeInList.next.prev = edgeToAdd
		edgeInList.next = edgeToAdd
		self.numEdges = self.numEdges + 1
		#print str(self)
		#print "done adding after"
		
	def removeInPlace(self, remEdge):
		#print "removing " + str(remEdge) + " from " + str(remEdge.edgeParentVertexNum)
		before = remEdge.prev
		after = remEdge.next
		#print before, remEdge, after
		#if remEdge.prev is not None:
		before.next = after
		after.prev = before
		if remEdge is self.head:
			self.head = after
		self.numEdges = self.numEdges - 1
		
	def getHeadVal(self):
		return self.head
		
	def getHeadNextVal(self):
		return self.head.next
 
	def __str__(self):
		retString = ""
		current_edge = self.head
		count = 0
		while count < self.numEdges:
			if current_edge.isOuter:
				retString = retString + "*"
			retString = retString + str(current_edge.edgeToVertexNum) + "-" 
			current_edge = current_edge.next
			count = count + 1
		return retString+" "	

def printAdjList(inputList):
	print ""
	n = len(inputList)
	for v in range(0,n):
		print str(inputList[v])

def graph_input():
	num_vertices = input("Enter number of vertices: ")
	num_edges = input("Enter number of edges: ")
	global adjList
	adjList = [None] * num_vertices
	global edgesDict
	edgesDict = {}
	
	for i in range(num_vertices):
		vert = Vertex(i)
		adjList[i] = vert
		
	for i in range(num_edges):
		print "Enter edge: "
		s = raw_input()
		edgeVertices = map(int, s.split())
		A = edgeVertices[0]
		B = edgeVertices[1]
		
		edgesDict[str(A)+'-'+str(B)] = True
		edgesDict[str(B)+'-'+str(A)] = True
		
		edgeToAddtoA = Edge(A, B, True)
		edgeToAddtoB = Edge(B, A, True)
		
		edgeToAddtoA.sisterEdge = edgeToAddtoB
		edgeToAddtoB.sisterEdge = edgeToAddtoA
		
		adjList[A].edges.append(edgeToAddtoA)
		adjList[A].numCleanEdges = adjList[A].numCleanEdges + 1
		adjList[B].edges.append(edgeToAddtoB)
		adjList[B].numCleanEdges = adjList[B].numCleanEdges + 1
		
	for vert in adjList:
		if(vert.numCleanEdges is 2):
			twoCleanQueue.put(vert)
			
def findPlanarEmbedding(adjacency_List):
	#print "---------------------"
	#printAdjList(adjacency_List)
	#print "^^^^^^"
	v = twoCleanQueue.get_nowait()
	
	#print "pulling v: " + str(v)
	edge1 = v.edges.getHeadVal()
	edge2 = v.edges.getHeadNextVal()
	#print edge1.sisterEdge
	#print edge2.sisterEdge
	vertA = adjacency_List[edge1.edgeToVertexNum]
	vertB = adjacency_List[edge2.edgeToVertexNum]
	
	#check triangle
	if vertA.numCleanEdges is 2 and vertB.numCleanEdges is 2 and (edge1.sisterEdge.next.edgeToVertexNum is edge2.edgeToVertexNum) and (edge2.sisterEdge.next.edgeToVertexNum is edge1.edgeToVertexNum):
		#print "Is triangle!"
		# update outer edges
		edge1.isOuter = False
		adjacency_List[edge1.edgeParentVertexNum].outerEdge = edge2
		edge2.isOuter = True
		edge1.isOuter = False
		adjacency_List[edge1.sisterEdge.edgeParentVertexNum].outerEdge = edge1.sisterEdge
		edge1.sisterEdge.isOuter = True
		edge1.sisterEdge.next.isOuter = False
		adjacency_List[edge2.sisterEdge.edgeParentVertexNum].outerEdge = edge2.sisterEdge.next
		edge2.sisterEdge.next.isOuter = True
		edge2.sisterEdge.isOuter = False
		return
	
	#edgeExistsBetweenBandA = vertA.edges.inList(vertB.vertexNumber) and vertB.edges.inList(vertA.vertexNumber)
	edgeExistsBetweenBandA = edgesDict.has_key(str(vertA.vertexNumber)+'-'+str(vertB.vertexNumber))
	if edgeExistsBetweenBandA:
		vertA.numCleanEdges = vertA.numCleanEdges -1
		vertB.numCleanEdges = vertB.numCleanEdges -1
		vertA.edges.removeInPlace(edge1.sisterEdge)
		vertB.edges.removeInPlace(edge2.sisterEdge)
		#update queue 
		if vertA.numCleanEdges is 2:
			twoCleanQueue.put(vertA)
		if vertB.numCleanEdges is 2:
			twoCleanQueue.put(vertB)
		
		findPlanarEmbedding(adjacency_List)
		#printAdjList(adjacency_List)
		
		#Build the edge back in
		if not (vertA.outerEdge.edgeToVertexNum is vertB.vertexNumber):
			edge2 = v.edges.getHeadVal()
			edge1 = v.edges.getHeadNextVal()
			vertA = adjacency_List[edge1.edgeToVertexNum]
			vertB = adjacency_List[edge2.edgeToVertexNum]
			
		#print "vertA : " + str(vertA)
		#print "vertB : " + str(vertB)
		
		edge1.isOuter = False
		edge2.isOuter = True
		v.outerEdge = edge2
		
		newEdgeAtoV = Edge(vertA.vertexNumber, v.vertexNumber, True)
		newEdgeAtoV.isOuter = True
		newEdgeAtoV.sisterEdge = edge1
		edge1.sisterEdge = newEdgeAtoV
		
		newEdgeBtoV = Edge(vertB.vertexNumber, v.vertexNumber, True)
		newEdgeBtoV.isOuter = False
		newEdgeBtoV.sisterEdge = edge2
		edge2.sisterEdge = newEdgeBtoV
		
		vertA.edges.addAfter(vertA.outerEdge, newEdgeAtoV)
		vertB.edges.addBefore(vertA.outerEdge.sisterEdge, newEdgeBtoV)
		
		vertA.outerEdge.isOuter = False
		vertA.outerEdge = newEdgeAtoV
		
	else: #consider when the edge between A and B does not exist
		newEdgeAtoB = Edge(vertA.vertexNumber, vertB.vertexNumber, True)
		newEdgeBtoA = Edge(vertB.vertexNumber, vertA.vertexNumber, True)
		newEdgeAtoB.sisterEdge = newEdgeBtoA
		newEdgeBtoA.sisterEdge = newEdgeAtoB
		vertA.edges.removeInPlace(edge1.sisterEdge)
		vertB.edges.removeInPlace(edge2.sisterEdge)
		vertA.edges.append(newEdgeAtoB)
		vertB.edges.append(newEdgeBtoA)
		
		findPlanarEmbedding(adjacency_List)
		
		if not (vertA.outerEdge.edgeToVertexNum is vertB.vertexNumber):
			edge2 = v.edges.getHeadVal()
			edge1 = v.edges.getHeadNextVal()
			vertA = adjacency_List[edge1.edgeToVertexNum]
			vertB = adjacency_List[edge2.edgeToVertexNum]
			
		#print "vertA : " + str(vertA)
		#print "vertB : " + str(vertB)
		
		edge1.isOuter = False
		edge2.isOuter = True
		v.outerEdge = edge2
		
		newEdgeAtoV = Edge(vertA.vertexNumber, v.vertexNumber, True)
		newEdgeAtoV.isOuter = True
		newEdgeAtoV.sisterEdge = edge1
		edge1.sisterEdge = newEdgeAtoV
		
		newEdgeBtoV = Edge(vertB.vertexNumber, v.vertexNumber, True)
		newEdgeBtoV.isOuter = False
		newEdgeBtoV.sisterEdge = edge2
		edge2.sisterEdge = newEdgeBtoV
		
		vertA.edges.addAfter(vertA.outerEdge, newEdgeAtoV)
		vertB.edges.addBefore(vertA.outerEdge.sisterEdge, newEdgeBtoV)
		
		#remove the old edge now that we have the two new ones set up
		removeFromA = vertA.outerEdge
		removeFromB = vertA.outerEdge.sisterEdge
		vertA.edges.removeInPlace(removeFromA)
		vertB.edges.removeInPlace(removeFromB)
		
		vertA.outerEdge = newEdgeAtoV
	
	return
	
if __name__ == '__main__':
   graph = graph_input()
   printAdjList(adjList)
   print ""
   findPlanarEmbedding(adjList)
   print "+++++++   Done!   +++++++"
   printAdjList(adjList)		
