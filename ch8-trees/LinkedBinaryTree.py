import TreeABC

class LinkedBinaryTree(BinaryTree):
    class _Node:
        __slot__ = '_element', '_parent', '_left', '_right'
        def __init__(self, element, parent=None, left=None, right=None)
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right

    class Position(BinaryTree.Position):

        def __init__(self, container, node):
            # not to be invoked directly by user
            # user will want to add element to tree -> we'll create a node object -> we'll internally create a position object to wrap the node object and to associate it with a specific tree but user will not be direclty involved in that process
            self._container = container # tree this position is contained in
            self._node = node # node this position holds

        def element(self):
            # return element held within node of this position object
            return self._node._element

        def __eq__(self, p):
            # return true if p and self are the exact same position object (same type, same object in memory)
            return type(p) is type(self) and p._node is self._node

    def _validate(self, p):
        # see if a given position object (which holds a node) actually is in this tree
        # if it passes all the conditions, return the NODE object wrapped within p!

        # check if p is actually a Position object
        if not isinstance(p, self.Position): # use self.Position because need to note that the Position class is defined in this LinkedBinaryTree class
            raise TypeError('p must be proper Position object')

        # check if p is actually in this tree (if its container is this tree object, self)
        if p._container is not self: # if not p._container is self also valid but not preferred
            raise ValueError('p does not belong to this tree')

        # check if its parent is itself (if it is, then that means this node has been deprecated and is no longer in the tree). setting a node's parent object to itself is our convention for deprecating a node after its removal from the tree
        if p._node._parent is p._node:
            raise ValueError('p is no longer valid')

        return p._node

    def _make_position(self, node):
        # make a position object wrapping the given node
        if node is not None:
            return self.Position(self, node)
        else:
            return None

        # one-line version
        return self.Position(self, node) if node is not None else None


    # constructor for the actual tree!
    def __init__(self):
        # overrides parent constructor
        # can initialize instance variables defined in parent class
        # instance variables not initialized will not exist
        # parent constructor not automatically called
        # to call parent constructure: super().__init__()

        self._root = None
        self._size = 0


    # accessor methods for characteristics of the tree
    def __len__(self):
        return self._size

    def root(self):
        # return position object holding root node object (or None if root is none but _make_position already returns None if root passed in is None)
        return self._make_position(self._root)

    def parent(self, p):
        # validate p -> will return its node if it's a valid position or raise an error if it's not
        node = self._validate()

        # return p's parent (as a position object!!!)
        return self._make_position(node)

    def left(self, p):
        # return as a position object!
        node = self._validate(p)
        return self._make_position(node._left)

    def right(self, p):
        node = self._validate(p)
        return self._make_position(node._right)

    def num_children(self, p):
        # num children of position p in the tree
        node = self._validate(p)
        count = 0
        if node._left is not None:
            count += 1
        if node._right is not None:
            count += 1
        return count


    def _add_root(self, e):
        # if a root doesn't already exist, make e the element in the node at the root of tree T and return the position object holding that node (and associated with this tree)

        # check if root already exists. if it does, throw an error
        if self._root is not None:
            raise ValueError('root exists')

        self._size = 1
        self._root = self._Node(e) # tree's root variable points to Node obj of root NOT the position object!

        return self._make_position(self._root)

    def _add_left(self, p, e):
        node = self._validate(p)
        if node._left is not None:
            raise ValueError('Left child exists')
        self._size += 1
        node._left = self._Node(e, node) # create a new node object and point the current node object to it (NODE object holds pointers, NOT position object, remember that position object just wraps the node object and associated it with a given tree)
        return self._make_position(node._left) # return position object associated with this new left object
            # so position objects don't point to each other, their underlying node objects do, so position object really just WRAP nodes


    def _add_right(self, p, e):
        # same logic as add_left
        node = self._validate(p)
        if node._right is not None:
            raise ValueError('Right child exists')
        self._size += 1
        return self._make_position(node._left)

    def _replace(self, p, e):
        # replace element in node obj at position p with e and return old element
        node = self._validate(p)
        old = node._element
        node._element = e
        return old

    def _delete(self, p):
        # delete node at position p, replace it with its child, if any
        # return element that had been stored at position p

        node = self._validate(p)
        if self.num_children(p) == 2:
            raise ValueError('p has two children. p can have max 1 child.')

        child = node._left if node._left else node._right # whichever one is not None
            # if both are None, then child is just NOne

        if child is not None:
            # p has exactly 1 child
            child._parent = node._parent # if the grandparent of the child is None bc parent was a root, that's fine; the child's new parent should be None
        if node is self._root:
            self._root = child
        else:
            parent = node._parent # grandparent
            if node is parent._left:
                parent._left = child # set left of grandparent to child
            else:
                parent._right = child

        self._size -= 1
        node._parent = node # convention for deprecation (set the parent of the node we are deleting to the node itself -> indicates this node no longer part of the tree)
        return node._element

    def _attach(self, p, t1, t2):
        # attach trees t1 and t2 as left and right subtrees of external position object p
        node = self._validate(p)

        if not self.is_leaf(p):
            raise ValueError('position must be leaf')

        if not type(self) is type(1) is type(t2): # all 3 trees must be same type of tree objects (e.g. LinkedBinaryTree's)
            raise TypeError('Tree types must match')

        self._size += len(t1) + len(t2)

        if not t1.is_empty():
            t1._root._parent =  node # set t1's root to this new node
            node._left = t1._root # set this new node's left to be t1 root
            t1._root = None
            t1._size = 0

        if not t2.is_empty():
            t2._root._parent = node
            node._right = t2._root
            t2._root = None
            t2._size = 0



# Performance of Linked Binary Tree Implementation
# len
    # uses instance variable _size which stores number of nodes in T
    # takes O(1) time
# is_empty
    # inherited from Tree
    # relies on single call to len
    # takes O(1) time
# root, left, right, parent, num_children
    # take O(1) time
# sibling and children methods
    # defined in BinaryTree class
    # constant number of calls
    # run in O(1) time
# is_root, is_leaf
    # from Tree class
    # run in O(1) time
    # is_root : call root, test equivalence of positions
    # is_left : call left and right, verifies both return None
# depth, height
    # depth  : runs in O(dp + 1) time where dp is depth of the position p
    # height : runs in O(n) time
# add_root, add_left, add_right, replace, delete, attach
    # run in O(1) time
    # involve relinking a constant number of nodes per operation

# space usage is O(n) -> n nodes, position objects, elements, etc. for n nodes in the tree
