#  * Imagine an Airbnb-like vacation rental service, where users in different cities can exchange their apartment with another user for a week.
#  * Each user compiles a wishlist of the apartments they like.
#  * These wishlists are ordered, so the top apartment on a wishlist is that user's first choice for where they would like to spend a vacation.
#  * You will be asked to write part of the code that will help an algorithm find pairs of users who would like to swap with each other.
#  *
#  * Given a set of users, each with an *ordered* wishlist of other users' apartments:
#  *   a's wishlist: c d
#  *   b's wishlist: d a c
#  *   c's wishlist: a b
#  *   d's wishlist: c a b
#  * The first user in each wishlist is the user's first-choice for whose apartment they would like to swap into.
#  * Write a function called has_mutual_first_choice() which takes a username and returns true if that user and another user are each other's first choice, and otherwise returns false.
#  *
#  * has_mutual_first_choice('a') // true (a and c)
#  * has_mutual_first_choice('b') // false (b's first choice does not *mutually* consider b as their first choice)
#  *
#  * Then expand the base case beyond just "first" choices, to include all "mutually ranked choices".
#  * Write another function which takes a username and an option called "rank" to indicate the wishlist rank to query on.
#  * If given a rank of 0, you should check for a first choice pair, as before.
#  * If given 1, you should check for a pair of users who are each others' second-choice.
#  * Call your new function has_mutual_pair_for_rank() and when done, refactor has_mutual_first_choice() to depend on your new function.
#  *
#  * has_mutual_pair_for_rank('a', 0) // true (a and c)
#  * has_mutual_pair_for_rank('a', 1) // true (a and d are mutually each others' second-choice)
#  *
#  * data = {
#  *   'a': ['c', 'd'],
#  *   'b': ['d', 'a', 'c'],
#  *   'c': ['a', 'b'],
#  *   'd': ['c', 'a', 'b'],
#  * }
#  *
#  * Part2
#  * Every wishlist entry in the network is either "mutually ranked" or "not mutually ranked" depending on the rank the other user gives that user's apartment in return.
#  * The most common operation in the network is incrementing the rank of a single wishlist entry on a single user.
#  * This swaps the entry with the entry above it in that user's list.
#  * Imagine that, when this occurs, the system must recompute the "mutually-ranked-ness" of any pairings that may have changed.
#  * Write a function that takes a username and a rank representing the entry whose rank is being bumped up.
#  * Return an array of the users whose pairings with the given user *would* gain or lose mutually-ranked status as a result of the change, if it were to take place.
#  * Call your function changed_pairings()
#  *
#  * // if d's second choice becomes their first choice, a and d will no longer be a mutually ranked pair
#  * changed_pairings('d', 1) // returns ['a']
#  *
#  * // if b's third choice becomes their second choice, c and b will become a mutually ranked pair (mutual second-choices)
#  * changed_pairings('b', 2) // returns ['c']
#  *
#  * // if b's second choice becomes their first choice, no mutually-ranked pairings are affected
#  * changed_pairings('b', 1) // returns []


user_wishlists = {'a': ['c', 'd'], 'b': ['d', 'a', 'c'], 'c': ['a', 'b'], 'd': ['c', 'a', 'b'] }

def has_mutual_pair_for_rank(user, rank):
    if user not in user_wishlists:
        raise AssertionError("incorect data")
    
    users_choices = user_wishlists[user]
    if rank >= len(users_choices):
        return False
        # raise AssertionError("user doesnt have a choice of that rank")
    
    users_choice_at_rank = users_choices[rank]

    if users_choice_at_rank not in user_wishlists:
        raise AssertionError("incorect data")
    
    opposite_wishlist = user_wishlists[users_choice_at_rank]

    if rank >= len(opposite_wishlist):
        return False
        # raise AssertionError("opposite user doesnt have a choice of that rank")
    
    return user == opposite_wishlist[rank]

def has_mutual_first_choice(user):
    return has_mutual_pair_for_rank(user, 0)
    # if user not in user_wishlists:
    #     raise AssertionError("incorect data")
    
    # users_first_choise = user_wishlists[user][0]

    # if users_first_choise not in user_wishlists:
    #     raise AssertionError("incorect data")

    # return user_wishlists[users_first_choise][0] == user

