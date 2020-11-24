#'////////////////////////////////////////////////////////////////////////////
#' FILE: emx_create_01_pkg.R
#' AUTHOR: David Ruvolo
#' CREATED: 2020-11-20
#' MODIFIED: 2020-11-20
#' PURPOSE: create GoNL EMX package
#' STATUS: working
#' PACKAGES: dplyr; readr
#' COMMENTS: This file should be executed in the `index.sh` script
#'////////////////////////////////////////////////////////////////////////////

#' pkgs
suppressPackageStartupMessages(library(dplyr))

#' ~ 1 ~
#' Create Package data.frame
#' Save as `.tsv` file
data.frame(
    id = "gonl",
    label = "GoNL",
    description = "Genome of the Netherlands",
    idAttribute = FALSE,
    labelAttribute = FALSE,
    parent = "",
    tags = ""
) %>%
    readr::write_tsv(
        x = .,
        path = "data/sys_md_Package.tsv"
    )
