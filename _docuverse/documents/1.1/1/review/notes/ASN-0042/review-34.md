# Review of ASN-0042

## REVISE

### Issue 1: O10 summary table missing O18 in derivation

**ASN-0042, Properties Introduced table**: "O10 | ... | from O1a, O6, FiniteRegistry, T0a, TA5(d) |"

**Problem**: The proof of O10 makes load-bearing use of O18 (DelegationBaptizes) — the "baptismal coupling" argument explicitly cites O18 to derive `S' ⊆ {1, ..., hwm_0}`, which is the linchpin that makes the unilateral trajectory unconditional. Yet the summary table omits O18 from O10's derivation list.

**Required**: Add O18 to O10's derivation chain in the summary table. Consider also listing the ASN-0040 dependencies (`next`, `hwm`) consumed by the trajectory analysis.

### Issue 2: Confusing prose around O18's bootstrap base case

**ASN-0042, O18 (DelegationBaptizes)**: "The base case is supplied by O14's second clause: every initial principal's prefix is covered by some address in Σ₀.B"

**Problem**: This phrase reverses the direction of O14's actual second clause. O14 says every `a ∈ Σ₀.B` is covered by some principal — i.e., for each address, ∃ a principal whose prefix is a prefix of the address. The text's phrasing "every initial principal's prefix is covered by some address" suggests the opposite (that some address is a prefix of `pfx(π)`), which neither matches O14 nor is what's needed. The intended assumption is the next sentence's "standard bootstrap reading" (`pfx(π) ∈ Σ₀.B` for `π ∈ Π₀`), which is a separate posit, not a consequence of O14.

**Required**: Either drop the misleading lead-in and state the bootstrap reading directly as the additional assumption, or restate O14's second clause accurately (every initial address is covered by an initial principal) and explain separately why the bootstrap reading is needed.

### Issue 3: Compressed derivation in NestingByDelegation

**ASN-0042, NestingByDelegation proof, inductive step (case `pfx(π₁) ≺ pfx(π')`)**: "by the most-specific property of `π_d` and the covering-chain structure ..., `pfx(π₁) ≼ pfx(π_d)`."

**Problem**: This single sentence compresses three steps: (1) `pfx(π₁)` and `pfx(π_d)` both cover `pfx(π')`, so by covering-chain they are ≼-comparable; (2) by condition (ii), `#pfx(π₁) ≤ #pfx(π_d)`; (3) combining (1) and (2) rules out `pfx(π_d) ≺ pfx(π₁)` (which would force `#pfx(π_d) < #pfx(π₁)`), leaving `pfx(π₁) ≼ pfx(π_d)`. Step (3) is the load-bearing case-elimination and is left implicit.

**Required**: Spell out the comparability resolution explicitly — name the three sub-cases (`pfx(π_d) ≺ pfx(π₁)`, equality, `pfx(π₁) ≼ pfx(π_d)`), and show that the most-specific clause eliminates the first.

### Issue 4: Covering-chain lemma is used implicitly across multiple proofs

**ASN-0042, throughout**: The lemma "any two prefixes of a common tumbler are ≼-comparable" is invoked in O2 Step 2, O7(a)'s case analysis, AccountLevelPermanence Step 3, NestingByDelegation's inductive step, and the AccountLevelPermanence★ corollary.

**Problem**: The lemma is stated inline only within O7(a)'s proof and re-derived (or assumed) at each subsequent use. This is a foundational structural fact that the ASN repeatedly relies on; stating it once early — either by citing Prefix (PrefixRelation) directly or as a named local lemma — would clarify dependencies and tighten the proofs.

**Required**: Extract the covering-chain lemma as a named claim near the start of the "Ownership Domains" section (or cite it explicitly from Prefix's component-by-component reading), and have subsequent proofs reference it by name rather than re-derive it.

### Issue 5: Property statements omit reachability while proofs require it

**ASN-0042, O3 and O4**: O3's property statement `(A a ∈ Σ.B, Σ, Σ' : Σ → Σ' ∧ ω_{Σ'}(a) ≠ ω_Σ(a) ⟹ ...)` and O4's `(A a ∈ Σ.B : (E π ∈ Π : pfx(π) ≼ a))` quantify over Σ without explicit reachability, but the proofs of both invoke iterated O12 (which requires a finite path from Σ₀ to Σ).

**Problem**: The reachability convention near the top of the ASN says "All states Σ discussed in this ASN are assumed to be reachable from the bootstrap state Σ₀" and that "Where a property's formal contract requires reachability for its derivation, the precondition is restated explicitly." O3 does restate it in its formal contract, but O4 does not, even though its proof's Case 2 invokes O5 and O16 in a way that ultimately needs reachability (to ensure π is in Π_Σ via the principal lineage). The property-statement / formal-contract split is uneven across O3, O4, O8, AccountLevelPermanence.

**Required**: Audit each property whose proof uses iterated O12 or repeated O15 applications, and either include reachability in the property statement or note explicitly in the formal contract. At minimum, O4's formal contract should include `Σ reachable from Σ₀`.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer mechanism

The ASN raises but defers the question of whether ownership transfer is possible (Nelson's reference to "someone who has bought the document rights" vs. the address's permanent provenance recording). The open question is properly noted; this is not a defect in the present ASN.

### Topic 2: Baptism mechanism details

The ASN cites `next` and `hwm` from ASN-0040 (foundation) and takes `allocated_by_Σ` as a primitive relation. Implementation details of how baptism produces specific addresses are correctly out of scope.

VERDICT: REVISE
