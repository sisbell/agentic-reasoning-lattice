#!/usr/bin/env python3
"""
Run the transclude-exit substring validator standalone.

Verifies each claim body markdown is a byte-substring of its source
note (the Claim File Contract's content-preservation invariant at
transclude exit). Mechanical, no LLM. Skips sidecar files and
structural underscore-prefixed files.

Usage:
    python scripts/derive-claims-validate-transclude.py <ASN>
    python scripts/derive-claims-validate-transclude.py 36
"""

from lib.claim_derivation.validate_transclude import main

if __name__ == "__main__":
    main()
