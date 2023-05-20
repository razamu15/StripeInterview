''' #PART 1
Throughout this interview, we'll pretend we're building a new analytical database. Don't worry about actually 
building a database though - these will all be toy problems.

Here's how the database works: all records are represented as maps, with string keys and integer values. 
The records are contained in an array, in no particular order.

To begin with, the database will support just one function: min_by_key. This function scans the array of records 
and returns the record that has the minimum value for a specified key. Records that do not contain the specified 
key are considered to have value 0 for the key. Note that keys may map to negative values!

Here's an example use case: each of your records contains data about a school student. You can use min_by_key to 
answer questions such as "who is the youngest student?" and "who is the student with the lowest grade-point average?"

Implementation notes:

You should handle an empty array of records in an idiomatic way in your language of choice.
If several records share the same minimum value for the chosen key, you may return any of them.
Java function signature:

public static Map<String, Integer> minByKey(String key, List<Map<String, Integer>> records);
Examples (in Python):

assert min_by_key("a", [ {"a": 1, "b": 2} , {"a": 2} ] ) == {"a": 1, "b": 2}
assert min_by_key("a", [{"a": 2}, {"a": 1, "b": 2}]) == {"a": 1, "b": 2}
assert min_by_key("b", [{"a": 1, "b": 2}, {"a": 2}]) == {"a": 2}
assert min_by_key("a", [{}]) == {}
assert min_by_key("b", [{"a": -1}, {"b": -1}]) == {"b": -1}
'''

def min_by_key(key, records_array):

    # min_key_record = { }
    
    # for record in records_array:
        
    #     record_key_value = record[key] if key in record else 0
        
    #     if key not in min_key_record or min_key_record[key] > record_key_value:
    #         min_key_record = record
    
    # return min_key_record
    return first_by_key(key, 'asc', records_array)


def first_by_key(key, direction, records_array):

    # replace_record = lambda x, y: x > y if direction == 'asc' else x <= y
    C = RecordComparator(key, direction)

    result_record = None
    
    for record in records_array:
        
        if C.compare(record, result_record) != 1:
            result_record = record
    
    return result_record

class RecordComparator:

    def __init__(self, key, direction):
        self.key = key
        self.direction = direction

    def _get_limit_value(self):
        if self.direction == 'asc':
            return float('inf')
        else: # direction == 'desc':
            return float('-inf')
        

    def compare(self, rec1, rec2):
        cur_key_value = rec1.get(self.key, 0)
        result_key_value = rec2.get(self.key, 0) if rec2 is not None else self._get_limit_value()

        if self.direction == 'asc':
            if cur_key_value < result_key_value:
                return -1
            elif cur_key_value > result_key_value:
                return 1
            else:
                return 0
        elif self.direction == 'desc':
            if cur_key_value > result_key_value:
                return -1
            elif cur_key_value < result_key_value:
                return 1
            else:
                return 0
        else:
            raise ValueError()


def main():
    # print(min_by_key("a", [ {"a": 1, "b": 2} , {"a": 2} ] ))
    # print(min_by_key("a", [{"a": 2}, {"a": 1, "b": 2}]))
    # print(min_by_key("b", [{"a": 1, "b": 2}, {"a": 2}]))
    # print(min_by_key("a", [{}]))
    # print(min_by_key("b", [{"a": -1}, {"b": -1}]))
    # print(min_by_key("a", [{"b": 1}, {"b": -2}, {"a": 10}]))

    assert min_by_key("a", [ {"a": 1, "b": 2} , {"a": 2} ] ) == {"a": 1, "b": 2}
    assert min_by_key("a", [{"a": 2}, {"a": 1, "b": 2}]) == {"a": 1, "b": 2}
    assert min_by_key("b", [{"a": 1, "b": 2}, {"a": 2}]) == {"a": 2}
    assert min_by_key("a", [{}]) == {}
    assert min_by_key("b", [{"a": -1}, {"b": -1}]) == {"b": -1}
    assert min_by_key("a", [{"b": 1}, {"b": -2}, {"a": 10}]) in [{"b": 1}, {"b": -2}]

    

    # print(first_by_key("a", "asc", [{"a": 1}]))
    # print(first_by_key("a", "asc", [{"b": 1}, {"b": -2}, {"a": 10}]))
    # print(first_by_key("a", "desc", [{"b": 1}, {"b": -2}, {"a": 10}]))
    # print(first_by_key("b", "asc", [{"b": 1}, {"b": -2}, {"a": 10}]))
    # print(first_by_key("b", "desc", [{"b": 1}, {"b": -2}, {"a": 10}]))
    # print(first_by_key("a", "desc", [{}, {"a": 10, "b": -10}, {}, {"a": 3, "c": 3}]))

    assert first_by_key("a", "asc", [{"a": 1}]) == {"a": 1}
    assert first_by_key("a", "asc", [{"b": 1}, {"b": -2}, {"a": 10}]) in [{"b": 1}, {"b": -2}]
    assert first_by_key("a", "desc", [{"b": 1}, {"b": -2}, {"a": 10}]) == {"a": 10}
    assert first_by_key("b", "asc", [{"b": 1}, {"b": -2}, {"a": 10}]) == {"b": -2}
    assert first_by_key("b", "desc", [{"b": 1}, {"b": -2}, {"a": 10}]) == {"b": 1}
    assert first_by_key("a", "desc", [{}, {"a": 10, "b": -10}, {}, {"a": 3, "c": 3}]) == {"a": 10, "b": -10}

    cmp = RecordComparator("a", "asc")
    assert cmp.compare({"a": 1}, {"a": 2}) == -1
    assert cmp.compare({"a": 2}, {"a": 1}) == 1
    assert cmp.compare({"a": 1}, {"a": 1}) == 0
    


main()


