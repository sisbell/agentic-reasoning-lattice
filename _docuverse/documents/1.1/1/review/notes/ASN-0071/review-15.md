# Review of ASN-0071

The mathematics here is unusually careful — the subspace-confinement argument (`actionPoint(ℓ) ≥ 2` ⟹ `t₁ = u₁` via TumblerAdd prefix-copy plus T1 trichotomy), the link/content disjointness routing through L14, the resolve-equivalence via C1a/B1/B3, and the infinite-`⟦σ⟧`/finite-intersection handling are all spelled out rather than hand-waved. I found one concrete defect.

## REVISE

### Issue 1: Worked scenario is not reachable as stated

**ASN-0071, "A worked scenario"**: "Start from `Σ₀` and apply the following transitions of ASN-0047 (each precondition is discharged by the prior state…)" followed by step 1: "K.δ creates document `d_A ∈ E_doc`".

**Problem**: The claim "each precondition is discharged by the prior state" is false at step 1. `Σ₀` has `E₀ = {n₀}` with `Node(n₀)`, so `(E₀)_doc = ∅` and `(E₀)_account = ∅`. Creating a document `d_A` requires K.δ case (ii) with `k = 2` (descent), whose precondition is `parent(e) ∈ E`. For `Document(d_A)` (`zeros = 2`), `parent(d_A)` is the *account* prefix, and P8 (EntityHierarchy) requires that account `∈ E`. No account exists at `Σ₀`. The same gap recurs at steps 5 and 8. The scenario therefore cannot fire from `Σ₀` as narrated, undermining the very thing the section is meant to do — verify the F-claims against a *reachable* concrete state.

**Required**: Either (a) insert the missing K.δ steps that mint a node descendant → account → document chain (`n₀ → A → d_A`) before step 1, discharging `parent ∈ E` at each document creation, or (b) restate the starting point as a state `Σ_pre` already containing a node and account under which `d_A`, `d_B`, `d_C` are descended, and drop the "start from `Σ₀` / each precondition discharged by the prior state" phrasing. As written, the precondition-discharge claim is incorrect.

## OUT_OF_SCOPE

(none)

VERDICT: REVISE
