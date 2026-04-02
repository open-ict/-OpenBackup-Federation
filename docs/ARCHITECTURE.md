# Architecture

## Components

- Agent: uploads backup files to API
- API: handles auth, metadata, node registry, and federation health checks
- PostgreSQL: stores users, backups, and nodes
- MinIO: stores backup objects
- Dashboard: lightweight operator UI

## Federation model

This MVP uses a simple node registry and remote health checks as a first federation layer.
A production version should add:

- signed node trust exchange
- remote catalog discovery
- cross-node restore workflows
- encryption key separation
- replication policy engine
