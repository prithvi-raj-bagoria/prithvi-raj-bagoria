import random
from enum import Enum

seed = 68

class HeapOperation(Enum):
    INSERT = 0
    EXTRACT = 1
    TOP = 2
    INIT = 3
    PRINT = 4
    
    def __str__(self):
        return self.name.lower().capitalize()

class HeapObject:
    def __init__(self, id):
        self.id = id
    
    def comp(x, y):
        return (x.eval(), x.id) < (y.eval(), y.id)
    
    def eval(self):
        raise NotImplementedError("Method not implemented")
    
    def __eq__(self, other):
        ret_val = True
        for attr in self.attributes:
            ret_val = ret_val and (getattr(self, attr) == getattr(other, attr))
        return ret_val

    def __str__(self):
        output = ""
        for attr in self.attributes:
            output += str(getattr(self, attr)) + " "
        return output.strip()

    def repair(self):
        for attr in self.attributes:
            if type(getattr(self, attr)) != self.attributes[attr]:
                setattr(self, attr, self.attributes[attr](getattr(self, attr)))
        return self

class ObjectGenerator:
    def __init__(self, dtype, seed=seed):
        self.dtype = dtype
        self.random = random.Random(seed)
        
    def dtype_name(self):
        return self.dtype.__name__
    
    def generate(self, **kwargs):
        kwarg_val = {}
        for key in kwargs:
            if type(kwargs[key]) == tuple:
                kwarg_val[key] = self.random.randint(kwargs[key][0], kwargs[key][1])
            elif type(kwargs[key]) == list:
                kwarg_val[key] = self.random.choice(kwargs[key])
            elif type(kwargs[key]) == int:
                kwarg_val[key] = kwargs[key]
            elif type(kwargs[key]) == float:
                kwarg_val[key] = kwargs[key]
            elif type(kwargs[key]) == str:
                kwarg_val[key] = kwargs[key]
            else:
                kwarg_val[key] = kwargs[key]()
        if id not in kwarg_val:
            kwarg_val['id'] = 0
        return self.dtype(**kwarg_val)
    
    def generate_list(self, n, **kwargs):
        return [self.generate(**kwargs) for _ in range(n)]
    
class IntHeapObject(HeapObject):
    attributes = {'val': int}
    
    def __init__(self, id, val):
        super().__init__(id)
        self.val = val
        
    def eval(self):
        return self.val
    
    def __lt__(self, other):
        return (self.val, self.id) < (other.val, other.id)

class NegIntHeapObject(HeapObject):
    attributes = {'val': int}
    
    def __init__(self, id, val):
        super().__init__(id)
        self.val = val
        
    def eval(self):
        return -self.val

    def __lt__(self, other):
        return (self.val, self.id) < (other.val, other.id)

class StringHeapObject(HeapObject):
    attributes = {'val': str}
    
    def __init__(self, id, val):
        super().__init__(id)
        self.val = val
        
    def eval(self):
        return self.val

    def __lt__(self, other):
        return (self.val, self.id) < (other.val, other.id)

class StringSortHeapObject(HeapObject):
    attributes = {'val': str}
    
    def __init__(self, id, val):
        super().__init__(id)
        self.val = val
        
    def eval(self):
        return "".join(sorted(list(self.val)))
    
    def __lt__(self, other):
        return (self.val, self.id) < (other.val, other.id)
    
class StringLengthHeapObject(HeapObject):
    attributes = {'val': str}

    def __init__(self, id, val):
        super().__init__(id)
        self.val = val
    
    def eval(self):
        return len(self.val)
    
    def __lt__(self, other):
        return (self.val, self.id) < (other.val, other.id)
    
class ListLengthHeapObject(HeapObject):
    attributes = {'val': lambda lst: list_constructor(lst, int)}
    
    def __init__(self, id, val):
        super().__init__(id)
        self.val = val
        
    def eval(self):
        return len(self.val)
    
    def __lt__(self, other):
        return (self.val, self.id) < (other.val, other.id)
    
    def __str__(self):
        return ",".join(str(elem) for elem in self.val)
    
