package org.molgenis.emx2;

import com.opencsv.CSVReader;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

public class EMX1_to_EMX2 {

  /**
   * Download Patients and Mutations CSV from https://chd7.molgeniscloud.org/
   * use options: Attribute Labels, Entity Labels, CSV
   *
   * @param args
   * @throws Exception
   */
  public static void main(String args[]) throws Exception {
    File mutationsFile = new File("/Users/joeri/Documents/EMX2/CHD7/Mutations.csv");
    File patientsFile = new File("/Users/joeri/Documents/EMX2/CHD7/Patients.csv");
    CSVReader mutationsReader = new CSVReader(new FileReader(mutationsFile));
    CSVReader patientsReader = new CSVReader(new FileReader(patientsFile));
    ArrayList<Patient> patients = new ArrayList<>();
    ArrayList<Mutation> mutations = new ArrayList<>();

    String[] values;
    while ((values = patientsReader.readNext()) != null) {
      Patient patient = new Patient(values);
      patients.add(patient);
    }
    while ((values = mutationsReader.readNext()) != null) {
      Mutation mutation = new Mutation(values);
      mutations.add(mutation);
    }




  }
}
