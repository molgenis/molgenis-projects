#' ////////////////////////////////////////////////////////////////////////////
#' FILE: emx_create_04_static_content.R
#' AUTHOR: David Ruvolo
#' CREATED: 2020-11-20
#' MODIFIED: 2020-11-20
#' PURPOSE: create GoNL EMX for static content
#' STATUS: working
#' PACKAGES: readr; dplyr
#' COMMENTS: NA
#' ////////////////////////////////////////////////////////////////////////////

#' pkgs
suppressPackageStartupMessages(library(dplyr))

#' ~ 1 ~
#' Create Static Content
#' read source html file
#' collapse into a single string and apply regex
#' transform to data.frame(
#' save as `.tsv` file
readLines("./src/index.html", warn = FALSE) %>%
    paste0(., collapse = "\n") %>%
    stringr::str_replace_all(
        string = .,
        pattern = "([\\r\\n\\t])",
        replacement = ""
    ) %>%
    stringr::str_replace_all(
        string = .,
        pattern = "\\s+",
        replacement = " "
    ) %>%
    data.frame(
        `key_` = "home",
        content = .
    ) %>%
    readr::write_tsv(
        x = .,
        path = "data/sys_StaticContent.tsv",
        quote_escape = "double" # this may need to be adjusted
    )