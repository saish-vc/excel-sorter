# Maintenance, Roadmap, and Backlog

## Maintenance

Use semantic versions: MAJOR.MINOR.PATCH. Triage support requests by data-loss/security impact first; ship hotfixes with a regression test; record release date, changes, migration steps, and rollback notes. Back up the SQLite metadata store daily during a pilot and test restore monthly. Review dependencies monthly and apply security updates after test-suite verification.

Release-note template: version; date; added; fixed; security; upgrade action; known limits.

## Post-pilot roadmap

| Priority | Feature | User story | Effort | Dependency |
|---|---|---|---|---|
| P0 | Authentication and roles | Administrators need protected audit access. | M | College identity decision |
| P0 | Real performance benchmark | IT needs proof for 50k-row target. | S | Representative data/hardware |
| P1 | Template validation | Staff need warning before submitting malformed reports. | M | Department templates |
| P1 | Bulk processing | Officers need repeatable processing of many files. | L | Job storage/monitoring |
| P1 | Pivot summaries/PDF | Heads need presentation-ready reports. | M | Report requirements |
| P2 | Google Sheets/ERP integration | Staff need less import/export work. | L | API access/security review |
| P2 | Multi-language/cloud | More colleges need accessible deployment. | L | Hosting and translation |
