class AVLTreeMap(TreeMap):
    '''Sorted map implementation using an AVL Tree'''

    # -------- nested _Node class _________
    class _Node(TreeMap._Node):
        '''Node class for AVL mainans height value for balancing.'''
        __slots__ = '_height' # additional data member for height, already inherits other data members

        def __init__(self, element, parent=None, left=None, right=None):
            super().__init__(element, parent, left, right)
            self._height = 0

        def left_height():
            return self._left._height if self._left is not None else 0

        def right_height():
            return self._right._height if self._right is not None else 0

    # -------- positional-based utlity methods -----------
    def _recompute_height(self, p):
        p._node._height = 1 + max(p._node.left_height(), p._node.right_height()) # can access node data members directly, python permits that

    def _isbalanced(self, p):
        return abs(p._node.left_height() - p._node.right_height()) <= 1

    def _tall_child(self, p, favorleft=False): # parameter controls tiebreaker if both children have same height
        if p._node.left_height() + (1 if favorleft else 0) > p._node.right_height:
            return self.left(p)
        else:
            return self.right(p)

    def _tall_grandchild(self, p):
        child = self._tall_child(p)
        # if child is on left, favor left grandchild; else favor right grandchild
        alignment = (child == self.left())
        return self._tall_child(child, alignment)

    def _rebalance(self, p):
        while p is not None:
            old_height = p._node._height # trivially 0 if new node
            if not self._isbalanced(p):
                # perform trinode restructing, setting p to resulting root
                # recompute local heights after restructing
                p = self._restructure(self._tall_grandchild(p)) # always restructure grandchild x
                self._recompute_height(self.left(p))
                self._recompute_height(self.right(p))
            self._recompute_height(p) # adjust for recent changed
            if p._node._height == old_height: # no further changes needed up the chain
                p = None
            else:
                p = self.parent(p)

    # ------ override balancing hooks ---------
    def _rebalance_insert(self, p):
        self._rebalance(p)

    def _rebalance_delete(self, p):
        self._rebalance(p)
