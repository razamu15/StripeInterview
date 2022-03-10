package com.kamarkaka.stripe;

import com.kamarkaka.common.Utilities;

import java.util.*;

/***
 * At Stripe we keep track of where the money is and move money between bank accounts to make sure their balances are not below some threshold.
 * This is for operational and regulatory reasons, e.g. we should have enough funds to pay out to our users, and we are legally required to separate our users' funds from our own.
 * This interview question is a simplified version of a real-world problem we have here.
 * Let's say there are at most 500 bank accounts, some of their balances are above 100 and some are below.
 * How do you move money between them so that they all have at least 100?
 * Just to be clear we are not looking for the optimal solution, but a working one.
 *
 * Example input:
 * - AU: 80
 * - US: 140
 * - MX: 110
 * - SG: 120
 * - FR: 70
 * Output:
 * - from: US, to: AU, amount: 20
 * - from: US, to: FR, amount: 20
 * - from: MX, to: FR, amount: 10
 *
 * followup1：反过来问，假设给你一系列transfer，问最后account balance是否满足条件。假设所给account balance无论如何也无法做到每个account>=100，问所给的transfer是不是best effort？
 * followup2：如何得到最优解？这里你需要问面试官如何定义最优解。面试官说转账次数越少越好。这样和LC0465就很像了
 */
public class MoneyTransfer {
   private final List<Account> balances;

   public MoneyTransfer() {
      this.balances = new ArrayList<>();
   }

   public void addAccount(String acct, float balance) {
      balances.add(new Account(acct, balance));
   }

   public List<Transfer> transfer() {
      List<Transfer> res = new ArrayList<>();
      balances.sort(Comparator.comparingDouble(a1->(-a1.amount)));

      int p0 = 0, p1 = balances.size() - 1;
      while (p0 < p1) {
         if (balances.get(p0).amount <= 100 || balances.get(p1).amount >= 100) return res;

         Account from = balances.get(p0);
         Account to = balances.get(p1);
         double amount = Math.min(from.amount - 100, 100 - to.amount);
         res.add(new Transfer(from.name, to.name, amount));
         from.amount -= amount;
         to.amount += amount;

         if (from.amount == 100) p0++;
         if (to.amount == 100) p1--;
      }
      return res;
   }

   public static void run() {
      MoneyTransfer sol = new MoneyTransfer();
      sol.addAccount("AU", 80);
      sol.addAccount("US", 140);
      sol.addAccount("MX", 110);
      sol.addAccount("SG", 120);
      sol.addAccount("FR", 70);

      List<Transfer> transfers = sol.transfer();
      for (Transfer transfer : transfers) {
         System.out.println(transfer);
      }
   }
}

class Account {
   String name;
   double amount;

   Account(String name, double amount) {
      this.name = name;
      this.amount = amount;
   }
}

class Transfer {
   String fromAcct;
   String toAcct;
   double amount;

   Transfer(String from, String to, double amount) {
      this.fromAcct = from;
      this.toAcct = to;
      this.amount = amount;
   }

   @Override
   public String toString() {
      return "from: " + fromAcct + ", to: " + toAcct + ", amount: " + amount;
   }
}
