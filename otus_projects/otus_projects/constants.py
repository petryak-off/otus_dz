import os
from pathlib import Path

from dagster_dbt import DbtCliResource
#from dagster. utils import file_relative_path

#dbt_project_dir = Path(file).joinpath("..", "..", "..", "..", "GitLab-Runner\\builds\\7jMF9y1w\\0\\Vladimir.Petryakov\\dbt\\dbt_projects").resolve()
#dbt = DbtCliResource(project_dir=os.fspath(dbt_project_dir))

DBT_DIRECTORY = Path(__file__).joinpath("..", "..", "dbt_projects/otus").resolve()

# If DAGSTER_DBT_PARSE_PROJECT_ON_LOAD is set, a manifest will be created at run time.
# Otherwise, we expect a manifest to be present in the project's target directory.

# if os.getenv("DAGSTER_DBT_PARSE_PROJECT_ON_LOAD"):
#     dbt_parse_invocation = dbt.cli(["parse"]).wait()
#     dbt_manifest_path = dbt_parse_invocation.target_path.joinpath("manifest.json")
# else:
#     dbt_manifest_path = dbt_project_dir.joinpath("target", "manifest.json")

DBT_PROJECT_DIR = 'home/yc-user/otus_projects/dbt_projects/otus'
DBT_PROFILES_DIR =  'home/yc-user/otus_projects/dbt_projects/otus'
DBT_CONFIG = {"project_dir": DBT_PROJECT_DIR, "profiles_dir": DBT_PROFILES_DIR}


#Airbyte configs
AIRBYTE_CONNECTION_ID = os.environ.get("AIRBYTE_CONNECTION_ID", "e6b2e408-2654-4f54-beec-dd4d56aeec01")

AIRBYTE_CONFIG = {
    "host": os.environ.get("AIRBYTE_HOST", "84.201.133.79"),
    "port": os.environ.get("AIRBYTE_PORT", "8000"),
    "username": "airbyte",
    "password": "password",
    #"password": {"env":"AIRBYTE_PASSWORD"},
}