class ListSumHeapObject(HeapObject):
    attributes = {'val': lambda lst: list_constructor(lst, int)}
    
    def __init__(self, id, val):
        super().__init__(id)
        self.val = val

    def eval(self):
        return sum(self.val)
    
    def __lt__(self, other):
        return (self.val, self.id) < (other.val, other.id)
    
    def __str__(self):
        return ",".join(str(elem) for elem in self.val) + " "
    
class ListMaxHeapObject(HeapObject):
    attributes = {'val': lambda lst: list_constructor(lst, int)}
    
    def __init__(self, id, val):
        super().__init__(id)
        self.val = val
    
    def eval(self):
        return max(self.val)

    def __lt__(self, other):
        return (self.val, self.id) < (other.val, other.id)
    
    def __str__(self):
        return ",".join(str(elem) for elem in self.val)

class DistHeapObject(HeapObject):
    attributes = {'val1': int, 'val2': int}
    
    def __init__(self, id, val1, val2):
        super().__init__(id)
        self.val1 = val1
        self.val2 = val2
        
    def eval(self):
        return self.val1**2 + self.val2**2
    
class DistHeapObject2(HeapObject):
    attributes = {'val1': int, 'val2': int}
    
    def __init__(self, id, val1, val2):
        super().__init__(id)
        self.val1 = val1
        self.val2 = val2
        
    def eval(self):
        return abs(self.val1) + abs(self.val2)

class IntGenerator(ObjectGenerator):
    def __init__(self):
        super().__init__(IntHeapObject)
        
class NegIntGenerator(ObjectGenerator):
    def __init__(self):
        super().__init__(NegIntHeapObject)
        
class StringGenerator(ObjectGenerator):
    def __init__(self):
        super().__init__(StringHeapObject)
        
class StringSortGenerator(ObjectGenerator):
    def __init__(self):
        super().__init__(StringSortHeapObject)
        
class StringLengthGenerator(ObjectGenerator):
    def __init__(self):
        super().__init__(StringLengthHeapObject)
        
class ListLengthGenerator(ObjectGenerator):
    def __init__(self):
        super().__init__(ListLengthHeapObject)
        
class ListSumGenerator(ObjectGenerator):
    def __init__(self):
        super().__init__(ListSumHeapObject)
        
class ListMaxGenerator(ObjectGenerator):
    def __init__(self):
        super().__init__(ListMaxHeapObject)
        
class DistGenerator(ObjectGenerator):
    def __init__(self):
        super().__init__(DistHeapObject)
        
class DistGenerator2(ObjectGenerator):
    def __init__(self):
        super().__init__(DistHeapObject2)

def rand_string_gen(min_val, max_val):
    def rand_string():
        return ''.join(chr(random.randint(97, 122)) for _ in range(random.randint(min_val, max_val)))
    return rand_string

def rand_list_gen(min_val, max_val, min_len, max_len):
    def rand_list():
        return [random.randint(min_val, max_val) for _ in range(random.randint(min_len, max_len))]
    return rand_list

def list_constructor(val, dtype):
    return list(map(dtype, val.split(",")))

dtype_map = {
    IntHeapObject.__name__: IntHeapObject,
    NegIntHeapObject.__name__: NegIntHeapObject,
    StringHeapObject.__name__: StringHeapObject,
    StringSortHeapObject.__name__: StringSortHeapObject,
    StringLengthHeapObject.__name__: StringLengthHeapObject,
    ListLengthHeapObject.__name__: ListLengthHeapObject,
    ListSumHeapObject.__name__: ListSumHeapObject,
    ListMaxHeapObject.__name__: ListMaxHeapObject,
    DistHeapObject.__name__: DistHeapObject,
    DistHeapObject2.__name__: DistHeapObject2
}
