package org.molgenis.emx2.entities.emx2;

public class GenomicVariationsClinInterpr {


    public static String[] GENVARCLININT_HEADER = new String[]{"id", "category", "clinicalRelevance"};

    public String id;
    public String category;
    public String clinicalRelevance;

    public String[] toRow()
    {
        return new String[]{id, category, clinicalRelevance};
    }

}
