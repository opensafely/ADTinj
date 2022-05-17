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
