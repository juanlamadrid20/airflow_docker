# airflow_docker

### To use this code:

**1. Clone**
```bash
git clone https://github.com/shaikhyasar/airflow_docker
```

**2. Create Virtual Environment**
```bash
cd airflow_docker
python3.6 -m venv venv
```

**3. Activate virtual environment and install requirements**
Mac/Linux
```
source venv/bin/activate
```

Windows:
```
. venv\Scripts\activate
```

```
pip install -r requirements.txt
```

> If using **pipenv**, run `pipenv shell` && `pipenv install`

Note: There is a demo airflow code inside dags folder, feel free to delete it and create your own

**Run docker compose**
```
docker compose up
```
**Login Credentials for Airflow**
```
admin:admin
```