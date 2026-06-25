class Tree:
    """Abstract base class representing a tree structure."""

    class Position:
        """Abstraction representing the location of a single element in the tree."""

        # class doesn't require an __init__ method, python automatically provides one

        def element(self): # return element stored in position object
            raise NotImplementedError('must be implemented by subclass')

        def __eq__(self, other): # check if two positions are equal to each other (self and other)
            raise NotImplementedError('must be implemented by subclass')

        def __ne__(self, other): # check if two positions are NOT equal to each other
            return not (self == other) # uses the __eq__ method previously defined

    # methods that must be implemented by subclasses!
    def root(self): # return Position object representing the root of the tree
        raise NotImplementedError('must be implemented by subclass')

    def parent(self, p): # return position object representing the parent of Position p (if p is root, return None)
        raise NotImplementedError('must be implemented by subclass')

    def num_children(self, p): # return the number of children that Position p has
        raise NotImplementedError('must be implemented by subclass')

    def children(self, p): # generate an iteration through all the children of Position p
        raise NotImplementedError('must be implemented by subclass')

    def __len__(self): # return total number of elements/Positions in the tree
        raise NotImplementedError('must be implemented by subclass')


    # methods implemented in this abstract base class! yay!
    def is_root(self, p): # return true if Position P is the root of the tree
        return self.root() == p # uses the method root() that will be implemented in child class

    def is_leaf(self, p): # return true if Position P has no children (meaning it's a leaf!)
        return self.num_children(p) == 0

    def is_empty(self): # return tree if the tree is empty, meaning its length is 0
        return len(self) == 0
