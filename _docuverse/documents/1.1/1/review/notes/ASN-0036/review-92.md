# Review of ASN-0036

## REVISE

### Issue 1: NAT-discrete citation missing from S8's Depends
**ASN-0036, S8 contract Depends section**: enumerates foundation claims T1, T3, T5, T10, TS4, TumblerAdd, OrdinalShift, OrdinalDisplacement but lists no NAT axioms.
**Problem**: The within-subspace incompatibility lemma's Case `j = m` derives "t_m ≥ v_m + 1 (NAT)" from "v_m < t_m" — precisely NAT-discrete's forward direction `m < n ⟹ m + 1 ≤ n` (ASN-0034). The "(NAT)" annotation marks the step, but the axiom is never named in the Depends list. The same omission appears elsewhere: OrdAddHom's `+1` steps, D-CTG-depth's `(v₁)ⱼ₊₁ + 1` successor reasoning, and D-SEQ's contiguity-of-k argument all invoke NAT-closure / NAT-addcompat / NAT-cancel without explicit citation.
**Required**: Audit every "(NAT)" annotation in the ASN. For each, cite the specific NAT-* axiom from ASN-0034. At minimum, add NAT-discrete to S8's Depends.

### Issue 2: S8's auxiliary lemma derives more than its stated postcondition claims
**ASN-0036, S8 contract Postconditions, Auxiliary lemma**: claims "every image `shift(aⱼ, k)` ... preserves the I-address subspace `subspace_I(aⱼ)`" only.
**Problem**: The proof body derives strictly more: `zeros(shift(aⱼ, k)) = zeros(aⱼ) = 3` (so `shift(aⱼ, k)` inherits S7b) and `#E(shift(aⱼ, k)) = #E(aⱼ) = δⱼ ≥ 2` (so `shift(aⱼ, k)` inherits S7c). The closing sentence makes this explicit: "both the subspace-preservation and field-structure-preservation conclusions hold for every k with 1 ≤ k < nⱼ". Downstream operation ASNs constructing correspondence runs of length > 1 will need to know that every `shift(a, k)` along a run remains a well-formed element-level I-address satisfying S7b and S7c — not merely that `subspace_I` is preserved. Additionally, the field-structure derivation glosses one supporting step: the equality `zeros(shift(a, k)) = zeros(a)` requires that position `#a` stay non-zero in `shift(a, k)`, which depends on T4's `t_{#t} ≠ 0` clause applied to `a` (since `a_{#a} ≥ 1` is what keeps `a_{#a} + k ≥ 1` from contributing a new zero).
**Required**: Lift the field-structure preservation facts to explicit postconditions (`zeros = 3` preserved, `#E ≥ 2` preserved). Cite T4's `t_{#t} ≠ 0` clause explicitly at the step that rules out position `#a` contributing a new zero in `shift(a, k)`.

## OUT_OF_SCOPE

### Topic 1: Subspace alignment between V-position and I-address subspaces
**Why out of scope**: The Remark following S8a defers `subspace(v) = subspace_I(M(d)(v))` to the operations layer with Nelson and Gregory evidence cited. Subspace alignment is established by specific editing operations, not by the strand model itself.

### Topic 2: Link subspace contiguity semantics
**Why out of scope**: D-CTG, D-MIN, D-CTG-depth, and D-SEQ are explicitly bound to subspace 1 (text). Link-subspace semantics (sparse, append-only with tombstones) are deferred to a future ASN.

### Topic 3: Operation-level preservation of D-CTG, D-MIN, S2 under INSERT / DELETE / COPY / REARRANGE
**Why out of scope**: The ASN states explicitly that operation-level preservation is a verification obligation for each operation's ASN. The Open Questions section reflects this scope decision.

### Topic 4: Subtraction homomorphism and round-trip identities on `ord`
**Why out of scope**: The Open Questions section flags these for future work. The ASN introduces `ord`, `vpos`, `w_ord`, OrdAddHom, OrdAddS8a, OrdShiftHom as forward-looking infrastructure for operation ASNs — additional identities on top of this scaffold belong with the operations that need them.

VERDICT: REVISE
