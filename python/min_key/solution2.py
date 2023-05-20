def min_by_key(key, records_array):
    '''
    #PART 1
    Throughout this interview, we'll pretend we're building a new analytical database. Don't worry about actually 
    building a database though – these will all be toy problems.

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

    assert min_by_key("a", [{"a": 1, "b": 2}, {"a": 2}]) == {"a": 1, "b": 2}
    assert min_by_key("a", [{"a": 2}, {"a": 1, "b": 2}]) == {"a": 1, "b": 2}
    assert min_by_key("b", [{"a": 1, "b": 2}, {"a": 2}]) == {"a": 2}
    assert min_by_key("a", [{}]) == {}
    assert min_by_key("b", [{"a": -1}, {"b": -1}]) == {"b": -1}
    '''
    # min_value = float('inf')
    # min_record = None

    # for record in records_array:
        
    #     key_value = record.get(key, 0)

    #     if key_value < min_value:
    #         min_value = key_value
    #         min_record = record
    
    # return min_record
    return first_by_key(key, 'asc', records_array)


def first_by_key(key, direction, records_array):
    '''
    Step 2: first_by_key

    Our next step in database development is to add a new function. We'll call this function first_by_key. It has much 
    in common with min_by_key. first_by_key takes three arguments:

    a string key
    a string sort direction (which must be either "asc" or "desc")
    an array of records, just as in min_by_key.
    If the sort direction is "asc", then we should return the minimum record, otherwise we should return the maximum 
    record. As before, records without a value for the key should be treated as having value 0.

    Once you have a working solution, you should re-implement min_by_key in terms of first_by_key .

    Java function signature:

    public static Map<String, Integer> firstByKey(String key, String direction, List<Map<String, Integer>> records);
    Examples (in Python):

    assert first_by_key("a", "asc", [{"a": 1}]) == {"a": 1}
    assert first_by_key("a", "asc", [{"b": 1}, {"b": -2}, {"a": 10}]) in [{"b": 1}, {"b": -2}]
    assert first_by_key("a", "desc", [{"b": 1}, {"b": -2}, {"a": 10}]) == {"a": 10}
    assert first_by_key("b", "asc", [{"b": 1}, {"b": -2}, {"a": 10}]) == {"b": -2}
    assert first_by_key("b", "desc", [{"b": 1}, {"b": -2}, {"a": 10}]) == {"b": 1}
    assert first_by_key("a", "desc", [{}, {"a": 10, "b": -10}, {}, {"a": 3, "c": 3}]) == {"a": 10, "b": -10}
    '''
    limit_value = { 'asc': float('inf'), 'desc': float('-inf') }
    # comparator = lambda x, y: x < y if direction == 'asc' else x > y
    c = Comparator(key, direction)
    
    first_record = { key: limit_value[direction] }
    
    for record in records_array:

        if c.compare(record, first_record) == -1:
            first_record = record
    
    return first_record
    

class Comparator():

    def __init__(self, key, direction):
        self.key = key
        self.direction = direction
    
    def compare(self, rec1, rec2):
        r1_val = rec1.get(self.key, 0)
        r2_val = rec2.get(self.key, 0)

        if r1_val == r2_val:
            return 0
        else:
            if self.direction == 'asc':
                return -1 if r1_val < r2_val else 1
            elif self.direction == 'desc':
                return -1 if r1_val > r2_val else 1



def part3():
    '''
    Step 3: first_by_key comparator

    As we build increasingly rich orderings for our records, we'll find it useful to extract the comparison of records 
    into a comparator. This is a function or object (depending on your language) which determines if a record is "less 
    than", equal, or "greater than" another.

    In object-oriented languages, you should write a class whose constructor accepts two parameters: a string key and a 
    string direction. The class should implement a method compare that takes as its parameters two records. This method 
    should return -1 if the first record comes before the second record (according to key and direction), zero if neither
    record comes before the other, or 1 if the first record comes after the second.

    In functional languages, you should write a function which accepts two parameters: a string key and a string direction.
    The function should return a method that takes as its parameters two records. This function should return -1 if the 
    first record comes before the second record (according to key and direction), zero if neither record comes before 
    the other, or 1 if the first record comes after the second.

    You should then use your comparator in your implementation of first_by_key.

    Examples (in Python):

    cmp = Comparator("a", "asc")
    assert cmp.compare({"a": 1}, {"a": 2}) == -1
    assert cmp.compare({"a": 2}, {"a": 1}) == 1
    assert cmp.compare({"a": 1}, {"a": 1}) == 0'''
    return


def test():
    assert min_by_key("a", [{"a": 1, "b": 2}, {"a": 2}]) == {"a": 1, "b": 2}
    assert min_by_key("a", [{"a": 2}, {"a": 1, "b": 2}]) == {"a": 1, "b": 2}
    assert min_by_key("b", [{"a": 1, "b": 2}, {"a": 2}]) == {"a": 2}
    assert min_by_key("a", [{}]) == {}
    assert min_by_key("b", [{"a": -1}, {"b": -1}]) == {"b": -1}

    assert first_by_key("a", "asc", [{"a": 1}]) == {"a": 1}
    assert first_by_key("a", "asc", [{"b": 1}, {"b": -2}, {"a": 10}]) in [{"b": 1}, {"b": -2}]
    assert first_by_key("a", "desc", [{"b": 1}, {"b": -2}, {"a": 10}]) == {"a": 10}
    assert first_by_key("b", "asc", [{"b": 1}, {"b": -2}, {"a": 10}]) == {"b": -2}
    assert first_by_key("b", "desc", [{"b": 1}, {"b": -2}, {"a": 10}]) == {"b": 1}
    assert first_by_key("a", "desc", [{}, {"a": 10, "b": -10}, {}, {"a": 3, "c": 3}]) == {"a": 10, "b": -10}

    cmp = Comparator("a", "asc")
    assert cmp.compare({"a": 1}, {"a": 2}) == -1
    assert cmp.compare({"a": 2}, {"a": 1}) == 1
    assert cmp.compare({"a": 1}, {"a": 1}) == 0

    cmp = Comparator("b", "desc")
    assert cmp.compare({"b": 1}, {"a": 2}) == -1
    assert cmp.compare({"a": 2}, {"b": 1}) == 1
    assert cmp.compare({"a": 1}, {"a": 1}) == 0


test()