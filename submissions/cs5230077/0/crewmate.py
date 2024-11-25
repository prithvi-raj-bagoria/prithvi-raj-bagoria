from heap import Heap

class CrewMate:
    '''
    A class to represent a crewmate.
    '''
    def __init__(self):
        '''
        Initializes a crewmate with no load and an empty list of assigned treasures.
        '''
        self.load = 0  
        self.assigned_treasures = []  

    def add_treasure(self, treasure):
        '''
        Assigns a treasure to the crewmate and updates the load.
        '''
        self.assigned_treasures.append(treasure)
        self.load += treasure.size

    def process_treasures(self):
        '''
        Handles the treasure processing for this crewmate, with the ability to preempt.
        '''
        current_time = 0  
        remaining_treasures = self.assigned_treasures[:]
        remaining_treasures.sort(key=lambda x: x.arrival_time)
        available_queue = []
        ongoing_treasure = None

        events = Heap(lambda a, b: a[0] < b[0], [])  # Custom heap for managing events

        for treasure in remaining_treasures:
            events.insert((treasure.arrival_time, 'arrival', treasure))

        while events.size > 0 or ongoing_treasure:
            
            if ongoing_treasure:
                estimated_completion_time = current_time + ongoing_treasure.remaining_size
                if events.size:
                    upcoming_event_time = min(estimated_completion_time, events.top()[0])
                else:
                    upcoming_event_time = estimated_completion_time
            else:
                if events.size:
                    upcoming_event_time = events.top()[0]
                else:
                    break  

            time_to_next_event = upcoming_event_time - current_time

            if ongoing_treasure:
                ongoing_treasure.processed_time += time_to_next_event
                ongoing_treasure.remaining_size -= time_to_next_event
                if ongoing_treasure.remaining_size <= 0:
                    ongoing_treasure.completion_time = upcoming_event_time
                    ongoing_treasure = None

            current_time = upcoming_event_time

            while events.size and events.top()[0] == current_time:
                event_time, event_type, treasure = events.extract()
                if event_type == 'arrival':
                    treasure.processed_time = 0
                    treasure.remaining_size = treasure.size
                    available_queue.append(treasure)

            if available_queue or ongoing_treasure:
                candidates = available_queue[:]
                if ongoing_treasure and ongoing_treasure.remaining_size > 0:
                    candidates.append(ongoing_treasure)

                def priority_metric(treasure):
                    waiting_time = current_time - treasure.arrival_time
                    return waiting_time - treasure.remaining_size

                candidates.sort(key=lambda treasure: (-priority_metric(treasure), treasure.id))
                next_treasure = candidates[0]

                if ongoing_treasure != next_treasure:
                    if ongoing_treasure and ongoing_treasure.remaining_size > 0:
                        available_queue.append(ongoing_treasure)
                    if next_treasure in available_queue:
                        available_queue.remove(next_treasure)
                    ongoing_treasure = next_treasure
                else:
                    if ongoing_treasure in available_queue:
                        available_queue.remove(ongoing_treasure)
            else:
                ongoing_treasure = None

            if not events.size and not ongoing_treasure:
                break

            if not events.size and ongoing_treasure:
                upcoming_event_time = current_time + ongoing_treasure.remaining_size
                time_to_next_event = upcoming_event_time - current_time
                ongoing_treasure.processed_time += time_to_next_event
                ongoing_treasure.remaining_size -= time_to_next_event
                ongoing_treasure.completion_time = upcoming_event_time
                current_time = upcoming_event_time
                ongoing_treasure = None

                if available_queue:
                    candidates = available_queue[:]
                    candidates.sort(key=lambda treasure: (-priority_metric(treasure), treasure.id))
                    ongoing_treasure = candidates[0]
                    available_queue.remove(ongoing_treasure)