from pathlib import Path
import os

from dagster import asset, AssetExecutionContext
from dagster_dbt import dbt_assets, get_asset_key_for_source, DbtCliResource


from ..resources import dbt_resource
from ..constants import DBT_DIRECTORY


dbt_resource.cli(["--quiet", "parse"], target_path=Path("target")).wait()

if os.getenv("DAGSTER_DBT_PARSE_PROJECT_ON_LOAD"):
    dbt_manifest_path = (
        dbt_resource.cli(["--quiet", "parse"]).wait()
        .target_path.joinpath("manifest.json")
    )
else:
    dbt_manifest_path = os.path.join(DBT_DIRECTORY, "target", "manifest.json")


@dbt_assets(manifest=dbt_manifest_path)
def dbt_my_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()