# DB_Performance

## 1. Introduction

## 2. File Structure

- docker-compose-gql.yaml : docker-compose file for GraphQL
- docker-compose-dbms.yaml : docker-compose file for DBMS

## 3. Run

docker compose -f "docker-compose-gql.yaml" up -d --build
docker compose -f "docker-compose-dbms.yaml" up -d --build
