package com.kamarkaka.stripe;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.reflect.TypeToken;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

import java.io.*;
import java.lang.reflect.Type;
import java.net.URISyntaxException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.Collection;
import java.util.List;
import java.util.Objects;

public class BikeMap {
   private final Path targetPath;
   private final Gson gson;
   private final OkHttpClient client;

   public BikeMap() throws URISyntaxException {
      this.targetPath = Paths.get(getClass().getResource("/").toURI());
      this.gson = new GsonBuilder()
         .setPrettyPrinting()
         .create();
      this.client = new OkHttpClient();
   }

   public void readFile(String filePath) throws IOException {
      Path file = Paths.get(targetPath + File.separator + filePath);
      BufferedReader reader = null;

      try {
         reader = new BufferedReader(new FileReader(file.toString()));
         String line;
         while ((line = reader.readLine()) != null) {
            System.out.println(line);
         }
         reader.close();
      } catch (FileNotFoundException ex) {
         System.out.println("FileNotFoundException");
      } catch (IOException e) {
         System.out.println("IOException");
      } finally {
         if (reader != null) reader.close();
      }
   }

   public void readObjectFromJsonString(String jsonString) {
      ExampleClass example = gson.fromJson(jsonString, ExampleClass.class);
      System.out.println(example.getName());
      System.out.println(example.getPopulation());
      System.out.println(example.getListOfStates());
   }

   public void readObjectFromJson(String filePath) throws IOException {
      Path file = Paths.get(targetPath + File.separator + filePath);
      BufferedReader reader = null;

      try {
         reader = new BufferedReader(new FileReader(file.toString()));
         ExampleClass example = gson.fromJson(reader, ExampleClass.class);
         System.out.println(example.getName());
         System.out.println(example.getPopulation());
         System.out.println(example.getListOfStates());
         reader.close();
      } catch (FileNotFoundException ex) {
         System.out.println("FileNotFoundException");
      } catch (IOException e) {
         System.out.println("IOException");
      } finally {
         if (reader != null) reader.close();
      }
   }

   public void readArrayFromJson(String filePath) throws IOException {
      Path file = Paths.get(targetPath + File.separator + filePath);
      BufferedReader reader = null;

      try {
         reader = new BufferedReader(new FileReader(file.toString()));
         ExampleClass[] examples = gson.fromJson(reader, ExampleClass[].class);
         for (ExampleClass example : examples) {
            System.out.println(example.getName());
            System.out.println(example.getPopulation());
            System.out.println(example.getListOfStates());
         }
         reader.close();
      } catch (FileNotFoundException ex) {
         System.out.println("FileNotFoundException");
      } catch (IOException e) {
         System.out.println("IOException");
      } finally {
         if (reader != null) reader.close();
      }
   }

   public void readListFromJson(String filePath) throws IOException {
      Path file = Paths.get(targetPath + File.separator + filePath);
      BufferedReader reader = null;

      try {
         reader = new BufferedReader(new FileReader(file.toString()));
         Type collectionType = new TypeToken<Collection<ExampleClass>>(){}.getType();
         Collection<ExampleClass> examples = gson.fromJson(reader, collectionType);
         for (ExampleClass example : examples) {
            System.out.println(example.getName());
            System.out.println(example.getPopulation());
            System.out.println(example.getListOfStates());
         }
         reader.close();
      } catch (FileNotFoundException ex) {
         System.out.println("FileNotFoundException");
      } catch (IOException e) {
         System.out.println("IOException");
      } finally {
         if (reader != null) reader.close();
      }
   }

   public void writeJson() throws IOException {
      Path filePath = Paths.get(targetPath + File.separator + "out.json");
      FileWriter writer = new FileWriter(filePath.toFile());
      ExampleClass example = ExampleClass.createInstance();
      gson.toJson(example, writer);
      writer.flush();
      writer.close();
   }

   public void download(String url, String filename) throws IOException {
      Request request = new Request.Builder()
         .url(url)
         .build();
      Response response = client.newCall(request).execute();
      if (response.body() == null) return;

      Path filePath = Paths.get(targetPath + File.separator + filename);

      OutputStream output = new FileOutputStream(filePath.toFile());
      InputStream stream = response.body().byteStream();
      stream.transferTo(output);
      output.close();
      stream.close();
   }

   public static void run() {
      try {
         BikeMap sol = new BikeMap();
         sol.readFile("text.txt");
         sol.readObjectFromJsonString("{\"name\": \"country name\", \"population\": 123, \"listOfStates\": [\"country1\", \"country2\", \"country3\"]}");
         sol.readObjectFromJson("object.json");
         sol.readArrayFromJson("array.json");
         sol.readListFromJson("array.json");
         sol.writeJson();

         sol.download("https://raw.github.com/square/okhttp/master/README.md", "README.md");
         sol.download("https://raw.githubusercontent.com/Luzifer/staticmap/master/example/postmap.png", "postmap.png");
      } catch (URISyntaxException ex) {
         System.out.println("URISyntaxException");
      } catch (IOException e) {
         System.out.println("IOException");
      }
   }
}

class ExampleClass {
   String name;
   int population;
   private List listOfStates;

   public String getName() {
      return name;
   }

   public void setName(String name) {
      this.name = name;
   }

   public int getPopulation() {
      return population;
   }

   public void setPopulation(int population) {
      this.population = population;
   }

   public List getListOfStates() {
      return listOfStates;
   }

   public void setListOfStates(List listOfStates) {
      this.listOfStates = listOfStates;
   }

   public static ExampleClass createInstance() {
      ExampleClass example = new ExampleClass();
      example.setName("output name");
      example.setPopulation(12321);
      example.setListOfStates(Arrays.asList("state1","state2","state3"));
      return example;
   }
}