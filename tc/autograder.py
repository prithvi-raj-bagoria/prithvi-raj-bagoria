import json
import heap_tc
import signal
import os
import sys
import pandas as pd
import importlib
import contextlib
import io

class Response():
    def __init__(self, status, body = None, comment = ''):
        self.status = status
        self.body = body
        self.comment = comment

class Student():
    def __init__(self, student_dir, tc_meta, log_dir, output_dir, submission_dir):
        self.id = student_dir.split()[-1]
        self.log_file_address = os.path.join(log_dir, f'{self.id}_log.json')
        self.output_address = os.path.join(output_dir, f'{self.id}')
        os.makedirs(self.output_address, exist_ok=True)
        self.output_file_address = {}
        for test_case_meta in tc_meta['heap']:
            self.output_file_address[test_case_meta['name']] = os.path.join(self.output_address, f'{test_case_meta["name"]}_out.txt')
        for test_case_meta in tc_meta['treasure']:
            self.output_file_address[test_case_meta['name']] = os.path.join(self.output_address, f'{test_case_meta["name"]}_out.txt')
        student_dir = os.path.join(submission_dir, student_dir)
        for folder in sorted(os.listdir(student_dir), reverse=True):
            student_dir = os.path.join(student_dir, folder)
            break
        sys.path.insert(0, student_dir)
        try:
            self.heap_module = importlib.import_module('heap', package=student_dir)
            importlib.reload(self.heap_module)
        except:
            self.heap_module = None
        try:
            self.heap_class = self.heap_module.Heap
        except:
            self.heap_class = None

        try:
            self.crewmate_module = importlib.import_module('crewmate', package=student_dir)
            importlib.reload(self.crewmate_module)
        except:
            self.crewmate_module = None

        try:
            self.custom_module = importlib.import_module('custom', package=student_dir)
            importlib.reload(self.custom_module)
        except:
            self.custom_module = None

        try:
            self.treasure_module = importlib.import_module('treasure', package=student_dir)
            importlib.reload(self.treasure_module)
        except:
            self.treasure_module = None
        try:
            self.treasure_class = self.treasure_module.Treasure
        except:
            self.treasure_class = None

        try:
            self.straw_hat_module = importlib.import_module('straw_hat', package=student_dir)
            importlib.reload(self.straw_hat_module)
        except:
            self.straw_hat_module = None
        try:
            self.straw_hat_class = self.straw_hat_module.StrawHatTreasury
        except:
            self.straw_hat_class = None

        sys.path.pop(0)
    
    def clean(self):
        delete(self.heap_class)
        delete(self.heap_module)
        delete(self.straw_hat_class)
        delete(self.straw_hat_module)
        delete(self.treasure_class)
        delete(self.treasure_module)
        delete(self.custom_module)
        delete(self.crewmate_module)

def handle_timeout(signum, frame):
    raise TimeoutError("Timed out")

def timeout(func, timeout_duration, *args):
    signal.signal(signal.SIGALRM, handle_timeout)
    signal.setitimer(signal.ITIMER_REAL, timeout_duration)
    try:
        result = Response(True, body=func(*args))
        signal.setitimer(signal.ITIMER_REAL, 0)
    except TimeoutError as exc:
        result = Response(False, comment='Timeout')
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
    return result

def delete(element):
    if element:
        del element

