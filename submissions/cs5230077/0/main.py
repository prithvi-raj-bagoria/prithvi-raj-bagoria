import heap
import straw_hat
import treasure
import sys

sys.setrecursionlimit(10**6)
            
class Parser():
    def __init__(self, filename):
        self.filename = filename
        self.data = []
        self.read_data()
        
    def read_data(self):
        with open(self.filename, 'r') as f:
            for line in f:
                self.data.append(line.strip())
    
    def parse(self):
        pass

class ParserTreasure(Parser):
    def parse(self):
        m = int(self.data[0])
        treasury = straw_hat.StrawHatTreasury(m)
        for i in range(1, len(self.data)):
            try:
                query = self.data[i].split()
                query_type = query[0]
                if query_type == 'Add':
                    id, size, arrival_time = query[1], query[2], query[3]
                    id = int(id)
                    size = int(size)
                    arrival_time = int(arrival_time)
            except:
                raise ValueError('Invalid Input')
            if query_type == 'Add':
                try:
                    treasure_obj = treasure.Treasure(id, size, arrival_time)
                    treasury.add_treasure(treasure_obj)
                    print(f'Treasure {id} added to treasury')
                except:
                    print(f"Cannot add treasure {id} to treasury")
            elif query_type == 'Get':
                try:
                    processed = treasury.get_completion_time()
                    print('Completion Time:', [(treasure_obj.id, treasure_obj.completion_time) for treasure_obj in processed])
                except:
                     print('Cannot get completion time')
            else:
                raise ValueError('Invalid Input')

class ParserHeap(Parser):
    def __init__(self, filename, comparison = lambda a, b: a<b):
        super().__init__(filename)
        self.comp = comparison
    
    def parse(self):
        h = heap.Heap(self.comp, [])
        num = 0
        for i in range(len(self.data)):
            query = self.data[i].split()
            if query[0] == 'Insert':
                try:
                    h.insert(int(query[1]))
                    num += 1
                    print(f'{query[1]} inserted')
                except:
                    print(f'Cannot insert {query[1]}')
            elif query[0] == 'Extract':
                try:
                    print(f'{h.extract()} extracted')
                    num -= 1
                except:
                    print('Cannot extract')
            elif query[0] == 'Top':
                try:
                    print(f'Top: {h.top()}')
                except:
                    print('Cannot get top')
            elif query[0] == 'Print':
                try:
                    for i in range(num):
                        print(h.extract(), end = ' ')
                        num -= 1
                    print()
                except:
                    print('Cannot print')
            else:
                raise ValueError('Invalid Input')
            
if __name__ == '__main__':
    print("----------tc_heap1.txt----------")
    parser = ParserHeap('tc_heap1.txt')
    parser.parse()
    print()
    
    print("----------tc_treasury1.txt----------")
    parser = ParserTreasure('tc_treasury1.txt')
    parser.parse()
    print()
    
    print("----------tc_treasury2.txt----------")
    parser = ParserTreasure('tc_treasury2.txt')
    parser.parse()
    print()
