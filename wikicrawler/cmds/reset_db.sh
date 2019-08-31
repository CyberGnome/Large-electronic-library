#!/usr/bin/env bash

PGPASSWORD=postgres psql -h 127.0.0.1 -p 5432 -U postgres -c "DROP DATABASE l_e_l;"
PGPASSWORD=postgres psql -h 127.0.0.1 -p 5432 -U postgres -c "CREATE DATABASE l_e_l;"
PGPASSWORD=postgres psql -h 127.0.0.1 -p 5432 -U postgres -c "GRANT ALL ON DATABASE l_e_l TO wikicrawler;"
