# Review of ASN-0036

## REVISE

### Issue 1: S8a carries downstream-consumer justification and restates the domain-restriction axiom

**ASN-0036, S8a (V-position componentwise positivity and depth)**: "The domain-restriction axiom also fixes a depth floor `#v ≥ 2`, which S8a re-exports so downstream consumers cite a single carrier for both facts."

**Problem**: This is meta-prose of exactly the kind the anti-bloat pass targets — it explains *why the claim exists* (so consumers cite one carrier) rather than advancing what the claim says. Compounding it, S8a's content is logically equivalent to the existing domain-restriction axiom (`zeros(v) = 0 ∧ #v ≥ 2`): given T0's ℕ-valued components, `zeros(v) = 0 ⟺ (A i : vᵢ > 0)`. S8a's only novelty is the per-component phrasing; the "re-export" framing dresses a thin restatement as a structural contribution. The Properties-table entry repeats the framing ("re-exporting the domain-restriction axiom's `zeros(v) = 0` (per-component form) and `#v ≥ 2`").

**Required**: Strike the "re-exports so downstream consumers cite a single carrier" justification. State S8a as what it is — the per-component form of the domain-restriction axiom, equivalent by T0 — without narrating its intended use sites. Trim the table entry to match.

### Issue 2: S5 existence construction is not verified to be a well-formed strand state

**ASN-0036, S5 (proof, cross-document construction)**: "`C_N = {a ↦ w}` for a single I-address `a` and arbitrary value `w ∈ Val`." and (opening) "each construction need only verify the genuine state predicates S2 and S3 together with the multiplicity count."

**Problem**: The proof restricts its verification to S2 and S3, but a legitimate state `Σ` in this model must also satisfy the always-on state-level requirements — the domain-restriction axiom on `Σ.M(d)`, S8-fin, and crucially S7b (`zeros(a) = 3` for every `a ∈ dom(C)`). The witness `a` is introduced as "a single I-address" with no commitment that `zeros(a) = 3`; an element-level address is never exhibited. If `Σ` is meant to be a system state, the construction is under-specified and may not be reachable; if `Σ` is merely a bare model of the four predicates S0–S3, the claim should say so, since "There exists a state `Σ` satisfying S0–S3" reads as a full strand state. (The chosen `dᵢ = [1,0,1,0,i]` and V-positions `[1,k]` do happen to satisfy the document and domain-restriction constraints, but this is asserted nowhere.)

**Required**: Either (a) instantiate `a` with an explicit element-level address (e.g. `a = 1.0.1.0.1.0.1.1`, `zeros = 3`) and verify the witnessing states satisfy the domain-restriction axiom, S7b, S8-fin, and S8a — making them genuine strand states — or (b) state explicitly that S5 is a relative-consistency result over the bare predicates S0–S3 and that well-formedness invariants are deliberately not imposed. Pick one and make the verification scope explicit rather than narrowing silently to S2/S3.

## OUT_OF_SCOPE

### Topic 1: Operation-layer preservation of D-CTG/D-MIN/S2 under INSERT/DELETE/COPY/REARRANGE
**Why out of scope**: The ASN states the contiguity invariants and the ValidInsertionPosition predicates as state-level characterizations; whether each editing operation preserves them is operation-specific (explicitly out of scope) and correctly deferred to the open questions and a future operations ASN.

### Topic 2: Subspace-alignment between `subspace(v)` and the I-address subspace component
**Why out of scope**: The note records this as an operations-layer preservation obligation rather than a state invariant; it is new territory, not an omission in the strand-state model.

VERDICT: REVISE
