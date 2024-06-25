from dagster import ScheduleDefinition
from ..jobs import dbt_asset_job

dbt_schedules = ScheduleDefinition(
    job=dbt_asset_job,
    cron_schedule="15 9 * * *",  # Расписание
    execution_timezone="Europe/Moscow"
)