def changed_pairings_oldest(user, rank):
    if rank < 1:
        raise AssertionError("cant increment rank 0")
    
    # check if each of the indices to be swapped already have mutual ranks
    a = has_mutual_pair_for_rank(user, rank)
    b = has_mutual_pair_for_rank(user, rank-1)

    usr_wsh_lish = user_wishlists[user]

    res = []

    if a:
        res.append( usr_wsh_lish[rank] )
    
    if b:
        res.append( usr_wsh_lish[rank-1] )
    
    # we check if opposite user at rank would be mutual with the value at rank-1
    # if it will be, then we add it to result
    opposite_A_wl = user_wishlists[ usr_wsh_lish[rank] ]
    if rank < len(opposite_A_wl) and opposite_A_wl[rank] == usr_wsh_lish[rank-1]:
        res.append(usr_wsh_lish[rank])
    
    opposite_B_wl = user_wishlists[ usr_wsh_lish[rank-1] ]
    if rank < len(opposite_B_wl) and opposite_B_wl[rank] == usr_wsh_lish[rank]:
        res.append(usr_wsh_lish[rank-1])


    return res


def changed_pairings_older(user, rank):
    if rank < 1:
        raise AssertionError("rank too small")
    
    user_wl = user_wishlists[user]
    left_entry = user_wl[rank-1]
    right_entry = user_wl[rank]

    left_mutual = has_mutual_pair_for_rank(user, rank-1)
    right_mutual = has_mutual_pair_for_rank(user, rank)

    res = []
    # if left is already mutual then it will lose its mutualness
    if left_mutual:
        res.append(left_entry)
    else: # or it could gain its mutualness
        opposite_wl = user_wishlists[left_entry]
        # if the rank of new rank of right_entry matches for both then yes
        try:
            right_entry_ind = opposite_wl.index(right_entry)
        except ValueError:
            right_entry_ind = None 
        finally:
            if right_entry_ind == rank - 1:
                res.append(left_entry)

    # if right is already mutual then it will lose its mutualness
    if right_mutual:
        res.append(right_entry)
    else: # or it could gain its mutualness
        opposite_wl = user_wishlists[right_entry]
        # if the rank of new rank of right_entry matches for both then yes
        try:
            left_entry_ind = opposite_wl.index(left_entry)
        except ValueError:
            left_entry_ind = None 
        finally:
            if left_entry_ind == rank:
                res.append(right_entry)
    
    return res

def changed_pairings(user, rank):
    if rank < 1:
        raise AssertionError("rank too small")
    
    user_wl = user_wishlists[user]
    left_entry = user_wl[rank-1]
    right_entry = user_wl[rank]

    left_mutual = has_mutual_pair_for_rank(user, rank-1)
    right_mutual = has_mutual_pair_for_rank(user, rank)

    res = []
    if left_mutual:
        res.append(left_entry)
    if right_mutual:
        res.append(right_entry)

    swapped_wl = user_wl.copy()
    swapped_wl[rank-1], swapped_wl[rank] = swapped_wl[rank], swapped_wl[rank-1]
    user_wishlists[user] = swapped_wl

    left_mutual = has_mutual_pair_for_rank(user, rank-1)
    right_mutual = has_mutual_pair_for_rank(user, rank)

    if left_mutual:
        res.append(right_entry)
    if right_mutual:
        res.append(left_entry)

    user_wishlists[user] = user_wl

    return res

    


def test():
    assert has_mutual_first_choice('a')
    assert not has_mutual_first_choice('b')
    
    assert has_mutual_pair_for_rank('a', 1)
    assert has_mutual_pair_for_rank('a', 0)
    assert not has_mutual_pair_for_rank('b', 0)
    assert not has_mutual_pair_for_rank('d', 2)
    try:
        has_mutual_pair_for_rank('b', 2)
        assert False
    except:
        assert True


    assert changed_pairings('d', 1) == ['a']
#  * // if b's third choice becomes their second choice, c and b will become a mutually ranked pair (mutual second-choices)
    assert changed_pairings('b', 2) == ['c']
#  * // if b's second choice becomes their first choice, no mutually-ranked pairings are affected
    assert changed_pairings('b', 1) == []


test()