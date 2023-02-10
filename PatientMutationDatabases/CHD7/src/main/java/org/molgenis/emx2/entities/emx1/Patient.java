package org.molgenis.emx2.entities.emx1;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Map;

public class Patient {

    public String Molgenis_ID;
    public String Patient_ID;
    public String Mutation_ID;
    public String Pubmed_ID;
    public String Original_ID_reference;
    public String Positive_family_history;
    public String Familial_information;
    public String Phenotype;
    public String Coloboma;
    public String Congenital_heart_defect;
    public String Choanal_anomaly;
    public String CLP;
    public String Growth_retardation;
    public String Developmental_delay;
    public String Genital_hypoplasia;
    public String Sense_of_smell;
    public String External_ear_anomaly;
    public String Hearing_loss;
    public String Semicircular_canal_anomaly;
    public String Facial_palsy;
    public String TE_anomaly;
    public String Feeding_difficulties;
    public String Other;
    public String Deceased;
    public String ID_CHD7_mutations;
    public String ID_CHARGE_database;
    public String Reference_refworks;
    public String Insert_detailed_information_column_other;
    public String Other_information_mutation;

    // map and add after loading the mutations
    public List<Mutation> mutation;

    public Patient(String[] values) throws Exception {
        if(values.length != 29)
        {
            System.out.println("Need 29 values, found " + values.length + " for " + Arrays.toString(values));
        }
        this.Molgenis_ID = values[0];
        this.Patient_ID = values[1];
        this.Mutation_ID = values[2];
        this.Pubmed_ID = values[3];
        this.Original_ID_reference = values[4];
        this.Positive_family_history = values[5];
        this.Familial_information = values[6];
        this.Phenotype = values[7];
        this.Coloboma = values[8];
        this.Congenital_heart_defect = values[9];
        this.Choanal_anomaly = values[10];
        this.CLP = values[11];
        this.Growth_retardation = values[12];
        this.Developmental_delay = values[13];
        this.Genital_hypoplasia = values[14];
        this.Sense_of_smell = values[15];
        this.External_ear_anomaly = values[16];
        this.Hearing_loss = values[17];
        this.Semicircular_canal_anomaly = values[18];
        this.Facial_palsy = values[19];
        this.TE_anomaly = values[20];
        this.Feeding_difficulties = values[21];
        this.Other = values[22];
        this.Deceased = values[23];
        this.ID_CHD7_mutations = values[24];
        this.ID_CHARGE_database = values[25];
        this.Reference_refworks = values[26];
        this.Insert_detailed_information_column_other = values[27];
        this.Other_information_mutation = values[28];
        this.mutation = new ArrayList<>();
    }

    public void updateMutationIdToMutation(Map<String, Mutation> idToMutation) throws Exception {
        String[] mutationIds = this.Mutation_ID.split(",", -1);
        for(String mutationId : mutationIds)
        {
            if(!idToMutation.containsKey(mutationId)){
                throw new Exception("Mutation ID not found: " + this.Mutation_ID);
            }
            this.mutation.add(idToMutation.get(mutationId));
        }
    }
}
