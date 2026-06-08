# Review of ASN-0100

This ASN is technically mature: preconditions are case-split correctly (empty vs. non-empty `V_{s_C}(d)`), the three regions are proven pairwise-disjoint via the shared-prefix reduction, the `INS.I3-coincide` restriction handle is sound (it correctly scopes to Left ∪ Shifted-right and excludes the gap that I3-V vacates), five worked examples exercise the live edge cases (prepend/forced-shrinkage, append, empty-document, deep-subspace `m_C = 3`, residual-content branch), and the wp analysis hits two non-trivial postconditions. The standard correctness, boundary-case, and invariant-conjunct checks pass. The findings below are anti-bloat (the note carries `review-mode.anti-bloat`).

## REVISE

### Issue 1: Use-site inventory and structural meta-prose in INS.I3-coincide
**ASN-0100, §Discovering the Three Effects → Effect Three (INS.I3-coincide)**: "This is the named handle the invariant verifications below cite. Because `M'(d) ↾ (Left ∪ Shifted-right)` *is* (pointwise) the I3-specified arrangement on that domain, every I3 lemma about `M_{I3}` — I3-S2 (functionality), I3-S3 (referential integrity), I3-VP / I3-VD (well-formedness and fixed depth), I3-fin (finiteness) — transports verbatim to that restriction; each full-arrangement property then follows by combining the restriction with the separately-handled Insertion region (whose cross-region disjointness from Left ∪ Shifted-right is established under §Arrangement functionality)."
**Problem**: The substantive content of the handle is one clause — the restriction is pointwise the I3 arrangement, so I3 lemmas transport. The framing "This is the named handle the invariant verifications below cite" is structural meta-prose that does not advance the claim. The parenthetical enumeration `I3-S2 / I3-S3 / I3-VP / I3-VD / I3-fin` is a downstream-consumer inventory: each of these is re-cited and applied at its actual use site (I3-S2 in §Arrangement functionality, I3-S3 in §Referential integrity, I3-VP/I3-VD/I3-fin in §Post-state V-position well-formedness), so the inventory duplicates content stated where it is used. The trailing "(whose cross-region disjointness… is established under §Arrangement functionality)" is a forward pointer.
**Required**: Reduce to the load-bearing statement (restriction equality ⇒ I3 lemmas transport on Left ∪ Shifted-right). Drop the "the invariant verifications below cite" framing, the per-lemma inventory (let each use site name the lemma it needs), and the forward pointer to §Arrangement functionality.

### Issue 2: Forward-reference / deferral accretion across sections
**ASN-0100, multiple sections**: e.g. §Background "(The consequence… is developed in §Identity Through Allocation.)"; §Cross-document independence "This is the `d' ≠ d` case of the projection-shift correspondence INS.proj, established below."; §A Worked Example (empty case) "The general argument is §Provenance; the case-specific delta is…".
**Problem**: Several paragraphs defer to a downstream location for content they gesture at, and the J0/J1★/J1'★ coupling is discharged three times — once generally in §Provenance and twice as worked-example "deltas," with the empty-case delta explicitly pointing back to §Provenance. This is the "multiple paragraphs defer to the same downstream location" accretion pattern; the empty-case provenance discharge in particular adds little beyond its deferral.
**Required**: Drop forward pointers that only announce where a consequence will be derived (the derivation site can stand alone). Collapse the empty-case provenance discharge into §Provenance's general argument, keeping only a genuinely case-specific fact if one exists (no K.μ⁻ fires; pre-state `ran(M(d)) = ∅`), rather than restating the discharge structure and deferring.

## OUT_OF_SCOPE

### Topic 1: Link-subspace insertion (`K.μ⁺_L`), DELETE/COPY/REARRANGE, version derivation, replication
**Why out of scope**: The ASN correctly bounds itself to content-subspace INSERT and lists these in §Bounding the Scope and §Open Questions; they are future-ASN territory, not defects here.

VERDICT: REVISE
