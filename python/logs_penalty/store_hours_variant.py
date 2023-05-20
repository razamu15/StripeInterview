def part1(store_log, closing_time):
    # Given a String like "Y N Y Y N" where Y denotes if there were any customers at a given hour 
    # and N denotes no customers at a given hour. There is a penalty for a hour where it is open 
    # and you have a N (i.e. no customer), and if you close at a certain hour and it turns out 
    # the hour had customers i.e. Y. 

    #  hour   :  1  2  3  4  5
    #  log    :  Y  N  Y  Y  N
    # close_at:  1  2  3  4  5   // close at 5th hour, no penalty
    # 					   ^

    #  hour   :  1  2  3  4  5
    #  log    :  Y  N  Y  Y  N
    # close_at:  1  2  3  4  5   // close at 4th hour, there was a Y and you closed, so you would have a penalty
    # 					^

                        
    # So, for the above string if you had closed at the 5th hour you would have no penalty. 
    # However, if you closed at the 4th hour there was a Y and you closed, so you would have a penalty. 
    # Given a String and an hour, calculate the penalty.

    # ----------------
    # basically for every hour your open and there are no customers, penalty += 1
    # for every hour your closed and there are customers, penalty += 1
    penalty = 0
    for ind, every_hour in enumerate(store_log.split(" ")):
        if ind < closing_time and every_hour == 'N':
            # if your open and no customers
            penalty += 1
        elif ind >= closing_time and every_hour == 'Y':
            # closed and yes customers
            penalty += 1
    return penalty

def part2(store_log):
    # Second part: Given a string, return the best hour to close for that string i.e., with minimum penalty. 
    # It does not matter which hour you return. You can return any of the hours with minimum penalty.
    
    best_hour = None
    min_penalty = float('inf')
    
    for possible_closing in range(len(store_log.split(" "))):
        penalty = part1(store_log, possible_closing)
        if penalty < min_penalty:
            min_penalty = penalty
            best_hour = possible_closing
        
    return best_hour

def part3():
    # 3rd Part 
	# Examples get_best_closing_times("BEGIN Y Y END \nBEGIN N N END") should
	# return an array: [2, 0]
	# get_best_closing_times("BEGIN BEGIN \nBEGIN N N BEGIN Y Y\n END N N END")
	# should return an array: [2]
    return 

def part4():
    # 4th part 
	# Logs are coming in stream one by one in a batch with each stream of data i.e. not passed at once
    return


tests_part_1 = [
    ["Y Y Y N N N N", 0, 3],
    ["Y Y Y N N N N", 7, 4],
    ["", 0, 0],
    ["Y N Y N N N N", 3, 1]
]

tests_part_2 = [
    ["Y Y Y N N N N", 3],
    ["Y Y N Y N N N N", 2], # 2, 3, 4
    ["Y Y N Y Y N N N N", 5],
    ["N N Y N N N N", 0] # 0, 1
]

for log, answer in tests_part_2:
    print(part2(log), answer)
    assert part2(log) == answer
    print("")
