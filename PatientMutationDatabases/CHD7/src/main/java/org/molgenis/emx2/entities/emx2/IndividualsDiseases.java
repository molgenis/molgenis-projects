package org.molgenis.emx2.entities.emx2;

public class IndividualsDiseases {

    public static String[] INDVDIS_HEADER = new String[]{"id", "diseaseCode", "familyHistory"};

    public String id;
    public String diseaseCode;
    public String familyHistory;

    public String[] toRow()
    {
        return new String[]{id, diseaseCode, familyHistory};
    }


}
