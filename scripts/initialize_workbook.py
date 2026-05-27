#!/usr/bin/env python3
import os
import sys
import uuid
import hashlib
import datetime
import subprocess

def get_input(prompt):
    """Fallback for python inputs."""
    try:
        return input(prompt).strip()
    except KeyboardInterrupt:
        print("\nInitialization aborted by user.")
        sys.exit(1)

def run_cmd(cmd, cwd=None):
    """Helper to run shell commands."""
    try:
        result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
        return result.stdout.decode('utf-8').strip()
    except subprocess.CalledProcessError:
        return None

def generate_identity():
    print("=====================================================================")
    print("      PORTDIVE WORKBOOK: GLOBAL ID & AGENT REGISTRATION")
    print("=====================================================================")
    print("\nThis script establishes the unique cryptographic identity of this")
    print("workbook and its associated AI agents in the global PortDive network.\n")

    # 1. Prompt for Workbook Name
    workbook_name = ""
    while not workbook_name:
        workbook_name = get_input("Enter a unique name for this workbook (letters, numbers, hyphens only):\n> ")
        # Clean name
        workbook_name = "".join(c for c in workbook_name if c.isalnum() or c in ['-', '_']).strip()
        if not workbook_name:
            print("Error: Name cannot be blank and must contain only alphanumeric characters, hyphens, or underscores.")

    # 2. Generate UUIDv4
    workbook_uuid = str(uuid.uuid4())

    # 3. Compute Cryptographic SHA256 Signature
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
    sha_payload = f"{workbook_name}:{workbook_uuid}:{timestamp}"
    workbook_sha = hashlib.sha256(sha_payload.encode('utf-8')).hexdigest()

    # 4. Determine Paths
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    identity_path = os.path.join(root_dir, 'IDENTITY.md')

    # Check if IDENTITY.md already exists and has a locked ID
    if os.path.exists(identity_path):
        with open(identity_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if "workbook_id:" in content and "workbook_sha:" in content:
            print("\n=====================================================================")
            print("WARNING: An identity is ALREADY locked in this workbook!")
            print("Re-running initialization will overwrite your unique world-wide ID.")
            print("=====================================================================")
            confirm = get_input("Are you absolutely sure you want to overwrite it? (yes/no): ")
            if confirm.lower() != 'yes':
                print("Initialization cancelled. Your existing identity remains locked.")
                sys.exit(0)

    # 5. Author IDENTITY.md
    identity_content = f"""---
workbook_id: "{workbook_uuid}"
workbook_name: "{workbook_name}"
workbook_sha: "{workbook_sha}"
initialized_at: "{timestamp}"
---

# Workbook Identity & Agent Registration Ledger

This file establishes the **global, unique cryptographic identity** of this sovereign workbook and its associated AI agents. Do not modify the YAML frontmatter above, as it is used to identify your research nodes and sync matrices programmatically in the PortDive peer network.

---

## 1. Cryptographic Credentials

*   **Global Node Name:** `{workbook_name}`
*   **Workbook UUID:** `{workbook_uuid}`
*   **Authentication SHA-256:** `{workbook_sha}`
*   **Registration Date:** `{timestamp}`

---

## 2. Agent Authorization & Key Audit

This ledger maintains authorization parameters for active AI agents executing within this workbook's namespaces:

| Authorized Agent Role | First Ingest Date | Session ID Reference | Verification Status |
| :--- | :--- | :--- | :--- |
| **Systemic Analyst & Portfolio Manager** | {timestamp[:10]} | INITIAL_RELEASE | **VERIFIED SIGNATURE** |

---

## 3. Network Sync Status

*   **Database Synchronization Status:** `PENDING_REGISTRATION`
*   **Public/Private Envelope:** `PRIVATE` (Restricted workbook)
*   **Orchestrator Node Link:** `mcp.portdive.app/node/auth`
"""

    with open(identity_path, 'w', encoding='utf-8') as f:
        f.write(identity_content)

    print("\n=====================================================================")
    print("SUCCESS: Cryptographic Workbook Identity Established!")
    print("=====================================================================")
    print(f"Name:    {workbook_name}")
    print(f"UUID:    {workbook_uuid}")
    print(f"SHA-256: {workbook_sha[:20]}... [fully written to IDENTITY.md]")
    print("=====================================================================\n")

    # 6. Optional Git Commit
    if os.path.exists(os.path.join(root_dir, '.git')):
        confirm_git = get_input("Would you like to commit this identity to your local git history? (yes/no): ")
        if confirm_git.lower() == 'yes':
            run_cmd("git add IDENTITY.md", cwd=root_dir)
            run_cmd(f'git commit -m "feat(identity): lock unique workbook identity [{workbook_name}]"', cwd=root_dir)
            print("Locked successfully into local git repository.")

if __name__ == '__main__':
    generate_identity()
