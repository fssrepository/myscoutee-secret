# MyScoutee secrets

This repository is the **versioned home for secret-management configuration and
operating instructions**. It is not a place to commit passwords, tokens, private
keys, unseal material, or exported vault data. The only supplied implementation
here is a disposable OpenBao development sandbox with synthetic data. It is not
a production secret manager.

## See it work

Docker Compose, Python 3, and curl are required. From this repository:

```sh
./scripts/lab.sh start
./scripts/lab.sh smoke
```

Open <http://127.0.0.1:8200/ui/>. Select **Token** login and obtain the local
sandbox token with `./scripts/lab.sh token`. In **Secrets > secret > demo >
sample**, the smoke test has written `example = sandbox-only-value`. You can
create and edit additional **synthetic** values in the UI. `./scripts/lab.sh
status` shows the container; `./scripts/lab.sh stop` stops it and discards its
in-memory data. The container never starts automatically and binds only to
localhost. Do not enter a real credential: development mode has no durable
storage or TLS.

The detailed rollout analysis is in [guides/development/secrets](guides/development/secrets/README.md).
The branded English PDF is in [guides/publication/manuals](guides/publication/manuals/README.md).

## What exists today

| Consumer | Current delivery | Current owner |
| --- | --- | --- |
| Backend and template development | Versioned development defaults plus ignored local environment files and a local Firebase service-account file | Each application repository |
| Backend and template Compose packaging | An ignored `.env.secrets` file and a mounted Firebase file | Each application's packaging flow |
| Microservices Kubernetes lab | Helm renders Kubernetes Secret objects from locally supplied credentials | `myscoutee-microservices` deployment flow |
| Local CI lab | Ignored local files and GitLab CI variables | `myscoutee-ci` |
| Other tools and services | Their own ignored `.env` or state files | Their respective repositories |

The local, path-level audit is in `.local/inventory.md` and is intentionally
ignored by Git. It records filenames and consumers, never secret values. The
inventory is a starting point, not proof that Git history or generated artifacts
are free of credentials.

## How to consolidate safely

1. Identify each credential's owner, consumer, environment, current storage,
   rotation method, and recovery requirement. Keep public configuration and
   example files in their existing repositories.
2. Select one low-impact, static credential as a pilot. OpenBao KV v2 is the
   initial candidate for a central store; HashiCorp Vault is an alternative.
   The sandbox proves the basic UI and KV behavior only. Choose authentication,
   access policies, TLS, durable storage, backup, and unseal procedure before
   storing real credentials.
3. Adapt the **existing** Compose, Helm, or CI delivery path to obtain that
   credential. Verify startup, restart, access denial, rotation, and recovery
   before migrating the next consumer.
4. Review old local copies, archives, logs, CI variables, and Git history. Only
   remove a copy after its owner and rollback needs are known. Rotate credentials
   that were exposed; moving a value into a vault does not revoke old copies.

Generated Terraform state, kubeconfig, application data, audit evidence, and
backups need their own retention and access controls. They are not automatically
KV secrets to import.

## References

- [OpenBao KV v2](https://openbao.org/docs/secrets/kv/kv-v2/)
- [OpenBao integrated storage and backups](https://openbao.org/docs/concepts/integrated-storage/)
- [OpenBao development mode limitations](https://openbao.org/docs/next/concepts/dev-server/)
- [HashiCorp Vault production hardening](https://developer.hashicorp.com/vault/docs/concepts/production-hardening)
