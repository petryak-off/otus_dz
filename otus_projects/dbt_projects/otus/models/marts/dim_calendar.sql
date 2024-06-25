{{
    config(
        materializws = 'table',
        dist="all",
        sort = 'date_day'
    )
}}

{{ config(
    schema='dim'
) }}

{{ dbt_date.get_date_dimension('2020-01-01', '2025-12-31')}}