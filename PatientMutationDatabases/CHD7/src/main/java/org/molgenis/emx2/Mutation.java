package org.molgenis.emx2;

public class Mutation {

    public String Mutation_ID;
    public String CHD7_c;
    public String CHD7_p;
    public String Exon;
    public String Domain;
    public String Pathogenicity;
    public String Mutation_type;
    public String Other_information_mutation;
    public String CADD_raw_score;
    public String CADD_phred_score;
    public String validated_cDNA;
    public String chromosome;
    public String start_nucleotide;
    public String ref;
    public String alt;
    public String start_nucleotide_cDNA;
    public String Molgenis_ID;

    public Mutation(String[] values)
    {
        if(values.length != 17)
        {
            System.out.println("Need 17 values, found " + values.length + " for " + values);
        }
        this.Mutation_ID = values[0];
        this.CHD7_c = values[1];
        this.CHD7_p = values[2];
        this.Exon = values[3];
        this.Domain = values[4];
        this.Pathogenicity = values[5];
        this.Mutation_type = values[6];
        this.Other_information_mutation = values[7];
        this.CADD_raw_score = values[8];
        this.CADD_phred_score = values[9];
        this.validated_cDNA = values[10];
        this.chromosome = values[11];
        this.start_nucleotide = values[12];
        this.ref = values[13];
        this.alt = values[14];
        this.start_nucleotide_cDNA = values[15];
        this.Molgenis_ID = values[16];

    }
}
