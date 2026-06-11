# Review of ASN-0120

The technical core of this ASN is sound. I checked the confinement argument (T5 with the length-(m−1) prefix, licensed by `wf`'s ordinal-displacement clause), the recovery equation and its extensional form (both directions of the coverage = union-of-unit-subtrees derivation go through via LP-Fin Corollary and the S3 merge identity), the K.μ⁺_L precondition discharge at the intermediate state (including the `a ∉ ran(M(d))` branch split), the ML6 necessity/sufficiency argument, and both Facts of the ML9 wp derivation including the `d' = d` boundary. The empty-resolution boundary is settled cleanly, and the coupling-constraint vacuity (J0/J1★/J1'★) is correctly grounded in the frames. The remaining issues are one depth gap in the worked example, one missing premise citation, and residual meta-prose under the anti-bloat mandate.

## REVISE

### Issue 1: The worked example never exercises an edit, so the ASN's headline guarantee is verified only abstractly
**ASN-0120, "A worked example"**: the example ends at the creating transition — "*Discoverability (ML9).* Evaluate `discoverable_from(a, d', Σ')` for each document." — with no post-creation state.
**Problem**: The problem statement, ML7, ML8, and ML9's future-state half are all about what happens *after* the link exists and the sources are edited — "the endset reference survives all editing of the content it names" — and `ρ`'s active-position filter is explicitly motivated by spans "some of whose positions have since been deleted." Yet the example checks only creation-state postconditions (ML0, ML1, ML2, ML6, ML9 at `Σ'`). Survivability, the invariant the entire V→I conversion is designed to buy, is never demonstrated against a concrete scenario.
**Required**: Extend the example by one foundation arrangement transition on a source document — e.g., K.μ⁻ (ASN-0047) contracting `A`'s arrangement so only the position carrying `a₁` survives — reaching `Σ''`, and verify concretely: (i) `Σ''.L(a) = Σ'.L(a)` (ML7); (ii) `coverage(e₁) ∩ dom(Σ''.C) = {a₁, a₂}` unchanged (ML1's stable trace); (iii) `discoverable_from(a, A, Σ'')` still holds via `a₁` while `a₂ ∉ ran(Σ''.M(A))` yet `a₂ ∈ dom(Σ''.C)` by S0 (ML8, and the partial-span survival that motivated `ρ`'s filter); (iv) discoverability from `B` and `D` unaffected (ML9's future-state consequence). This uses only substrate vocabulary, not the out-of-scope DELETE operation.

### Issue 2: T4-validity of chain addresses asserted without naming its source
**ASN-0120, resolution section (reference-decomposition paragraph)**: "Each chain address is T4-valid, so `sig(aₖ) = #aₖ` (TA5-SigValid, ASN-0034) and the sibling step is exactly the last-component shift, `aₖ₊₁ = inc(aₖ, 0) = shift(aₖ, 1)`".
**Problem**: The consequence is cited (TA5-SigValid) but the premise is not. T4-validity of the run members is load-bearing here — it is what collapses `inc(·, 0)` to `shift(·, 1)`, which grounds adjacency, the merge identity, and ultimately the extensional coverage form. The source is membership in the content store (`aₖ ∈ ρ(R_j, Σ) ⊆ dom(Σ.C)`) together with StoreT4Validity (ASN-0093). The same uncited premise recurs in the worked example ("`a₂ = inc(a₁, 0) = shift(a₁, 1)` by TA5-SigValid"). Every comparable per-step inference in this ASN names its source; this one should too.
**Required**: Cite StoreT4Validity (ASN-0093) at the first occurrence, with the membership chain `aₖ ∈ ρ ⊆ dom(Σ.C)` making it applicable.

### Issue 3: Residual meta-prose (anti-bloat)
**ASN-0120, ML2 paragraph and ML7**: three spots fit the flagged accretion patterns.
**Problem**: (a) ML2 paragraph: "and any future read-back operation over `Σ.L` would do the same" — speculation about unspecified future operations; the Observe_K instance already carries the observability point. (b) ML7: "so a link-retirement facility, were one wanted, would be a model extension outside the vocabulary this claim quantifies over" — imagines a facility the closed transition vocabulary already excludes; the preceding clause ("the transition vocabulary contains no operation that removes a link address or rewrites its value") is the complete ground for unconditionality. (c) The pins-coverage/leaves-decomposition-free rationale is stated twice in the body — once when the postcondition is introduced ("The postcondition pins each stored endset's *coverage* exactly, while leaving its *span decomposition* free") and again closing the ML2 paragraph ("That division is exactly why the postcondition deliberately pins coverage and leaves the decomposition free") — in addition to the claims-table summary.
**Required**: Delete (a) and (b); keep one body statement of the ML2 rationale (the table summary may stand).

## OUT_OF_SCOPE

### Topic 1: N-ary link creation (arity > 3)
**Why out of scope**: K.λ admits `N ≥ 3`, but MAKELINK is Nelson's three-endset operation; an N-ary creation variant is a future operation ASN, not a gap here.

### Topic 2: Direct I-address endset arguments and link-subspace endsets
**Why out of scope**: The ASN itself correctly defers both — supplying I-addresses directly (bypassing V-span resolution, the route to L4/L9 generality) is a distinct argument shape, and link-pointing-at-link endsets are an open question on a different precondition surface.

VERDICT: REVISE
