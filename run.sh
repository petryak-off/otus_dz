-----
# dagster

cd /home/yc-user
source venv/bin/activate
cd /home/yc-user/otus_projects
bash /home/yc-user/otus_projects/daster_run.sh

# dbt

cd /home/yc-user/otus_projects/dbt_projects/otus
dbt docs serve --port 5000

# airbyte
cd /home/yc-user/airbyte
sudo ./run-ab-platform.sh 
Авторизация = airbyte / password

-----
apache/superset

sudo docker start superset 
Авторизация = admin / admin