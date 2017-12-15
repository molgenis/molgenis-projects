library('RCurl')
library('rjson')
library('httr')

eval(expr = parse(text = getURL("${url}/molgenis.R?molgenis-token=${molgenisToken}")))

age = function(from, to) {
  from_lt = as.POSIXlt(as.Date(from))
  to_lt = as.POSIXlt(as.Date(to))
  
  age = to_lt$year - from_lt$year
  
  ifelse(to_lt$mon < from_lt$mon |
           (to_lt$mon == from_lt$mon & to_lt$mday < from_lt$mday),
         age - 1, age)
}

percentage = function(total, number) {
  return(round(number/total * 100, 1))
}

getTotalRows <- function(table) {
  url <- paste0("${url}/api/v2/",table,"?molgenis-token=${molgenisToken}")
  response <- fromJSON(getURL(url))
  return(response$total)
}

getPatientDataPerSampleType = function(sampleType, patient_data) {
  id <- sampleType
  
  numberPatients <- nrow(patient_data)
  
  patient_onset_age <- patient_data$age_at_onset
  patient_final_age <- patient_data$age_at_last_record_diagnosis
  meanOnsetAge <- round(mean(patient_onset_age, na.rm=TRUE), 1)
  sdOnsetAge <- round(sd(patient_onset_age, na.rm=TRUE), 1)
  meanFinalAge <- round(mean(patient_final_age, na.rm=TRUE), 1)
  sdFinalAge <- round(sd(patient_final_age, na.rm=TRUE), 1)
  
  gender <- patient_data$Sex
  countMale <- length(gender[gender == 'Male'])
  countFemale <- length(gender[gender == 'Female'])
  percentageMale <- percentage(numberPatients, countMale)
  percentageFemale <- percentage(numberPatients, countFemale)
  
  disease <- patient_data$diagnosis_last_record
  UC_patients_with_na <- patient_data[disease == 'UC',]
  UC_patients <- UC_patients_with_na[!is.na(UC_patients_with_na$diagnosis_last_record),]
  CD_patients_with_na <- patient_data[disease == 'CD',]
  CD_patients <- CD_patients_with_na[!is.na(CD_patients_with_na$diagnosis_last_record),]
  IBDU_patients_with_na <- patient_data[disease == 'IBDU',]
  IBDU_patients <- IBDU_patients_with_na[!is.na(IBDU_patients_with_na$diagnosis_last_record),]
  IBDI_patients_with_na <- patient_data[disease == 'IBDI',]
  IBDI_patients <- IBDI_patients_with_na[!is.na(IBDI_patients_with_na$diagnosis_last_record),]
  totalUC <- nrow(UC_patients)
  totalCD <- nrow(CD_patients)
  totalIBDU <- nrow(IBDU_patients)
  totalIBDI <- nrow(IBDI_patients)
  
  percentageUC <- percentage(numberPatients, totalUC)
  percentageCD <- percentage(numberPatients, totalCD)
  percentageIBDI <- percentage(numberPatients, totalIBDI)
  percentageIBDU <- percentage(numberPatients, totalIBDU)
  
  pNumber <- length(CD_patients$Montreal_Bp[CD_patients$Montreal_Bp == 1])
  pPercentage <- percentage(totalCD, pNumber)
  
  L1 <- CD_patients$Montreal_L[CD_patients$Montreal_L == 'L1']
  L1L4 <- CD_patients$Montreal_L[CD_patients$Montreal_L == 'L1+L4']
  L1L4_without_NA <- L1[!is.na(L1)] + L1L4[!is.na(L1L4)]
  L1Number = length(L1L4_without_NA)
  L1Percentage <- percentage(totalCD, L1Number)
  
  L2 <- CD_patients$Montreal_L[CD_patients$Montreal_L == 'L2']
  L2L4 <- CD_patients$Montreal_L[CD_patients$Montreal_L == 'L2+L4']
  L2L4_without_NA <- L2[!is.na(L2)] + L2L4[!is.na(L2L4)]
  L2Number = length(L2L4_without_NA)
  L2Percentage <- percentage(totalCD, L2Number)
  
  L3 <- CD_patients$Montreal_L[CD_patients$Montreal_L == 'L3']
  L3L4 <- CD_patients$Montreal_L[CD_patients$Montreal_L == 'L3+L4']
  L3L4_without_NA <- L3[!is.na(L3)] + L3L4[!is.na(L3L4)]
  L3Number = length(L3L4_without_NA)
  L3Percentage <- percentage(totalCD, L3Number)
  
  L4Number <- length(CD_patients$Montreal_L4[CD_patients$Montreal_L4 == 'Yes'])
  L4Percentage <- percentage(totalCD, L4Number)
  
  E1Number <- length(UC_patients$Montreal_E[UC_patients$Montreal_E == 'E1'])
  E1Percentage <- percentage(totalUC, E1Number)
  
  E2Number <- length(UC_patients$Montreal_E[UC_patients$Montreal_E == 'E2'])
  E2Percentage <- percentage(totalUC, E2Number)
  
  E3Number <- length(UC_patients$Montreal_E[UC_patients$Montreal_E == 'E3'])
  E3Percentage <- percentage(totalUC, E3Number)
  
  countsPerSampleType <- data.frame(id, numberPatients, meanOnsetAge, sdOnsetAge, meanFinalAge, sdFinalAge, countMale, countFemale, 
                                    percentageMale, percentageFemale, totalUC, totalCD, pNumber, pPercentage, L1Number,
                                    L1Percentage, L2Number, L2Percentage, L3Number, L3Percentage, L4Number, 
                                    L4Percentage, E1Number, E1Percentage, E2Number, E2Percentage, E3Number, 
                                    E3Percentage, totalIBDI, totalIBDU, percentageCD, percentageUC, percentageIBDU, percentageIBDI)
  return(countsPerSampleType)
}

patient_data <- molgenis.get("${phenotypes}", num=10000)
stool_patient_data <- patient_data[patient_data$feces_16S_ID!="",]
ichip_patient_data <- patient_data[patient_data$Ichip_ID!="",]

iChipSamples <- getTotalRows("${ichip}")
stoolSamples <- getTotalRows("${otu}")
totalSamples <- iChipSamples+stoolSamples

allPatientSamples <- getPatientDataPerSampleType("all_patients", patient_data)
stoolPatientSamples <- getPatientDataPerSampleType("ichip_patients", ichip_patient_data)
ichipPatientSamples <- getPatientDataPerSampleType("stool_patients", stool_patient_data)

numberSamples <- c(totalSamples)
allPatientSamples <- cbind(allPatientSamples, numberSamples)

numberSamples <- c(stoolSamples)
stoolPatientSamples <- cbind(stoolPatientSamples, numberSamples)

numberSamples <- c(iChipSamples)
ichipPatientSamples <- cbind(ichipPatientSamples, numberSamples)

molgenis.deleteList("IBD_counts", c("all_patients", "stool_patients", "ichip_patients"))

molgenis.addAll('IBD_counts', allPatientSamples)
molgenis.addAll('IBD_counts', stoolPatientSamples)
molgenis.addAll('IBD_counts', ichipPatientSamples)