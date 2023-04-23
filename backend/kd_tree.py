import heapq

class KDTree(object):
    def __init__(self, points, dim, dist_sq_func=None):
        # Euclidean sqaured distance function
        if dist_sq_func is None:
            dist_sq_func = lambda a, b: sum((x - b[i]) ** 2 for i, x in enumerate(a))

        # Creation of KD Tree        
        def make_tree(points, i=0):
            if len(points) > 1:
                # Sort the points by the i-th dimension
                points.sort(key=lambda x: x[i])
                i = (i + 1) % dim
                m = len(points) // 2
                # Recursively build the KD Tree by splitting the points into 2 halves
                return [make_tree(points[:m], i), make_tree(points[m + 1:], i), points[m]]
            if len(points) == 1:
                return [None, None, points[0]]
        
        # Adding a point to the KD Tree
        def add_point(node, point, i=0):
            if node is not None:
                dx = node[2][i] - point[i]
                for j, c in ((0, dx >= 0), (1, dx < 0)):
                    # If branch is empty, add the point to that branch
                    if c and node[j] is None:
                        node[j] = [None, None, point]
                    # If branch is not empty, recursively add the point to that branch
                    elif c:
                        add_point(node[j], point, (i + 1) % dim)

        # Getting the k nearest neighbors of a point
        def get_knn(node, point, k, return_dist_sq, heap, i=0, tiebreaker=1):
            if node is not None:
                dist_sq = dist_sq_func(point, node[2])
                dx = node[2][i] - point[i]
                i = (i + 1) % dim

                # If the heap is not full, add the node to the heap
                if len(heap) < k:
                    heapq.heappush(heap, (-dist_sq, tiebreaker, node[2]))
                
                # If current node is closer than the farthest node in the heap, replace it
                elif dist_sq < -heap[0][0]:
                    heapq.heappushpop(heap, (-dist_sq, tiebreaker, node[2]))
                                
                # Goes into the left branch, then the right branch if needed
                for b in (dx < 0, dx >= 0)[:1 + (dx * dx < -heap[0][0])]:
                    get_knn(node[b], point, k, return_dist_sq, heap, i, (tiebreaker << 1) | b)
            
            # Breaks ties with same distance by using the unique binary number (tiebreaker)
            if tiebreaker == 1:
                return [(-h[0], h[2]) if return_dist_sq else h[2] for h in sorted(heap)][::-1]

        self._add_point = add_point
        self._get_knn = get_knn 
        self._root = make_tree(points)
        
    def add_point(self, point):
        if self._root is None:
            self._root = [None, None, point]
        else:
            self._add_point(self._root, point)

    def get_knn(self, point, k=1, return_dist_sq=True):
        return self._get_knn(self._root, point, k, return_dist_sq, [])