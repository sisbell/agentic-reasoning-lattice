# Review of ASN-0132

The mathematics here is sound. I checked the load-bearing derivations and the worked example and found no correctness defects:

- **CN-MONO's wp** is a genuine derivation, not a hand-wave: it splits the contribution of pre-existing links (fixed by L12/LP13 + unchanged `L_R`) from the fresh link's contribution, and lands exactly on FL-WP(a)'s two conjuncts (`sat(ℓ,q,Σ') ∧ ¬(E (b,F',G') ∈ L_R^Σ :: ℓ ∈ coverage(G'))`). The non-decrease lift to `Σ →* Σ'` via FL-MON is valid.
- **CN-UNIT(d)** checks against J4 (ASN-0047): the fork composite uses only K.δ, K.μ⁺ over `V_{s_C}`, and K.ρ — no K.λ, no K.μ⁺_L — so `Σ.L` is untouched and version-refraction reduces to appearance multiplicity. Correct.
- **The worked example** is arithmetically correct end to end: `coverage(F)` spans ordinals 5..12; `a₁` (three matching spans → one yes), `a₂` (nullified, sat-true but excluded), `a₃` (orphan, counted), `a₄` (document-component divergence `2>1`, excluded), `a_R` (empty from-endset, FL-EMP) all resolve as claimed; `count = 2`, wildcard `= 4`, the two home-bound variants (`H₁` admits all, `H₂` yields a genuine CN-ZERO) are right.
- Cross-ASN citations are all to foundation ASNs (0034/0036/0043/0047/0058/0086/0093/0098/0121/0127). No self-containment violation. No out-of-scope operation is given a claim; delivery is correctly deferred (CN-OBT).

The note is not META — it defines a read-only operation and pins what its number *means* abstractly. The findings below are all the anti-bloat classifier's targets: accumulated meta-prose, not logic errors.

## REVISE

### Issue 1: Three implementation notes restate one mechanical fact
**ASN-0132, implementation notes after CN-SHARED, after CN-SNAP, and in the final cost section**:
- "Gregory's back end computes the count by invoking the *same* matching routine the enumeration invokes, taking its materialised result, and reporting its length."
- "it computes the count by running the full matching search, materialising every match into a list, and returning the list's length"

**Problem**: Three of the four implementation notes each re-establish the same premise — *the back end runs the full enumeration and reports the resulting list's length*. The CN-SHARED note and the final cost note are near-verbatim. Each note's *distinct* conclusion is fine (single-state agreement / per-inquiry recompute / cost-equality), but the shared premise is stated three times. (The dedup-defect note after CN-UNIT is distinct — keep it.)

**Required**: State the realisation mechanism once; at the later two sites carry only the section-specific consequence ("hence single-state agreement," "hence two inquiries observe two states," "hence how-many costs what which-ones costs") without re-describing the search.

### Issue 2: The resolution boundary, declared upstream, is re-argued where CN-LOC already settles it
**ASN-0132, CN-STAB**: "By that same resolution principle of the opening remark, a rearrangement that preserves addresses leaves every address-phrased count exactly invariant; any apparent movement is the request re-resolving, not the link."

**Problem**: The opening "remark on the request as given" establishes resolution as upstream and out of scope. CN-STAB has already proved invariance for a fixed `q` from CN-LOC, and its own preceding caveat paragraph already states that re-phrasing submits a different `q`. This closing sentence restates the opening remark plus that caveat — it advances no new reasoning. The resolution theme recurs across the opening remark, CN-ZERO, and CN-STAB; the CN-ZERO instance earns its place (it distinguishes empty-request zero from empty-store zero), but this CN-STAB sentence is the redundant one.

**Required**: Delete the back-referencing sentence; the fixed-`q` caveat immediately above it already carries the point.

### Issue 3: Claims-table CN-UNIT entry embeds a derivation and re-explains a clause
**ASN-0132, Claims Introduced table, CN-UNIT row**: "(the latter three excluded by CN-LOC; forking shares content (references the same I-addresses via J4's K.μ⁺ step, no K.α), not links — J4 ASN-0047 — so the version DAG adds no link address). Clause (b) is transclusion invariance: a link reachable through any number of documents contributes 1, document-reach being an Σ.M quantity, not a link count"

**Problem**: The claims table is a summary slot. This entry carries the J4 mechanics already given in full in body CN-UNIT(d) ("populates its arrangement over the content subspace alone … performs no link allocation"), and re-explains clause (b), which body CN-UNIT(b) already states. Essay/derivation content in a structural slot.

**Required**: Reduce the table entry to a terse statement of the claim (each satisfying addressable link contributes 1, independent of anchoring/transclusion/appearance/version multiplicity); leave the J4 argument and clause (b) gloss in the body.

## OUT_OF_SCOPE

None. The note stays within its bounds — enumeration semantics are cited to ASN-0121 (foundation), delivery and resolution are explicitly deferred, and the Open Questions correctly park federated counting, cross-inquiry concurrency, cache validity, fragmentation/identity, and cost-as-correctness for future work.

VERDICT: REVISE
