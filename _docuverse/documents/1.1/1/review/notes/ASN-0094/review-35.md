# Review of ASN-0094

## REVISE

### Issue 1: NAT-card and NAT-sub cited as foundation but not in provided foundation vocabulary

**ASN-0094, AllocatedAddressAntichain Step 3.1 and RetractionTargetNotOnChain Steps II.0/II.1**: Cites "NAT-card (NatFiniteSetCardinality, ASN-0034)" and "NAT-sub (NatPartialSubtraction, ASN-0034)" as foundation axioms.

**Problem**: Neither NAT-card nor NAT-sub appears in the foundation vocabulary I was provided (which lists NAT-addcompat, NAT-closure, NAT-discrete, NAT-order, NAT-wellorder). The proofs depend critically on them:
- AllocatedAddressAntichain Step 3.1 uses NAT-card for the strictly-increasing enumeration of `Z_x` and the subset-with-equal-cardinality argument (`{n_1, n_2, n_3} ⊆ Z_a ∧ |·| = |Z_a| ⟹ {n_1, n_2, n_3} = Z_a`).
- RetractionTargetNotOnChain Step II.0 uses NAT-sub for `#w := #a − #b ≥ 1`.
- RetractionTargetNotOnChain Step II.1 uses NAT-card for the additivity argument `|Z_a| = |Z_b| + |Z_w^shift|` and NAT-sub for `zeros(w) = 3 − 3 = 0`.

Without these, the proofs are not closed.

**Required**: Either add NAT-card (cardinality of finite ℕ-subsets with the strictly-increasing-enumeration characterization and additivity over disjoint unions) and NAT-sub (partial subtraction `m − n` for `n ≤ m`) to the foundation extraction if they exist in ASN-0034, or derive these primitives inline from the available NAT axioms (well-ordering gives cardinality; closure plus discreteness gives partial subtraction).

### Issue 2: Cross-ASN references to non-foundation ASNs (ASN-0036, ASN-0093)

**ASN-0094, multiple sites**: References "S7d and M0" (SharedDepthOneAllocator sub-claim (a)), "ASN-0093's structural chain" (AllocatorTreeDepth Definition), "ASN-0093 substrate invariants: M0, M1, C0, C1, C1b, C1c, C-fin" (SubstrateConformingLayer Definition), "ASN-0036 content/arrangement invariants: S0, S1, S2, S3, S7a, S7b, S7c, S7d, S8-fin, S8a, S8-depth, D-CTG, D-MIN, D-SEQ" (same Definition).

**Problem**: ASN-0036 and ASN-0093 are not in the foundation list provided. The prompt's standard #7 requires flagging cross-ASN references except to foundation ASNs.

**Required**: Either treat ASN-0036/0093 as foundation (extend the foundation list) or rewrite these references to go through the substrate-conforming-layer scaffolding's named clauses (which the ASN already does in many places — e.g., "Document address structure" scaffolding clause supplies `zeros(d) = 2` without naming S7d/M0). The scaffolding pattern decouples successfully in most uses; SharedDepthOneAllocator and AllocatorTreeDepth are the holdouts.

### Issue 3: SharedDepthOneAllocator is introduced but never consumed

**ASN-0094, SharedDepthOneAllocator section**: The lemma is proved with three sub-claims but is not cited in any subsequent proof — neither in Sh0–Sh4, EffectiveWpSimplification, RetractionTargetNotOnChain, AllocatedAddressAntichain, nor any walkthrough.

**Problem**: A lemma included in the formal claims table without downstream consumption is either dead weight or its consumption is missing. The ZeroCountDepth and AllocatorTreeDepth definitions exist only to support this lemma's prose.

**Required**: Either cite SharedDepthOneAllocator where it's used (perhaps in the substrate-conforming-layer scaffolding's justification?), demote it to a remark, or remove it. Same for ZeroCountDepth and AllocatorTreeDepth definitions.

### Issue 4: Sub-case II.A's home(a) derivation is one sentence covering two distinct cases

**ASN-0094, RetractionTargetNotOnChain Sub-case II.A**: "K.λ's construction gives home(a) = d (first-emission deposits at [d.0.s_L.1] whose home is d; subsequent-emission inherits home from the parent chain at d)."

**Problem**: The subsequent-emission case `a = inc(ℓ_prev, 0)` requires unpacking through TA5(c)'s position-preservation. `inc(·, 0)` modifies only `sig(ℓ_prev)`. Since `home(ℓ_prev)` is determined by positions `1..#d` (containing N, U, D fields), and `sig(ℓ_prev) > #d + 1` (the link sub-allocator's chain has the sig position beyond the document prefix), `inc` preserves home. This is true but not on the page. The reader has to reconstruct the argument from TA5(c) + the scaffolding's chain enumeration property.

