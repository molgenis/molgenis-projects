![Genome of the Netherlands proejct](src/images/gonl_logo.png)

# GoNL Molgenis Server

This repository contains the code used to update the GoNL MOLGENIS app. The motivation behind this project is to create a reproducible workflow for updating the GoNL Molgenis server. This project was started during the update the GoNL MOLGENIS server from `v4.0` to `8.5+`. I wanted a worflow that does everything from downloading the source data to pushing the files to the server.

## Getting Started

First, you will need to request access to internal servers (both data and GoNL). Contact your manager for more information.

Several R scripts were created to build the EMX data model. These files are located in the `R` folder. Each file is responsible for creating a specific component for the EMX model. This allows elements of the model to be updated on-demand. To run these scripts, you will need to install Base R ([https://cran.r-project.org](https://cran.r-project.org)).

Once R is installed, you will need the following R packages.

```r
install.packages(c("dplyr", "jsonlite", "readr", "stringr"))
```

In the main shell script `index.sh`, use the `Rscript` commands to generate the GoNL EMX data files. For example, let's say that I want to update the entities EMX. First, make the required changes in the `R/emx_create_02_entities.R` files, and then run it using `Rscript`.

```shell
Rscript -e "source('R/emx_create_02_entities.R')"
```

All files are saved in the `data/` folder.

### Notes

1. In the main shell script, the logo is downloaded from the project website via `curl`. Image optimizations are applied using the Image Optim app ([https://imageoptim.com/mac](https://imageoptim.com/mac)).

## Resources

More information can be found in the following places.

- GoNL `v4.0`: [https://molgenis95.gcc.rug.nl](https://molgenis95.gcc.rug.nl)
- GoNL data source: [https://molgenis26.gcc.rug.nl/downloads/gonl_public/variants/release5/](https://molgenis26.gcc.rug.nl/downloads/gonl_public/variants/release5/)
- Project Website: [http://www.nlgenome.nl](http://www.nlgenome.nl)
