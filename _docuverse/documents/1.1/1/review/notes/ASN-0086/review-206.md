# Review of ASN-0086

## REVISE

### Issue 1: "Higher-arity addresses are in A_rel but in no L_K" stated four times
**ASN-0086, Definition — Partition / Definition — TupleAddress / Definition — Nullified / Properties table**:
- Partition note: "*A_rel^Σ names the whole link store, not only the tuples.* ... such addresses inhabit `A_rel^Σ` but correspond to no tuple of any `L_K`."
- TupleAddress: "The map is *into but not onto*: its image is exactly the standard-triple subset `{a ∈ dom(Σ.L) : |Σ.L(a)| = 3}` ... which omits any higher-arity link address."
- Nullified: "any higher-arity entry in `nullified(Σ)` is unreachable by the active-subset exclusion."
- Table (A_doc/A_rel row): "the latter holds all link addresses, including higher-arity ones in no `L_K`."

**Problem**: One fact — higher-arity links occupy `dom(Σ.L)` but are not tuples of any `L_K` — is restated in four places in different words. This is the "two paragraphs say the same thing" pattern compounding across cycles.
**Required**: State it once (the Partition note is the natural home) and let the later sites assume it without re-explaining.

### Issue 2: Codomain choice justified with "for uniformity" meta-prose
**ASN-0086, Definition — TupleAddress**: "We declare the codomain as the full `A_rel^Σ` for uniformity with the partition above, noting that surjectivity holds only onto the arity-3 slice."

**Problem**: This is prose justifying a *notational choice* (why the codomain is declared as the full set) rather than advancing the definition's meaning. "Into but not onto" with the image identified is the whole content; the uniformity rationale is meta-commentary a precise reader must skip.
**Required**: Drop the justification clause; give the map, its image, and stop.

### Issue 3: Defensive deferral + scope-disclaimer prose around AdmissibleTypes
**ASN-0086, Definition — AdmissibleTypes**: "We require only that type-equality is decidable by endset comparison: L8 ... supplies the *criterion* ... and Lemma CoverageEqualityDecidable (below) supplies its decidability ... (L8 itself speaks only to the equivalence relation, not to its decidability.) Type indices in what follows range over `T_admissible` ... membership in a given coverage class `[K]` is then determined per-tuple by `L_K^Σ`'s coverage-equivalence criterion (below)."

**Problem**: Two forward deferrals to "(below)" stacked in one paragraph, plus a parenthetical clarifying what L8 does *not* do — defensive meta-prose that pre-empts an objection rather than stating the definition. The decidability dependency belongs at the lemma, not announced twice here.
**Required**: Define `T_admissible` and note that type-equivalence is `~` (coverage equality); let CoverageEqualityDecidable carry its own decidability claim without the forward announcement and the L8-disclaimer.

## OUT_OF_SCOPE

### Topic 1: Higher-arity typed relations `L_K^{(n)}` and dynamic type-address coordination
**Why out of scope**: The note correctly confines itself to standard triples (`|Σ.L(a)| = 3`) and routes the n-ary generalization and cross-layer type-collision questions to its Open Questions. These are new territory, not gaps in the present development.

### Topic 2: Atomicity/consistency model for concurrent Observe vs. Emit
**Why out of scope**: Concurrency semantics for `A_K` transitions is a future-ASN concern, already flagged in Open Questions; the single-writer `→` model here is internally complete.

VERDICT: REVISE
