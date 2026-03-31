# OpenBackup Federation

OpenBackup Federation is an open-source, decentralised backup system designed for federated infrastructure environments.

## Features

- Federated backup nodes
- End-to-end encryption
- Incremental backups
- Multi-node replication
- S3-compatible storage

## Architecture

- Federation Layer (DHT + protocol)
- Backup Engine (chunking + versioning)
- Storage Layer (MinIO / IPFS)
- Security Layer (AES-256 + keys)

## Quick Start

```bash
git clone https://github.com/openict/openbackup-federation
cd openbackup-federation
docker-compose up
