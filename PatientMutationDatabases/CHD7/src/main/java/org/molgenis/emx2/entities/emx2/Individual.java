package org.molgenis.emx2.entities.emx2;

public class Individual {

    public static String[] IND_HEADER = new String[]{"id", "sex", "diseases", "diseaseCausalGenes", "phenotypicFeatures"};

    public String id;
    public String sex;
    public String diseases;
    public String diseaseCausalGenes;
    public String phenotypicFeatures;

    public String[] toRow()
    {
        return new String[]{id, sex, diseases, diseaseCausalGenes, phenotypicFeatures};
    }

}
