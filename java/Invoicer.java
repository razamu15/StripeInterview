package com.kamarkaka.stripe;

import java.util.*;

public class Invoicer {
   private final Map<Integer, String> sendSchedule;
   private final Map<Integer, Invoice> invoices;

   public Invoicer() {
      sendSchedule = new HashMap<>();
      sendSchedule.put(-10, "Upcoming");
      sendSchedule.put(0, "New");
      sendSchedule.put(20, "Reminder");
      sendSchedule.put(30, "Due");

      invoices = new HashMap<>();
   }

   public void addInvoice(int timestamp, String name, int amount) {
      invoices.put(timestamp, new Invoice(timestamp, name, amount));
   }

   public List<String> output() {
      List<String> res = new ArrayList<>();
      List<ScheduledMessage> messageList = new ArrayList<>();
      for (int timestamp : invoices.keySet()) {
         for (int timeDelta : sendSchedule.keySet()) {
            int scheduledTime = timestamp + timeDelta;
            messageList.add(new ScheduledMessage(scheduledTime, sendSchedule.get(timeDelta), invoices.get(timestamp)));
         }
      }

      messageList.sort(Comparator.comparingInt(m -> m.timestamp));
      for (ScheduledMessage message : messageList) {
         res.add(message.toString());
      }
      return res;
   }

   public static void run() {
      Invoicer sol = new Invoicer();
      sol.addInvoice(0, "Alice", 200);
      sol.addInvoice(1, "Bob", 100);
      List<String> output = sol.output();
      for (String message : output) {
         System.out.println(message);
      }
   }
}

class ScheduledMessage {
   int timestamp;
   String schedule;
   Invoice invoice;

   public ScheduledMessage(int timestamp, String schedule, Invoice invoice) {
      this.timestamp = timestamp;
      this.schedule = schedule;
      this.invoice = invoice;
   }

   @Override
   public String toString() {
      return timestamp + ": [" + schedule + "] Invoice for " + invoice.name + " for " + invoice.amount + " dollars";
   }
}

class Invoice {
   int timestamp;
   String name;
   int amount;

   Invoice(int timestamp, String name, int amount) {
      this.timestamp = timestamp;
      this.name = name;
      this.amount = amount;
   }

   @Override
   public String toString() {
      return "{\"invoice_time\": " + timestamp + ", \"name\": \"" + name + "\", \"amount\": " + amount + "}";
   }
}
