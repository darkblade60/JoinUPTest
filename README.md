# JoinUPTest


## ENV VARS
      #IF YOU WANT THE ACTIVATION PROCESS
      export ACTIVATION_PROCESS=True

      #EMAIL CONFIG
      export EMAIL_HOST=
      export EMAIL_USE_TLS=
      export EMAIL_PORT=
      export EMAIL_HOST_USER=j
      export EMAIL_HOST_PASSWORD=

      #SMS CONFIG
      export TWILIO_ACCOUNT_SID=
      export TWILIO_AUTH_TOKEN=
      export TWILIO_NUMBER=

      #REDIS SERVER
      export CELERY_BROKER_URL=
      export CELERY_RESULT_BACKEND=


## Configuration

    - Initialize redis server : redis-server
    - Initialize celery-worker : python -m celery -A djangoProject worker -l info
    - Initialize django app and enjoy



## Testing

    - run python manage.py test

    ** Test also displays number of db connections for each endpoint

## API Endpoints

api/v1/signup

```text 
curl --request POST \
  --url http://127.0.0.1:8000/api/v1/signup \
  --header 'Content-Type: application/json' \
  --data '{
            "email": "test@gmail.com",
            "password": "123456789_",
            "password2": "123456789_",
            "first_name": "Test",
            "last_name": "Test",
            "phone_number": "+34123123123",
            "hobbies_description": "Dancing"
}'
```


api/v1/login

```text
curl --request POST \
  --url http://127.0.0.1:8000/api/v1/login \
  --header 'Content-Type: application/json' \
  --data '{
	"username": 
		"test@gmail.com",
	"password": 
		"123456789_"
}'
```


api/v1/profile

```text
curl --request GET \
  --url http://127.0.0.1:8000/api/v1/profile \
  --header 'Authorization: Token 9c3e681c8223543be04a9969b6345f7ed62a845a' \
  --header 'Content-Type: application/json'
```


api/v1/activation/{code}

```text
curl --request GET \
  --url http://127.0.0.1:8000/api/v1/activation/ed5080bd-d349-4a10-a730-73bc5034edc3 \
  --header 'Content-Type: application/json'
```






