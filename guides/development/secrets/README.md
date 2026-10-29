# Secret-management integration plan

This is the editable engineering guide. The branded reader guide is under
`guides/publication/manuals/`. No real MyScoutee credential has been migrated.
The local path inventory stays in the Git-ignored `.local/inventory.md`.

## What the sandbox proves

`scripts/lab.sh` starts OpenBao 2.7.2 with its built-in web UI at
<http://127.0.0.1:8200/ui/>. It creates a random token in
`.local/sandbox/root-token` (mode `0600`). `smoke` writes and reads one synthetic
KV v2 value and verifies that an invalid token cannot read it. The image is
pinned by digest in `compose.yaml`; the port is bound to host loopback. `stop`
destroys the in-memory sample. This validates the learning path, not production
availability, TLS, authentication design, backup, or integration with an app.

In plain terms, OpenBao stores values behind an API. A client authenticates,
receives a token with policies, and reads only the paths it is allowed to read.
The UI is one client. MyScoutee services will need an approved identity and a
delivery path; pointing a service at the UI address alone does nothing.

## Current integration points

| Case | Existing owner and delivery | Candidate integration | Proof required |
| --- | --- | --- | --- |
| Developer machine | Backend and template use local ignored `.env.secrets` and Firebase files alongside versioned defaults. | A local fetch command could populate the same paths after operator login; keep examples in each app. | No real secret in the sandbox; correct file mode, missing-token failure, app startup, and local cleanup. |
| Compose deployment | Backend/template packaging installs `.env.secrets`; Compose mounts the Firebase file and reads environment variables. | A host-side, authenticated render step could supply the existing files before Compose starts. | Atomic write, restricted permissions, failed-fetch behavior, restart, rotation, and rollback on both products. |
| Kubernetes lab | `myscoutee-microservices` Helm templates create Kubernetes Secret objects from locally supplied credentials. | Choose an agent/CSI/operator or a controlled pre-deploy sync only after checking the cluster's identity and storage model. Preserve existing Helm consumers during migration. | Pod startup/restart, namespace policy denial, value refresh, Helm release data, etcd exposure, and deployment rollback. |
| CI laboratory | `myscoutee-ci` reads ignored inputs and configures GitLab CI variables. | Keep GitLab variable delivery initially; a bounded job credential can fetch selected values later. | Scope to trusted jobs, redacted logs, revocation, pipeline retry, and no token in artifacts. |
| Operator and release keys | Signing, SSH, TLS, kubeconfig, Terraform state, and backup material have separate local owners. | Decide custody per key type. A signing operation may need a dedicated engine or external signer; Terraform state and kubeconfig are not KV import targets by default. | Rotation, independent backup, restore, offline recovery, and verified signatures/access. |

This table describes candidates, not implemented connections. The backend and
template have equivalent application boundaries; any future shared fix must be
made and verified in both, preserving their deployment-specific settings.

## Rollout order

1. For one credential, record its issuer, owner, consumers, environment,
   current path, rotation method, expiry, and recovery owner without recording
   its value in Git. Confirm whether it is already exposed in history or
   artifacts; if so, rotate it at the issuer.
2. Build a persistent, isolated OpenBao service with TLS, a non-root operating
   identity, scoped auth and policies, audit device, backup, restore test, and
   documented unseal/key custody. Keep it separate from this disposable lab.
3. Pilot one non-critical static credential through its existing delivery
   boundary. Compare app behavior before and after. Confirm failed fetch denies
   startup or uses only a specifically approved last-good copy.
4. Repeat for each environment and consumer only after access denial, rotation,
   restart, recovery, and rollback are demonstrated. Reconcile old copies and
   retention after the consumer is proven stable.

## Boundaries and decisions

- KV v2 keeps versions of static values. Its version history is useful for
  accidental changes but is not a substitute for backup or issuer-side rotation.
- Development mode is intentionally insecure and loses data on restart. Never
  use it to protect a real MyScoutee secret.
- Kubernetes Secret objects and Helm release records may hold credential data.
  A vault integration must account for those copies, not just change the source.
- A vault adds operational dependencies: access when sealed/unavailable,
  authentication renewal, storage backup, and recovery of the unseal mechanism.
- OpenBao and HashiCorp Vault are alternatives. This lab uses OpenBao; the
  integration contract should follow the chosen product's documented API and
  be tested against the version actually deployed.

## Primary references

- [OpenBao UI](https://openbao.org/docs/configuration/ui/)
- [OpenBao KV v2](https://openbao.org/docs/secrets/kv/kv-v2/)
- [OpenBao architecture](https://openbao.org/docs/internals/architecture/)
- [OpenBao integrated storage](https://openbao.org/docs/concepts/integrated-storage/)
- [OpenBao dev server](https://openbao.org/docs/next/concepts/dev-server/)
- [Vault production hardening](https://developer.hashicorp.com/vault/docs/concepts/production-hardening)
- [Vault Kubernetes integration comparison](https://developer.hashicorp.com/vault/docs/deploy/kubernetes/comparisons)
