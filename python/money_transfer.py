# At Stripe we keep track of where the money is and move money between bank accounts to make sure their balances are not below some threshold.
# This is for operational and regulatory reasons, e.g. we should have enough funds to pay out to our users, and we are legally required to separate our users' funds from our own.
# This interview question is a simplified version of a real-world problem we have here.
# Let's say there are at most 500 bank accounts, some of their balances are above 100 and some are below.
# How do you move money between them so that they all have at least 100?
# Just to be clear we are not looking for the optimal solution, but a working one.
#  *
# Example input:
# - AU: 80
# - US: 140
# - MX: 110
# - SG: 120
# - FR: 70
# Output:
# - from: US, to: AU, amount: 20
# - from: US, to: FR, amount: 20
# - from: MX, to: FR, amount: 10
#  *

# followup1：Ask in reverse, assuming you are given a series of transfers, ask whether the final account balance meets the conditions. Assuming that the given account balance cannot achieve each account>=100 anyway, ask if the given transfer is the best effort?

# followup2：How to get the optimal solution? Here you need to ask the interviewer how to define the optimal solution. The interviewer said that the fewer transfers, the better. This is very similar to LC0465


# -------------------------------------------

# so we can just keep track of account that are above 100 and below 100
# then as long as we have accounts below, we keep taking any account above 100 at random and then equalize. (also put one of them back in their respective pools if needed)
THRESHOLD = 100


def balance_account(accounts):
    # accounts = { 'AU': 80, 'US':140 }
    above_threshold = set()
    below_threshold = set()

    for acc, bal in accounts.items():
        if bal > THRESHOLD:
            above_threshold.add(acc)
        elif bal < THRESHOLD:
            below_threshold.add(acc)

    transfers = []

    while len(below_threshold) > 0:
        if len(above_threshold) == 0:
            raise AssertionError("not enough money in the system")

        giving_account = above_threshold.pop()
        receiving_account = below_threshold.pop()

        excess_money = accounts[giving_account] - 100

        accounts[giving_account] -= excess_money
        accounts[receiving_account] += excess_money
        transfers.append(
            f'from: {giving_account}, to {receiving_account}, amount: {excess_money}')

        # giving account is now 100, so we dont do anything. receiving could be more or less
        if accounts[receiving_account] > 100:
            above_threshold.add(receiving_account)
        elif accounts[receiving_account] < 100:
            below_threshold.add(receiving_account)

    return transfers

for t in balance_account({'AU': 80, 'US': 140, 'MX': 110, 'SG': 120, 'FR': 70}):
    print(t)
