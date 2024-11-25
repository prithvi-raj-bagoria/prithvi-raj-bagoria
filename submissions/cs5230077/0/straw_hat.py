'''
    This file defines the StrawHatTreasury class, which manages treasures assigned to crew members.
'''
import crewmate
import heap

class StrawHatTreasury:
    '''
    A class representing the treasury of the StrawHat crew.
    '''
    def __init__(self, num_crewmates):
        '''
        Parameters:
            num_crewmates : int : The total number of crew members (must be a positive integer)
        
        Description:
            Initializes the StrawHat treasury by creating crew members and organizing them in a heap based on their current load.
        
        Time Complexity:
            O(num_crewmates)
        '''
        self.num_crewmates = num_crewmates
        self.crewmates = []
        for i in range(num_crewmates):
            crew_member = crewmate.CrewMate()
            self.crewmates.append(crew_member)
      
        self.crewmate_heap = heap.Heap(
            lambda a, b: a.load < b.load or (a.load == b.load and id(a) < id(b)),
            self.crewmates.copy()
        )
    
    def add_treasure(self, treasure_obj):
        '''
        Parameters:
            treasure_obj : Treasure : The treasure object to be added to the treasury.
        
        Description:
            Finds the crew member with the lowest current load and assigns the treasure to them. After assignment, it re-balances the heap of crew members.
        
        Time Complexity:
            O(log(num_crewmates) + log(num_treasures)) where
                num_crewmates : Total number of crew members.
                num_treasures : Total number of treasures.
        '''
     
        least_loaded_crewmate = self.crewmate_heap.extract()
    
        least_loaded_crewmate.add_treasure(treasure_obj)
     
        self.crewmate_heap.insert(least_loaded_crewmate)
    
    def get_completion_time(self):
        '''
        Returns:
            List[Treasure] : A list of all treasures sorted by their unique IDs, after their completion times have been updated.
        
        Description:
            Processes the treasures for all crew members, updates their completion times, and returns them sorted by ID.
        
        Time Complexity:
            O(num_treasures(log(num_crewmates) + log(num_treasures))) where
                num_crewmates : Total number of crew members.
                num_treasures : Total number of treasures.
        '''
        for crew_member in self.crewmates:
            crew_member.process_treasures()

        all_treasures = []
        for crew_member in self.crewmates:
            all_treasures.extend(crew_member.assigned_treasures)

        all_treasures.sort(key=lambda treasure: treasure.id)
        return all_treasures
