package org.molgenis.emx2;

import com.opencsv.CSVReader;
import com.opencsv.CSVWriter;
import org.apache.commons.lang3.StringUtils;
import org.molgenis.emx2.entities.emx1.Mutation;
import org.molgenis.emx2.entities.emx1.Patient;
import org.molgenis.emx2.entities.emx2.*;

import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static org.molgenis.emx2.Mapping.*;
import static org.molgenis.emx2.entities.emx2.GenomicVariations.GENVAR_HEADER;
import static org.molgenis.emx2.entities.emx2.GenomicVariationsCaseLevel.GENVARCASELVL_HEADER;
import static org.molgenis.emx2.entities.emx2.GenomicVariationsClinInterpr.GENVARCLININT_HEADER;
import static org.molgenis.emx2.entities.emx2.Individual.IND_HEADER;
import static org.molgenis.emx2.entities.emx2.IndividualsDiseases.INDVDIS_HEADER;
import static org.molgenis.emx2.entities.emx2.IndividualsPhenotypicFeatures.INDPHENFEAT_HEADER;

public class ConvertEMX1ToEMX2FAIRDataHub {

  /**
   * Convert EMX1 CHD7 data into EMX2 'FAIR Data Hub' structure as best we can
   *
   * How to:
   * Download Patients and Mutations from https://chd7.molgeniscloud.org using options: Attribute Labels, Entity Labels, CSV
   *
   * Input original EMX1 data exports:
   * - Mutations.csv
   * - Patients.csv
   *
   * Output EMX2 'FAIR Data Hub' tables for import:
   * - GenomicVariations.csv
   * - GenomicVariationsClinInterpr.csv
   * - GenomicVariationsCaseLevel.csv
   * - Individuals.csv
   * - IndividualsDiseases.csv
   * - IndividualsPhenotypicFeatures.csv
   *
   */
  public static void main(String[] args) throws Exception {

    // paths
    File mutationsFile = new File("/Users/joeri/Documents/EMX2/CHD7/Mutations.csv");
    File patientsFile = new File("/Users/joeri/Documents/EMX2/CHD7/Patients.csv");
    File outputDir = new File("/Users/joeri/Documents/EMX2/CHD7/output");

    //readers
    CSVReader mutationsReader = new CSVReader(new FileReader(mutationsFile));
    CSVReader patientsReader = new CSVReader(new FileReader(patientsFile));

    //writers
    CSVWriter individualsWriter =  new CSVWriter(new FileWriter(new File (outputDir, "Individuals.csv")));
    CSVWriter individualsDiseasesWriter =  new CSVWriter(new FileWriter(new File (outputDir, "IndividualsDiseases.csv")));
    CSVWriter individualsPhenotypicFeaturesWriter =  new CSVWriter(new FileWriter(new File (outputDir, "IndividualsPhenotypicFeatures.csv")));
    CSVWriter genomicVariationsWriter =  new CSVWriter(new FileWriter(new File (outputDir, "GenomicVariations.csv")));
    CSVWriter genomicVariationsCaseLevelWriter =  new CSVWriter(new FileWriter(new File (outputDir, "GenomicVariationsCaseLevel.csv")));
    CSVWriter genomicVariationsClinInterprWriter =  new CSVWriter(new FileWriter(new File (outputDir, "GenomicVariationsClinInterpr.csv")));

    // load original data into POJO structure
    Map<String, Mutation> idToMutation = new HashMap<>();
    List<Patient> patients = new ArrayList<>();
    String[] values;
    mutationsReader.readNext(); // skip header
    while ((values = mutationsReader.readNext()) != null) {
      Mutation mutation = new Mutation(values);
      idToMutation.put(mutation.Mutation_ID, mutation);
    }
    patientsReader.readNext(); // skip header
    while ((values = patientsReader.readNext()) != null) {
      Patient patient = new Patient(values);
      patient.updateMutationIdToMutation(idToMutation);
      patients.add(patient);
    }

    // writer output headers
    individualsWriter.writeNext(IND_HEADER);
    individualsDiseasesWriter.writeNext(INDVDIS_HEADER);
    individualsPhenotypicFeaturesWriter.writeNext(INDPHENFEAT_HEADER);
    genomicVariationsWriter.writeNext(GENVAR_HEADER);
    genomicVariationsCaseLevelWriter.writeNext(GENVARCASELVL_HEADER);
    genomicVariationsClinInterprWriter.writeNext(GENVARCLININT_HEADER);

    // keep track of variants and interpretations, output later
    Map<String, GenomicVariations> uniqueVariants = new HashMap<>();
    Map<String, GenomicVariationsClinInterpr> uniqueInterpretations = new HashMap<>();

    // iterate over patients and produce output files
    for(Patient patient : patients)
    {
      Individual individual = new Individual();
      individual.id = patient.Molgenis_ID;
      individual.sex = "assigned unspecified at birth";

      // map to diseases
      List<String> orphaTermNames = diseaseToOntology(patient.Phenotype);
      List<String> indToDiseases = new ArrayList<>();
      for(int i = 0; i < orphaTermNames.size(); i ++)
      {
        IndividualsDiseases individualsDiseases = new IndividualsDiseases();
        individualsDiseases.id = patient.Molgenis_ID+"_dis"+i;
        individualsDiseases.diseaseCode = orphaTermNames.get(i);
        individualsDiseases.familyHistory = familyHistory(patient.Positive_family_history);
        indToDiseases.add(individualsDiseases.id);
        individualsDiseasesWriter.writeNext(individualsDiseases.toRow());
        individual.diseaseCausalGenes = "CHD7";
      }
      individual.diseases = StringUtils.join(indToDiseases, ",");

      // map to phenotypes
      List<String> hpoTermNames = phenotypeToHPO(patient);
      List<String> indToPhen = new ArrayList<>();
      for(int i = 0; i < hpoTermNames.size(); i ++)
      {
        IndividualsPhenotypicFeatures indvPhenFeat = new IndividualsPhenotypicFeatures();
        indvPhenFeat.id = patient.Molgenis_ID+"_phen"+i;
        indvPhenFeat.featureType = hpoTermNames.get(i);
        indToPhen.add(indvPhenFeat.id);
        individualsPhenotypicFeaturesWriter.writeNext(indvPhenFeat.toRow());

      }
      individual.phenotypicFeatures = StringUtils.join(indToPhen, ",");

      // mutations
      for(int i = 0; i < patient.mutation.size(); i ++)
      {

        Mutation mutation = patient.mutation.get(i);

        if(!uniqueVariants.containsKey(mutation.Mutation_ID))
        {
          GenomicVariationsClinInterpr clinInterpr = new GenomicVariationsClinInterpr();
          clinInterpr.id = mutation.Mutation_ID + "_ci" + i;
          clinInterpr.category = pathogenicityToCategory(mutation.Pathogenicity);
          clinInterpr.clinicalRelevance = pathogenicityToClinRevelance(mutation.Pathogenicity);
          uniqueInterpretations.put(clinInterpr.id, clinInterpr);

          GenomicVariations variant = new GenomicVariations();
          variant.variantInternalId = mutation.Mutation_ID;
          variant.variantType = mutation.Mutation_type;
          variant.referenceBases = mutation.ref;
          variant.alternateBases = mutation.alt;
          variant.position_assemblyId = "GRCh37";
          variant.position_refseqId = "8";
          variant.position_start = mutation.start_nucleotide;
          variant.geneId = "CHD7";
          variant.genomicHGVSId = mutation.validated_cDNA.isEmpty() ? mutation.CHD7_c : mutation.validated_cDNA;
          variant.proteinHGVSIds = mutation.CHD7_p;
          variant.transcriptHGVSIds = "NM_017780.3";
          variant.clinicalInterpretations = clinInterpr.id;
          uniqueVariants.put(variant.variantInternalId, variant);
        }

        GenomicVariations variant = uniqueVariants.get(mutation.Mutation_ID);
        GenomicVariationsCaseLevel genVarCaseLvl = new GenomicVariationsCaseLevel();
        genVarCaseLvl.id = mutation.Mutation_ID + "_" + individual.id;
        genVarCaseLvl.individualId = individual.id;
        genVarCaseLvl.clinicalInterpretations = variant.clinicalInterpretations;
        // also update variant with link to the case level data
        variant.caseLevelData = variant.caseLevelData == null ? genVarCaseLvl.id : variant.caseLevelData + "," + genVarCaseLvl.id;
        genomicVariationsCaseLevelWriter.writeNext(genVarCaseLvl.toRow());

      }

      individualsWriter.writeNext(individual.toRow());
    }

    // write all unique genomic variants
    for(String variantId : uniqueVariants.keySet())
    {
      genomicVariationsWriter.writeNext(uniqueVariants.get(variantId).toRow());
    }

    // write all unique interpretations (1 per variant)
    for(String clinInterprId : uniqueInterpretations.keySet())
    {
      genomicVariationsClinInterprWriter.writeNext(uniqueInterpretations.get(clinInterprId).toRow());
    }

    // close all writers
    individualsWriter.close();
    individualsDiseasesWriter.close();
    individualsPhenotypicFeaturesWriter.close();
    genomicVariationsWriter.close();
    genomicVariationsCaseLevelWriter.close();
    genomicVariationsClinInterprWriter.close();
  }
}
