# Review of ASN-0094

## REVISE

### Issue 1: Sh3 proof violates "no proof by similarly" standard
**ASN-0094, Sh3 (ToSlotTargetRestricted)**: "*Proof.* Symmetric to Sh2. ∎"
**Problem**: Sh3's entire proof is one line claiming symmetry. The standard explicitly forbids this. Note that Sh1 (the G-side analog of Sh0) does *not* take this shortcut — it spells out the proof and cites Sh-conf clauses (b) and (c) at each step. The discipline is inconsistent.
**Required**: Restate Sh3's proof with Case A (monotone preservation on `t_G^Σ`) and Case B (Sh-conf clause (d) on G at emission), mirroring Sh2's structure with explicit substitution F → G.

### Issue 2: Direct cross-ASN references to ASN-0093 (non-foundation)
**ASN-0094, Definition — AllocatorTreeDepth**: "is the number of T10a child-spawn pairs `(·, k')` with `k' ∈ {1, 2}` on ASN-0093's structural chain from `d` to A's base address"
**ASN-0094, SharedDepthOneAllocator**: "the subspace-specific sub-allocators ASN-0093 names — `A_C(d) = A_{d.0.s_C.1}` (anchored at `b_C(d)`) and `A_L(d) = A_{d.0.s_L.1}` (anchored at `b_L(d)`)"
**Problem**: ASN-0093 is not in the foundation list — only ASN-0034, ASN-0043, and ASN-0086 are listed. Standard 7 forbids cross-ASN references except to foundations.
**Required**: Reframe these references through ASN-0086's substrate-conforming-layer interface (which already lists ASN-0093 invariants in catalog (a) of its substrate-conforming-layer definition). Replace "ASN-0093's structural chain" with "the substrate-conforming layer's structural chain", and "ASN-0093 names" with "the substrate-conforming layer names" (or similar).

### Issue 3: Sh-conf "iff" formulation potentially misleading
**ASN-0094, Sh-conf — ShapeConformanceAxiom**: "`Emit_K(Σ, d, F, G)` succeeds iff `K ∈ T_cat ∧ conf_K^Σ(F, G)`."
**Problem**: The "iff" reads as fully characterizing success, but the body says Sh-conf "*adds* two preconditions" and the wp_eff formulation writes the full conjunction `wp_086 ∧ K ∈ T_cat ∧ conf_K^Σ(F, G)`. A reader could mistakenly conclude ASN-0086's preconditions (e.g., `d ∈ dom(Σ.M)`) are no longer required.
**Required**: Reformulate as "succeeds iff ASN-0086's preconditions hold *and* `K ∈ T_cat` *and* `conf_K^Σ(F, G)`", or state both conditions as additions explicitly: "the two added preconditions are `K ∈ T_cat` and `conf_K^Σ(F, G)`; failure of either produces `⊥`."

### Issue 4: Retraction-shape enforcement of unit-depth discipline not exhibited
**ASN-0094, Sh-conf section, Effective wp**: "the last two conjuncts collapsing to `⊤` under the relational layer's committed operations (regime (i) of ASN-0086's wp simplification under the unit-depth retraction discipline)"
**Problem**: ASN-0086's wp simplification requires the unit-depth retraction discipline. The shape framework *enforces* this implicitly — canonical-slot form combined with Retraction's `c_G = 1` forces G to a single span `{(b, δ(1, #b))}`. But the connection is not stated; a reader cannot verify regime (i) applies without tracing the definitions.
**Required**: Add a sentence in Retraction's catalog row (or in Sh-conf's prose): "Retraction's `c_G = 1` together with canonical-slot form enforces every Retraction emission's G-endset as a single unit-depth span, satisfying ASN-0086's unit-depth retraction discipline directly."

### Issue 5: SharedDepthOneAllocator lemma has no downstream consumer
**ASN-0094, Scope section, SharedDepthOneAllocator (LEMMA)**: Proves uniqueness of the depth-1 allocator under each document.
**Problem**: Labeled LEMMA but never explicitly cited in any subsequent proof. The Scope's content-side scaffolding already supplies link sub-allocator existence via ASN-0086's interface. The lemma adds prose weight without a load-bearing role.
**Required**: Either cite the lemma at a specific consuming proof site, or demote it to a Definition (e.g., "Definition — AllocatorTreeStructure") that documents the substrate's allocator structure without claiming theorem status.

### Issue 6: Properties Introduced table contains internal-history annotation
**ASN-0094, Properties Introduced table, row "cov"**: "Coverage projection `L_K → ℘(T) × ℘(T)` (codomain corrected from prior draft's `℘_fin`)"
**Problem**: "(codomain corrected from prior draft's `℘_fin`)" is revision-history metadata. The Properties table is a downstream-consumer reference; revision history belongs in commit messages.
**Required**: Remove the parenthetical. State the codomain as `L_K → ℘(T) × ℘(T)` directly.

### Issue 7: `subspace_I(a) = E(a).1` connection implicit at AllocatedAddressAntichain Step 3.3
**ASN-0094, AllocatedAddressAntichain proof, Step 3.3**: "L0 (SubspacePartition, ASN-0043) gives `E(x).1 = s_L` for links"
**Problem**: L0 (ASN-0043) actually states `subspace_I(a) = s_L`, using the function `subspace_I(·)`, not `E(a).1`. The framework consistently writes `E(a).1`. The equivalence `subspace_I(a) = E(a).1` follows from T7 plus T4b's E-field structure but is implicit.
**Required**: Add a one-sentence bridge in Step 3.3 (or as a remark in Scope) identifying `subspace_I(a) = E(a).1` from T4b, so the citation L0 → `E(x).1 = s_L` is grounded.

## OUT_OF_SCOPE

### Topic 1: Composite shapes (multi-relation slot constraints)
**Why out of scope**: Explicitly listed in Open Questions. Forward-looking design question about extending the catalog, not a gap in the current framework.

### Topic 2: Cross-process shape registry consistency
**Why out of scope**: Explicitly listed in Open Questions. Lifetime constancy is asserted within a single process; distributed coordination is future work.

### Topic 3: Ghost-targeting slot semantics
**Why out of scope**: Listed as open question. The current framework forbids ghost addresses in slot positions; admitting them is a separate design decision.

### Topic 4: `(0, 0)` shape admission
**Why out of scope**: Open question whether such shapes should be admitted to the catalog. No current use case demands them.

### Topic 5: Bipartite coverage gaps (e.g., `(*, *, A, A, _)` shapes)
**Why out of scope**: The catalog is hand-curated (Sh5 META) and admits non-canonical shapes at the substrate level without template support. Adding rows is future work, not a current correctness gap.

VERDICT: REVISE
