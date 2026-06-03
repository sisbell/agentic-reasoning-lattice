# Channel Assignment — ASN-0069 review-73

**Date:** 2026-06-02 23:46

## Issue 1: V5a duplicates the K.μ~ "not elementary" explanation
Reason: Pure editorial deduplication — the fix moves an already-present fact to a single location. No design intent or implementation evidence required.

## Issue 2: V8b's "Non-monotonicity" disclaimer is defensive meta-prose, and the property's machinery is unused
Reason: Deciding whether to delete V8b or trim its disclaimer depends only on whether downstream claims consume its apparatus, which is verifiable within the ASN itself.

## Issue 3: V8 paragraph justifies *not* promoting a claim and defers to the worked example
Reason: The transitive subsequent-fork correspondence is already derived in-ASN by composing V8 at consecutive forks; condensing the meta-prose to one sentence needs no external input.

## Issue 4: Dependency Audit carries justification prose beyond its accounting role
Reason: Trimming a trailing justification clause from the audit is purely internal editing; the discharge sites already cite the relevant lemmas.
