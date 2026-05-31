# Review of ASN-0093

## REVISE

### Issue 1: Anchor structural identities depend on SubspaceConventionAxiom but cite only TA5

**ASN-0093, "Address sub-allocators under documents"**: "These anchors are structurally producible by T10a `inc` steps from `d`: `b_C(d) = inc(d, 2) = [d.0.s_C]` (TA5(d), `k = 2`) and `b_L(d) = inc(b_C(d), 0) = [d.0.s_L]` (TA5(c))."

**Problem**: Both identities are load-bearing and both silently consume the SubspaceConventionAxiom, yet cite only TA5.
- `inc(d, 2)` appends `[0, 1]` (TA5(d)), giving `[d.0.1]`. Identifying the final `1` with `s_C` requires `s_C = 1`.
- `inc(b_C(d), 0)` increments the sig component of `[d.0.s_C]` to `s_C + 1` (TA5(c)). Identifying `s_C + 1` with `s_L` requires `s_L = s_C + 1`.

Both equalities come from SubspaceConventionAxiom, not from TA5. The link sub-allocator anchor in particular *cannot* be produced by `inc(b_C(d), 0)` unless the two subspace identifiers are consecutive — a genuine dependency. The FirstEmission lemma compounds this by disposing of the link case as "symmetric," which hides the non-symmetric `s_L = s_C + 1` step (the content anchor reaches `b_C(d)` by `inc(d,2)`, the link anchor reaches `b_L(d)` by a sibling `inc(·,0)` off `b_C(d)` whose result-value identification rests on the axiom). The worked example (Step 3) does note "By SubspaceConventionAxiom, `s_L = 2 = s_C + 1`," confirming the dependency is real — but the general construction omits it.

**Required**: Cite SubspaceConventionAxiom alongside TA5 at both anchor identities, and replace "the link case is symmetric" in FirstEmission with an explicit note that `b_L(d) = inc(b_C(d), 0) = [d.0.s_L]` consumes `s_L = s_C + 1`.

### Issue 2: C2 / L1a subsequent-emit discharge claims `origin(a) = d` is "pinned" when it is derived

**ASN-0093, "Discharge" matrix, C2 row**: "K.α: Discharged at new key: precondition pins `origin(a) = d ∧ d ∈ dom(M)`."

**Problem**: For the subsequent-emit branch the binding precondition pins `a = inc(a_prev, 0)`, not `origin(a) = d`. The equality `origin(a) = d` must be *derived* — `inc(·,0)` modifies only `sig(a_prev) = #a_prev` (TA5-SigValid, the element-field terminal position), leaving the document-level prefix fixed, so `origin(inc(a_prev,0)) = origin(a_prev) = d` by IH. (Equivalently from `b_C(d) ≼ a` via ChainPrefixExtension.) This derivation appears nowhere in the discharge section — only the worked example (Step 4) gestures at it, and even there cites TA5(b) without invoking TA5-SigValid to place `sig` at the last position. The same imprecision affects the L1a K.λ row. C2/L1a at the new key genuinely require `origin(a) = d`, so the gap is load-bearing.

**Required**: In the C2 (K.α) and L1a (K.λ) discharge rows, separate the first-emit case (`origin(a) = d` by the pinned form `[d.0.s_C.1]`) from the subsequent-emit case, and show the `origin(inc(a_prev,0)) = d` derivation explicitly.

### Issue 3: Duplicated statement that M2 grounds the vacuous ASN-0036 arrangement invariants

**ASN-0093, Scope** vs. **M2 body**. Scope: "arrangement-side invariants from ASN-0036 (S2, S3, S8a, S8-depth, S8-fin, D-CTG, D-MIN) hold vacuously here, since by M2 (EmptyArrangement, below) `M(d) = ∅`…". M2: "M2 is the explicit ground on which the arrangement-side invariants of ASN-0036 (S2, S3, S8a, S8-depth, S8-fin, D-CTG, D-MIN) hold vacuously in the substrate."

**Problem**: Two paragraphs in different sections assert the same fact with the same invariant list — the flagged anti-bloat pattern (same thing said twice, plus a forward reference "below" pointing from Scope to a restatement). The precise reader reads the list, reaches M2, and re-reads it.

**Required**: Keep the statement once (at M2, where the invariant lives) and reduce the Scope mention to a bare pointer, or drop one of the two.

## OUT_OF_SCOPE

None. The deferred topics (arrangement mutation, entity allocation, provenance, coupling, withdrawal) are correctly named as deferred and the note defines no claims for them.

VERDICT: REVISE
