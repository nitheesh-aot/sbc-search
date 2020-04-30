[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

# sbc-search

BC Registries and Online Services Director Search Services

## Project setup (Docker)

Development

set docker compose config

```
cp dc.dev.yml docker-compose.override.yml
cp search-web/example.env search-web/.env
cp search-api/example.env search-api/.env
docker-compose up
```
Some values for the `.env` can be taken from the DEV openshift environment, for configuring auth.

Browse to `localhost:8080`

Please take care not to commit unintended changes to `.env` files that are specific to your dev environment.

Updating database and create mock data in a dev environment:

```
docker-compose exec search_api bash
flask db upgrade
python bootstrap.py
```

## connecting to the dev database

Connect to VPN

Download [cisco VPN client](https://software.cisco.com/download/home/286281283/type/282364313/release/4.7.04056?i=!pp)

```
cd /opt
tar zxvf anyconnect-linux64-4700136-predeploy-k9tar.gz
cd anyconnect*
./vpn_install.sh
vpn
>> connect vpn2.gov.bc.ca
```

(enter your IDIR username and password)

Install `ncat` to enable port-forwarding. (Note: depending on your version of `nmap` you may need to install both `nmap` and `ncat`, or just `nmap`.)

```
apt-get install nmap ncat
ncat -l 0.0.0.0 1521 --keep-open --sh-exec "ncat nettle.bcgov 1521"
```

set your search-api/.env database URL to `DB_CONNECTION_URL=oracle://$USERNAME:$PASSWORD@$DOCKER_IP:1521/CDEV`

WHERE $USERNAME and $PASSWORD are read only dev db creds, and \$DOCKER_IP is findable from running `ip addr show` in your search_api container, and changing the last digit to 1. It's a refrence to your HOST's IP from inside your container, typically such as 172.1.0.1 .

## Migrations

This project uses

- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/)
- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/), based on alembic.

These operations are done in the search_api container

To initially get your DB up to date:

```
flask db upgrade
```

To create new migration scripts

```
flask db migrate
git add
```

### DB Environments

Oracle - required for the 'similar' type search. Used in production. Has some performance challenges.
Postgres - used for local development with a small fake DB, generated by bootstrap.py
Sqlite - used for testing

### Benchmarking

With an oracle connection configured in `search-api/.env` 
