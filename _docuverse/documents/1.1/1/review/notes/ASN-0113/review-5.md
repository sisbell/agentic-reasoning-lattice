# Review of ASN-0113

## REVISE

### Issue 1: W15's independence derivation rests on a false universal premise about K.μ⁻

**ASN-0113, "Invariants across the members" (W15, Independence)**: "Because every transition that adds or removes a V-position acts within one subspace, a content edit cannot alter `V_{s_L}(d)` and a link edit cannot alter `V_{s_C}(d)`." The supporting text also states K.μ⁻ "contracts under a per-subspace retention count, removing positions only from the subspace it targets."

**Problem**: This mischaracterizes the foundation operation. ASN-0047's K.μ⁻ (per-subspace scope) selects a retention count `n'_S` *for each* `S ∈ {s_C, s_L}` and contracts to `R := ∪_{S ∈ {s_C, s_L}} {[S,1,…,1,k] : 1 ≤ k ≤ n'_S}`, "subject to at least one S admitting strict contraction." A single K.μ⁻ transition may therefore strictly contract *both* the text run and the link run at once — it does not act "within one subspace," and does not target only one. The universal premise "every transition that adds or removes a V-position acts within one subspace" is false.

**Required**: Correct the derivation. The independence conclusion still holds, but for a different reason: `n_S(d) = |V_S(d)|` is a function of `V_S(d)` alone (W1) because membership is decided by the predicate `v₁ = S`, so the two counts are read off disjoint position sets. A transition that changes both counts (like a both-contracting K.μ⁻) changes each through its own subspace's positions, with neither change forcing the other. The "edit confined to one subspace leaves the other unchanged" statement is fine as a conditional, but it must not be justified by the false claim that all transitions are single-subspace.

### Issue 2: The single-occupied-subspace result is never concretely exercised

**ASN-0113, "A worked instance" / W7**: the only worked instance is a both-subspaces-occupied document (five characters, two links), yielding a two-member span-set. W7's central claim is that the result has exactly `|occupied(d)|` members.

**Problem**: The operation's whole thesis is cardinality — "the difference between one span and several is the whole subject of this note." The result-cardinality boundaries are 0 (`⟨⟩`, W0), 1 (single occupied subspace), and 2 (worked). The one-member case — a text-only document with no links, the default state of a freshly populated document — is the boundary between `⟨⟩` and the two-member report and is never instantiated against specific tumblers. "Boundary cases mandatory" and the concrete-example standard both point at it.

**Required**: Add a concrete one-member instance (e.g., a text-only document) verifying W3, W4, W7 (`|occupied(d)| = 1`), and W13 (single-member normal form), confirming the result is `⟨ext(d, s_C)⟩` and that the absent link subspace yields no member while `n_{s_L}(d) = 0` as a fact about `V_{s_L}(d)` (W14).

## OUT_OF_SCOPE

### Topic 1: Consumer interpretation of an omitted (empty) member across document vintages
**Why out of scope**: Open Question 2 correctly defers this. How a *consumer* reads an absent member as "extent zero" versus "subspace unsupported" is consumer-side convention, not a guarantee this query operation must establish; the note explicitly declines to rely on it.

### Topic 2: Relationship to the single overall extent (RETRIEVEDOCVSPAN / ASN-0112)
**Why out of scope**: Listed in the ASN's own scope exclusions and raised as Open Question 5; cross-consistency with the whole-document bound belongs to that operation's note.

META: not applicable — the ASN stays in specification territory, defining the query's result type, per-member coverage guarantees, and cross-member invariants abstractly, with implementation traces used only as confirming evidence.

VERDICT: REVISE
