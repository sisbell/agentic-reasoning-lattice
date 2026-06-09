# Review of ASN-0119

## REVISE

### Issue 1: State model and contiguity invariants are cited inconsistently

**ASN-0119, "The two streams" / "What is preserved"**: The ASN declares "We work in the state `Σ = (C, M, L)` of the strand and link models" (ASN-0036 + ASN-0043), whose text-subspace contiguity invariant is the unstarred **D-CTG / D-SEQ / D-MIN** (text-only, ASN-0036). Yet the preservation paragraph claims to inherit "per-subspace contiguity (ASN-0047, **D-CTG★**), sequentiality (**D-SEQ★**), the minimum position (**D-MIN★**)" — invariants of ASN-0047's *extended* state `(C, L, E, M, R)`. P3 then reverts to the unstarred form: "the active V-positions of the text subspace `s_C` form a contiguous run by **D-CTG**."

**Problem**: The ASN cannot simultaneously be in the `(C, M, L)` model and discharge ASN-0047's starred invariants. If the state is `(C, M, L)`, the starred per-subspace invariants are not part of its invariant set (and D-CTG★/D-SEQ★/D-MIN★ should not be cited as "preserved"). If the ambient model is genuinely ASN-0047, the state is `(C, L, E, M, R)` — not `(C, M, L)` — and the ASN would additionally owe preservation of CL-OWN, CL-UNIQ, S3★, S3★-aux, P6–P8 for the post-state, none of which are mentioned. The mixed citation (D-CTG in P3, D-CTG★ in the preservation list) leaves it ambiguous which guarantee is actually established.

**Required**: Commit to a single state model and cite one consistent contiguity invariant throughout. Either (a) work in `(C, M, L)` and discharge D-CTG/D-SEQ/D-MIN (text-only), explicitly noting the link subspace is frame; or (b) declare the ASN-0047 state `(C, L, E, M, R)` and discharge the full starred invariant package, including CL-OWN/CL-UNIQ for the untouched link subspace.

### Issue 2: The link-store frame `Σ'.L = Σ.L` is not covered by the imported operation's specification

**ASN-0119, "Links"**: "The link store is not consulted by any clause of the operation, so `Σ'.L = Σ.L` **(P6)**."

**Problem**: REARRANGE is defined as "the operation REARRANGE_K of ASN-0084," and ASN-0084's frame conditions R-FRAME-P / R-FRAME-S contain only three clauses — non-S subspace invariance, other-document invariance, and `C' = C`. They say *nothing* about a link store (ASN-0084's model has no `L`). So in the extended `(C, M, L)` state the imported operation's effect on `L` is simply undefined by the import; `Σ'.L = Σ.L` is a fresh specification commitment, and "the operation does not even read L" is an appeal to a presumed realization rather than to the imported contract.

**Required**: State `Σ'.L = Σ.L` as an explicit added frame clause of REARRANGE in the `(C, M, L)` state (extending REARRANGE_K's frame), rather than presenting it as a consequence of the imported operation. P6 is already labeled "introduced," so promote the justification from "does not read L" to an explicit frame extension.

## OUT_OF_SCOPE

### Topic 1: Cut on a V-position shared via transclusion; serializability of concurrent rearrangements; index/footprint-fragmentation invariant; arrangement recoverability; subspace-boundary preservation under displacement; first/last-position cut well-formedness

**Why out of scope**: These are correctly placed in the Open Questions section as future work. The abstract operation here is fully specified by its target arrangement (the tiling of `[c₀, c_{n-1})`), and the worked examples exercise the last-position boundary (`c₂ = ord 6` past a 5-byte document) successfully; the deferred questions concern genuinely new territory (concurrency, index maintenance, version recovery), not gaps in this ASN.

VERDICT: REVISE
