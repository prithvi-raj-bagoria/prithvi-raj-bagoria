'''
Python Code to implement a heap with general comparison function
'''
class Heap:
    '''
    Class to implement a heap with general comparison function
    '''
    def __init__(self, comparison_function, init_array):
        '''
        Arguments:
            comparison_function : function : A function that takes in two arguments and returns a boolean value
            init_array : List[Any] : The initial array to be inserted into the heap
        Returns:
            None
        Description:
            Initializes a heap with a comparison function
            Details of Comparison Function:
                The comparison function should take in two arguments and return a boolean value
                If the comparison function returns True, it means that the first argument is to be considered smaller than the second argument
                If the comparison function returns False, it means that the first argument is to be considered greater than or equal to the second argument
        Time Complexity:
            O(n) where n is the number of elements in init_array
        '''
        
        # Write your code here
        self.compare = comparison_function
        self._data = init_array[:]  # heap array copy of init_array
        self.size = len(self._data)

        if self.size == 0:
            # Handle empty heap case by not trying to access or build a heap
            self._root = None
            self._lastNode = None
        else:
            # Bottom-up heap construction
            height = self.height(self.size - 1) - 1  # starting with children at height h-1

            while height >= 0:
                start = int(2 ** height - 1)
                end = min(int(2 ** (height + 1) - 1), self.size)
                for i in range(start, end):  # traverse all the children and do downHeap
                    self.downHeap(i)
                height -= 1

            self._root = self._data[0]
            self._lastNode = self.size - 1

    def insert(self, value):
        '''
        Arguments:
            value : Any : The value to be inserted into the heap
        Returns:
            None
        Description:
            Inserts a value into the heap
        Time Complexity:
            O(log(n)) where n is the number of elements currently in the heap
        '''
        self._data.append(value)  # Append new value at the end
        self.size += 1
        self.upHeap(self.size - 1)  # Restore heap property by moving the new element up
        self._lastNode = self.size-1
    
    def extract(self):
        '''
        Arguments:
            None
        Returns:
            Any : The value extracted from the top of heap
        Description:
            Extracts the value from the top of heap, i.e. removes it from heap
        Time Complexity:
            O(log(n)) where n is the number of elements currently in the heap
        '''
        
        # Write your code here
        if self.size == 0:
            return None  # Return None if heap is empty

        # Swap the root with the last element and remove the last element
        root = self._data[0]
        self._data[0] = self._data[self.size - 1]
        self._data.pop()  # Remove the last element
        self.size -= 1

        self._lastNode =  self.size - 1
        if self.size > 0:
            self.downHeap(0)  # Restore heap property by moving down the new root

        return root
    
    def top(self):
        '''
        Arguments:
            None
        Returns:
            Any : The value at the top of heap
        Description:
            Returns the value at the top of heap
        Time Complexity:
            O(1)
        '''
        # Write your code here
        return None if self.is_empty() else self._data[0]
    
    # You can add more functions if you want to

    def __len__(self):
        return len(self._data)
    
    def is_empty( self ):
        return len(self) == 0

    def parent( self , i : int):
        return (i-1)//2
    
    def left( self , i : int):
        return int(2*i) + 1
    
    def right(self ,i : int):
        return int(2*i) + 2
    
    def has_parent(self , i:int):
        return self.parent(i) >=0
    
    def has_left( self , i:int):
        return self.left(i) < len(self)
    
    def has_right( self, i : int):
        return self.right(i) < len(self)
    
    def swap( self , i , j):
        self._data[i] , self._data[j] = self._data[j] , self._data[i]
        return None
    
    def height(self  , i:int ):
        if self.has_parent(i):
            return 1 + self.height(self.parent(i))
        return 0

    def upHeap( self , i : int, time:int=0):
        if not self.has_parent(i):
            return None
        parent = self.parent(i)
        if self.compare( self._data[i] , self._data[parent]) == True: # self._data[i] > self._data[parent]
            #swap parent and i
            self.swap(i , parent)
            #upheap for parent
            self.upHeap(parent)
        return None
    
    def downHeap( self ,  i : int):
        left = right = None
        if self.has_left(i):
            left = self.left(i)
        min_child = left

        if self.has_right(i):
            right = self.right(i)
            if self.compare(self._data[left],self._data[right]) == False:
                min_child = right
        
        if min_child != None and self.compare(self._data[min_child] , self._data[i]) == True:
            self.swap(min_child , i)
            self.downHeap(min_child)

        return None

def min_compare(val1 , val2):
    return -1 if val1<val2 else 1 if val1>val2 else 0
def max_compare(val1 , val2):
    return 1 if val1<val2 else -1 if val1>val2 else 0