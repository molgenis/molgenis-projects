#'////////////////////////////////////////////////////////////////////////////
#' FILE: emx_create_02_entities.R
#' AUTHOR: David Ruvolo
#' CREATED: 2020-11-20
#' MODIFIED: 2020-11-20
#' PURPOSE: create GoNL EMX Entities
#' STATUS: working
#' PACKAGES: dplyr; readr
#' COMMENTS: NA
#'////////////////////////////////////////////////////////////////////////////

#' pkgs
suppressPackageStartupMessages(library(dplyr))

#' ~ 1 ~
#' Create entities
data.frame(
    name = "gonl_attribs",
    package = "gonl",
    extends = "",
    abstract = "",
    description = "package attributes"
) %>%
    bind_rows(
        data.frame(
            name = sapply(
                seq.int(1, 22, 1),
                function(d) {
                    paste0("gonl_chr", d)
                }
            ),
            package = "gonl",
            extends = "attribs",
            abstract = "",
            description = sapply(
                seq.int(1, 22, 1),
                function(d) {
                    paste0("GoNL chr", d)
                }
            )
        )
    ) %>%
    readr::write_tsv(
        x = .,
        path = "data/gonl_entities.tsv"
    )