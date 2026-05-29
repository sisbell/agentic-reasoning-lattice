# Review of ASN-0036

## REVISE

### Issue 1: S8a presents a domain-membership axiom as a derived postcondition

**ASN-0036, S8a (V-position well-formedness)**: Postcondition `(A v ∈ dom(Σ.M(d)) :: zeros(v) = 0 ∧ #v ≥ 2 ∧ ...)`, with proof "From the Definition, `zeros(v) = 0` and `#v ≥ 2` hold directly."

**Problem**: The Definition states what a V-position *is* (`zeros(v) = 0 ∧ #v ≥ 2`). The proof then applies this to an arbitrary `v ∈ dom(M(d))` — but that step is valid only if every element of `dom(M(d))` is a V-position. That bridge ("arrangements map only V-positions") is never stated as an axiom; it is silently assumed and then re-presented as a derived conclusion. The first two conjuncts of the postcondition are therefore not derived — they *are* the unstated axiom. Only componentwise positivity is genuinely derived (via T0 + NAT-discrete). This is mildly circular: the postcondition asserts that `dom(M(d))` consists of V-positions, and the "proof" presupposes exactly that.

**Required**: State `dom(Σ.M(d)) ⊆ {t : zeros(t) = 0 ∧ #t ≥ 2}` as an explicit axiom (e.g., part of the Σ.M(d) contract, alongside `Σ.M(d) : T ⇀ T`). Then S8a's only proved content is positivity, and the proof should be scoped to that.

### Issue 2: Forward-reference meta-prose and tangents that do not advance the local claim

**ASN-0036, S2 Frame**: "Distinct V-positions may map to the same I-address (sharing — S5); injectivity is *not* asserted."
**ASN-0036, S1 prose**: "(Gregory's reclamation machinery exists but is deactivated, consistent with this absence.)"

**Problem**: The S2 frame line previews S5 rather than constraining S2; the non-injectivity remark is a forward pointer, not part of S2's functionality claim. The S1 parenthetical about reclamation machinery is an implementation tangent that adds nothing to the monotonicity argument. Per the note's `review-mode.anti-bloat` classifier, these are the accreted forward-reference / use-site asides flagged for removal.

**Required**: Drop the S5 forward pointer from S2's frame (non-injectivity is established where S5 lives). Remove the reclamation-machinery parenthetical from S1.

### Issue 3: Redundant example sections

**ASN-0036, "Concrete example" (after D-SEQ) vs. "Worked example" (d₁/d₂)**

**Problem**: The "Concrete example" verifies D-CTG/D-MIN/S8 on a contiguous depth-2 text arrangement `{[1,1]↦a₁,[1,2]↦a₂,[1,3]↦a₃}`; the "Worked example" Σ₁ verifies the same properties on the depth-2 "hello" arrangement. The two sections demonstrate the same checks on near-identical contiguous arrangements in different words. The depth-3 and violation cases in "Concrete example" are non-redundant and worth keeping; the depth-2 D-CTG/D-MIN walkthrough duplicates Σ₁.

**Required**: Consolidate — keep one depth-2 demonstration and the depth-3/violation cases; fold the lifecycle (S0/S3/S5/S7) demonstration into the single retained worked example rather than maintaining two parallel contiguous-arrangement checks.

## OUT_OF_SCOPE

### Topic 1: Operation preservation of D-CTG/D-MIN/S2 under INSERT/DELETE/COPY/REARRANGE
**Why out of scope**: The note correctly defers operation-specific frame/postconditions (Scope list; Open Questions). The state-level invariants and the ValidInsertionPosition predicates here are the right abstract substrate; the preservation proofs belong in the operations ASN.

### Topic 2: Canonical choice of V-position depth `m` and subspace-alignment enforcement
**Why out of scope**: The ASN explicitly fixes only `m ≥ 2` and names depth-selection and subspace alignment as operation-layer obligations (Open Questions). New territory, not an error here.

VERDICT: REVISE
