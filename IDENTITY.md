# Workbook Identity & Agent Registration Ledger

This workbook is currently **UNINITIALIZED**.

To participate in the global PortDive peer network, establish a unique cryptographic identity for this workbook, and register active AI research agents, you must run the identity initialization script.

---

## Post-Clone Initialization Step

Run the following command from the root of your workbook directory:

```bash
python3 scripts/initialize_workbook.py
```

This script will:
1. Prompt you for a user-chosen, custom name for this research node.
2. Generate a globally unique UUIDv4.
3. Compute a cryptographic SHA-256 signature locking the name, UUID, and initialization timestamp.
4. Overwrite this file (`IDENTITY.md`) with your sealed credentials inside an Obsidian-compatible YAML frontmatter block.
5. Optionally lock this identity forever by committing it directly to your local git ledger.

---

*Status: Cryptographic Identity Pending Registration*
