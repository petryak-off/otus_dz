"""Definitions that provide Dagster code locations."""

import os
from dagster import Definitions, AssetSelection, define_asset_job, load_assets_from_package_module, repository, with_resources, asset, ScheduleDefinition, AssetKey
from dagster_dbt import load_assets_from_dbt_project, dbt_cli_resource, DbtCliResource, DagsterDbtTranslator

from .assets.all_dbt_assets import dbt_my_assets
from .assets.airbyte_ozon_csv import airbyte_assets
from .jobs import docs_generate_job, my_dbt_cli_job, dbt_asset_job
from .schedules import dbt_schedules
#from .sensors import *
#from .constants import dbt_project_dir
from .resources import dbt_resource


all_jobs = [docs_generate_job, my_dbt_cli_job , dbt_asset_job]
all_schedules = [dbt_schedules]
#all_sensors = []


defs = Definitions(
    #assets = [dbt_my_assets],
    assets = [dbt_my_assets, airbyte_assets],
    resources= {
                #"dbt": dbt_cli_resource.configured({"project-dir": DBT_PROJECT_DIR, "profiles-dir": DBT_PROFILES_DIR})
                "dbt": dbt_resource
    },
    jobs = all_jobs,
    schedules = all_schedules,
    #sensors = all_sensors,
)