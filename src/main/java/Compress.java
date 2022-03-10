package com.kamarkaka.stripe;

/***
 * Prompt
 * Everyday we look at a lot of URLs, for example in our log files from client request.
 * We want our data science team to perform analytics and machine learning, but:
 *    1. we want to preserve the privacy of the user, but without completely obfuscating/hashing the URLs and making them useless,
 *    2. we simply have a lot of data and we want to reduce our storage/processing costs
 * In real world, we may solve this with hashing; due to the time constraints of the interview, we use numeronyms instead of compress Strings.
 *
 * Example starter code
 * String compress(String s) {
 *    // requirement 1, 2, etc
 *    String compressed_s = fx(s);
 *    return compressed_s;
 * }
 *
 * Part 1
 * Given a String, split it into "major parts" separated by special char '/'.
 * For each major part that's split by '/', we can further split it into "minor parts" separated by '.'.
 * We assume the given Strings:
 *    - Only have lower case letters and two separators ('/', '.').
 *    - Have no empty minor parts (no leading / trailing separators or consecutive separators like "/a", "a/", "./..").
 *    - Have >= 3 letters in each minor part.
 *
 * Example:
 *    stripe.com/payments/checkout/customer.maria
 *    s4e.c1m/p6s/c6t/c6r.m3a
 *
 * Part 2
 * In some cases, major parts consists of dozens of minor parts, that can still make the output String large.
 * For example, imagine compressing a URL such as "section/how.to.write.a.java.program.in.one.day".
 * After compressing it by following the rules in Part 1, the second major part still has 9 minor parts after compression.
 *
 * Task:
 * Therefore, to further compress the String, we want to only keep m (m > 0) compressed minor parts from Part1 within each major part.
 * If a major part has more than m minor parts, we keep the first (m-1) minor parts as is, but concatenate the first letter of the m-th minor part and the last letter of the last minor part with the count
 */
public class Compress {
   public String compress(String s) {
      StringBuilder sb = new StringBuilder();
      String[] majors = s.split("/");
      for (int i = 0; i < majors.length; i++) {
         if (i > 0) {
            sb.append("/");
         }

         String major = majors[i];
         String[] minors = major.split("\\.");
         for (int j = 0; j < minors.length; j++) {
            String minor = compressPart(minors[j]);
            if (j > 0) {
               sb.append(".");
            }
            sb.append(minor);
         }

      }
      return sb.toString();
   }

   public String compress(String s, int m) {
      StringBuilder sb = new StringBuilder();
      String[] majors = s.split("/");
      for (int i = 0; i < majors.length; i++) {
         if (i > 0) {
            sb.append("/");
         }

         String major = majors[i];
         String[] minors = major.split("\\.");

         char c1 = 0, c2 = 0;
         int len = 0;

         for (int j = 0; j < minors.length; j++) {
            if (j < m - 1) {
               if (j > 0) {
                  sb.append(".");
               }
               String minor = compressPart(minors[j]);
               sb.append(minor);
               continue;
            }

            if (j == m - 1) {
               c1 = minors[j].charAt(0);
               len--;
            }
            if (j == minors.length - 1) c2 = minors[j].charAt(minors[j].length() - 1);
            len += minors[j].length() + 1;
         }

         if (len > 0) {
            if (m > 1) sb.append(".");
            sb.append(c1).append(len - 2).append(c2);
         }

      }
      return sb.toString();

   }

   private String compressPart(String s) {
      int len = s.length();
      StringBuilder sb = new StringBuilder();
      sb.append(s.charAt(0));
      sb.append(len - 2);
      sb.append(s.charAt(len - 1));
      return sb.toString();
   }

   public static void run() {
      Compress comp = new Compress();
      System.out.println(comp.compress("stripe.com/payments/checkout/customer.maria"));
      System.out.println(comp.compress("stripe.com/payments/checkout/customer.maria", 1));
      System.out.println(comp.compress("section/how.to.write.a.java.program.in.one.day"));
      System.out.println(comp.compress("section/how.to.write.a.java.program.in.one.day", 3));
   }
}
