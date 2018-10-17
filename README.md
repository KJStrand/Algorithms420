# CS 420 Algorithms Honors Project 
Program to find outerplanar embedding of graph, using Manfred Weigers' trick to achieve O(n) time

- outerplanarSlow.py - Naive implementation to sort graph into outerplanar embedding given adjancency list (slow).
- outerplanarDict.py - Uses dictionary to achieve expected O(n) sort time.
- outerplanarDirtyEdges.py - Uses Manfred Weigers' edge indexing trick ("clean" or "dirty" edges) to achieve worst case O(n) sort time.
- weigers.py - Removed comments from outerplanarDirtyEdges.py
