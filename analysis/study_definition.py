from cohortextractor import (
    StudyDefinition,
    Measure,
    patients,
)

from codelists import *

start_date = "2015-01-01"
end_date = "2023-12-01"

study = StudyDefinition(
    default_expectations={
        "date": {"earliest": "2015-01-01", "latest": "today"},
        "rate": "uniform",
        "incidence": 0.5,
    },
    index_date="2023-12-01",
    population=patients.all(),

    ethnicity=patients.categorised_as(
        {
            "Missing": "DEFAULT",
            "White": """ ethnicity_code=1 """,
            "Mixed": """ ethnicity_code=2 """,
            "Asian": """ ethnicity_code=3 """,
            "Black": """ ethnicity_code=4 """,
            "Chinese": """ ethnicity_code=5 """,
        },
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "Missing": 0.4,
                    "White": 0.1,
                    "Mixed": 0.1,
                    "Asian": 0.1,
                    "Black": 0.1,
                    "Chinese": 0.2,
                }
            },
        },
        ethnicity_code=patients.with_these_clinical_events(
            ethnicity_codes,
            returning="category",
            find_last_match_in_period=True,
            include_date_of_match=False,
            return_expectations={
            "category": {"ratios": {"1": 0.2, "2": 0.2, "3": 0.2, "4": 0.2, "5": 0.2}},
            "incidence": 0.75,
            },
        ),
    ),
    died=patients.died_from_any_cause(
        on_or_before="index_date",
        returning="date_of_death",
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest" : "2010-02-01"},
            "rate": "exponential_increase"
        },
    ),
    has_died=patients.died_from_any_cause(
        on_or_before="index_date",
        returning='binary_flag',
        return_expectations={
            "incidence": 0.4
        },
    ),
    prostate_ca=patients.with_these_clinical_events(
        prostate_cancer_codes,
        on_or_before="index_date",
        find_first_match_in_period=True,
        include_date_of_match=True,
        include_month=True,
        include_day=True,
        returning="binary_flag",
        return_expectations={
            "date": {"earliest": "2000-01-01", "latest": "today"},
            "incidence": 0.8
        }
    ),
    age_pa_ca=patients.age_as_of(
        "prostate_ca_date",
        return_expectations={
            "rate": "exponential_increase",
            "int": {"distribution": "population_ages"},
        },
    ),
    age_group=patients.categorised_as(
        {
            "Missing": "DEFAULT",
            "<65": """ age_pa_ca < 65""",
            "65-74": """ age_pa_ca >= 65 AND age_pa_ca < 75""",
            "75-84": """ age_pa_ca >= 75 AND age_pa_ca < 85""",
            "85+": """ age_pa_ca >= 85""",
        },
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "Missing": 0.2,
                    "<65": 0.2,
                    "65-74": 0.2,
                    "75-84": 0.2,
                    "85+": 0.2,
                }
            },
        },
    ),
    sex=patients.sex(
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"M": 0.99, "F": 0.01}},
        }
    ),
    imd_cat=patients.categorised_as(
        {
            "Unknown": "DEFAULT",
            "1 (most deprived)": "imd >= 0 AND imd < 32844*1/5",
            "2": "imd >= 32844*1/5 AND imd < 32844*2/5",
            "3": "imd >= 32844*2/5 AND imd < 32844*3/5",
            "4": "imd >= 32844*3/5 AND imd < 32844*4/5",
            "5 (least deprived)": "imd >= 32844*4/5 AND imd <= 32844",
        },
        imd=patients.address_as_of(
            "2023-12-01",
            returning="index_of_multiple_deprivation",
            round_to_nearest=100,
        ),
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "Unknown": 0.05,
                    "1 (most deprived)": 0.19,
                    "2": 0.19,
                    "3": 0.19,
                    "4": 0.19,
                    "5 (least deprived)": 0.19,
                }
            },
        },
    ),
    ADTinj=patients.with_these_medications(
        ADTinj,
        on_or_before="index_date",
        returning="binary_flag",
        return_expectations={"incidence": 0.50},
    ),
    ADToral=patients.with_these_medications(
        ADToral,
        on_or_before="index_date",
        returning="binary_flag",
        return_expectations={"incidence": 0.50},
    ),
    ADTsecond_gener=patients.with_these_medications(
        ADTsecond_gener,
        on_or_before="index_date",
        returning="binary_flag",
        return_expectations={"incidence": 0.50},
    ),
    HCD=patients.with_high_cost_drugs(
        drug_name_matches=[
            "enzalutamide",
            "abiraterone",
            "darolutamide",
            "apalutamide"
        ],
        on_or_before="index_date",
        find_first_match_in_period=True,
        returning="binary_flag",
        return_expectations={"incidence": 0.15,},
    ),
    HCDexpanded=patients.with_high_cost_drugs(
        drug_name_matches=[
            "enzalutamide", "enzalutamide 40mg capsules",
            "enzalutamide 40mg tablets", "xtandi 40mg tablets Astellas Pharma Ltd",
            "xtandi", "xtandi 40mg capsules", "xtandi 40mg tablets",
            "abiraterone", "abiraterone 250mg tablets",
            "abiraterone 500mg tablets", "abiraterone 1g tablets",
            "zytiga", "zytiga 250mg tablets", "zytiga 500mg tablets",
            "abiraterone acetate", "abiraterone acetate 500mg",
            "abiraterone acetate 500mg tablets",
            "zytiga 500mg tablets (Janssen-Cilag Ltd)",
            "abiraterone 250mg tablets Tillomed Laboratories Ltd",
            "abiraterone 500mg tablets Accord Healthcare Ltd",
            "abiraterone 500mg tablets Alliance Healthcare (Distribution) Ltd",
            "abiraterone 500mg tablets Aristo Pharma Ltd",
            "abiraterone 500mg tablets Celix Pharma Ltd",
            "abiraterone 500mg tablets Dr Reddy's Laboratories (UK) Ltd",
            "abiraterone 500mg tablets Genus Pharmaceuticals Ltd",
            "abiraterone 500mg tablets Sandoz Ltd",
            "abiraterone 500mg tablets Teva UK Ltd",
            "abiraterone 500mg tablets Tillomed Laboratories Ltd",
            "abiraterone 500mg tablets Torrent Pharma (UK) Ltd",
            "abiraterone 500mg tablets Viatris UK Healthcare Ltd",
            "abiraterone 500mg tablets Zentiva Pharma UK Ltd",
            "zytiga 500mg tablets Janssen-Cilag Ltd",
            "abiraterone 1g tablets Sandoz Ltd",
            "abiraterone 1g tablets Viatris UK Healthcare Ltd",
            "darolutamide", "nubeqa", "darolutamide 300mg", "nubeqa 300mg",
            "apalutamide", "apalutamide 60mg tablets",
            "erleada", "erleada 60mg tablets",
            "Enzalutamide", "Enzalutamide 40mg capsules",
            "Enzalutamide 40mg tablets", "Xtandi 40mg tablets Astellas Pharma Ltd",
            "Xtandi", "Xtandi 40mg capsules", "Xtandi 40mg tablets",
            "Abiraterone", "Abiraterone 250mg tablets",
            "Abiraterone 500mg tablets", "Abiraterone 1g tablets",
            "Zytiga", "Zytiga 250mg tablets", "Zytiga 500mg tablets",
            "Abiraterone acetate", "Abiraterone acetate 500mg",
            "Abiraterone acetate 500mg tablets",
            "Zytiga 500mg tablets (Janssen-Cilag Ltd)",
            "Darolutamide", "Nubeqa", "Darolutamide 300mg", "Nubeqa 300mg",
            "Apalutamide", "Apalutamide 60mg tablets",
            "Erleada", "Erleada 60mg tablets",
        ],
        on_or_before="index_date",
        find_first_match_in_period=True,
        returning="binary_flag",
        return_expectations={"incidence": 0.15},
    ),
)
