
class Treasure:
    '''
    Class to implement a treasure
    '''
    def __init__(self, id, size, arrival_time):
        '''
        Arguments:
            id : int : The id of the treasure (unique positive integer for each treasure)
            size : int : The size of the treasure (positive integer)
            arrival_time : int : The arrival time of the treasure (non-negative integer)
        Returns:
            None
        Description:
            Initializes the treasure
        '''
        self.id = id
        self.size = size
        self.arrival_time = arrival_time
        self.completion_time = None
    
    # You can add more methods if required