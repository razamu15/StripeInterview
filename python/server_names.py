# You're running a pool of servers where the servers are numbered sequentially starting from 1. Over time, any given server might explode, in which case its server number is made available for reuse. When a new server is launched, it should be given the lowest available number.
# Write a function which, given the list of currently
# allocated server numbers, returns the number of the next server to allocate.
# For example, your function should behave something like the following:
# >> next_server_number ((5, 3, 1])
# 2
# >> next_server_number (5, 4, 1, 2])
# 3
# >> next_server_number([3, 2, 1])
# 4
# >> next_server_number ([2, 3])
# 1
# >> next_server_number([])
# 1
# Server names consist of an alphabetic host type (e.g. "apibox") concatenated with the server number,
# with server numbers allocated as before (so "apibox1"
# "apibox2", etc. are valid hostnames).
# Write a name tracking class with two operations, allocate(host_type) and deallocate (hostname).
# The former should reserve and return the next available hostname, while the latter should release that hostname back into the pool.
# # For example:
# ＃
# # >> tracker = Tracker.new)
# # >> tracker.allocate("apibox")
# # "apibox1"
# # >> tracker.allocate("apibox")
# # "apibox2"
# # >> tracker.deallocate ("apibox1")
# # nil
# # >> tracker.allocate("apibox")
# # "apibox1"
# # >> tracker.allocate("sitebox")
# # "sitebox1"

import collections

class NumberAllocator:

    @staticmethod
    def next_server_number(allocated):

        allocated = set(allocated)

        for num in range(1, len(allocated)+1):
            if num not in allocated:
                return num
        
        return len(allocated) + 1

class ServerTracker:

    def __init__(self) -> None:
        self.servers = collections.defaultdict(list)

    
    def allocate(self, name):
        allocated = self.servers[name]

        next_num = NumberAllocator.next_server_number(allocated)
        allocated.append(next_num)

        return f'{name}{next_num}'
    

    def deallocate(self, name):
        num_ind = len(name) - 1
        while name[num_ind].isnumeric():
            num_ind -= 1

        base_name = name[:num_ind+1]
        server_num = name[num_ind+1:]
        
        allocated = self.servers[base_name]
        allocated.remove(int(server_num))


def test_next_server_number():
    assert NumberAllocator.next_server_number([5, 3, 1]) == 2
    assert NumberAllocator.next_server_number([5, 4, 1, 2]) == 3
    assert NumberAllocator.next_server_number([3, 2, 1]) == 4
    assert NumberAllocator.next_server_number([2, 3]) == 1
    assert NumberAllocator.next_server_number([]) == 1

def test_server_tracker():
    tracker = ServerTracker()
    assert tracker.allocate("apibox") == "apibox1"
    assert tracker.allocate("apibox") == "apibox2"
    assert tracker.deallocate("apibox1") is None
    # breakpoint()
    assert tracker.allocate("apibox") == "apibox1"
    assert tracker.allocate("sitebox") == "sitebox1"
    


test_next_server_number()
test_server_tracker()