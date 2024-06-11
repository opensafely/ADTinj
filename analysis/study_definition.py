from cohortextractor import (
    StudyDefinition,
    Measure,
    patients,
)

from codelists import *

start_date = "2015-01-01"
end_date = "2024-05-01"

study = StudyDefinition(
    default_expectations={
        "date": {"earliest": "2015-01-01", "latest": "today"},
        "rate": "uniform",
        "incidence": 0.5,
    },
    index_date="2024-05-01",
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
            "2024-05-01",
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
    ADTinj1=patients.with_these_medications(
        ADTinj1,
        on_or_before="index_date",
        returning="binary_flag",
        return_expectations={"incidence": 0.50},
    ),
    ADTinj3=patients.with_these_medications(
        ADTinj3,
        on_or_before="index_date",
        returning="binary_flag",
        return_expectations={"incidence": 0.50},
    ),
    ADTinj6=patients.with_these_medications(
        ADTinj6,
        on_or_before="index_date",
        returning="binary_flag",
        return_expectations={"incidence": 0.50},
    ),
)
