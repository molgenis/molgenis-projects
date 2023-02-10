package org.molgenis.emx2.entities.emx2;

public class GenomicVariationsCaseLevel {


    public static String[] GENVARCASELVL_HEADER = new String[]{"id", "individualId", "clinicalInterpretations"};

    public String id;
    public String individualId;
    public String clinicalInterpretations;

    public String[] toRow()
    {
        return new String[]{id, individualId, clinicalInterpretations};
    }

}