**Required**: One or two sentences unpacking why `home(inc(ℓ_prev, 0)) = home(ℓ_prev)` — citing TA5(c) (modifies only `sig`) and noting `sig(ℓ_prev) > #d + 1` since `ℓ_prev`'s chain index is in the link sub-allocator chain extending beyond the document prefix.

### Issue 5: AllocatedAddressAntichain "Element-level character of A^Σ" reasoning leans on a layer-commitment that conditions the lemma

**ASN-0094, AllocatedAddressAntichain preamble**: "Element-level character of A^Σ. The hypothesis x ∈ A^Σ is sufficient to invoke the lemma without a separate side-condition: every address in A^Σ = dom(Σ.C) ∪ dom(Σ.L) is element-level..."

**Problem**: The "every content address is element-level" half rests on the element-level content-address scaffolding clause, which itself rests on the *layer-commitment* identification `subspace_I(·) = E(·).1`. The scaffolding's own *Layer-commitment status* paragraph admits: "A substrate that surfaces `subspace_I` via a different physical projection... lies outside the framework's scope; the framework's preservation theorems and the AllocatedAddressAntichain lemma make no claims at such a substrate." So AllocatedAddressAntichain's element-level claim is conditional on the layer-commitment. This conditioning should be surfaced at the lemma statement, not buried in the preamble.

**Required**: Add the layer-commitment qualifier to the lemma statement explicitly, e.g., "For every reachable state Σ at a substrate-conforming layer honoring the `subspace_I(·) = E(·).1` identification, and every x ∈ A^Σ:..."

### Issue 6: ShapeWellFormedness "Behavior at c_F = 0|1" walkthrough has subtle reading hazard

**ASN-0094, ShapeWellFormedness Definition**: "Neither `c_F = 0` fires (since `0|1 ≠ 0`) nor `t_F = -` fires at a `c_F = 0|1` row: `t_F = -` is excluded at `c_F = 0|1` rows by the well-formedness implication `t_F = - ⟹ c_F = 0`, whose consequent fails (`0|1 ≠ 0`)."

**Problem**: This reads correctly but the implication-direction is reversed in the explanation. The implication is `t_F = - ⟹ c_F = 0`. Its consequent is `c_F = 0`. At a row with `c_F = 0|1`, we're asking whether the implication is *satisfied*, which requires the consequent to hold whenever the antecedent does. To "fail" the implication, the antecedent holds but the consequent fails. So at `c_F = 0|1` with `t_F = -`: antecedent holds, consequent fails (`0|1 ≠ 0`), implication is violated. The prose's "consequent fails" is correct, but the framing "is excluded by the implication" is backwards — the implication *would be violated* by such a row, which is why ShapeWellFormedness excludes it.

**Required**: Reword for clarity: "`t_F = -` at a `c_F = 0|1` row would violate the implication `t_F = - ⟹ c_F = 0` (antecedent holds, consequent fails since `0|1 ≠ 0`), so ShapeWellFormedness excludes such rows."

### Issue 7: NullifyActiveSubsetCompatibility Case A's "by ASN-0086's substrate-level argument under R0a and R6a" is too brief

**ASN-0094, NullifyActiveSubsetCompatibility Corollary, Case A**: "The active-subset content (i) and (ii) of ASN-0086's Nullify postcondition follow directly at Σ_target := Σ' by ASN-0086's substrate-level argument under R0a (FlatLinkDomain) and R6a (RetractionStability) — the same argument that delivered the postcondition in the absence of the framework. ✓"

**Problem**: The Case B argument is unpacked carefully (a paragraph each for (i) and (ii)), but Case A is dispatched in one sentence appealing to "ASN-0086's substrate-level argument." For a corollary that's structurally important (it preserves the operationally-significant content of ASN-0086's Nullify across the framework's return-type extension), both cases deserve symmetric treatment.

**Required**: Unpack Case A's discharge of (i) and (ii) at Σ_target := Σ', citing R0a for the single-tuple scope and R6a for nullification stability with the same level of explicitness as Case B.

## OUT_OF_SCOPE

### Topic 1: Composite predicates beyond the catalog's atomic templates
The Consequences section paragraph (b) notes "the framework does not establish a closure theorem about these primitives." This is appropriately flagged as a refinement candidate in Open Questions.

### Topic 2: Multi-process substrate consistency
Cross-process consistency of T_cat registration and atomicity of the per-K disciplines is acknowledged as a scope boundary in Open Questions. Not within this ASN's scope.

### Topic 3: Ghost-targeting slot semantics
L9 (TypeGhostPermission) admits ghost spans in endsets, but Sh-conf restricts slot positions to allocated targets. Whether future shape families should admit ghost-targeting slot semantics is acknowledged as an open design question.

VERDICT: REVISE
