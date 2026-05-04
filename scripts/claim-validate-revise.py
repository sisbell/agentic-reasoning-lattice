"""claim-validate-revise — apply mechanical fixes driven by validator findings.

Paired with claim-validate.py: that script finds structural-invariant
violations; this one applies per-invariant fixes via the
structural-rule-fix agent. Loop is validator finds → reviser fixes →
validator re-runs between passes. Six passes in order:
body-uniqueness, declaration-label-mismatch, depends-agreement,
references-resolve, acyclic-depends (propose-only).

Usage:
    python scripts/claim-validate-revise.py 34 [--dry-run|--apply]
                                                        [--rule RULE]
                                                        [--file FILE]
                                                        [--from-pass N]
                                                        [--to-pass N]
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.orchestrators.claim_validate_revise import main


if __name__ == "__main__":
    sys.exit(main())
