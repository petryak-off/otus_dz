-----
dagster

cd /home/yc-user
#activate virtual dagster-env
source venv/bin/activate
cd /home/yc-user/otus_projects
bash /home/yc-user/otus_projects/daster_run.sh
ps -la

-----
apache/superset

sudo docker run apache/superset

sudo docker run -d -p 8080:8088  apache/superset