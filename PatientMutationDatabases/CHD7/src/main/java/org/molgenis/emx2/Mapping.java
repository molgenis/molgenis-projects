package org.molgenis.emx2;

import org.molgenis.emx2.entities.emx1.Patient;

import java.util.ArrayList;
import java.util.List;

public class Mapping {

    public static String pathogenicityToCategory(String value) throws Exception {
        if(value.equals("Benign"))
        {
            return "Not related to clinical phenotype";
        }
        else if(value.equals("Pathogenic")){
            return "Disease causing";
        }
        else if(value.equals("Unclassified variant")){
            return null;
        }
        else{
            throw new Exception("unmapped Pathogenicity value: " + value);
        }
    }

    public static String pathogenicityToClinRevelance(String value) throws Exception {
        if(value.equals("Benign"))
        {
            return "Benign";
        }
        else if(value.equals("Pathogenic")){
            return "Pathogenic";
        }
        else if(value.equals("Unclassified variant")){
            return "Unknown Significance";
        }
        else{
            throw new Exception("unmapped Pathogenicity value: " + value);
        }
    }

    public static List<String> diseaseToOntology(String value) {
        List<String> diseases = new ArrayList<>();
        if (value.contains("CHARGE syndrome")) {
            diseases.add("CHARGE syndrome");
        }
        if (value.contains("CLP")) {
            diseases.add("Cleft lip/palate");
        }
        if (value.contains("idiopathic scoliosis")) {
            diseases.add("NON RARE IN EUROPE: Adolescent idiopathic scoliosis");
        }
        if (value.contains("hypogonadotropic hyogonadism")) {
            diseases.add("Congenital hypogonadotropic hypogonadism");
        }
        if (value.contains("Kallmann syndrome")) {
            diseases.add("Kallmann syndrome");
        }
        if (value.contains("congenital heart defect")) {
            diseases.add("Rare congenital non-syndromic heart malformation");
        }
        return diseases;
    }

    public static String familyHistory(String value) throws Exception {
        if (value.isEmpty() || value.equals("probably") || value.equals("parent phenotype not provided")) {
            return null;
        }
        if (value.equals("yes")) {
            return "true";
        }
        if (value.equals("no")) {
            return "false";
        }
        throw new Exception("no mapping for " + value);
    }

    public static List<String> phenotypeToHPO(Patient patient)
    {
        List<String> hpoTerms = new ArrayList<>();

        if(patient.Coloboma.equals("yes")){
            hpoTerms.add("Coloboma");
        }
        if(patient.Congenital_heart_defect.equals("yes"))
        {
            hpoTerms.add("Abnormal heart morphology");
        }
        if(patient.Choanal_anomaly.equals("yes"))
        {
            hpoTerms.add("Choanal atresia");
        }
        if(patient.CLP.equals("yes")){
            hpoTerms.add("Cleft lip");
            hpoTerms.add("Cleft palate");
        }
        if(patient.Growth_retardation.equals("yes")){
            hpoTerms.add("Postnatal growth retardation");
        }
        if(patient.Developmental_delay.equals("yes")){
            hpoTerms.add("Global developmental delay");
        }
        if(patient.Genital_hypoplasia.equals("yes")){
            hpoTerms.add("External genital hypoplasia");
        }
        if(patient.Sense_of_smell.contains("Hyposmia")){
           hpoTerms.add("Hyposmia");
        }
        if(patient.Sense_of_smell.contains("Anosmia")){
            hpoTerms.add("Anosmia");
        }
        if(patient.External_ear_anomaly.equals("yes")){
            hpoTerms.add("External ear malformation");
        }
        if(patient.Hearing_loss.equals("yes")){
            hpoTerms.add("Hearing impairment");
        }
        if(patient.Semicircular_canal_anomaly.equals("yes")){
            hpoTerms.add("Morphological abnormality of the semicircular canal");
        }
        if(patient.Facial_palsy.equals("yes")){
            hpoTerms.add("Facial palsy");
        }
        if(patient.TE_anomaly.equals("yes")){
            hpoTerms.add("Abnormal tracheobronchial morphology");
        }
        if(patient.Feeding_difficulties.equals("yes")){
            hpoTerms.add("Feeding difficulties");
        }
        return hpoTerms;
    }
}
