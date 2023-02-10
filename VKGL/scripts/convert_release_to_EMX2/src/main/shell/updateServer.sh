# go to web app and make new schema, e.g.
# https://vkgl-emx2.molgeniscloud.org --> "VKGL_public_consensus_jan2023"
# temporarily allow anonymous as Editor so that data can be imported
# Settings -> add 'anonymous' -> Editor

# go to dir with output of VKGLVariantsToEMX2Beacon
cd /Users/joeri/Documents/VKGL/vkgl-emx2/jan2023

# import the output into VKGL EMX2 server
curl -X POST --data-binary @GenomicVariationsClinInterpr.tsv https://vkgl-emx2.molgeniscloud.org/VKGL_public_consensus_jan2023/api/csv/GenomicVariationsClinInterpr
curl -X POST --data-binary @GenomicVariations.tsv https://vkgl-emx2.molgeniscloud.org/VKGL_public_consensus_jan2023/api/csv/GenomicVariations

# go to web app and set permissions back to Viewer only
# Settings -> add 'anonymous' -> Viewer

# check if it works by running a few queries
curl "https://vkgl-emx2.molgeniscloud.org/api/beacon/g_variants?start=105167860&referenceName=14&referenceBases=T&alternateBases=G"
curl "https://vkgl-emx2.molgeniscloud.org/api/beacon/g_variants?geneId=TERC"
curl "https://vkgl-emx2.molgeniscloud.org/api/beacon/g_variants?start=2000000&end=5000000&referenceName=1"

# remove Viewer permissions from previous releases (or delete)
