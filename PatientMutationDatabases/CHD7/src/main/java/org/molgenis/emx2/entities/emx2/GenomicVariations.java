package org.molgenis.emx2.entities.emx2;

public class GenomicVariations {

    public static String[] GENVAR_HEADER = new String[]{"variantInternalId", "variantType", "referenceBases", "alternateBases", "position_assemblyId", "position_refseqId", "position_start", "geneId", "genomicHGVSId", "proteinHGVSIds", "transcriptHGVSIds", "clinicalInterpretations", "caseLevelData"};

    public String variantInternalId;
    public String variantType;
    public String referenceBases;
    public String alternateBases;
    public String position_assemblyId;
    public String position_refseqId;
    public String position_start;
    public String geneId;
    public String genomicHGVSId;
    public String proteinHGVSIds;
    public String transcriptHGVSIds;
    public String clinicalInterpretations;
    public String caseLevelData;

    public String[] toRow()
    {
        return new String[]{variantInternalId, variantType, referenceBases, alternateBases, position_assemblyId, position_refseqId, position_start, geneId, genomicHGVSId, proteinHGVSIds, transcriptHGVSIds, clinicalInterpretations, caseLevelData};
    }

}
