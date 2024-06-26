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
# dbt размещаем локально в корень паки с дагстером. Создаем виртуальную среду:

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


# Схема потоков данных
![image](https://github.com/savadevel/OpenDataByModernStack/assets/69199994/e0fc8ae7-aac6-4934-bcfc-e96fd1f5c40e)

# Выводы и планы по развитию
1. Выбранный стек позволят построить пайплайн загрузки данных
2. Cosmos позволяет связать AirFlow c dbt, а это дает сделать оркестрация функционала dbt из "коробки", как, например, создание моделей данных, тестирование и инкрементальную загрузку протестированных данных 
3. Дальнейшие планы по развитию:
* вынести в настройку задание наборов загружаемых открытых данных 
* минимизировать количество операций по настройки созданных контейнеров (запустил "docker compose up" и перешел к анализу данных в Superset) 
* создание инфраструктуры сделать через Terraform 
* использовать облачные ресурсы
* выстроить зависимость дагов загрузки данных
* документирование проекта 
