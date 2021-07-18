# A test project to join Plink

## Installation & Configuration


**1. Clone the repository**  
```bash
git clone https://github.com/iterlace/plink_test.git
cd plink_test
```

**2. Create and configure .env file from a template**
```bash
cp .env.base .env
vim .env
```

**3. Build a docker image**
```bash
docker-compose build backend
```

**4. Ensure everything works properly**
```bash
docker-compose run backend scripts/test.sh
```

**5. Run migrations**
```bash
docker-compose run backend python manage.py migrate
```

**6. Run the application**
```bash
docker-compose up backend
```


## .env configuration

**DEBUG (default: 0)**  
Whether to enable debug mode.
In the debug mode, the application uses standard Django runner and logs additional information.  
When DEBUG=0, gunicorn is used.

**TEST (default: 0)**

--

**DB_PATH**  
If running the docker compose service, DB_PATH is set automatically, and maps to a mounted docker volume.  
Otherwise, it must represent a path to the .sqlite3 DB.


**DOCKER_IMAGE**  
Docker image name

**DOCKER_TAG**  
Docker tag name
