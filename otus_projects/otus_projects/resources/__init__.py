# from dagster_duckdb import DuckDBResource
# from dagster import EnvVar
# import boto3
import os
from ..constants import DBT_DIRECTORY
from dagster_dbt import DbtCliResource


# the import lines go at the top of the file

dbt_resource = DbtCliResource(
    project_dir=DBT_DIRECTORY,
)