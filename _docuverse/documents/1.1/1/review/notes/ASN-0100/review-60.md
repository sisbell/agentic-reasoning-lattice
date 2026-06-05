# Review of ASN-0100

This is an unusually thorough and rigorous note. The substrate decomposition is sound, the three-region partition is verified against S2/S3★/D-CTG★/D-MIN★/D-SEQ★ with explicit boundary arithmetic, the per-state invariants are checked at every intermediate, the worked examples (interior, append, empty, empty-but-non-fresh-allocator) cover the edge cases, and the wp analysis includes a genuinely non-trivial case (provenance membership / tight-vs-non-tight discoverability). I found no hand-waved proof, no missing edge case, and no improper cross-ASN reference (all citations are to foundation ASNs).

The note carries the `review-mode.anti-bloat` classifier. My findings are confined to residual prose accretion, not correctness.

## REVISE

### Issue 1: COPY declared out-of-scope repeatedly (deferral accretion)
**ASN-0100, §INSERT vs. COPY and §Bounding the Scope**:
- "We address the distinction only to fix the identity character of INSERT; COPY's full operation specification is out of scope for this ASN."
- "By contrast, COPY (out of scope here) creates V→I mappings to existing I-addresses without allocating new content — the defining structural difference being that INSERT allocates fresh I-addresses while COPY does not."
- "COPY, which creates V→I references without content allocation. Out of scope."

**Problem**: COPY's out-of-scope status is asserted three-plus times across two sections, plus the parenthetical in INS.identity.version. This matches the flagged pattern "multiple paragraphs in different sections defer to the same downstream location." One contrast suffices to fix INSERT's identity character (INS.identity already carries this); the canonical scoping belongs in §Bounding the Scope alone.
**Required**: Keep a single COPY contrast (the structural "fresh vs. existing" point) where it does analytic work, and let §Bounding the Scope carry the out-of-scope declaration. Remove the duplicate out-of-scope assertions.

### Issue 2: Effects section defers formalization to §Formal Contract more than once
**ASN-0100, §Discovering the Three Effects**:
- Effect One: "The post-state content store is stated formally by the content-store effect in §The Operation: Formal Contract (INS.C)…"
- Effect Three: "This is the Shifted right clause of the arrangement effect in §The Operation: Formal Contract, the specified effect of INSERT's step-3 K.μ⁺."

**Problem**: The Effects subsections derive the three effects, then point forward to where each is formally stated. Two of the three end with a pointer to the same downstream section. The derivation (e.g. "every existing v ≥ p must remap by n") is the content; the forward pointer adds navigation, not reasoning, and is the kind of cross-section deferral the classifier flags as accreting.
**Required**: Drop the "stated formally in §… " pointers; the §Formal Contract section already names the same claims (INS.C, INS.M-shift), so the forward reference is redundant with the table of claims.

## OUT_OF_SCOPE

(none — the three identity corollaries, the tight/non-tight wp split, and the empty-vs-fresh-allocator sub-case are all legitimate consequences of INSERT's own behaviour, not drift into COPY/version/replication territory.)

VERDICT: REVISE
