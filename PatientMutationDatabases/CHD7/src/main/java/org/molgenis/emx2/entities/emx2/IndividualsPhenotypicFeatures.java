package org.molgenis.emx2.entities.emx2;

public class IndividualsPhenotypicFeatures {

    public static String[] INDPHENFEAT_HEADER = new String[]{"id", "featureType"};

    public String id;
    public String featureType;

    public String[] toRow()
    {
        return new String[]{id, featureType};
    }

}
