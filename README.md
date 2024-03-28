# DB_Performance

https://hub.docker.com/u/dangquytaikb



## What is going on

This is a project for students. Students are cooperating on this project under supervision of teacher.
It is also a model of an information systems which could be used for some administrative task in university life.

## Used technologies

- Python (see https://www.python.org/)
    - SQLAlchemy for modelling the database entitied (async queries) (see https://www.sqlalchemy.org/)
    - FastAPI for API definition and run (see https://fastapi.tiangolo.com/)
    - Uvicorn as executor of FastAPI (see https://www.uvicorn.org/)
    - Strawberry for GraphQL endpoint (federated GraphQL) (see https://strawberry.rocks/)
    - Appolo federation for GraphQL federation queries (see https://www.apollographql.com/docs/federation/)

- Javascript (see https://developer.mozilla.org/en-US/docs/Web/JavaScript)
    - ReactJS as a library for building bricks of user interface (see https://react.dev/)
    - fetch for fetching the data from endpoints

- Docker (see https://www.docker.com/)
    - containerization of applications
    - inner connection of containers
    - deployment of service stacks (see https://docs.docker.com/compose/)

- Postgres (see https://www.postgresql.org/)
    - and its compatible replacements (Yugabyte - https://www.yugabyte.com/, Cockroach - https://www.cockroachlabs.com/)
    - can be also used, with small refactoring (thanks to SQLalchemy), different SQL engine such MSSQL, MariaDB, etc.

## Base concept

The project has several docker containers
- `apollo` master of federation
- `frontend` provides static files = REACT compiled items (including GQL interface)
- `gql_*` apollo federation member
- `prostgres` is database server
- `pgadmin` is an interface for database server administration (see https://www.pgadmin.org/)