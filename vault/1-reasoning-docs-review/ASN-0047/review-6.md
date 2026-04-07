# Review of ASN-0047

## REVISE

### Issue 1: K.α preconditions embedded in prose, not formalized

**ASN-0047, Elementary transitions, K.α**: "The creating document origin(a) must be in E_doc — the allocation mechanism inc(·, k) operates within an ownership domain, requiring the document entity to exist before content can be allocated under its prefix."

**Problem**: K.δ is the only elementary transition with an explicit `*Precondition:*` block. K.α states `origin(a) ∈ E_doc` and `IsElement(a)` as prose observations within the body, not as formal preconditions. P6's derivation cites "origin(a) ∈ E_doc by precondition" — but K.α never designates it as such. The same inconsistency applies to K.μ⁺ (which calls S3, S8a, S8-depth, S8-fin "preconditions on the V-positions being added" in prose) and K.μ~ (which requires π to produce valid V-positions, stated in prose). Without explicit precondition blocks, a reader cannot distinguish formal preconditions from derived observations, and P6's inductive step is ungrounded.

**Required**: State preconditions for all six elementary transitions in the same format as K.δ. At minimum, K.α needs:

- `a ∉ dom(C)`
- `IsElement(a)` (S7b)
- `origin(a) ∈ E_doc`

### Issue 2: J1/J1' biconditional characterization overstated for re-addition

**ASN-0047, Coupling and isolation, J1'**: "Together they give a bidirectional coupling: K.ρ fires for (a, d) if and only if K.μ⁺ introduces a into d's arrangement in the same composite transition."

**Problem**: The backward direction fails when `(a, d) ∈ R` from a prior insertion-deletion cycle. Scenario: (1) K.μ⁺ introduces `a` into `d`, K.ρ records `(a, d)`; (2) K.μ⁻ removes `a` from `d`'s arrangement; (3) K.μ⁺ re-introduces `a` into `d`. At step (3), `a ∈ ran(M'(d)) \ ran(M(d))` — K.μ⁺ introduces. But `(a, d) ∈ R` already (from step 1, preserved by P2), so J1's requirement `(a, d) ∈ R'` is satisfied without K.ρ firing. The backward direction "K.μ⁺ introduces ⟹ K.ρ fires" fails.

The formal J1 and J1' are correct — J1 requires `(a, d) ∈ R'` (not that K.ρ executes), and J1' constrains `R' \ R` (genuinely new entries only). The imprecision is confined to the informal characterization.

The same imprecision propagates into P4's proof: "K.μ⁺ alone does not preserve the invariant" and "K.μ⁺ never occurs alone." In the re-addition case, K.μ⁺ alone *does* preserve P4 — `Contains(Σ') = Contains(Σ) ∪ {(a, d)} ⊆ R ∪ {(a, d)} = R = R'` — and K.μ⁺ *can* occur without K.ρ.

**Required**: Replace the biconditional with: "K.ρ produces a new entry `(a, d) ∈ R' \ R` if and only if K.μ⁺ introduces `a` into `d`'s arrangement and `(a, d) ∉ R`." In P4's K.μ⁺ case, split into two subcases: (i) `(a, d) ∉ R` — K.ρ must co-occur; (ii) `(a, d) ∈ R` — P4 is preserved by existing membership alone.

### Issue 3: Historical fidelity of R claimed without derivation

**ASN-0047, State model, Σ.R definition**: "This historical fidelity — that every entry reflects an actual past containment event, not merely eligibility — is not assumed by the definition alone; it is established by the bidirectional coupling J1 + J1' below."

**Problem**: The establishment is never given. The claim is a derived guarantee — it requires an inductive argument over transitions:

- *Base*: `R₀ = ∅`. Vacuously, every entry reflects a past event.
- *Step*: Each `(a, d)` entering `R` does so via K.ρ. By J1', `(a, d) ∈ R' \ R` implies `a ∈ ran(M'(d)) \ ran(M(d))` — so at recording time, `d`'s post-state arrangement contains `a`. That post-state is the past containment event. P2 preserves the entry; P0 preserves the content at `a`.

The pieces (J1', P2, P0) are all present, but the inductive chain connecting them to "every entry reflects a past event" is not shown.

**Required**: Add the inductive derivation, either as a named property or as an explicit paragraph following J1'.

## OUT_OF_SCOPE

### Topic 1: Version-arrangement coupling
**Why out of scope**: The ASN defines arrangement transitions but does not model version lineage. The relationship between version creation and arrangement snapshots is new territory, acknowledged in the open questions.

### Topic 2: Link-specific provenance and discoverability
**Why out of scope**: The ASN treats links uniformly as E_doc members and defers endset semantics. Whether contraction in one document affects link discoverability from another, and what additional permanence provenance needs for link endsets, are questions about link structure — not about the state transition taxonomy defined here.

VERDICT: REVISE
