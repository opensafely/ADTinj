from cohortextractor import (
    StudyDefinition,
    Measure,
    patients,
)

from codelists import *

start_date = "2015-01-01"
end_date = "2022-12-01"

study = StudyDefinition(
    default_expectations={
        "date": {"earliest": "2015-01-01", "latest": "today"},
        "rate": "uniform",
        "incidence": 0.5,
        },
    index_date="2015-01-01", # for measures
    population=patients.satisfying(
        """
        registered
        AND NOT has_died
        AND prostate_ca
        AND (sex="M")
        AND (age >=18 AND age <= 120)
        """
    ),
    registered=patients.registered_as_of(
        "index_date",
        return_expectations={"incidence":0.95}
    ),
    has_died=patients.died_from_any_cause(
        on_or_before="index_date",
        returning="binary_flag",
    ),
    prostate_ca=patients.with_these_clinical_events(
        prostate_cancer_codes,
        on_or_before="last_day_of_month(index_date)",
        find_first_match_in_period=True,
        include_date_of_match=True,
        include_month=True,
        include_day=True,
        returning="binary_flag",
        return_expectations={
            "date": {"earliest": "1950-01-01", "latest": "today"},
            "incidence": 1.0
        }
    ),
    # demographics
    age=patients.age_as_of(
        "index_date",
        return_expectations={
            "rate": "exponential_increase",
            "int": {"distribution": "population_ages"},
        },
    ),
    age_group=patients.categorised_as(
        {
            "Missing": "DEFAULT",
            "<65": """ age < 65""",
            "65-74": """ age >= 65 AND age < 75""",
            "75-84": """ age >= 75 AND age < 85""",
            "85+": """ age >= 85""",
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
            "category": {"ratios": {"M": 0.49, "F": 0.51}},
        }
    ),
    region=patients.registered_practice_as_of(
        "index_date",
        returning="nuts1_region_name",
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "North East": 0.1,
                    "North West": 0.1,
                    "Yorkshire and the Humber": 0.2,
                    "East Midlands": 0.1,
                    "West Midlands": 0.1,
                    "East of England": 0.1,
                    "London": 0.1,
                    "South East": 0.2,
                },
            },
        },
    ),
    imd_cat=patients.categorised_as(
        {
            "Missing": "DEFAULT",
            "IMD_1": """index_of_multiple_deprivation >=1 AND index_of_multiple_deprivation < 32844*1/5""",
            "IMD_2": """index_of_multiple_deprivation >= 32844*1/5 AND index_of_multiple_deprivation < 32844*2/5""",
            "IMD_3": """index_of_multiple_deprivation >= 32844*2/5 AND index_of_multiple_deprivation < 32844*3/5""",
            "IMD_4": """index_of_multiple_deprivation >= 32844*3/5 AND index_of_multiple_deprivation < 32844*4/5""",
            "IMD_5": """index_of_multiple_deprivation >= 32844*4/5 AND index_of_multiple_deprivation < 32844""",
        },
        index_of_multiple_deprivation=patients.address_as_of(
            "index_date",
            returning="index_of_multiple_deprivation",
            round_to_nearest=100,
        ),
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "Missing": 0.05,
                    "IMD_1": 0.19,
                    "IMD_2": 0.19,
                    "IMD_3": 0.19,
                    "IMD_4": 0.19,
                    "IMD_5": 0.19,
                }
            },
        },
    ),
######### injectables
    ADTinj=patients.with_these_medications(
        ADTinj,
        between=[
            "first_day_of_month(index_date)",
            "last_day_of_month(index_date)",
            ],
        returning="binary_flag",
        return_expectations={"incidence": 0.50},
    ),
    ADTinj1=patients.with_these_medications(
        ADTinj1,
        between=[
            "first_day_of_month(index_date)",
            "last_day_of_month(index_date)",
            ],
        returning="binary_flag",
        return_expectations={"incidence": 0.50},
    ),
    ADTinj3=patients.with_these_medications(
        ADTinj3,
        between=[
            "first_day_of_month(index_date)",
            "last_day_of_month(index_date)",
            ],
        returning="binary_flag",
        return_expectations={"incidence": 0.50},
    ),
    ADTinj6=patients.with_these_medications(
        ADTinj6,
        between=[
            "first_day_of_month(index_date)",
            "last_day_of_month(index_date)",
            ],
        returning="binary_flag",
        return_expectations={"incidence": 0.50},
    ),
######### oral treatment
    ADToral=patients.with_these_medications(
        ADToral,
        between=[
            "first_day_of_month(index_date)",
            "last_day_of_month(index_date)",
            ],
        returning="binary_flag",
        return_expectations={"incidence": 0.50},
    ),
    ADTsecond_gener=patients.with_these_medications(
        ADTsecond_gener,
        on_or_before="index_date",
        returning="binary_flag",
        return_expectations={"incidence": 0.50},
    ),
)

measures = [
    Measure(
        id="ADT_inj_rate",
        numerator="ADTinj",
        denominator="population",
        group_by="population",
        small_number_suppression=True,
    ),
    Measure(
        id="ADT_inj1_rate",
        numerator="ADTinj1",
        denominator="population",
        group_by="population",
        small_number_suppression=True,
    ),
    Measure(
        id="ADT_inj3_rate",
        numerator="ADTinj3",
        denominator="population",
        group_by="population",
        small_number_suppression=True,
    ),
    Measure(
        id="ADT_inj6_rate",
        numerator="ADTinj6",
        denominator="population",
        group_by="population",
        small_number_suppression=True,
    ),
    Measure(
        id="ADTinjbyRegion_rate",
        numerator="ADTinj",
        denominator="population",
        group_by="region",
        small_number_suppression=True,
    ),
    Measure(
        id="ADTinjbyIMD_rate",
        numerator="ADTinj",
        denominator="population",
        group_by="imd_cat",
        small_number_suppression=True,
    ),
    Measure(
        id="ADTinjbyEthnicity_rate",
        numerator="ADTinj",
        denominator="population",
        group_by="ethnicity",
        small_number_suppression=True,
    ),
    Measure(
        id="ADTinjbyAge_rate",
        numerator="ADTinj",
        denominator="population",
        group_by="age_group",
        small_number_suppression=True,
    ),
    Measure(
        id="ADT_oral_rate",
        numerator="ADToral",
        denominator="population",
        group_by="population",
        small_number_suppression=True,
    ),
    Measure(
        id="ADToralbyRegion_rate",
        numerator="ADToral",
        denominator="population",
        group_by="region",
        small_number_suppression=True,
    ),
    Measure(
        id="ADToralbyIMD_rate",
        numerator="ADToral",
        denominator="population",
        group_by="imd_cat",
        small_number_suppression=True,
    ),
    Measure(
        id="ADToralbyEthnicity_rate",
        numerator="ADToral",
        denominator="population",
        group_by="ethnicity",
        small_number_suppression=True,
    ),
    Measure(
        id="ADToralbyAge_rate",
        numerator="ADToral",
        denominator="population",
        group_by="age_group",
        small_number_suppression=True,
    ),
    Measure(
        id="ADTsecongen_rate",
        numerator="ADTsecond_gener",
        denominator="population",
        group_by="population",
        small_number_suppression=True,
    ),
]
