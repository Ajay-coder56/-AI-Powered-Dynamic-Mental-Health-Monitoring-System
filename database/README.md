# Database Configuration

This directory contains the database initialization and seeding scripts for the MindSafe PostgreSQL instance.

## Structure
- `migrations/`: Contains the DDL (schema) definitions. `001_initial_schema.sql` is automatically executed on the first start of the Docker container.
- `seeds/`: Contains mock/demo data SQL. `001_demo_data.sql` is automatically executed after the schema on the first start.

## Auto-Initialization
When you run `docker compose up -d` for the first time, PostgreSQL executes all `.sql` files mapped into `/docker-entrypoint-initdb.d/` in alphabetical order.

To force a reset of the database, you can run:
```bash
docker compose down -v
docker compose up -d
```
**(Warning: this deletes all data!)**
