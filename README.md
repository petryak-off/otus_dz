# Data Warehouse Analyst

## Общая информация
Аналитика показателей продаж OZON на базе современного стека инструментов - airbyte, postgres, dagster, dbt, superset.

## Цели
1. Декларативный подход к организации обработки данных
2. Орекстрация данных ELT через одно «окно».
3. Визализация и аналитика показателей в Apache Superset.

## Планы
1. Развернуть сервисы в YC
2. Настроить коннекторы для выгрузки и загрузки данных.
3. Провести трансформацию данных для BI
4. «Уложить» все в оркестратор dagster
5. Визуализировать в BI

## Используемые технологии
* ГуглДрайв - источник данных
* Airbyte - сервис для выгрузки и загрузки сырых данных.
* PostgreSQL – хранилище данных (DWH).
* Dagster – оркестратор.
* DBT - трансформация данных.
* Superset - визуацлизация данных.

## Что получилось

1. Исходный набор данных “Продажи OZON 2020” размещен на [гугл диске](https://drive.google.com/drive/folders/1VJrJ2PKcXxKt-k4zoJfO5_qFrkNWDM0y?ths=true)

2. Архитектура проекта
   
![image](https://github.com/petryak-off/otus_dz/blob/main/image-1.jpg)

3. Развертывание инфраструктуры

* БД Postgres развернут через маркетплейс Yandex Cloud.
* ВМ airbyte-dagster-dbt-node для airbyte, dagster, dbt. Где airbyte развернут при помощи docker, dagster - локально, dbt - локально в корень папки дагстера для удосбтва подключения моделей к оркестратору. 
* ВМ superset-node для BI Superset - развернут при помощи docker.

Инструкция по развертыванию представлена вконце раздела.

4. Airbyte - http://158.160.121.23:8000

* Источник данных для проекты был выбран ГуглДрайв, т.к. часто приходится работать с ручными выгрузками в формате csv, а ГуглДрайв самый быстрый и простой способ размещения информации, а забор данных с Airbyte становится очень простым.


![image](https://github.com/petryak-off/otus_dz/blob/main/image-2.jpg)

5. Dagster - http://158.160.121.23:3000

* Удобный инструемент для оркестрации всего в одном месте и визуализации.
* Конфиг Для того чтобы связать airbyte/dbt - dagster:

```py
import os
from pathlib import Path
from dagster_dbt import DbtCliResource
DBT_DIRECTORY = Path(__file__).joinpath("..", "..", "dbt_projects/otus").resolve()
DBT_PROJECT_DIR = 'home/yc-user/otus_projects/dbt_projects/otus'
DBT_PROFILES_DIR =  'home/yc-user/otus_projects/dbt_projects/otus'
DBT_CONFIG = {"project_dir": DBT_PROJECT_DIR, "profiles_dir": DBT_PROFILES_DIR}
#Airbyte configs
AIRBYTE_CONNECTION_ID = os.environ.get("AIRBYTE_CONNECTION_ID", "e6b2e408-2654-4f54-beec-dd4d56aeec01")
AIRBYTE_CONFIG = {
    "host": os.environ.get("AIRBYTE_HOST", "158.160.121.23"),
    "port": os.environ.get("AIRBYTE_PORT", "8000"),
    "username": "airbyte",
    "password": "password",
    #"password": {"env":"AIRBYTE_PASSWORD"},
}
```
![image](https://github.com/petryak-off/otus_dz/blob/main/image-3.1.png)


6.  DBT - http://158.160.121.23:5000

* Повзоляет быстро вносить изменения, генерировать документацию по проекту. Скорощает написание повторяющегося кода за счет джтнжи и макросов.

![image](https://github.com/petryak-off/otus_dz/blob/main/image-4.png)

7. Airbyte - http://158.160.104.146:8080

![image](https://github.com/petryak-off/otus_dz/blob/main/image-5.png)


# Выводы и планы по развитию
1. Построенный стек позволяет построить пайпланы загрузки и обработки данных за короткий срок без использования кода. Airbyte хорош, особенно когда есть опыт создания собственных коннекторов. Подходит для любых задач. Есть многое из «коробки».
2. Dagster может контролировать все. На нашем примере мы можем оркестровать задачи ayrbite и dbt, следить за ходом отработки пайплайнов на графах. Смотреть код, и статистическую информацию. 
3. Порог вхождения в DBT высок, но как только встаешь на «рельсы» инструмент кажется незаменимым. Легко вносить изменения в проект и быстро их применять к модели данных.
4. Superset в связке с dbt кажется вполне рабочим инструментом, за счет того, что можно подать на вход готовые витрины под каждый чарт.
5. В планах:
* Подключить к стеку данных CH для обработки больших объёмов данных. Postgres использовать как промежуточную БД.
* Минимизировать количество операций по развертыванию инфраструктуры. Dagster и dbt развернуть через docker. 
* Внедрить DataVault средствами dbt 
________________________________________________________________________________________________

# Развертывание ВМ airbyte-dagster-dbt-node:

Пусть к ssh-key указываем свой.
```bash
    yc compute instance create \
    --name airbytedagsterdbt-node \
    --ssh-key ~/.ssh/id_ed25519.pub \
    --create-boot-disk image-folder-id=standard-images,image-family=ubuntu-2004-lts,size=100,auto-delete=true \
    --network-interface subnet-name=default-ru-central1-a,nat-ip-version=ipv4 \
    --memory 16G \
    --cores 4 \
    --zone ru-central1-a \
    --hostname airbyte-dagster-dbt-node
```
Обновляем компоненты yc
```bash
yc components update
```
Подключаемся к ВМ через ssh
```bash
ssh yc-user@xx.xx.xx.xx
```
Устанавливаем докер
```bash
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
```
Добавдяем в репозиторий Apt источники:
```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
Проверка установки докера.
```bash
sudo docker ps
```
# Устанавливаем Airbyte
```bash
git clone --depth=1 https://github.com/airbytehq/airbyte.git
```
Запускаем Airbyte
```bash
cd airbyte
sudo ./run-ab-platform.sh
```
После развертывания Airbyte на своих серверах обязательно измените логин и пароль на свои в .env файле:
```bash
BASIC_AUTH_USERNAME=your_new_username_here
BASIC_AUTH_PASSWORD=your_new_password_here
```

# Установка dagster и dbt
dbt размещаем локально в корень паки с дагстером. Создаем виртуальную среду:

```bash
sudo apt update
sudo apt install python3.11-venv
python3.11 -m venv dbt-env
source venv/bin/activate
alias env_dbt='source venv/bin/activate'
```
Устанавливаем все библиотеки из requirements.txt. Некоторые библиотеки не устанавливаются из-за несовместимости с версией питона, их ставим вручную или пропускаем.
```bash
python3.11 -m pip install -r /path/to/requirements.txt
```
Создаем проект дагстера.
```bash
dagster project scaffold --name otus_projects
```
Создаем проект dbt.
```bash
cd cd /home/yc-user/otus_projects/dbt_projects
dbt init
dbt debug
```
Настраиваем airbyte-dagster-dbt-postgres
Готово!

# Развертывание BI Superset'а:
```bash
yc compute instance create \
    --name superset-node \
    --ssh-key ~/.ssh/id_ed25519.pub \
    --create-boot-disk image-folder-id=standard-images,image-family=ubuntu-2004-lts,size=100,auto-delete=true \
    --network-interface subnet-name=default-ru-central1-a,nat-ip-version=ipv4 \
    --memory 16G \
    --cores 4 \
    --zone ru-central1-a \
    --hostname superset-node
```
Обновляем компоненты yc
```bash
yc components update
```
Подключаемся к ВМ через ssh
ssh yc-user@xx.xx.xx.xx

#Устанавливаем докер
```bash
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
```
Add the repository to Apt sources:
```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
Проверка установки докера.
```bash
sudo docker ps
```
Генерируем ключ
```bash
openssl rand -base64 42
```
Запускаем
```bash
sudo docker run -d -p 8080:8088 -e "SUPERSET_SECRET_KEY=your_secret_key_here" --name superset apache/superset
```
Проверка
```bash
sudo docker ps
```
Добавляем админа:
```bash
sudo docker exec -it superset superset fab create-admin \
          --username admin \
          --firstname Superset \
          --lastname Admin \
          --email admin@superset.com \
          --password admin
```
Инициализируем БД
```bash
sudo docker exec -it superset superset db upgrade
```
Загрузка примеров
```bash
sudo docker exec -it superset superset load_examples
```
Инициализируем суперсет
```bash
sudo docker exec -it superset superset init
```
Готово!