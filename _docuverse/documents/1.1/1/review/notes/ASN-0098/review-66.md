# Review of ASN-0098

This is a carefully constructed note. The core projection machinery (LP2–LP21) is mechanically sound: the growth/shrink/rebind lemmas track `Σ.M(d)` faithfully, boundary cases (empty endset, empty arrangement, `R = ∅`) are addressed, and LP-Fin's interval-finitude proof is genuinely worked through case by case rather than hand-waved. My findings are one citation-precision error and several instances of the meta-prose the anti-bloat classifier targets.

## REVISE

### Issue 1: LP12a attributes arity invariance to the wrong lemma
**ASN-0098, LP12a derivation**: "using LP2 (which fixes both `a ∈ dom(Σ'.L)` and `|Σ'.L(a)| = |Σ.L(a)|`) to keep the slot index range stable"
**Problem**: LP2, as stated (both in prose and in the Claims table), establishes only address persistence `a ∈ dom(Σ'.L)` and *per-slot* equality `Σ'.L(a).eᵢ = Σ.L(a).eᵢ`. It does not state arity invariance `|Σ'.L(a)| = |Σ.L(a)|`. Arity preservation comes from L12's full value equality `Σ'.L(a) = Σ.L(a)` — which is exactly how LP13 derives it ("value preservation under L12 forces equal-length sequences"). LP12a genuinely *needs* arity invariance to lift the per-slot biconditional existentially over `1 ≤ i ≤ |Σ.L(a)|` with a stable index range, so the miscitation is load-bearing, not cosmetic.
**Required**: Cite L12 (or LP13) for the `|Σ'.L(a)| = |Σ.L(a)|` clause; LP2 supports only the membership and per-slot conjuncts.

### Issue 2: "Architectural significance / lever" essay prose in structural slots
**ASN-0098, Discovery-Independence opener and LP19 closing paragraph**: "The transclusion mechanism is the architectural lever that activates this provenance-indifference." / "The architectural significance of LP19 is that the canonical construction … produces tight endsets …"
**Problem**: These are interpretive essay sentences sitting in the reasoning flow. The first restates LP16's content as motivational framing; the second editorializes on LP19 rather than advancing a claim. (By contrast, the adjacent sentence "Boundary insertion as a composite (K.α + K.μ⁺) cannot enlarge a tight link's reach" is a statement of what the operation does — keep that.) The reader must skip the "architectural" framing to reach the operative content.
**Required**: Delete the "architectural lever" and "architectural significance" sentences; let LP16 and LP19 carry their own weight.

### Issue 3: LP12a re-enumerates K.μ⁻'s precondition (foundation content)
**ASN-0098, LP12a**: "where `enabled(K.μ⁻[d, R])` is K.μ⁻'s applicability predicate — `d ∈ E_doc`, `dom(Σ.M(d)) ≠ ∅`, the strict-shrink admissibility `(E S :: n'_S < n_S)`, and `R` a valid D-SEQ★ prefix set — under which the post-state … exists."
**Problem**: This re-states K.μ⁻'s precondition, which ASN-0047 already fixes. Spelling out the four conjuncts here is the "new prose around an [operation] explaining its applicability rather than what the claim says" pattern. The wp statement needs only the *symbol* `enabled(K.μ⁻[d, R])`.
**Required**: Replace the inline enumeration with a bare reference: `enabled(K.μ⁻[d, R])` is K.μ⁻'s applicability predicate (ASN-0047).

### Issue 4: Redundant "Working reference frame" and Nelson-correspondence framing
**ASN-0098, "Working reference frame" one-liner and the "Nelson correspondence" paragraph closing the Resurrection section**
**Problem**: The "Working reference frame" sentence ("This ASN operates in the ASN-0047 transition-model frame layered over the ASN-0093 allocation substrate") duplicates the State-Components section, which already names both foundations operationally. The Nelson-correspondence paragraph restates LP16/LP18/LP12a in informal terms — a use-site inventory of "which lemma discharges which informal claim." Neither advances the argument; both are orientation/recap.
**Required**: Drop the "Working reference frame" line (the dependency is established where the stores are introduced). For the Nelson paragraph, either cut it or compress to a single sentence — it should not re-narrate three lemmas already proved.

## OUT_OF_SCOPE

### Topic 1: Reverse discovery, V-order reflection, cross-document operation comparison
**Why out of scope**: The Open Questions section already defers these (reverse-discovery primitive, V-order vs I-order under K.μ~, identical-projection guarantees across "same" operation sequences). They are correctly future territory — projection displacement is fully characterized here without them, and each would introduce new state/operations rather than fix a gap in LP2–LP21.

### Topic 2: Link-canonical contraction discoverability
**Why out of scope**: The final Open Question (link-canonical endset under content-subspace-emptying contraction, where LP12b's disjointness argument inverts) is the correct placement — LP12b honestly scopes itself to the content-canonical case and flags the link-canonical case as not yet discharged, rather than overclaiming.

VERDICT: REVISE
