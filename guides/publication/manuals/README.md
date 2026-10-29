# MyScoutee Secrets guide

The English, MyScoutee-branded PDF is
[MyScoutee Secrets Introduction Guide](MyScoutee_Secrets_Introduction_Guide_EN.pdf).
Document ID: `MSC-SEC-VAULT-001`; version: `0.1.0`.

Regenerate from the `myscoutee-secret` repository root:

```sh
python3 guides/publication/manuals/build-guide.py
```

The editable generator is `build-guide.py`; the shared MyScoutee brand asset
is `assets/heart.png`. ReportLab and DejaVu fonts are required. Update the
generator, version, and PDF together when a documented integration changes.
The detailed engineering plan is in `../../development/secrets/README.md`.
