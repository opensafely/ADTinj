from cohortextractor import (
    codelist_from_csv,
    codelist,
)
ethnicity_codes = codelist_from_csv(
    "codelists/opensafely-ethnicity-snomed-0removed.csv",
    system="snomed",
    column="snomedcode",
    category_column="Grouping_6",
)
ADTinj = codelist_from_csv(
    "codelists/user-agleman-adt-injectable-dmd.csv",
    system="snomed",
    column="dmd_id",
)

ADTinj1 = codelist_from_csv(
    "codelists/user-agleman-adt-inj-1monthly-dmd.csv",
    system="snomed",
    column="dmd_id",
)

ADTinj3 = codelist_from_csv(
    "codelists/user-agleman-adt-inj-3monthly-dmd.csv",
    system="snomed",
    column="dmd_id",
)

ADTinj6 = codelist_from_csv(
    "codelists/user-agleman-adt-inj-6monthly-dmd.csv",
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
ADTsecond_gener = codelist_from_csv(
    "codelists/user-agleman-second-generation-antiandrogens3-dmd.csv",
    system="snomed",
    column="dmd_id",
)

# high cost drugs from the hospital - this is not avaiable pass 3 2020 - not usable 
# Abiraterone
# abiraterone = codelist(
#     ["abiraterone", "abiraterone acetate", "abiraterone acetate 500mg", "abiraterone acetate 500mg tablets", "Zytiga 500mg tablets", "Zytiga 500mg tablets (Janssen-Cilag Ltd)"], 
#     system="ctv3"
# )
#hcd = codelist(enzalutamide,abiraterone,darolutamide,apalutamide
#
#     ["abiraterone", "abiraterone acetate", "abiraterone acetate 500mg", "abiraterone acetate 500mg tablets", "Zytiga 500mg tablets", "Zytiga 500mg tablets (Janssen-Cilag Ltd)"], 
#     system="ctv3"
# )