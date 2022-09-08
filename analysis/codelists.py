from cohortextractor import (
    codelist_from_csv,
    codelist,
)
ethnicity_codes = codelist_from_csv(
    "codelists/opensafely-ethnicity.csv",
    system="ctv3",
    column="Code",
    category_column="Grouping_6",
)
ethnicity_codes_16 = codelist_from_csv(
    "codelists/opensafely-ethnicity.csv",
    system="ctv3",
    column="Code",
    category_column="Grouping_16",
)
ADTinj = codelist_from_csv(
    "codelists/user-agleman-adt-injectable-dmd.csv",
    system="snomed",
    column="dmd_id",
)

ADToral = codelist_from_csv(
    "codelists/user-agleman-oral-adt-prostate-ca-dmd.csv",
    system="snomed",
    column="dmd_id",
)

prostate_cancer_codes = codelist_from_csv(
    "codelists/user-agleman-prostate_cancer_snomed.csv",
    system="snomed",
    column="code",
)
# high cost drugs from the hospital - this is not avaiable pass 3 2020 - not usable 
# Abiraterone
# abiraterone = codelist(
#     ["abiraterone", "abiraterone acetate", "abiraterone acetate 500mg", "abiraterone acetate 500mg tablets", "Zytiga 500mg tablets", "Zytiga 500mg tablets (Janssen-Cilag Ltd)"], 
#     system="ctv3"
# )

