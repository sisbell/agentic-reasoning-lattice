# Review of ASN-0047

## REVISE

### Issue 1: Property-definition slots carry downstream-bookkeeping meta instead of meaning
**ASN-0047, *Coupling and isolation* (P4★)**: "P4★ is a Class (b) composite-boundary property. Validity of a composite transition `Σ →* Σ'` is ValidComposite★. P4★ is discharged at composite boundaries by clause (2)'s couplings."

**Problem**: These three sentences sit in the slot that defines P4★ but say nothing about what the bound `Contains_C(Σ) ⊆ R` *means* — they preview the property's proof-class and its discharge mechanism, both defined elsewhere (*Extended reachable-state invariants*, ValidComposite★). A reader trying to understand P4★ must skip past classification bookkeeping to reach the claim. This is the explicitly-flagged pattern: a definition's introduction enumerating downstream consumers rather than advancing the definition's meaning. The same accretion recurs at sibling definitions:
- **P7a**: "It is a composite-boundary property (Class (b) of ExtendedReachableStateInvariants)."
- **S8★**: "S8★ takes the place of ASN-0036's S8 in ExtendedReachableStateInvariants, applied per-subspace to each projection. The S8★ conjunct of ExtendedReachableStateInvariants is the conjunction of S8★(s_C) … and S8★(s_L)…"

**Required**: Keep each property's bound/statement and its substantive rationale (e.g. P4★'s content-subspace scoping for P7-coexistence). Move the "is a Class (b) property / is discharged by clause (2) / is the conjunct of X" bookkeeping to the single section that owns that classification (*Extended reachable-state invariants*), where it is already restated. The definition slots should carry meaning, not proof-index previews.

### Issue 2: Derivation/statement split for J1★ and J1'★ forces forward-and-back tracking
**ASN-0047, *Coupling and isolation***: "The K.ρ/K.μ⁺ coupling is range-based … see J1★ in *Scoped coupling constraints* below." The wp-derivations of J1★ and J1'★ (in *Scoped coupling constraints*) in turn run "backward from P4★" and "backward from P4a (stated above)," while their formal statements J1★/J1'★ are interleaved among those derivations and P4a/P4★ live back in *Coupling and isolation*.

**Problem**: To follow the J1'★ derivation a reader must simultaneously hold P4a (defined in the prior section), P4★ (prior section), and ValidComposite★ (a later section) — the argument is distributed across three section boundaries with forward and backward pointers crossing each. This is the "multiple paragraphs deferring to the same downstream location" pattern: the coupling story is genuine but its presentation is scattered enough that the load-bearing chain (P4★/P4a → wp → J1★/J1'★ → ValidComposite★ clause 2) cannot be read in one pass.

**Required**: Co-locate each coupling's *statement* and its *wp-derivation*, and place P4★/P4a immediately adjacent to the derivations that consume them, so the wp-chain reads top-to-bottom without forward jumps. This is a local re-anchoring of already-present prose, not a content change.

## OUT_OF_SCOPE

### Topic 1: Interior link-arrangement contraction with renumbering
The ASN's K.μ⁻ contracts the link subspace by suffix removal only; the implementation's interior `DELETEVSPAN` compacts-and-renumbers. This is correctly held for a future ASN (already listed as an open question) and is not an error here — K.μ⁻'s suffix-only contraction is a coherent abstract operation on its own terms.

### Topic 2: One-sided / type-only links (`e₁ ∪ e₂` emptiness)
Whether K.λ should require non-empty from/to endsets is a genuine modeling question, properly deferred to the listed open question rather than resolved here.

VERDICT: REVISE
