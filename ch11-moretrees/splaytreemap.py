# implementation of splay trees is simple adaptation of standard BST
# based on TreeMap class
# the original TreeMap class makes calls to _rebalance_access method in __getitem__ and __setitem__ when modifting the value associated with an existing key and after any map operations that result in a failed search

class SplayTreeMap(TreeMap):
    '''Sorted map implementation using a splay tree.'''

    # ----- splay operation -----
    def _splay(self, p):
        while p != self.root(): # node p = x
            parent = self.parent(p) # parent = y
            grand = self.parent(parent) # grandparent = z
            if grand is None:
                # zig
                self._rotate(p) # move p up
            elif (parent == self.left(p)) == (grand == self.left(parent)): # y and x are both RC or both LC
                # zig zig
                self._rotate(parent) # move parent up
                self._rotate(p) # move p up
            else:
                # zig zag
                self._rotate(p) # move p up
                self._rotate(p) # move p up

    # ----- override balancing hooks -----
    def _rebalance_insert(self, p):
        self._splay(p)

    def _rebalance_delete(self, p):
        if p is not None:
            self._splay(p)

    def _rebalance_access(self, p):
        self._splay(p)
