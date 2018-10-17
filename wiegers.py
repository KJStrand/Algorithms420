# Kaden Strand - CS 420 Algorithms Honors Project 
# Program to find outerplanar embedding of graph, using Manfred Weigers' trick to achieve O(n) time

import Queue

#Holds vertices with clean degree 2
twoCleanQueue = Queue.Queue()

class Vertex:
	
	def __init__(self, vertexNumber):
		self.vertexNumber = vertexNumber
		self.edges = EdgeDoubleList()
		self.dirtyEdges = EdgeDoubleList()
		self.numCleanEdges = 0
		self.outerEdge = None
		
	def __str__(self):
		return ( "Vertex " + str(self.vertexNumber) + ": "
		+ "Clean Edges: " + str(self.edges) + " Dirty Edges: " + str(self.dirtyEdges) )
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
		if self.numEdges is 1:
			self.head = None
			self.tail = None
			self.numEdges = 0
			return
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

def findPlanarEmbeddingWeigers(adjacency_List):
	#print "++++++++++++++++++"
	#printAdjList(adjacency_List)
	#print "edge 1 dirty edges: " + str(adjacency_List[1].dirtyEdges)

	v = twoCleanQueue.get_nowait()
	#print "Pulling from two Clean Queue: " + str(v)
	edge1 = v.edges.getHeadVal()
	edge2 = v.edges.getHeadNextVal()
	vertA = adjacency_List[edge1.edgeToVertexNum]
	vertB = adjacency_List[edge2.edgeToVertexNum]
	#print "vertA: " + str(vertA.vertexNumber)
	#print "vertB: " + str(vertB.vertexNumber)

	if (v.dirtyEdges.numEdges > 0):
		#print v.dirtyEdges.numEdges
		dirtyEdgeFromV = v.dirtyEdges.getHeadVal()
		dirtyToNum = dirtyEdgeFromV.edgeToVertexNum
		if (dirtyToNum is edge1.edgeToVertexNum) or (dirtyToNum is edge2.edgeToVertexNum):
			v.dirtyEdges.removeInPlace(dirtyEdgeFromV)
			adjacency_List[dirtyToNum].dirtyEdges.removeInPlace(dirtyEdgeFromV.sisterEdge)
			#print "Throwing out " + str(dirtyEdgeFromV) + " from vertex " + str(v.vertexNumber)
			#print "And throwing out " + str(dirtyEdgeFromV.sisterEdge) + " from vertex " + str(adjacency_List[dirtyToNum].vertexNumber)
			#print v.dirtyEdges
			#print adjacency_List[dirtyToNum].dirtyEdges
			twoCleanQueue.put(v)
			findPlanarEmbeddingWeigers(adjacency_List)
		else:
			newCleanEdgeFromDirty = Edge(v.vertexNumber, dirtyToNum, True)
			newCleanEdgeFromDirtySister = Edge(dirtyToNum, v.vertexNumber, True)

			newCleanEdgeFromDirty.sisterEdge = newCleanEdgeFromDirtySister
			newCleanEdgeFromDirtySister.sisterEdge = newCleanEdgeFromDirty
			
			v.edges.append(newCleanEdgeFromDirty)
			adjacency_List[dirtyToNum].edges.append(newCleanEdgeFromDirtySister)
			findPlanarEmbeddingWeigers(adjacency_List)

	# #check line
	# if vertA.edges.numEdges is 1 and vertB.edges.numEdges is 1 and (edge1.sisterEdge is edge2.sisterEdge):
	# 	print "Is line!"
	# 	# update outer edges
	# 	edge1.isOuter = False
	# 	adjacency_List[edge1.edgeParentVertexNum].outerEdge = edge2
	# 	edge2.isOuter = True
	# 	edge1.isOuter = False
	# 	adjacency_List[edge1.sisterEdge.edgeParentVertexNum].outerEdge = edge1.sisterEdge
	# 	edge1.sisterEdge.isOuter = True
	# 	edge1.sisterEdge.next.isOuter = False
	# 	adjacency_List[edge2.sisterEdge.edgeParentVertexNum].outerEdge = edge2.sisterEdge.next
	# 	edge2.sisterEdge.next.isOuter = True
	# 	edge2.sisterEdge.isOuter = False
	# 	return

	#check triangle
	check1 = (edge1.sisterEdge.next.edgeToVertexNum is edge2.edgeToVertexNum)
	check2 = (edge2.sisterEdge.next.edgeToVertexNum is edge1.edgeToVertexNum)
	if vertA.edges.numEdges is 2 and vertB.edges.numEdges is 2 and check1 and check2 and vertA.dirtyEdges.numEdges is 0 and vertB.dirtyEdges.numEdges is 0:
		print "Is triangle!"
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

	vertA.edges.removeInPlace(edge1.sisterEdge)
	vertB.edges.removeInPlace(edge2.sisterEdge)
	
	#printAdjList(adjacency_List)

	if vertA.edges.numEdges is 2:
		twoCleanQueue.put(vertA)
	if vertB.edges.numEdges is 2:
		twoCleanQueue.put(vertB)

	dirtyEdge_AB = Edge(vertA.vertexNumber, vertB.vertexNumber, False)
	dirtyEdge_BA = Edge(vertB.vertexNumber, vertA.vertexNumber, False)
	#print dirtyEdge_AB
	#print dirtyEdge_BA

	dirtyEdge_AB.sisterEdge = dirtyEdge_BA
	dirtyEdge_BA.sisterEdge = dirtyEdge_AB
	
	#print str(dirtyEdge_AB)
	#print str(dirtyEdge_BA)

	#print "edge 1 dirty edges middle: " + str(adjacency_List[1].dirtyEdges)

	condition = vertA.edges.numEdges is 1 and vertB.edges.numEdges is 1
	#print "condition1: " + str(condition)
	if condition:
		if ((vertA.edges.getHeadVal().edgeToVertexNum is vertB.vertexNumber) and (vertB.edges.getHeadVal().edgeToVertexNum is vertA.vertexNumber)):
	 		vertA.edges.append(edge1.sisterEdge)
	 		vertB.edges.append(edge2.sisterEdge)
			while vertA.dirtyEdges.numEdges is not 0:
				delDirty = vertA.dirtyEdges.getHeadVal()
				vertA.dirtyEdges.removeInPlace(delDirty)
				vertB.dirtyEdges.removeInPlace(delDirty.sisterEdge)
			findPlanarEmbeddingWeigers(adjacency_List)
			return
	 		# if vertA.edges.numEdges is 2:
	 			# twoCleanQueue.put(vertA)
	 			# print "A"
	 		# if vertB.edges.numEdges is 2:
	 			# twoCleanQueue.put(vertB)
	 			# print "B"
	 	else:
	 		cleanEdge_AB = Edge(vertA.vertexNumber, vertB.vertexNumber, True)
	 		cleanEdge_BA = Edge(vertB.vertexNumber, vertA.vertexNumber, True)
	 		cleanEdge_AB.sisterEdge = cleanEdge_BA
	 		cleanEdge_BA.sisterEdge = cleanEdge_AB
	 		vertA.edges.append(cleanEdge_AB)
	 		vertB.edges.append(cleanEdge_BA)
	 	#findPlanarEmbeddingWeigers(adjacency_List)
	 	#vertA.edges.removeInPlace(cleanEdge_AB)
	 	#vertB.edges.removeInPlace(cleanEdge_BA)

	#print "condition1: " + str(condition)
	if not condition:
		#print str(vertA.dirtyEdges.head)
		#print str(vertB.dirtyEdges.head)

	#print "Adding dirty edge: " + str(dirtyEdge_AB) + "to vertex: " + str(vertA.vertexNumber)
	#print "edge 1 dirty edges A: " + str(adjacency_List[1].dirtyEdges)
	#print str(dirtyEdge_AB.edgeParentVertexNum) + " " + str(dirtyEdge_AB.edgeToVertexNum) + " " + str(dirtyEdge_AB.clean)
	#print "blah vertA: " + str(vertA)
		vertA.dirtyEdges.append(dirtyEdge_AB)
	#print "Adding dirty edge: " + str(dirtyEdge_BA) + "to vertex: " + str(vertB.vertexNumber)
	#print "edge 1 dirty edges B: " + str(adjacency_List[1].dirtyEdges)
		vertB.dirtyEdges.append(dirtyEdge_BA)
	#print "edge 1 dirty edges again: " + str(adjacency_List[1].dirtyEdges)

	findPlanarEmbeddingWeigers(adjacency_List)
	#printAdjList(adjacency_List)
	
	

	if not (vertA.outerEdge.edgeToVertexNum is vertB.vertexNumber):
		edge2 = v.edges.getHeadVal()
		edge1 = v.edges.getHeadNextVal()
		vertA = adjacency_List[edge1.edgeToVertexNum]
		vertB = adjacency_List[edge2.edgeToVertexNum]
		
	#print "Building lines back in from " + str(vertA.vertexNumber) + " to " + str(v.vertexNumber) + " to " + str(vertB.vertexNumber)
		
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
	
	removeFromA = vertA.outerEdge
	removeFromB = vertA.outerEdge.sisterEdge
	removeFromA.isOuter = False
	removeFromB.isOuter = False
	if condition:
		vertA.edges.removeInPlace(removeFromA)
		vertB.edges.removeInPlace(removeFromB)
	
	vertA.outerEdge = newEdgeAtoV

	return


			
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
   findPlanarEmbeddingWeigers(adjList)
   print "+++++++   Done!   +++++++"
   printAdjList(adjList)		
