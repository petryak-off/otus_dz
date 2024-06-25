from dagster import job, AssetSelection, define_asset_job, AssetKey
from dagster_dbt import dbt_compile_op, dbt_docs_generate_op, dbt_cli_resource, build_dbt_asset_selection
from ..assets.all_dbt_assets import dbt_my_assets
#import os
#from dagster_dbt import DbtCliResource
#from ..constants import dbt_project_dir

DBT_PROFILES = "/home/yc-user/otus_projects/dbt_projects/otus"
DBT_PROJECT = "/home/yc-user/otus_projects/dbt_projects/otus"



@job(resource_defs={"dbt":dbt_cli_resource.configured({"project-dir": DBT_PROJECT, "profiles-dir": DBT_PROFILES})})
def my_dbt_cli_job():
    dbt_compile_op()

@job(resource_defs={"dbt": dbt_cli_resource.configured({"project-dir": DBT_PROJECT, "profiles-dir": DBT_PROFILES})})
def docs_generate_job():
    dbt_docs_generate_op()

dbt_asset_job = define_asset_job(name="materialize_dbt_models", 
    selection=AssetSelection.all(),
    )