# Clairvoyance

[Used this template as a base.](https://github.com/progressify/django-inertia-svelte-template-starter)

Backend: Django
Routing: Inertia.js
Frontend: Svelte

## Installation and usage

- Clone and cd into the project
- Create a Python virtual environment

```shell
python3 -m venv env
```

- Activate the virtual environment

```shell
source env/bin/activate
```

- Install the Python requirements

```shell
python3 -m pip install -r requirements.txt
```

- Create a Django secret key

```shell
echo "SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')" >> .env
```

- Apply the migrations

```shell
python3 manage.py migrate
```

- Install the NPM dependencies

```shell
npm install
```

- Run the Python server

```shell
python manage.py runserver
```

- Open another terminal window and run the Vite server

```shell
npm run dev

Now open your browser and go to: `http://localhost:8000/`
