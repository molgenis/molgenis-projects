#' ////////////////////////////////////////////////////////////////////////////
#' FILE: emx_create_03_attribs.R
#' AUTHOR: David Ruvolo
#' CREATED: 2020-11-20
#' MODIFIED: 2020-11-20
#' PURPOSE: create GoNL EMX attributes
#' STATUS: working
#' PACKAGES: dplyr; readr
#' COMMENTS: NA
#' ////////////////////////////////////////////////////////////////////////////

#' pkgs
suppressPackageStartupMessages(library(dplyr))

#' ~ 1 ~
#' load json file as data.frame
#' apply transformations
#' save as `.tsv` file
jsonlite::read_json(
    path = "R/emx_utils_base_attribs.json",
    simplifyVector = TRUE
) %>%
    `[[`(1) %>%
    mutate(
        entity = "attribs"
    ) %>%
    readr::write_tsv(x = ., path = "data/gonl_attributes.tsv")