
{{ config(
    schema='ads'
) }}

select t."Name" , count(t."Name")
from {{ source('analytics', 'ozon_sales')}} t
group by 1
order by 2 desc
limit 1
