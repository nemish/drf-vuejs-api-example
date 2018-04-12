# Test API project

Using [django-rest-framework](http://www.django-rest-framework.org/) for robust API and [vuejs](https://vuejs.org/) as cool frontend.

Python 3.6.5

Node 8.1.3

## Installation backend

```shell
$ virtualenv -p python3 test
$ source ./test/bin/activate
$ git clone https://github.com/nemish/drf-vuejs-api-example.git testapi
$ cd testapi
$ add2virtualenv .
$ pip install -r requirements
$ python manage.py migrate
$ python manage.py test
$ python manage.py create_test_data # to create some fixtures
$ python manage.py runserver 0.0.0.0:8001
```

## Installation frontend

In a new terminal tab:
```shell
$ cd testapi/client
$ yarn install
$ yarn start
```

Open your browser and navigate to 127.0.0.1:8080 and try to login with credentials test_user_1:123