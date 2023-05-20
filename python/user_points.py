# * Background
#  * Our users have points in their accounts.
#  * Users only see a single balance in their accounts.
#  * But for reporting purposes we actually track their points per payer/partner.
#  * In our system, each transaction record contains:
#  *    payer (String), points (String), timestamp (date).
#  * For earning points it is easy to assign a payer, we know which actions earned the points.
#  * And thus which partner should be paying for the points.
#  *
#  * When a user spends points, they don't know or care which payer the points come from.
#  * But, our accounting team does car how the points are spent.
#  * There are two rules for determining what points to "spend" first:
#  *    We want the oldest points to be spent first
#  *    We want no payer's points to go negative
#  *
#  * You need to do:
#  *    Add transaction for a specific payer and date.
#  *    Spend points using the rules above and return a list of
#  *       {"payer": <string>, "points": <integer>} for each call
#  *    Return all payer point balances.
#  *
#  * Example
#  * Suppose you call your add transaction route with the following sequence of calls:
#  *    { "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" }
#  *    { "payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z" }
#  *    { "payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z" }
#  *    { "payer": "MILLER COORS", "points": 10000, "timestamp": "2020-11-01T14:00:00Z" }
#  *    { "payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z" }
#  *
#  * Then you call your spend points route with the following request:
#  *    { "points": 5000 }
#  * The expected response from the spend call would be:
#  *    [
#  *       { "payer": "DANNON", "points": -100 },
#  *       { "payer": "UNILEVER", "points": -200 },
#  *       { "payer": "MILLER COORS", "points": -4,700 }
#  *    ]
#  * A subsequent call to the points balance route, after the spend, should returns the following results:
#  *    {
#  *       "DANNON": 1000,
#  *       "UNILEVER": 0,
#  *       "MILLER COORS": 5300
#  *    }
#  *
#  * FAQ: For any requirements not specified via an example, use your best judgement to determine the expected result.

from datetime import datetime
import collections

def ts_to_epoch(ts):
    utc_time = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
    return (utc_time - datetime(1970, 1, 1)).total_seconds()


class PointBank():

    def __init__(self):
        self.transactions = []
        self.all_payers = set()

    def add_transaction(self, record):
        self.transactions.append( ( ts_to_epoch(record['timestamp']), record ) )
        self.all_payers.add(record['payer'])
        self.transactions.sort()
    
    def points_balance(self):
        total = { payer: 0 for payer in self.all_payers }
        
        for key, record in self.transactions:
            total[ record['payer'] ] +=  record['points']

        return total
    
    def spend_points(self, amount):
        spent_points = collections.defaultdict(int)

        while amount > 0 and self.transactions:
            key, record = self.transactions.pop(0)
            points_bal = record['points']
            points_spent = min(points_bal, amount)

            spent_points[ record['payer'] ] -= points_spent
            amount -= points_spent
            record['points'] -= points_spent
        
        if record['points'] > 0:
            self.transactions = [ (key, record) ] + self.transactions
        
        if amount > 0:
            raise AssertionError("not enough points")
        
        res = []
        for payer, bal_change in spent_points.items():
            res.append( { 'payer': payer, 'points': bal_change } )
        return res


pb = PointBank()
pb.add_transaction({ "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" })
pb.add_transaction({ "payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z" })
pb.add_transaction({ "payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z" })
pb.add_transaction({ "payer": "MILLER COORS", "points": 10000, "timestamp": "2020-11-01T14:00:00Z" })
pb.add_transaction({ "payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z" })

print(pb.points_balance())

print(pb.spend_points(5000))


print(pb.points_balance())

    


    