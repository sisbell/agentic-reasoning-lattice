# Review of ASN-0113

## REVISE

### Issue 1: W5 biconditional is false for an empty subspace
**ASN-0113, "Exactness is contingent on contiguity" (W5)**: "*there exists* a single level-uniform span `σ` of subspace `S` at depth `m` satisfying `⟦σ⟧ ∩ VSlice(S, m) = V_S(d)` *if and only if* `V_S(d)` is contiguous in `VSlice(S, m)`."

**Problem**: The statement carries no non-emptiness hypothesis, but the forward proof silently assumes one ("Let `V_S(d)` be contiguous *and non-empty*"). For empty `V_S(d)` the biconditional breaks: the RHS ("contains every V-slice tumbler between its own minimum and maximum") is vacuous/ill-defined (no min or max), while the LHS is *false* — any level-uniform span "of subspace `S` at depth `m`" contains its own start, a depth-`m` subspace-`S` tumbler in `VSlice(S, m)`, so `⟦σ⟧ ∩ VSlice(S, m) ≠ ∅`, and no span can denote `∅` (S2, ASN-0053). So a vacuously-contiguous empty run admits no exact span, contradicting the claimed iff. The empty subspace is exactly the boundary case W0/W7 take pains to handle elsewhere, so it cannot be left implicit here.

**Required**: Add `V_S(d) ≠ ∅` to W5's hypotheses (the proof already relies on it), and state the empty case separately as it is handled in W0.

### Issue 2: No weakest-precondition characterization of the result shape
**ASN-0113, throughout**: the note derives consequences (W12, W14–W19) and supplies concrete instances, but gives no weakest-precondition analysis.

**Problem**: The operation has a genuinely non-trivial result-shape that depends on state — `⟨⟩` (both subspaces empty), one member (exactly one occupied), two members (both occupied) — yet the conditions under which each arises are never assembled into a wp statement. The standard asks for a non-trivial wp case rather than only trivially-true ones; for a pure query the informative wp is precisely the state-characterization of the result's cardinality (e.g. `wp(RETRIEVEDOCVSPANSET(d), "result = ⟨⟩") ≡ d ∈ dom(M) ∧ V_{s_C}(d) = ∅ ∧ V_{s_L}(d) = ∅`, and the two-member analogue). The ingredients exist scattered across W0/W6/W7 but are never derived as a precondition.

**Required**: Add an explicit wp characterization for at least the non-trivial result-cardinality cases, derived from W6/W7 and W-pre.

## OUT_OF_SCOPE

### Topic 1: Consumer interpretation of an omitted (empty) member
W14 and Open Question 2 raise how a *consumer* should read an absent member as "extent zero" vs "subspace unsupported." This is a cross-document/versioning concern belonging to a future ASN, and the note correctly defers it rather than relying on it.

### Topic 2: Permanence across version fork / transclusion
The Open Questions on fork-shared content and transclusion are genuinely new territory (version comparison, transclusion edits), not gaps in this query's own guarantees.

VERDICT: REVISE
