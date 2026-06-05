# Review of ASN-0110

## REVISE

### Issue 1: No concrete worked example
**ASN-0110, throughout**: The note defines `retrieveendsets`, `Eᵢ`, `W`, and proves RE-exact, RE-full, RE-role, RE-anon, etc., but never verifies these against a single specific scenario.
**Problem**: The constructions in RE-anon and RE-empty are existence proofs, not a worked instance. Standard 6 makes a concrete example mandatory: pick a specific region `I` (or V-region `R` in a document `d`), populate `Σ.L` with at least two links of stated arity and endset spans — including one whose endset has a *non*-touching span and a touching span — and walk the result. This is the only way to exercise RE-full (whole-not-clipped) and RE-role (slot filing, same endset value under two roles) against actual data rather than prose.
**Required**: Add one fully instantiated scenario with concrete tumblers, computing `W(I, Σ)`, each `Eᵢ(I, Σ)`, and checking RE-full and RE-role on it.

### Issue 2: Role-index range of the returned family is underspecified
**ASN-0110, RE-result**: "`retrieveendsets(I, Σ) = ⟨E₁(I, Σ), E₂(I, Σ), E₃(I, Σ), …⟩`" and "for `N`-ary links the family simply runs to `N`."
**Problem**: With a heterogeneous store (links of arity 3, 5, 7), the tuple length is not pinned. Does the family run to the maximum arity among *all* links, among *touching* links, or is it the total function `i ↦ Eᵢ`? It also leaves unclear whether a slot `i` with `Eᵢ = ∅` (e.g. an arity-4 link present but none of its slot-4 endsets touch) occupies a position in the returned tuple. Since the operation returns a finite object, its arity must be determined.
**Required**: State the index range explicitly — e.g. define the result as the function `i ↦ Eᵢ(I, Σ)` for `i ≥ 1` (eventually empty), or fix the tuple length to `max{|Σ.L(a)| : a ∈ dom(Σ.L)}` — and say whether empty role-slots are reported.

### Issue 3: No weakest-precondition analysis
**ASN-0110, throughout**: The note proves monotonicity and survivability but offers no wp analysis.
**Problem**: Standard 6 requires a non-trivial wp case, not merely the trivial frame `Σ' = Σ`. A genuine case exists: for a `K.λ` allocation step `Σ → Σ'`, compute `wp(K.λ, "e ∈ E₁(I, Σ')")` — i.e. what must hold of the allocated link value for a given endset to enter the role-1 result — and contrast it with the unconditional persistence of already-present touching endsets (RE-mono). This is the analogue of F9-λ in ASN-0099 and would sharpen the conditional-idempotence claim in RE-det.
**Required**: Add a wp derivation for at least one non-trivial postcondition (result growth under `K.λ`, or non-emptiness of a role family).

## OUT_OF_SCOPE

### Topic 1: V-space presentation of a partially-arranged endset
The note's first open question (what the system must guarantee when a querying document arranges only part of an endset's coverage) is correctly deferred. The lossy V-presentation contract is genuinely new territory, not an error here.

### Topic 2: Sub-region / super-region invariants beyond additive union
The second open question (relating endsets returned for a region to those for its sub/super-regions beyond RE-add) is future work, not a gap in this ASN.

VERDICT: REVISE
