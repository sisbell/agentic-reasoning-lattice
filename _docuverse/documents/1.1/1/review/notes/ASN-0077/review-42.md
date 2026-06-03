# Review of ASN-0077

## REVISE

### Issue 1: Citations to a non-existent foundation claim "SubAllocatorAxiom"

**ASN-0077, "Where origin already lives" / O0 / O1**: O0(a) cites "SubAllocatorAxiom (c) (ASN-0047) gives `zeros(x) = 3`"; O0(b) and the Summary cite "SubAllocatorAxiom (e) (ASN-0047)"; O1(c) cites "SubAllocatorAxiom (a) and (e) (ASN-0047)".

**Problem**: ASN-0047 (foundation) contains no claim named **SubAllocatorAxiom** with lettered clauses (a)/(c)/(e). The relevant facts live under different, real names: `zeros(x) = 3` for links is **L1 (LinkElementLevel)**; subspace-identity of `A_C(d)`/`A_L(d)` outputs is the **Allocator hierarchy** definition; cross-(sub)allocator domain disjointness is **SubAllocatorBundle**. ASN-0047's SubAllocatorBundle explicitly notes these descend from "ASN-0093's sub-allocator lemmas" (not a foundation here). Citing a fabricated claim name violates citation hygiene (reviewer rule 7) and makes the dependencies unverifiable.

**Required**: Replace every "SubAllocatorAxiom (·)" citation with the actual ASN-0047 claim that supplies the fact (L1, L1a, AllocatorHierarchy, SubAllocatorBundle).

### Issue 2: "LinkVPositionDepthAxiom: m_L = 2" is fabricated and contradicts m_L(d)

**ASN-0077, O11' sub-case (b), O11.1 (u₁ = s_L / K.μ⁺_L case), worked example**: "LinkVPositionDepthAxiom (ASN-0047) — `(A d ∈ E_doc :: m_L = 2)` — fixes the link-subspace depth uniformly at every state, so `m' = m_L = m = 2`."

**Problem**: No such axiom exists in ASN-0047, and it directly contradicts the foundation claim **m_L(d) (LinkSubspaceDepth)**, which states `m_S(d) ≥ 2` and that "the next insertion re-pins `m_S(d)` from scratch at any value ≥ 2." K.μ⁺_L's own precondition confirms variability: "If `V_{s_L}(d) = ∅`: `ValidFirstLinkPosition(d, v_ℓ, m)` — for any chosen `m ≥ 2`." So a document's link depth may be 3, 4, …; forcing `m = 2` is false. O11.1 even concludes `m' = m = 2` as a sub-claim.

**Required**: Drop the universal `m_L = 2` axiom. The depth coincidence the proof actually needs (`#v_ℓ = m`) follows correctly from K.μ⁺_L's precondition `#v_ℓ = m_L(d)` together with σ's precondition (v) naming `m` as the current link-subspace depth — both at the same state, both equal to `m_L(d)`. Re-derive via these, with no claim that `m = 2`. (The worked example's concrete choice `v_{ℓ_a} = [2,1]` with `m = 2` is fine as one admissible value; just stop citing it as a universal law.)

### Issue 3: "M-sub(a) (SubspaceConfinement)" is not an ASN-0058 claim

**ASN-0077, O2 (Block uniformity)**: "M-sub(a) (SubspaceConfinement, ASN-0058) then yields `subspace(vⱼ + i) = subspace(vⱼ)`"; the precondition is said to be discharged by "S8a … gives `#vⱼ ≥ 2`, which discharges M-sub(a)'s precondition."

**Problem**: ASN-0058 has no claim **M-sub / SubspaceConfinement**. The subspace-agreement fact is **M-int (TumblerIntervalCharacterization)**, whose precondition is `x, y ∈ dom(M(d))` with `x ≤ y < x + n` — not `#vⱼ ≥ 2`. The stated precondition-discharge therefore matches a claim that does not exist.

**Required**: Cite M-int. The hypotheses are available: `vⱼ ∈ dom(M(d))` and `vⱼ + i ∈ dom(M(d))` (B1), with `vⱼ ≤ vⱼ + i < vⱼ + nⱼ`, so M-int delivers `subspace(vⱼ + i) = subspace(vⱼ)` directly.

### Issue 4: O0(c) link-case totality is over-derived through fabricated claims when L1a states it directly

**ASN-0077, O0 derivation (c)**: the `dom(L)` totality argument routes through "SubAllocatorAxiom … activates a link sub-allocator `A_L(d)` only at the entity-allocation event … so `origin(ℓ) ∈ E_doc` at that activation event, and P1 keeps `origin(ℓ) ∈ E_doc`."

**Problem**: ASN-0047 already supplies **L1a (LinkScopedAllocation): `(A a ∈ dom(Σ.L) :: origin(a) ∈ E_doc)`** as a per-state invariant. The multi-step activation-plus-P1 derivation reinvents this through a non-existent axiom and is unnecessary.

**Required**: Discharge the `dom(L)` codomain conjunct of O0(c) by citing L1a directly.

### Issue 5: Minor citation-name drift — "KMuPlusContentSubspaceRestriction"

**ASN-0077, O11 Case (ii), O11.1**: cites "KMuPlusContentSubspaceRestriction (ASN-0047)".

**Problem**: The foundation names this **"K.μ⁺ amendment — ContentSubspaceRestriction"**. The substance ("new V-positions must satisfy `subspace(v) = s_C`") is correct, but the citation name does not match.

**Required**: Use the foundation's name (ContentSubspaceRestriction / K.μ⁺ amendment).

## OUT_OF_SCOPE

### Topic 1: Reporting link origins from an I-span (author's Open Question 1)
**Why out of scope**: The I-span lift restricting to `dom(C)` and dropping link addresses is a deliberate definitional choice, correctly flagged as a future question rather than a defect here.

### Topic 2: Surfacing the transclusion chain / historical containment from Σ.R
**Why out of scope**: These are complementary operations the ASN explicitly defers; SHOWORIGIN's direct-origin contract is self-contained.

VERDICT: REVISE
