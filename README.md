https://wagtail.io/blog/getting-started-with-wagtail-and-graphql/
https://wagtail.io/blog/graphql-with-streamfield/#
https://cloud.google.com/python/django/appengine
https://cloud.google.com/sql/docs/mysql/quickstart-connect-run

## Development

#### Install virtualenv
https://virtualenv.pypa.io/en/latest/installation/

#### Create virtualenv
```bash
python3 -m virtualenv -p python3 venv
```

#### Activate virtualenv
```bash
source venv/Scripts/activate
```

#### Install requirements
```bash
pip install -r requirements.txt
```

### Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### Create an admin user
```bash
python manage.py createsuperuser
```

### Create proxy to connect google cloud sql
```bash
./cloud_sql_proxy -instances="liu-onecampus-dev:us-central1:cms"=tcp:3306
```

#### Run
```bash
python manage.py runserver 0.0.0.0:8080 --settings=cms.settings.<dev|production>
```


## Run on Docker (locally)

#### Install Docker
https://docs.docker.com/docker-for-windows/

#### Build image

```bash
docker image build -t cms .
```

#### Run container

```bash
docker container run --rm --publish=8080:8080 --name=cms cms
```

#### Stop container

```bash
docker container stop cms
```

#### Delete container

```bash
docker container rm cms
```

#### Delete image

```bash
docker image rm cms
```


## Run on Google Cloud Run

#### Install gcloud
https://cloud.google.com/sdk/docs/downloads-interactive

#### Build container image

```bash
gcloud builds submit --tag=gcr.io/liu-onecampus-dev/cms --project=liu-onecampus-dev
```

#### Deploy container image

```bash
gcloud run deploy cms --image=gcr.io/liu-onecampus-dev/cms --platform=managed --region=us-central1 --revision-suffix=v1 --allow-unauthenticated --set-cloudsql-instances liu-onecampus-dev:us-central1:cms --project=liu-onecampus-dev
```