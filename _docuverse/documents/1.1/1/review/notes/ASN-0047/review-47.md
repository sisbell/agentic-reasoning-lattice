# Review of ASN-0047

## REVISE

### Issue 1: L3 amendment weakens foundation without semantic justification

**ASN-0047, Link store and extended system state**: "ASN-0043's non-empty type-endset clause (`Σ.L(a).e₃ ≠ ∅`) is dropped: the udanax-green implementation silently accepts empty Θ, and the Endset definition above (`𝒫_fin(Span)`) admits `∅` as a well-formed endset."

**Problem**: The ASN weakens a foundation invariant (ASN-0043's L3 required non-empty type endset) using implementation precedent as the sole justification. What does an empty type endset mean semantically? Is it an untyped link, a sentinel for "no type", or a degenerate case the spec should forbid? The implementation accepting it doesn't establish that it's correct for it to do so. The L3 arity narrowing (N≥3 → N=3) is a strengthening and is fine; the type-endset weakening is a different matter — it lets K.λ produce links that violate ASN-0043's L3.

**Required**: Either restore the non-empty type endset requirement, or explain the semantic meaning of an empty type endset and why the abstract specification admits it.

### Issue 2: K.δ precondition for nodes contradicts the analysis text

**ASN-0047, K.δ definition**: "For non-root entities, the address is produced by a T10a-conforming allocation event (TA5, ASN-0034)..." applies uniformly to all non-root entities.

**Problem**: The subsequent analysis explicitly contradicts this for nodes: "node creation, however, is *not* constrained to a single inc(·, k) operation under a single owner... The abstract specification leaves the protocol mechanism unspecified — any allocator satisfying the namespace property `e ∉ E` suffices." NodeUniqueAllocation is then introduced as a separate axiom precisely because T10a doesn't underwrite node uniqueness. So non-root nodes don't necessarily satisfy the stated precondition. A reader applying the precondition literally would reject the global granfilade case Gregory describes.

**Required**: Restructure the K.δ precondition to handle nodes and non-nodes separately — T10a-conforming for non-nodes (with parent(e) ∈ E), and NodeUniqueAllocation-satisfying for nodes.

### Issue 3: L-fin omitted from ExtendedReachableStateInvariants theorem

**ASN-0047, ExtendedReachableStateInvariants theorem**: The conjunction lists L0, L1, L1a, L1b, L3, L12, L14, CL-OWN but not L-fin.

**Problem**: ASN-0043's L-fin (`|dom(Σ.L)| < ∞`) is a state invariant preserved by every transition (K.λ adds one address; all others hold L in frame; L₀ = ∅). The proof structure already establishes finiteness implicitly, but the theorem statement does not list L-fin among the preserved invariants. ASN-0036's S8-fin is included; the parallel link-store invariant is dropped.

**Required**: Add L-fin to the theorem's conjunction with a brief inductive argument, or document why it is omitted.

### Issue 4: Missing wp analysis for content/link coupling asymmetry

**ASN-0047, Orphan links and coupling flexibility**: "We do not add a J0 analog for links — the orphan state is architecturally intentional, satisfying both the permanence guarantee (L12: links are immutable once created) and the owner's right to withdraw (Nelson, LM 2/29)."

**Problem**: J1 is derived by explicit wp analysis showing K.μ⁺ alone cannot maintain Contains_C(Σ) ⊆ R, forcing K.ρ to co-occur. J0 is then necessitated by P7a (every I-address has provenance, requiring placement of fresh content). The parallel reasoning for links is absent. The ASN cites design intent, but doesn't show that no invariant *requires* link placement. The asymmetry should be derived: there is no link-provenance invariant analogous to P4★/P7a, hence no wp pressure on K.λ.

**Required**: State explicitly that no link-provenance invariant analogous to P4★/P7a exists (and why this is acceptable — links carry their own permanence guarantee via L12, while orphan content would lose history irretrievably), so no J0-analog is required. Make the absence invariant-driven rather than design-asserted.

### Issue 5: K.μ⁻ precondition forward-references D-SEQ★ before its derivation

**ASN-0047, K.μ⁻ amendment Precondition**: "Admissible removal (per-subspace suffix or full-subspace clearance). For each non-empty subspace S in M(d), the input arrangement has a contiguous, minimum-anchored, uniform-depth range — a structural property established self-containedly in this precondition by the conjunction of D-CTG, D-MIN, S8-depth, S8-fin, and S8a."

**Problem**: The precondition declares a "self-contained" structural form `V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n_S}` and then explicitly says this same form is named D-SEQ★ and derived later. The ASN acknowledges the forward reference ("Reading order: the precondition here uses the structural form as a self-contained statement; the Amendments section formalises and derives that same form (under the name D-SEQ★)"), but a precondition that relies on a multi-step derivation (an infinite-cardinality contradiction against S8-fin, plus a separate contiguity argument) is not self-contained in any meaningful sense — the reader must trust the later derivation works.

**Required**: Either move the D-SEQ★ derivation to precede the K.μ⁻ amendment, or replace K.μ⁻'s structural-form precondition with the underlying conjuncts (D-CTG, D-MIN, S8-depth, S8-fin, S8a all hold at the input state) plus a citation of D-SEQ★ as a derived lemma. The current "self-contained" framing obscures the dependency rather than eliminating it.

VERDICT: REVISE
