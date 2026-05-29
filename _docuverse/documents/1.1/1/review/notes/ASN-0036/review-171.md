# Review of ASN-0036

The mathematics is sound. I checked the S8 partition proof (within- and across-subspace uniqueness via the incompatibility lemma, T5, T10), the D-CTG-depth infinite-intermediates construction, and the D-SEQ assembly — all cases close, boundaries (empty `dom(M(d))`, `m=2` vs `m≥3`, `j=m` divergence) are handled, and the worked example exercises S0/S3/S7/S8/D-SEQ across three states including deletion-orphaning. The findings below are accretion/clarity, consistent with this note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Forward-reference annotation in S2
**ASN-0036, S2 (Arrangement functionality)**: "even when its I-addresses are scattered across multiple documents' Istreams (the load-bearing case for the sharing analysis of S5)."
**Problem**: The parenthetical names a downstream consumer (S5) and labels the case "load-bearing" for it. This is use-site inventory — it does not advance what S2 *says* (each V-position has one image). A reader following S2 must skip past a pointer to a property defined three sections later.
**Required**: Delete the parenthetical. If the scattered-Istream observation matters to S2 itself, state it plainly without naming S5 or asserting downstream load-bearingness.

### Issue 2: Malformed definition sentence in S8a
**ASN-0036, S8a (V-position componentwise positivity)**: "Over the ℕ-carrier (T0), zeros(v) (T4) counts the components equal to 0, so the domain-restriction axiom's conjunct zeros(v) = 0 ⟺ (A i : 1 ≤ i ≤ #v : vᵢ > 0):"
**Problem**: The clause is a fragment — "the conjunct zeros(v) = 0 ⟺ ..." has no verb and runs directly into the displayed formula through a colon. The biconditional is presented as if it were the statement of S8a rather than the justification for it. The reader has to reconstruct the intended claim.
**Required**: Two sentences: "Over ℕ (T0), `zeros(v) = 0` iff every component is positive. Hence:" followed by the displayed formula.

### Issue 3: S8a postcondition restates the axiom verbatim
**ASN-0036, S8a, Postconditions**: "Together with the domain-restriction axiom, every `v ∈ dom(Σ.M(d))` satisfies `zeros(v) = 0 ∧ #v ≥ 2`."
**Problem**: S8a's genuine contribution is the componentwise-positivity form `(A i : vᵢ > 0)`. This postcondition re-asserts the domain-restriction axiom (`zeros(v)=0 ∧ #v≥2`) — the very thing S8a is derived *from* — adding no new content. It is restatement of an upstream axiom in a derived property's contract slot.
**Required**: Drop the restatement; S8a's postcondition is the componentwise-positivity form alone. Downstream consumers needing `#v ≥ 2` can cite the domain-restriction axiom directly.

## OUT_OF_SCOPE

### Topic 1: Operation-layer preservation of D-CTG/D-MIN/S2
The ASN states the contiguity invariants on well-formed states but does not show that INSERT/DELETE/COPY/REARRANGE preserve them (including insertion at an occupied `ValidInsertionPosition` with the consequent ordinal shift). This is correctly deferred — the Open Questions already name it and operation effects are listed out of scope. No error here; flagging only to confirm it belongs to a future operations ASN, not this one.

### Topic 2: Subspace-alignment between `subspace(v)` and the element field of `M(d)(v)`
Whether a V-position's `v₁` must match the first element-field component of its target I-address is treated as an operations-layer obligation (Open Questions). Belongs to a future ASN; not a gap in the state model.

VERDICT: REVISE
