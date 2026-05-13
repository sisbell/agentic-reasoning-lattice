# Review of ASN-0043

## REVISE

### Issue 1: TA5a wording attributes a constraint where none exists

**ASN-0043, L9 proof (L1c verification step iii)**: "`inc(1.0.1.0.1.0.s_L, 1)` → `1.0.1.0.1.0.s_L.1` = `a` — child-spawn to element field depth 2 (`k' = 1`, requiring `zeros(1.0.1.0.1.0.s_L) ≤ 3` by TA5a; satisfied since `zeros(1.0.1.0.1.0.s_L) = 3`)."

**ASN-0043, worked example (L1c verification, step iii)**: "`inc(1.0.1.0.1.0.2, 1)` → `1.0.1.0.1.0.2.1` = `a` — child at depth 2 (`k' = 1` with `zeros(1.0.1.0.1.0.2) = 3`, satisfying TA5a: `k' = 1` requires `zeros ≤ 3`)."

**Problem**: TA5a's Guarantee is "`inc(t, k)` satisfies T4 iff `k ∈ {0, 1}`, or `k = 2 ∧ zeros(t) ≤ 2`". For `k' = 1`, preservation is unconditional — there is no `zeros ≤ 3` constraint. A reader who cross-references TA5a will find no such requirement and may suspect a tighter precondition than actually exists.

**Required**: Replace with language that reflects TA5a accurately — e.g., "`k' = 1` unconditionally preserves T4 by TA5a; the output's zero count is `zeros(parent) = 3`, satisfying T4's overall bound." Apply the fix at both sites.

### Issue 2: L1a's English claim is stronger than its formal statement (allows non-registered "documents")

**ASN-0043, L1a**: English — "Every link address is allocated under the tumbler prefix of the document whose owner created it." Formal — `(A a ∈ dom(Σ.L) :: (E d :: d is a T4-valid document-level tumbler (zeros(d) = 2) ∧ home(a) = d ∧ a is producible from d by a finite sequence of T10a-conforming inc steps))`.

**Problem**: The English ("the document whose owner created it") implies `d` is a document existing in the system per S7d — a T10a-allocated document tumbler with an owner. The formal statement only requires `d` to be a *structural* document-level tumbler (T4-valid with `zeros(d) = 2`), with no requirement that `d` is the output of any allocation event. The L9 proof exploits this gap: it constructs `d' = 1.0.1.0.1` "independent of whether `Σ` already contains documents" and never adds `d'` to any document registry, yet uses it as `home(a)` for the new link. If `d'` was not a document in `Σ`, then "the document whose owner created [`a`]" denotes an entity that does not exist in the system, and the English claim fails for `a`.

**Required**: Pick one interpretation and align both. Either (a) tighten the formal statement to require `d` to be a T10a-allocated document tumbler (e.g., add a conjunct linking `d` to an S7d-style allocation event), then have the L9 proof construct `d'` as such; or (b) weaken the English to "every link address has a T4-valid document-level prefix that names its allocator origin" and explicitly note that structural document-level-ness need not coincide with system-registered documenthood.

### Issue 3: GlobalUniqueness cited under an unrecognized name

**ASN-0043, multiple sites (L9 L1c verification, L11b proof, property table for L11a)**: "GlobalUniqueness (UniqueAddressAllocation, ASN-0034)".

**Problem**: The foundation defines the claim as `## GlobalUniqueness — GlobalUniqueness` — both label and name are "GlobalUniqueness". "UniqueAddressAllocation" is not a recognized name for this foundation claim. Standards rule 7 forbids reinventing notation for foundation-defined concepts; the parenthetical alternate name conflicts with the canonical name. Internal usage is also inconsistent — some sites use the parenthetical, others use `GlobalUniqueness (ASN-0034)` alone.

**Required**: Drop "UniqueAddressAllocation" everywhere; cite the foundation claim consistently as `GlobalUniqueness (ASN-0034)`.

## OUT_OF_SCOPE

None — the explicit Scope statement and the Open Questions section already defer the topics that the model does not address (operations, V-stream effects, query semantics, three-layer deletion, etc.).

VERDICT: REVISE
