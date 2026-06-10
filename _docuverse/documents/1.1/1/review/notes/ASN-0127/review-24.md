# Review of ASN-0127

The mathematics held up under a full re-derivation: I checked every derivation (F-IMG through D-ZERO), re-verified all seven reorder/contraction witnesses by computing the post-states and preimages by hand, confirmed the witness-admissibility argument against K.μ~'s five admissibility clauses, and confirmed the foundation citations (T10a.2, T7, Prefix, TA5(c), LP11–LP13, C1a, D-SEQ★) are applied within their preconditions. Two issues remain: one incomplete case sweep in the worked illustration, and two sentences of accreted meta-prose flagged under the anti-bloat classifier.

## REVISE

### Issue 1: The cardinality-changing variant's negative match check for L_2' skips slot 2

**ASN-0127, Worked illustration, swing under K.μ~ (cardinality-changing variant)**: "`L_2'` leaves the pre-state result untouched — its from-slot misses `{a_1}` (`coverage(e₁) ∩ {a_1} = subtree(a_2) ∩ {a_1} = ∅`, since `a_2 ⋠ a_1`) and its type slot misses as well (`coverage(e₃) ∩ {a_1} = subtree(a_θ) ∩ {a_1} = ∅`, as established above), so `findlinks_disc(W₀, d, Σ) = {L_1}` still"

**Problem**: The non-membership claim `L_2' ∉ findlinks({a_1}, Σ)` requires every slot of F-MATCH's existential to fail. `L_2' = ({a_2}, ∅, Θ)` has three slots; the sweep checks slots 1 and 3 and silently skips slot 2, the empty to-endset. The needed fact — `coverage(∅) = ∅`, the union over an empty span set — is true and immediate from the Coverage definition, but it is stated nowhere in the note, even though empty endsets appear twice (`L_3` and `L_2'`). This is a lapse from the note's own standard: the initial Phase-2 computation and the base swing both enumerate all three slots explicitly when establishing a non-match ("The other slots do not fire: both links' slot 2 is `{a_3}`, so `coverage(e₂) ∩ {a_1, a_2} = … = ∅`, and the type slot gives…"; "its slots — anchored at `a_1`, `a_3`, `a_θ` — all miss `{a_2}`").

**Required**: State once that `coverage(∅) = ∅` (empty union over no spans, per the Coverage definition), and include slot 2 in `L_2'`'s pre-state sweep — e.g., "(its empty to-endset has `coverage(∅) = ∅`, so slot 2 cannot fire)".

### Issue 2: Two sentences of meta-prose that restate or defend rather than advance

**ASN-0127, E-INV, final sentence of the derivation**: "LP3★ (ASN-0098) alone fixes per-slot coverage but not the arity bound `|Σ.L(a)|` over which the existential ranges; LP13 supplies both."

**Problem**: This defends the citation choice against a lemma the proof does not use. The preceding sentence already discharges the step and names exactly what LP13 supplies ("the middle equality discharged by LP13 (arity and per-slot coverage together)"). LP3★ appears nowhere else in the note; the sentence is a contrast with a road not taken — reviewer-directed prose, the accretion pattern this note is flagged for.

**ASN-0127, F-FULL, final sentence of the derivation**: "The composite's two boundaries are thereby pinned: an empty resolved region induces the empty comprehension (F-V, degenerate case), and a full region collects exactly the links discoverable from `d` — the region-indexed query recovers ASN-0098's per-document discovery set at the whole arrangement."

**Problem**: The first half repeats F-V's stated degenerate case verbatim in function; the second half repeats F-FULL's own statement line, which the derivation has just established. The sentence contributes no new content within the derivation slot — it is a restatement of two claims at their already-proper sites.

**Required**: Delete both sentences. No content relocation is needed — everything they say already exists where it belongs (the LP13 discharge inside E-INV's derivation; the empty boundary in F-V; the full-region equality in F-FULL's statement).

## OUT_OF_SCOPE

### Topic 1: Composite-boundary stability under coupling constraints
The note's stability lemmas quantify over elementary transitions, which is correct for its purpose (ASN-0047's per-state invariants hold at all elementary-reachable states, so D-SEQ★ etc. are available at every step the lemmas touch). A separate question is stability across *valid composites*, where J0/J1★ can force accompanying K.ρ or K.μ⁺ steps alongside the transition under analysis — e.g., a K.α inside a valid composite is necessarily followed by a placement.
**Why out of scope**: Q3 already asks for the uniform per-transition weakest precondition; the composite-level, coupling-aware version is a further layer of new territory, not an error in the elementary analysis here.

### Topic 2: Discovery sets across fork composites
How `findlinks_disc` behaves when J4's fork composite populates `d_new` with `d_op`'s content range (the transclusion-discovery situation LP16 touches per-link) — i.e., the relationship between the discovery sets of a document and its fork — is a natural next question once the per-document algebra here is fixed.
**Why out of scope**: it composes this note's primitives with the fork composite, which this note deliberately does not treat.

VERDICT: REVISE
