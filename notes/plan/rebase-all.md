# Batch Rebase — Design and Process

## Overview

`rebase-all.py` processes all active ASNs in dependency order, ensuring each ASN is consistent with its foundation statements. It combines a cheap sonnet pre-check (fast eyes) with an opus rebase (heavy lifting) to find and fix foundation drift.

## The Process

1. **Topological sort** all active ASNs by dependency graph (foundations first)
2. **For each ASN in order:**
   - Check yaml: is `last_rebase_check` newer than all dependency exports? → **skip**
   - Otherwise → run sonnet pre-check (writes as `review-N.md`)
   - Pre-check findings are fed to opus rebase as supplementary input
   - **Rebase always runs** if timestamps say it's needed — the pre-check is a helper, not a gate. Opus three-pass rebase may find things sonnet missed.
   - After rebase → review/revise cycle → post-check (sonnet)
   - Post-check CLEAN → export, update yaml timestamps
   - Post-check findings → retry once with new findings → fail if still findings, **stop batch**

The batch stops on failure because a broken ASN's export would propagate bad state to everything downstream. The topological ordering ensures foundations are processed and re-exported before their dependents are checked.

## Where Things Are Stored

| What | Where |
|------|-------|
| Reasoning docs | `vault/1-reasoning-docs/ASN-NNNN-*.md` |
| Reviews + consistency checks | `vault/2-review/ASN-NNNN/review-N.md` |
| Exports | `vault/3-export/ASN-NNNN-statements.md` |
| Project model + state | `vault/project-model/ASN-NNNN.yaml` |

Consistency checks are written as numbered reviews — they follow the same format and sit in the same history. The header distinguishes them (`# Consistency Check of ASN-NNNN` vs `# Review of ASN-NNNN`).

## Metadata

Each project model yaml tracks rebase state:

```yaml
depends: [34, 36, 47]                          # dependency graph
last_rebase_check: "2026-03-23T09:54:00"       # last time rebase verified this ASN
last_consistency_check: "2026-03-23T10:30:00"   # last time consistency check ran
last_consistency_result: "CLEAN"                # CLEAN or FINDINGS
```

## Decision Logic

```
last_rebase_check > all dep exports?  →  skip (already rebased)
otherwise                             →  pre-check + rebase + post-check
```

The `last_rebase_check` timestamp is written after a successful rebase (post-check CLEAN + export), or when the pre-check finds nothing and the rebase makes no changes. On re-run, ASNs with fresh timestamps are skipped.

## Cascade

When ASN-0047 is rebased and re-exported, its export timestamp advances. Every downstream ASN (0051, 0059, 0061, etc.) now has `last_rebase_check` older than ASN-0047's export. Their turn in the topological order comes later, so they see the fresh export and get checked/rebased as needed.

## Commands

```bash
python scripts/rebase-all.py                       # full run
python scripts/rebase-all.py --exclude 40 42 45    # skip specific ASNs
python scripts/rebase-all.py --dry-run             # preview order and skip/rebase status
python scripts/rebase-all.py --force               # ignore timestamps, rebase everything
```

## Related Tools

- `run/check-project-status.sh` — timestamp-based health dashboard (Needs Export / Needs Rebase)
- `scripts/check-consistency.py` — standalone semantic audit, writes to `vault/consistency-check/`
- `scripts/rebase.py` — single-ASN rebase (used by rebase-all internally)

## Known Limitation

The system only checks **declared dependencies**. If an ASN uses properties from a foundation it doesn't list in `depends`, neither the consistency check nor the rebase will detect the mismatch. Finding missing dependencies requires manual investigation or a separate full-project scan against all foundation exports.
