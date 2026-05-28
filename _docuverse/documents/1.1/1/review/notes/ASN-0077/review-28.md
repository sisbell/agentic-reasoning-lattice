# Review of ASN-0077

## REVISE

### Issue 1: OQ4 and OQ6 listed as open questions but answered by the ASN's own claims

**ASN-0077, Open Questions section**:

OQ4: "What guarantee must hold for SHOWORIGIN when the home document's I-addresses are no longer reachable for byte-fetching, but the address itself remains well-formed?"

OQ6: "When multiple V-positions in a single arrangement map to the same I-address (intra-document sharing per S5 of ASN-0036), what must SHOWORIGIN report at each position?"

**Problem**: OQ4 is fully discharged by O3 (structural derivation: origin reads only the address, not any byte-fetch-related state) combined with O5★ (multi-step permanence). The ASN's own prose explicitly acknowledges this: "The unreachability of the source bears on whether the bytes can be fetched, not on whether the origin can be named." OQ6 is answered by the set-form definition of `origins_V` — multiple V-positions mapping to the same `a` all contribute `origin(a)`, which collapses to a single set element. Listing already-answered questions as "open" weakens the OQ list's signal of what genuinely remains future work.

**Required**: Remove OQ4 and OQ6, OR rephrase to identify genuine future extensions (e.g., for OQ6: "Should a separate operation report position-level sharing multiplicity?"; for OQ4: drop entirely since fetch-independence is already established).

### Issue 2: Closure argument cites a documentation note for a load-bearing step

**ASN-0077, O0 derivation (b)**: "every reachable transition `Σ → Σ'` belongs to the closed enumeration of elementary transitions matching ASN-0098's LP-Comp scope... Direct inspection of each transition's effect and frame clauses... fixes which transitions can modify L."

**Problem**: ASN-0098 explicitly labels LP-Comp as a "Documentation note, not a load-bearing lemma." ASN-0077's O0(b) (and the parallel argument in O0(c) for `dom(C)`) makes load-bearing use of LP-Comp's enumeration to discharge that K.λ is the unique source of `dom(L)` growth. Although the ASN then performs direct frame inspection, the completeness of the enumeration itself rests on LP-Comp. If a future ASN introduces a transition outside LP-Comp's scope, ASN-0077's closure could silently fail.

**Required**: Either (a) discharge the monotonicity portion via P3 (ArrangementMutabilityOnly, ASN-0047) — `dom(L) ⊆ dom(L')` is a per-transition invariant that is load-bearing without needing enumeration completeness — and rely on direct frame inspection only to identify K.λ as the unique non-trivial extension; or (b) enumerate transitions self-containedly from ASN-0047 + ASN-0093 without citing LP-Comp as the completeness witness.

### Issue 3: wp section opens "one wp" but presents two

**ASN-0077, Weakest precondition section**: "We compute one wp characterising what SHOWORIGIN reveals about state." (Followed shortly by: "A second wp characterises when a specific document is reported by SHOWORIGIN_V: ...")

**Problem**: Internal inconsistency between the opening assertion ("one wp") and the content (two wps).

**Required**: Change opening to "We compute two wp characterisations" or restructure so each wp is introduced with its own framing sentence.

### Issue 4: Second wp lacks explicit derivation

**ASN-0077, Weakest precondition section**: The first wp (single-origin output) is given a step-by-step derivation across numbered steps (1)–(4). The second wp (`d_q ∈ result`) is stated with only an interpretive gloss ("That is, the precondition that some block of the C1a decomposition of (d, σ) is sourced from d_q.") and no derivation.

**Problem**: Pedagogical asymmetry between the two wps. The second derivation is trivial but should be stated for parity with the first.

**Required**: Add a one-sentence derivation: "By (F1), `d_q ∈ origins_V(Σ, d, σ)` iff `∃v ∈ ⟦σ⟧ ∩ dom(M(d))` with `origin(M(d)(v)) = d_q`; since SHOWORIGIN_V's frame is `Σ' = Σ`, the post-state predicate equals the pre-state predicate, yielding the wp."

## OUT_OF_SCOPE

### Topic 1: Mixed-subspace I-span semantics

**Why out of scope**: OQ1 asks what SHOWORIGIN_I should guarantee when the input span crosses content and link subspaces. The ASN's design choice (silently drop link addresses from the I-span lift) is documented in the "Cross-subspace I-span" edge case; extending I-span queries to also report link origins is a future design extension, not a defect in this ASN.

### Topic 2: Transitive provenance / chain walking

**Why out of scope**: OQ2 and OQ3 ask about distinct operations — surfacing intermediate transclusion chains, or distinguishing natively-allocated from transcluded content. These are new operations belonging to future ASNs.

### Topic 3: Historical containment via Σ.R

**Why out of scope**: OQ5 asks about a complementary operation reading Σ.R for historical containment, explicitly distinguished from SHOWORIGIN in the "Three exclusions" section. An operation reading Σ.R is a future ASN.

VERDICT: REVISE
