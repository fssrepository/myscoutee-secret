#!/usr/bin/env python3
"""Build the English MyScoutee secrets introduction and rollout guide."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "MyScoutee_Secrets_Introduction_Guide_EN.pdf"
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
for name, filename in (
    ("Guide", "DejaVuSans.ttf"),
    ("GuideBold", "DejaVuSans-Bold.ttf"),
    ("GuideMono", "DejaVuSansMono.ttf"),
):
    pdfmetrics.registerFont(TTFont(name, str(FONT_DIR / filename)))

NAVY = colors.HexColor("#17324d")
BLUE = colors.HexColor("#176b87")
MUTED = colors.HexColor("#586675")
SOFT = colors.HexColor("#edf5f8")
LINE = colors.HexColor("#d9e1e8")
INK = colors.HexColor("#1c2633")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle("BodyGuide", fontName="Guide", fontSize=8.7,
                          leading=13, textColor=INK, spaceAfter=8))
styles.add(ParagraphStyle("SmallGuide", parent=styles["BodyGuide"],
                          fontSize=7.4, leading=10.6, textColor=MUTED))
styles.add(ParagraphStyle("TitleGuide", fontName="GuideBold", fontSize=24,
                          leading=29, textColor=NAVY, spaceAfter=12))
styles.add(ParagraphStyle("SectionGuide", fontName="GuideBold", fontSize=13.2,
                          leading=18, textColor=NAVY, spaceBefore=8,
                          spaceAfter=8))
styles.add(ParagraphStyle("SubGuide", fontName="GuideBold", fontSize=9.7,
                          leading=13, textColor=BLUE, spaceBefore=6,
                          spaceAfter=5))
styles.add(ParagraphStyle("KickerGuide", fontName="GuideBold", fontSize=8,
                          leading=12, textColor=BLUE, spaceAfter=8))
styles.add(ParagraphStyle("CellGuide", parent=styles["BodyGuide"],
                          fontSize=7.25, leading=10.3, spaceAfter=0))
styles.add(ParagraphStyle("CodeGuide", fontName="GuideMono", fontSize=7.6,
                          leading=11, textColor=NAVY, backColor=SOFT,
                          borderPadding=10, spaceBefore=5, spaceAfter=11))


def p(value, style="BodyGuide"):
    return Paragraph(value, styles[style])


def table(rows, widths, header=True):
    cells = [[p(str(value), "CellGuide") for value in row] for row in rows]
    result = Table(cells, colWidths=widths, hAlign="LEFT",
                   repeatRows=1 if header else 0)
    commands = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE),
    ]
    if header:
        commands.append(("BACKGROUND", (0, 0), (-1, 0), SOFT))
    result.setStyle(TableStyle(commands))
    return result


def frame(canvas, document):
    width, height = A4
    canvas.saveState()
    if document.page == 1:
        canvas.drawImage(str(ROOT / "assets/heart.png"), 45, height - 76,
                         width=42, height=42, mask="auto")
        canvas.setFont("GuideBold", 19)
        canvas.setFillColor(NAVY)
        canvas.drawString(94, height - 55, "yScoutee")
        canvas.setFont("Guide", 8)
        canvas.setFillColor(MUTED)
        canvas.drawString(95, height - 69, "Engineering documentation")
    else:
        canvas.setFont("GuideBold", 8)
        canvas.setFillColor(NAVY)
        canvas.drawString(45, height - 35, "MYSCOUTEE  /  ENGINEERING")
    canvas.setStrokeColor(LINE)
    canvas.line(45, 41, width - 45, 41)
    canvas.setFont("Guide", 7.2)
    canvas.drawString(45, 28, "MSC-SEC-VAULT-001  |  0.1.0  |  2026-10-29  |  EN")
    canvas.drawRightString(width - 45, 28, str(document.page))
    canvas.restoreState()


story = [
    p("SECRETS / LOCAL SANDBOX AND ROLLOUT", "KickerGuide"),
    p("MyScoutee Secrets", "TitleGuide"),
    p("A hands-on OpenBao introduction and a case-by-case path from scattered local credentials to controlled delivery."),
    Spacer(1, 9),
    table([
        ["Document", "MSC-SEC-VAULT-001 / version 0.1.0 / English"],
        ["Owner", "myscoutee-secret"],
        ["Audience", "Developers, operators, and the product owner"],
        ["Current state", "Disposable OpenBao sandbox works with synthetic data. No production vault or application migration is in place."],
    ], [126, 379], header=False),
    p("The basic idea", "SectionGuide"),
    p("A secret manager is a service that stores sensitive values behind an authenticated API. Applications or deployment tools authenticate, read only permitted paths, and pass values to the existing runtime. The web UI is another client of the same service."),
    table([
        ["Part", "What it does here"],
        ["OpenBao server", "Stores versioned sample values in the sandbox. A future persistent server would need storage, TLS, backup, audit, and recovery."],
        ["Identity and policy", "Decide who can read or change a named path. The sandbox has a powerful development token; real clients need narrower identities."],
        ["Delivery path", "The current Compose file, Helm chart, or CI variable remains the consumer boundary until its specific integration is proven."],
    ], [130, 375]),
    p("What a vault does not solve by itself", "SubGuide"),
    p("Git-ignored copies, old archives, logs, Terraform state, and issued credentials remain where they are until reviewed. Moving a value does not revoke an earlier copy. The issuer must rotate an exposed credential."),
    PageBreak(),

    p("Try the sandbox", "TitleGuide"),
    p("This isolated exercise uses a pinned OpenBao image, host loopback port 8200, an ignored local token, and in-memory storage. It never uses a real MyScoutee credential."),
    p("From the myscoutee-secret repository", "SubGuide"),
    Preformatted("./scripts/lab.sh start\n./scripts/lab.sh smoke\n./scripts/lab.sh token   # use this token in the web login", styles["CodeGuide"]),
    table([
        ["Step", "What you should see"],
        ["1. Open the UI", "Visit http://127.0.0.1:8200/ui/ in your local browser. Choose Token login and enter the token printed by the command above."],
        ["2. Read the sample", "Open Secrets > secret > demo > sample. The example field has the synthetic value sandbox-only-value."],
        ["3. Explore", "Edit that synthetic value, save it, and inspect its KV version history. You can create another synthetic path."],
        ["4. Stop", "Run ./scripts/lab.sh stop. The sample disappears because the dev server stores everything in memory."],
    ], [112, 393]),
    p("What the smoke test checks", "SectionGuide"),
    p("It verifies server health, the UI route, a KV v2 write and read, and denial of a read with an invalid token. This is evidence that the sandbox works; it does not test a durable store, production TLS, role-based access, backup, or an application connection."),
    p("Sandbox boundary", "SubGuide"),
    p("The listener uses HTTP only on 127.0.0.1. OpenBao's development mode starts unsealed and loses data at restart. Never enter a real key, password, token, or customer data in this UI."),
    PageBreak(),

    p("Choose the right integration", "TitleGuide"),
    p("MyScoutee already has delivery mechanisms. Introduce a vault at their input boundary instead of teaching every application a separate secret API at once."),
    table([
        ["Case", "Existing path", "Candidate first step"],
        ["Developer machine", "Ignored local .env.secrets and Firebase files; versioned examples/defaults.", "Use an authenticated local fetch to populate the same paths, then check permissions and missing-value failure."],
        ["Compose deployment", "Package-provided .env.secrets plus a mounted Firebase file.", "Render those files on the host before Compose starts. Prove atomic writes, restart, rotation, and rollback."],
        ["Kubernetes lab", "Helm creates Kubernetes Secret objects from locally supplied credentials.", "Compare an agent, CSI, operator, or pre-deploy sync against the current cluster and identity model. Check Helm and etcd copies."],
        ["CI laboratory", "Ignored inputs become scoped GitLab CI variables.", "Keep current variable delivery initially. Later, give trusted jobs a short-lived, narrowly scoped fetch identity."],
        ["Operator keys and state", "Signing/SSH/TLS keys, kubeconfig, Terraform state, and backups have different owners.", "Define custody, signing, retention, and recovery per type. Do not bulk import state into KV."],
    ], [105, 190, 210]),
    p("Backend and template", "SectionGuide"),
    p("A shared change to application delivery must be carried into both repositories and verified in both. Their deployment settings and generated image identities remain separate."),
    p("OpenBao or HashiCorp Vault?", "SubGuide"),
    p("They are alternative server products. This sandbox uses OpenBao to learn the UI and KV model. Select the long-lived product only after the required authentication, operations, support, and deployment model are clear."),
    PageBreak(),

    p("Roll out one credential at a time", "TitleGuide"),
    table([
        ["Gate", "Required evidence before moving on"],
        ["1. Inventory", "Name the credential's issuer, owner, consumers, environment, current path, rotation method, expiry, and recovery owner. Record no value in Git."],
        ["2. Persistent store", "Configure TLS, scoped authentication, policies, audit, durable storage, backup, a restore exercise, and unseal/key custody. Keep this separate from the sandbox."],
        ["3. First consumer", "Choose one low-impact static credential. Adapt its existing delivery path and verify startup, restart, missing-vault behavior, access denial, rotation, and rollback."],
        ["4. Expand", "Repeat per environment and consumer. Compare behavior with the old path before removing old copies."],
        ["5. Retire copies", "Review Git history, local archives, CI variables, logs, and generated artifacts. Rotate exposed credentials at their issuer; preserve needed recovery evidence."],
    ], [125, 380]),
    p("Questions that must have owners", "SectionGuide"),
    p("Who can unseal and restore the store? How do workloads authenticate after restart? What happens when the store is unavailable? Where do fetched values land on disk, in Kubernetes, or in CI logs? Who rotates a credential and confirms every consumer has the new version?"),
    p("Source and limits", "SectionGuide"),
    p("This guide reflects the repository state on 2026-10-29 and the disposable sandbox. The local path inventory is Git-ignored. Neither the sandbox nor this guide proves that history, generated artifacts, or operational backups are free of secrets."),
    p("Primary documentation", "SubGuide"),
    p('OpenBao: <link href="https://openbao.org/docs/configuration/ui/" color="#176b87">UI</link>, '
      '<link href="https://openbao.org/docs/secrets/kv/kv-v2/" color="#176b87">KV v2</link>, '
      '<link href="https://openbao.org/docs/concepts/integrated-storage/" color="#176b87">integrated storage</link>, '
      '<link href="https://openbao.org/docs/next/concepts/dev-server/" color="#176b87">development mode</link>. '
      'HashiCorp Vault: <link href="https://developer.hashicorp.com/vault/docs/concepts/production-hardening" color="#176b87">production hardening</link>, '
      '<link href="https://developer.hashicorp.com/vault/docs/deploy/kubernetes/comparisons" color="#176b87">Kubernetes integration comparison</link>.', "SmallGuide"),
]

doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=45,
                        rightMargin=45, topMargin=105, bottomMargin=58,
                        title="MyScoutee Secrets Introduction Guide",
                        author="MyScoutee Engineering")
doc.build(story, onFirstPage=frame, onLaterPages=frame)
print(OUT)
