# Review of ASN-0042

## REVISE

### Issue 1: Inconsistent state subscripting on ω

**ASN-0042, throughout**: `ω(a)` is written sometimes as `ω_Σ(a)` (e.g., in O3, O8, SelfOwnershipAtPrefix proof) and sometimes as bare `ω(a)` (e.g., in O2's definition, the EffectiveOwner definition, the worked example "ω(a₁) = π_A", and O6's invariant statement "pfx(ω(a)) ≼ acct(a)").

**Problem**: `ω` is state-dependent — it ranges over `Π_Σ` and depends on which principals are present. The bare form `ω(a)` is ambiguous about which state's registry is consulted. This is load-bearing for O3 (the entire claim is about how `ω_{Σ'}(a)` relates to `ω_Σ(a)` across a transition) and for O6's invariant (whose intended quantifier "for all `a ∈ Σ.B`" implies "for the same `Σ`" but the formal statement doesn't carry the subscript).

**Required**: Either thread `Σ` through every appearance of `ω` consistently, or state once that "`ω` is implicitly state-relativized" and ensure no statement compares `ω` outcomes from different states without explicit subscripts.

### Issue 2: Allocator-delegator equivalence is implicit but load-bearing

**ASN-0042, Delegation section and Bop axiom (cross-ref to ASN-0040)**: When delegation introduces `π'` and O18 baptizes `pfx(π')` into `Σ'.B`, O16 requires some `π ∈ Π_Σ` with `allocated_by_{Σ'}(π, pfx(π'))`. By O5 + condition (ii) of `delegated` + most-specific-covering uniqueness (O2 Step 4), that allocator must be `π_d` — the delegator.

**Problem**: This equivalence is consumed implicitly in O4's inductive step ("By O5 (SubdivisionAuthority), whenever `π` allocates `a`, the first conjunct of the postcondition gives `pfx(π) ≼ a`") and underlies the consistency between the principal registry and the baptismal registry at delegation transitions. But the equivalence is never stated as a named property. Worse, the O5 corollary ("allocator is effective owner for non-introducing transitions") explicitly excludes the introducing case and defers to O7(a), leaving the allocator's identity at introducing transitions unstated.

**Required**: Add a named derived property — e.g., `DelegatorAllocatesPrefix`: `delegated_Σ(π_d, π') ∧ Σ → Σ' ⟹ allocated_by_{Σ'}(π_d, pfx(π'))` — derived from O5 + O16 + condition (ii) + most-specific uniqueness. Without this, the bridge between ASN-0040's baptism mechanism and ASN-0042's authorization model has a visible gap.

### Issue 3: O3's formal statement is weaker than the prose

**ASN-0042, O3 (OwnershipRefinement)**: The prose says "changes only when delegation introduces a principal with a strictly longer matching prefix. No other transition alters `ω`". The formal statement reads:
> `(A a ∈ Σ.B, Σ, Σ' : Σ → Σ' ∧ ω_{Σ'}(a) ≠ ω_Σ(a) ⟹ (E π' ∈ Π_{Σ'} ∖ Π_Σ : pfx(π') ≼ a ∧ #pfx(π') > #pfx(ω_Σ(a))))`

**Problem**: The formal statement requires only "some new principal with a longer matching prefix", not "introduced by a delegation". The proof argues via O15 + reachability that the new principal must have arrived through delegation (bootstrap excluded), but this conclusion is never reflected in the postcondition. AccountLevelPermanence (one level down) carries the delegation witness explicitly; O3 does not. Downstream consumers reading only O3's formal contract cannot conclude "delegation occurred" without redoing the O15 argument.

**Required**: Strengthen the formal postcondition to `(E π_d ∈ Π_Σ, π' ∈ Π_{Σ'} ∖ Π_Σ : delegated_Σ(π_d, π') ∧ pfx(π') ≼ a ∧ #pfx(π') > #pfx(ω_Σ(a)))`. The proof already establishes this; only the contract needs updating.

### Issue 4: O10's field-opening boundary case is exhibited only via a scenario substitution

**ASN-0042, "Field-opening boundary case" paragraph in the Worked Example**: The running scenario establishes `Σ_1` with pre-delegation baptisms placing `[1, 0, 2, 0, 1]`, `[1, 0, 2, 0, 2]`, `[1, 0, 2, 0, 3]` in `Σ_1.B`, forcing `hwm(Σ_1.B, [1, 0, 2], 2) ≥ 3`. The boundary case `hwm_0 = 0` is then exhibited by switching to an "alternative scenario `Σ_alt`" in which "π_N performed no pre-delegation baptism under [1, 0, 2]".

**Problem**: The reader must track two parallel scenarios for the same delegation event, and the alternative scenario's reachability premise is asserted rather than constructed (the worked example earlier *forced* the pre-delegation baptisms by deriving `a₁ ∈ Σ_0.B` from State Σ₁'s setup, so the alternative requires retracting those derivations). A boundary case is more convincingly demonstrated by an instance the running scenario itself reaches — e.g., a *second* account-level principal `π_D` delegated to a fresh prefix `[1, 0, 9]` immediately, where `hwm(Σ.B, [1, 0, 9], 2) = 0` by construction.

**Required**: Either exhibit the field-opening case via a delegation event for which `hwm_0 = 0` is structurally forced (a freshly delegated prefix that hasn't yet been baptized under), or merge the two scenarios so the boundary case is reached by an authorized transition rather than by hypothetical retraction.

### Issue 5: O0's framing overstates structural decidability

**ASN-0042, opening paragraph and O0**: The prose claims "the address itself — through its field structure — encodes its owner. Authorization reduces to prefix comparison." O0 itself says "Whether principal π owns address a is decidable from pfx(π) and a alone, without consulting any mutable system state."

**Problem**: O0 as formalized is about the predicate `owns(π, a)` — given a candidate `π`, is `pfx(π) ≼ a`? This is indeed structural. But determining `ω(a)` (which principal owns `a`?) requires enumerating `Π_Σ` to find the longest match. The prose's "encodes its owner" reads as a claim about `ω`, not `owns`. O6 (StructuralProvenance) partially recovers this: `ω(a)` is determined by `acct(a)` *given* `Π_Σ` and `pfx`. But that's a function of the address *and* the registry, not the address alone.

**Required**: Tighten the opening to distinguish: `owns(π, a)` is decidable from `(pfx(π), a)` alone; `ω(a)` is decidable from `(a, Π_Σ, pfx)` — and O6 sharpens this to `(acct(a), Π_Σ, pfx)`. The "address itself encodes its owner" framing is only true given the registry as context.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer mechanism
**Why out of scope**: The ASN itself raises this as Open Question 1 and 6, noting the tension between Nelson's "someone who has bought the document rights" (LM 2/29) and the absence of any transfer machinery. The ASN takes the conservative reading that O3 describes the refinement regime as specified. Transfer machinery belongs to a separate ASN.

### Topic 2: Cross-node identity federation
**Why out of scope**: Open Question 5. O9 establishes that ownership cannot cross node boundaries; federation of identity across nodes would need additional invariants beyond what this ASN covers.

### Topic 3: Authentication / session-to-principal binding
**Why out of scope**: The "Scope note (Identity is exogenous)" explicitly defers this. O0–O10 hold for any consistent mapping from sessions to account tumblers. Concrete authentication mechanisms are out of scope per the Scope section.

### Topic 4: Density of ownership domains and recording delegation events
**Why out of scope**: Open Questions 4 and 7. The ASN is silent on whether every address in a domain must be reachable and on whether delegation events must be persisted (vs. reconstructed from address structure).

VERDICT: REVISE