class Autograder():
    def __init__(self, root_dir, submission_dir, log_dir, output_dir, test_case_json_file, buffer_testcases = True):
        self.root_dir = root_dir
        self.submission_dir = submission_dir
        self.log_dir = log_dir
        self.output_dir = output_dir
        self.test_case_json_file = test_case_json_file
        self.buffer_testcases = buffer_testcases
        self.buffer = {}
    
    def run(self, index):
        data = self.parse_json()
        if self.buffer_testcases:
            self.buffer_test_case_from_json(data)
        # Create students, iterate over them and run
        student_dir = sorted(os.listdir(self.submission_dir))[index]
        if not os.path.isdir(os.path.join(self.submission_dir, student_dir)):
            return
        with contextlib.redirect_stdout(io.StringIO()):
            student = Student(student_dir, data, self.log_dir, self.output_dir, self.submission_dir)
            self.run_per_student(data, student)
        student.clean()
        del student
            
    def run_per_student(self, json_data, student):
        log_data = {"heap_tc": [], "treasure_tc": [], "marks": 0}
        for heap_test_case_meta in json_data['heap']:
            heap_test_case = self.get_test_case(heap_test_case_meta)
            if not student.heap_class:
                response = Response(False, comment="Error Importing heap.Heap")
            else:
                response = self.run_heap_test_case(heap_test_case, 
                                                student.output_file_address[heap_test_case_meta['name']], 
                                                student.heap_class)
            log_data["heap_tc"].append({
                "name": heap_test_case_meta['name'],
                "status": response.status,
                "comment": response.comment,
                "marks": response.status * heap_test_case_meta['marks']
            })
            log_data["marks"] += response.status * heap_test_case_meta['marks']
        for treasure_test_case_meta in json_data['treasure']:
            treasure_test_case = self.get_test_case(treasure_test_case_meta)
            if not student.treasure_class:
                response = Response(False, comment="Error Importing treasure.Treasure")
            elif not student.straw_hat_class:
                response = Response(False, comment="Error Importing straw_hat.StrawHatTreasury")
            else:
                response = self.run_treasure_test_case(treasure_test_case, 
                                                student.output_file_address[treasure_test_case_meta['name']], 
                                                student.straw_hat_class,
                                                student.treasure_class)
            log_data["treasure_tc"].append({
                "name": treasure_test_case_meta['name'],
                "status": response.status,
                "comment": response.comment,
                "marks": response.status * treasure_test_case_meta['marks']
            })
            log_data["marks"] += response.status * treasure_test_case_meta['marks']

        log_data["marks"] = round(10*log_data["marks"])/10

        with open(student.log_file_address, 'w') as log_file:
            json.dump(log_data, log_file, indent=4)
 
    def parse_json(self):
        with open(self.test_case_json_file) as json_file:
            data = json.load(json_file)
        return data
    
    def parse_file(self, file_address):
        with open(file_address) as file:
            parsed_data = file.readlines()
        for i in range(len(parsed_data)):
            parsed_data[i] = parsed_data[i].strip()
        return parsed_data
    
    def buffer_test_case(self, test_case_meta):
        if self.buffer_testcases:
            self.buffer[test_case_meta['name']] = self.get_test_case(test_case_meta)
        else:
            raise Exception("Buffering is disabled. Cannot buffer testcases.")
    
    def buffer_test_case_from_json(self, json_data):
        for _, test_cases_meta in json_data.items():
            for test_case_meta in test_cases_meta:
                self.buffer_test_case(test_case_meta)
                
    def get_test_case(self, test_case_meta):
        if self.buffer_testcases and test_case_meta['name'] in self.buffer:
            return self.buffer[test_case_meta['name']]
        else:
            test_case = {}
            for key, value in test_case_meta.items():
                test_case[key] = value
            test_case['tc_data'] = self.parse_file(os.path.join(self.root_dir, 'tc', test_case_meta['input_file']))
            test_case['expected_output'] = self.parse_file(os.path.join(self.root_dir, 'tc', test_case_meta['output_file']))
            return test_case
                
    def parse_heap_test_case(self, heap_test_case, output_file_address, heap_class):
        with open(output_file_address, 'w') as output_file:
            num = 0
            dtype_name = heap_test_case['tc_data'][0]
            dtype = heap_tc.dtype_map[dtype_name]
            init_arr = []
            for i in range(1, len(heap_test_case['tc_data'])):
                query = heap_test_case['tc_data'][i].split()
                if query[0] == 'Init':
                    init_arr.append(dtype(i, *query[1:]).repair())
                    num += 1
                else:
                    break
            try:
                h = heap_class(dtype.comp, init_arr)
                output_file.write('Heap initialized\n')
            except TimeoutError:
                raise TimeoutError("Timed Out")
            except:
                output_file.write('Cannot initialize heap\n')
                return
            for i in range(i, len(heap_test_case['tc_data'])):
                query = heap_test_case['tc_data'][i].split()
                if query[0] == 'Insert':
                    try:
                        h.insert(dtype(i, *query[1:]).repair())
                        num += 1
                        output_file.write(f'{dtype(i, *query[1:]).repair()} inserted\n')
                    except TimeoutError:
                        raise TimeoutError("Timed Out")
                    except:
                        output_file.write(f'Cannot insert {dtype(i, *query[1:]).repair()}\n')
                elif query[0] == 'Extract':
                    try:
                        output_file.write(f'{h.extract()} extracted\n')
                        num -= 1
                    except TimeoutError:
                        raise TimeoutError("Timed Out")
                    except:
                        output_file.write('Cannot extract\n')
                elif query[0] == 'Top':
                    try:
                        output_file.write(f'Top: {h.top()}\n')
                    except TimeoutError:
                        raise TimeoutError("Timed Out")
                    except:
                        output_file.write('Cannot get top\n')
                elif query[0] == 'Print':
                    try:
                        output_file.write("Printing heap:\n")
                        for i in range(num):
                            output_file.write(f'{h.extract()}\n')
                            num -= 1
                        output_file.write('\n')
                    except TimeoutError:
                        raise TimeoutError("Timed Out")
                    except:
                        output_file.write('Cannot print\n')
                else:
                    raise ValueError('Invalid Input for heap')
           
    def run_heap_test_case(self, heap_test_case, output_file_address, heap_class):
        response = timeout(self.parse_heap_test_case,
                           heap_test_case['time_limit'],
                           heap_test_case, output_file_address, heap_class)
        if not response.status:
            return response
        return self.compare_outputs(heap_test_case, output_file_address)
    
    def parse_treasure_test_case(self, treasure_test_case, output_file_address, straw_hat_class, treasure_class):
        with open(output_file_address, 'w') as output_file:
            m = int(treasure_test_case['tc_data'][0])
            try:
                treasury = straw_hat_class(m)
            except TimeoutError:
                raise TimeoutError('timed out')
            except:
                output_file.write('Can not initialize straw hat treasury')
                return
            for i in range(1, len(treasure_test_case['tc_data'])):
                try:
                    query = treasure_test_case['tc_data'][i].split()
                    query_type = query[0]
                    if query_type == 'Add':
                        id, size, arrival_time = query[1], query[2], query[3]
                        id = int(id)
                        size = int(size)
                        arrival_time = int(arrival_time)
                except TimeoutError:
                    raise TimeoutError("Timed Out")
                except:
                    raise ValueError('Invalid Input')
                if query_type == 'Add':
                    try:
                        treasure_obj = treasure_class(id, size, arrival_time)
                        treasury.add_treasure(treasure_obj)
                        output_file.write(f'{id} added\n')
                    except TimeoutError:
                        raise TimeoutError("Timed Out")
                    except:
                        output_file.write(f"Cannot add {id}\n")
                elif query_type == 'Get':
                    try:
                        processed = treasury.get_completion_time()
                        output_file.write(f'Completion Time: {sorted([(treasure_obj.id,treasure_obj.completion_time) for treasure_obj in processed])}\n')
                    except TimeoutError:
                        raise TimeoutError("Timed Out")
                    except:
                        output_file.write('Cannot get completion time\n')
                else:
                    raise ValueError('Invalid Input for treasure')
    
    def run_treasure_test_case(self, treasure_test_case, output_file_address, straw_hat_class, treasure_class):
        response = timeout(self.parse_treasure_test_case,
                           treasure_test_case['time_limit'],
                           treasure_test_case, output_file_address, straw_hat_class, treasure_class)
        if not response.status:
            return response
        return self.compare_outputs(treasure_test_case, output_file_address)
    
    def compare_outputs(self, test_case, output_file_address):
        output_data = self.parse_file(output_file_address)
        expected_output = test_case['expected_output']
        if len(output_data) != len(expected_output):
            return Response(False, comment='Output length mismatch')
        for i in range(len(output_data)):
            if output_data[i] != expected_output[i]:
                return Response(False, comment=f'Output mismatch at line {i+1}')
        return Response(True)

    def compile_logs(self):
        compiled_log = []
        for log in sorted(os.listdir(self.log_dir)):
            if os.path.splitext(log)[-1] != ".json":
                continue
            with open(os.path.join(self.log_dir, log)) as log_file:
                data = json.load(log_file)
            kerberos = log.split('_')[0]
            compiled_log.append({
                "entry no": "20"+kerberos[-6:-4]+kerberos[:-6].upper()+kerberos[-4:],
                "email id": kerberos+"@iitd.ac.in",
                "marks": data['marks']
            })
        df = pd.DataFrame(compiled_log)
        df.to_csv(os.path.join(self.log_dir, 'compiled_log.csv'), index=False)
        print(f'Mean: {df['marks'].mean()}\tStdDev: {df["marks"].std()}')

root_dir = os.path.abspath(__file__)
root_dir = os.path.dirname(os.path.dirname(root_dir))
# submission_dir = os.path.join(root_dir, 'sub_dummy')
submission_dir = os.path.join(root_dir, 'submissions')

log_dir = os.path.join(root_dir, 'logs')
os.makedirs(log_dir, exist_ok=True)
output_dir = os.path.join(root_dir, 'outputs')
os.makedirs(output_dir, exist_ok=True)

autograder = Autograder(
    root_dir=root_dir,
    submission_dir=submission_dir,
    log_dir=log_dir,
    output_dir=output_dir,
    test_case_json_file=os.path.join(root_dir, 'tc', 'test_case.json'),
    buffer_testcases=True
)
if int(sys.argv[1])>=0:
    autograder.run(index = int(sys.argv[1]))
else:
    autograder.compile_logs()