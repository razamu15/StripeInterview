package com.kamarkaka.stripe;

import java.util.*;
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.ReentrantLock;

public class LoadBalancer {
   private final int initialCapacity;
   private final PriorityQueue<ServerMetadata> pq;
   private final Map<Integer, ServerMetadata> map;
   private final ReentrantLock lock;
   private final Condition notEmpty;
   private final Condition notFull;
   private final Timer timer;

   public LoadBalancer(int initialCapacity) {
      this.initialCapacity = initialCapacity;
      this.pq = new PriorityQueue<>(initialCapacity, Comparator.comparingInt(s -> -(s.capacity - s.load)));
      this.map = new HashMap<>();
      this.lock = new ReentrantLock();
      this.notEmpty = this.lock.newCondition();
      this.notFull = this.lock.newCondition();
      this.timer = new Timer();
   }

   public void addServer(int id, int capacity) {
      lock.lock();
      try {
         while (pq.size() == initialCapacity) {
            notFull.await();
         }
         System.out.println("add server " + id + " with initial capacity " + capacity);
         ServerMetadata metadata = new ServerMetadata(id, 0, capacity);
         pq.add(metadata);
         map.put(id, metadata);
         notFull.signal();
      } catch (InterruptedException ignored) {
      } finally {
         lock.unlock();
      }
   }

   public int routeRequest(int weight, int ttl) {
      lock.lock();
      try {
         while (pq.isEmpty()) {
            notEmpty.await();
         }
         ServerMetadata metadata = pq.peek();
         if (weight > metadata.capacity - metadata.load) return -1;

         metadata = pq.poll();
         metadata.load += weight;

         pq.add(metadata);
         notFull.signal();

         System.out.println("schedule task to finish after " + ttl + "ms on server " + metadata.id + " with load " + weight + " (" + metadata.load + "/" + metadata.capacity + ")");
         timer.schedule(new DelayedTask(metadata.id, weight, pq, map, lock), ttl);
         return metadata.id;
      } catch (InterruptedException ignored) {
      } finally {
         lock.unlock();
      }
      return -1;
   }

   public void end() {
      timer.cancel();
   }

   public static void run() {
      try {
         LoadBalancer lb = new LoadBalancer(10);
         lb.addServer(1, 10);
         lb.routeRequest(4, 1000);
         lb.routeRequest(5, 500);
         Thread.sleep(600);
         lb.routeRequest(6, 500);

         Thread.sleep(3000);
         lb.end();
      } catch (InterruptedException ignored) {
      }
   }
}

class DelayedTask extends TimerTask {
   private final int serverId;
   private final int load;
   private final PriorityQueue<ServerMetadata> pq;
   private final Map<Integer, ServerMetadata> map;
   private final ReentrantLock lock;

   public DelayedTask(int serverId, int load, PriorityQueue<ServerMetadata> pq, Map<Integer, ServerMetadata> map, ReentrantLock lock) {
      this.serverId = serverId;
      this.load = load;
      this.pq = pq;
      this.map = map;
      this.lock = lock;
   }

   @Override
   public void run() {
      lock.lock();
      ServerMetadata metadata = map.get(serverId);
      metadata.load -= load;
      pq.remove(metadata);
      pq.add(metadata);
      System.out.println("free server " + metadata.id + " with load " + load);
      lock.unlock();
   }
}

class ServerMetadata {
   int id;
   int load;
   int capacity;

   public ServerMetadata(int id, int load, int capacity) {
      this.id = id;
      this.load = load;
      this.capacity = capacity;
   }
}
