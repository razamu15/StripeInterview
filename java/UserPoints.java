package com.kamarkaka.stripe;

import org.junit.jupiter.api.Test;

import java.sql.Timestamp;
import java.util.*;

import static org.junit.jupiter.api.Assertions.assertEquals;

/***
 * Background
 * Our users have points in their accounts.
 * Users only see a single balance in their accounts.
 * But for reporting purposes we actually track their points per payer/partner.
 * In our system, each transaction record contains:
 *    payer (String), points (String), timestamp (date).
 * For earning points it is easy to assign a payer, we know which actions earned the points.
 * And thus which partner should be paying for the points.
 *
 * When a user spends points, they don't know or care which payer the points come from.
 * But, our accounting team does car how the points are spent.
 * There are two rules for determining what points to "spend" first:
 *    We want the oldest points to be spent first
 *    We want no payer's points to go negative
 *
 * You need to do:
 *    Add transaction for a specific payer and date.
 *    Spend points using the rules above and return a list of
 *       {"payer": <string>, "points": <integer>} for each call
 *    Return all payer point balances.
 *
 * Example
 * Suppose you call your add transaction route with the following sequence of calls:
 *    { "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" }
 *    { "payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z" }
 *    { "payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z" }
 *    { "payer": "MILLER COORS", "points": 10000, "timestamp": "2020-11-01T14:00:00Z" }
 *    { "payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z" }
 *
 * Then you call your spend points route with the following request:
 *    { "points": 5000 }
 * The expected response from the spend call would be:
 *    [
 *       { "payer": "DANNON", "points": -100 },
 *       { "payer": "UNILEVER", "points": -200 },
 *       { "payer": "MILLER COORS", "points": -4,700 }
 *    ]
 * A subsequent call to the points balance route, after the spend, should returns the following results:
 *    {
 *       "DANNON": 1000,
 *       "UNILEVER": 0,
 *       "MILLER COORS": 5300
 *    }
 *
 * FAQ: For any requirements not specified via an example, use your best judgement to determine the expected result.
 */
public class UserPoints {
   private final SortedSet<Transaction> transactions;

   public UserPoints() {
      this.transactions = new TreeSet<>(Comparator.comparing(o -> o.timestamp));
   }

   public void add(String payer, int point, String timestamp) {
      transactions.add(new Transaction(timestamp, payer, point));
   }

   public List<String> spend(int point) {
      Map<String, Integer> map = new HashMap<>();
      Iterator<Transaction> iter = transactions.iterator();
      while (iter.hasNext()) {
         if (point == 0) break;
         Transaction transaction = iter.next();
         int deduction = Math.min(transaction.point, point);
         transaction.point -= deduction;
         point -= deduction;

         map.putIfAbsent(transaction.payer, 0);
         map.put(transaction.payer, map.get(transaction.payer) + deduction);
      }

      List<String> list = new ArrayList<>();
      for (Map.Entry<String, Integer> entry : map.entrySet()) {
         String payer = entry.getKey();
         int sum = entry.getValue();
         list.add(payer + ": -" + sum);
      }
      return list;
   }

   public List<String> getBalance() {
      Map<String, Integer> map = new HashMap<>();
      for (Transaction transaction : transactions) {
         map.putIfAbsent(transaction.payer, 0);
         map.put(transaction.payer, map.get(transaction.payer) + transaction.point);
      }

      List<String> list = new ArrayList<>();
      for (Map.Entry<String, Integer> entry : map.entrySet()) {
         String payer = entry.getKey();
         int sum = entry.getValue();
         list.add(payer + ": " + sum);
      }
      return list;
   }

   private class Transaction {
      private final Timestamp timestamp;
      private final String payer;
      private int point;

      public Transaction(String timestamp, String payer, int point) {
         this.timestamp = Timestamp.valueOf(timestamp);
         this.payer = payer;
         this.point = point;
      }
   }

   public static void run() {
      UserPoints p1 = new UserPoints();
      p1.add("DANNON", 1000, "2020-11-02 14:00:00");
      p1.add("UNILEVER", 200, "2020-10-31 11:00:00");
      p1.add("DANNON", -200, "2020-10-31 15:00:00");
      p1.add("MILLER COORS", 10000, "2020-11-01 14:00:00");
      p1.add("DANNON", 300, "2020-10-31 10:00:00");

      System.out.println(p1.getBalance());
      System.out.println(p1.spend(5000));
      System.out.println(p1.getBalance());
   }
}

class UserPointsTest {
   @Test
   void Test1() {
      UserPoints p1 = new UserPoints();
      p1.add("DANNON", 1000, "2020-11-02 14:00:00");
      p1.add("UNILEVER", 200, "2020-10-31 11:00:00");
      p1.add("DANNON", -200, "2020-10-31 15:00:00");
      p1.add("MILLER COORS", 10000, "2020-11-01 14:00:00");
      p1.add("DANNON", 300, "2020-10-31 10:00:00");

      assertEquals(p1.getBalance().toString(), "[UNILEVER: 200, MILLER COORS: 10000, DANNON: 1100]");
      assertEquals(p1.spend(5000).toString(), "[UNILEVER: -200, MILLER COORS: -4700, DANNON: -100]");
      assertEquals(p1.getBalance().toString(), "[UNILEVER: 0, MILLER COORS: 5300, DANNON: 1000]");
   }
}