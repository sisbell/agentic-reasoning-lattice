# Review of ASN-0098

The core mathematics is sound. I checked LP-Fin's interval-finitude argument (the `#d ≤ #d_0` bound, the zeros-prefix sub-cases A/B, the chain-index count of exactly `n`), the LP12a weakest-precondition derivation, the LP12b per-subspace disjointness chain, LP11's bijection rebinding and `ran` preservation, and both branches of the worked trace. These hold. The findings below are confined to forward-reference/meta-prose accretion the anti-bloat classifier asks me to surface.

## REVISE

### Issue 1: LP9's K.μ⁺_L paragraphs are defensive justification, not reasoning
**ASN-0098, LP9 ("K.μ⁺_L's additional constraints leave (E1) and (E2) intact")**: two paragraphs enumerate constraints (a)–(c) of K.μ⁺_L and then repeatedly assert they do not matter — "Each constraint restricts ... but does not alter the structural form," "do not modify the way Σ'.M(d) relates to Σ.M(d)," "LP9's argument consumes only (E1) and (E2); it is invariant under these constraint-level differences."
**Problem**: The load-bearing content is one sentence: K.μ⁺_L's effect clause supplies (E1) and (E2), so the LP9 argument applies verbatim. The enumeration of (a)–(c) followed by three restatements that they are irrelevant is exactly the defensive/exhaustiveness prose pattern — the reader must skip it to reach the actual derivation.
**Required**: Collapse to a single sentence: "K.μ⁺_L's effect clause `M'(d) = M(d) ∪ {v_ℓ ↦ ℓ}` with `dom(Σ'.M(d)) ⊃ dom(Σ.M(d))` supplies (E1) and (E2) directly, so the argument above applies unchanged." Drop the constraint inventory.

### Issue 2: LP8 closing sentence is a forward-reference justification of its own postconditions
**ASN-0098, LP8**: "Both postconditions are commitments — LP18 (resurrection) requires the well-defined empty projection through a newly-registered document until a K.μ⁺ or K.μ⁺_L fires; (a) and (b) together establish that no displacement occurs at registration time, neither at pre-existing documents nor at the new one."
**Problem**: The postconditions are already proved in the two preceding sentences. This trailer enumerates a downstream consumer (LP18) to motivate why the postconditions exist, which is the "definition/lemma justified by naming its downstream use" pattern. It does not advance LP8.
**Required**: Delete the sentence. If the LP18 dependency needs recording, it belongs in LP18's premises, not LP8's conclusion.

### Issue 3: "What the Link Holder Can Rely On" duplicates the Claims-Introduced table
**ASN-0098, section "What the Link Holder Can Rely On"**: a five-bullet recap that restates LP2★/LP3★/LP12/LP9–LP11/LP19 in holder-facing English.
**Problem**: Every bullet points back to lemmas already stated, and the same labels are catalogued in the "Claims Introduced" table. It is summary essay content occupying a structural slot; following any individual guarantee requires going back to the lemma anyway.
**Required**: Remove the section, or if a reader-facing index is wanted, fold its one genuinely synthetic point (storage vs. navigability are independently regulated — already made at LP13) into LP13 and drop the rest.

### Issue 4: The canonical-span caveat is restated four-plus times
**ASN-0098, tight definition / LP-Fin statement / LP-Fin table row / "Achievability (under canonical-ℓ assumption)" / "The analysis below restricts to canonical spans"**: the fact that non-canonical spans are definitionally non-tight and therefore out of LP-Fin's domain is asserted in at least five places, each in slightly different words.
**Problem**: Matches "two paragraphs say the same thing in different words," compounded. Once tightness is defined to require `ℓ = δ(n, #s)`, the exclusion of non-canonical spans is automatic and needs stating once.
**Required**: State the canonical restriction once at the tight definition; in LP-Fin and the achievability prose, reference it rather than re-deriving "non-canonical ⇒ non-tight."

### Issue 5: LP4 frame note enumerates downstream use-pattern
**ASN-0098, LP4 frame note**: "Downstream uses instantiate `d ∈ dom(Σ.M)` and lift to the intersection via M1 (ASN-0093), `dom(Σ.M) ⊆ dom(Σ'.M)`."
**Problem**: Use-site inventory — it describes how later lemmas consume LP4 rather than advancing LP4. The well-definedness rationale (first sentence of the note) is sufficient.
**Required**: Drop the second sentence; the M1 lift can be cited at the point of use (it already is, e.g., in LP5/LP6).

### Issue 6: Four near-identical multi-step closure inductions
**ASN-0098, LP2★, LP3★, Store Monotonicity★, LP13**: each carries the same boilerplate induction ("The empty sequence gives ... by reflexivity. For the inductive step ... by transitivity of equality the full chain holds").
**Problem**: The closure of a single-step preservation guarantee under `→*` is mechanical and identical across all four. Repeating the induction verbatim four times is scaffolding noise; LP13's content is moreover entailed by LP2★ together with arity preservation.
**Required**: State the induction schema once (e.g., at LP2★) and have LP3★, Store Monotonicity★, and LP13 cite it. Consider deriving LP13 from LP2★ rather than re-proving from L12.

## OUT_OF_SCOPE

### Topic 1: Reverse-discovery, V-order reflection, cross-document operation comparison
**Why out of scope**: These are correctly deferred to the Open Questions and concern primitives this ASN does not define; they are future ASNs, not gaps here.

META: not applicable — the ASN stays in abstract state/operation/invariant territory throughout; the findings are prose accretion, not drift.

VERDICT: REVISE
