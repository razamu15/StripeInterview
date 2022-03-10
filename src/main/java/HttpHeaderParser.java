package com.kamarkaka.stripe;

import java.util.*;

/***
 * Part 1
 * In an HTTP request, the Accept-Language header describes the list of languages that the requester would like content to be returned in.
 * The header takes the form of a comma-separated list of language tags.
 * For example: "Accept-Language: en-US, fr-CA, fr-FR" means that the reader would accept:
 *   1. English as spoken in the United States (most preferred)
 *   2. French as spoken in Canada
 *   3. French as spoken in France (least preferred)
 * We're writing a server that needs to return content in an acceptable language for the requester, and we want to make use of this header.
 * Our server doesn't support every possible language that might be requested (yet!), but there is a set of languages that we do support.
 * Write a function that receives two arguments:
 *   an Accept-Language header value as a string and a set of supported languages,
 *   and returns the list of language tags that will work for the request.
 * The language tags should be returned in descending order of preference (the same order as they appeared in the header).
 * In addition to writing this function, you should use tests to demonstrate that it's correct, either via an existing testing system or one you create.
 *
 * Examples:
 *   parse_accept_language(
 *     "en-US, fr-CA, fr-FR", # the client's Accept-Language header, a string
 *     ["fr-FR", "en-US"] # the server's supported languages, a set of strings
 *   )
 *   returns: ["en-US", "fr-FR"]
 *
 *   parse_accept_language("fr-CA, fr-FR", ["en-US", "fr-FR"])
 *   returns: ["fr-FR"]
 *
 *   parse_accept_language("en-US", ["en-US", "fr-CA"])
 *   returns: ["en-US"]
 *
 * Part 2
 * Accept-Language headers will often also include a language tag that is not region-specific - for example, a tag of "en" means "any variant of English".
 * Extend your function to support these language tags by letting them match all specific variants of the language.
 *
 * Examples:
 *   parse_accept_language("en", ["en-US", "fr-CA", "fr-FR"])
 *   returns: ["en-US"]
 *
 *   parse_accept_language("fr", ["en-US", "fr-CA", "fr-FR"])
 *   returns: ["fr-CA", "fr-FR"]
 *
 *   parse_accept_language("fr-FR, fr", ["en-US", "fr-CA", "fr-FR"])
 *   returns: ["fr-FR", "fr-CA"]
 *
 * Part 3
 * Accept-Language headers will sometimes include a "wildcard" entry, represented by an asterisk, which means "all other languages".
 * Extend your function to support the wildcard entry.
 *
 * Examples:
 *   parse_accept_language("en-US, *", ["en-US", "fr-CA", "fr-FR"])
 *   returns: ["en-US", "fr-CA", "fr-FR"]
 *
 *   parse_accept_language("fr-FR, fr, *", ["en-US", "fr-CA", "fr-FR"])
 *   returns: ["fr-FR", "fr-CA", "en-US"]
 */
public class HttpHeaderParser {
   public List<String> parseAcceptLanguage(String header, String[] supported) {
      List<String> list = new ArrayList<>();
      HashSet<String> set = new HashSet<>(Arrays.asList(supported));
      List<String> languages = parseHeader(header);
      for (String lang : languages) {
         if (set.contains(lang)) {
            list.add(lang);
         }
      }

      return list;
   }

   public List<String> parseAcceptLanguage2(String header, String[] supported) {
      List<String> list = new ArrayList<>();
      Map<String, List<String>> map = buildMap(supported);

      List<String> languages = parseHeader(header);
      for (String lang : languages) {
         String[] parts = lang.split("-");
         if (parts.length == 2) {
            if (map.containsKey(parts[0]) && map.get(parts[0]).contains(parts[1])) {
               list.add(lang);
               map.get(parts[0]).remove(parts[1]);
            }
         } else if (parts.length == 1) {
            if (map.containsKey(parts[0])) {
               for (String country : map.get(parts[0])) {
                  list.add(parts[0] + "-" + country);
               }
            }
         }
      }

      return list;
   }

   public List<String> parseAcceptLanguage3(String header, String[] supported) {
      List<String> list = new ArrayList<>();
      Map<String, List<String>> map = buildMap(supported);

      List<String> languages = parseHeader(header);
      for (String lang : languages) {
         String[] parts = lang.split("-");
         if (parts[0].equals("*")) {
            for (String supportedLang : supported) {
               String[] langParts = supportedLang.split("-");
               if (map.containsKey(langParts[0]) && map.get(langParts[0]).size() > 0) {
                  for (String country : map.get(langParts[0])) {
                     if (country.equals(langParts[1])) {
                        list.add(supportedLang);
                        break;
                     }
                  }
               }
            }
         } else if (parts.length == 2) {
            if (map.containsKey(parts[0]) && map.get(parts[0]).contains(parts[1])) {
               list.add(lang);
               map.get(parts[0]).remove(parts[1]);
            }
         } else if (parts.length == 1) {
            if (map.containsKey(parts[0])) {
               Iterator<String> iter = map.get(parts[0]).iterator();
               while (iter.hasNext()) {
                  list.add(parts[0] + "-" + iter.next());
                  iter.remove();
               }
            }
         }
      }

      return list;
   }

   private Map<String, List<String>> buildMap(String[] supported) {
      Map<String, List<String>> map = new HashMap<>();

      for (String lang : supported) {
         String[] parts = lang.split("-");
         map.putIfAbsent(parts[0], new ArrayList<>());
         map.get(parts[0]).add(parts[1]);
      }

      return map;
   }

   private List<String> parseHeader(String header) {
      List<String> list = new ArrayList<>();
      String[] parts = header.split(",");
      for (String part : parts) {
         list.add(part.trim());
      }
      return list;
   }

   public static void run() {
      HttpHeaderParser parser = new HttpHeaderParser();
      System.out.println(parser.parseAcceptLanguage("en-US, fr-CA, fr-FR", new String[] {"fr-FR", "en-US"}));
      System.out.println(parser.parseAcceptLanguage("fr-CA, fr-FR", new String[] {"en-US", "fr-FR"}));
      System.out.println(parser.parseAcceptLanguage("en-US", new String[] {"en-US", "fr-CA"}));

      System.out.println(parser.parseAcceptLanguage2("en", new String[] {"en-US", "fr-CA", "fr-FR"}));
      System.out.println(parser.parseAcceptLanguage2("fr", new String[] {"en-US", "fr-CA", "fr-FR"}));
      System.out.println(parser.parseAcceptLanguage2("fr-FR, fr", new String[] {"en-US", "fr-CA", "fr-FR"}));

      System.out.println(parser.parseAcceptLanguage3("en-US, *", new String[] {"en-US", "fr-CA", "fr-FR"}));
      System.out.println(parser.parseAcceptLanguage3("fr-FR, fr, *", new String[] {"en-US", "fr-CA", "fr-FR"}));

   }
}
