# Review of ASN-0115

I checked the proofs first; the mathematics is sound. Confinement is correct (T5 applied to `s ≤ t ≤ reach(σ)` with the length-`(m−1)` prefix `p ≼ s`, `p ≼ reach(σ)`). The R6 gap analysis is genuinely careful — it correctly restricts the no-interior-hole guarantee to the *bindable* depth-`m_S` slice rather than to every named tumbler in `⟦σ⟧` (the worked `[1,2,1]`-between-`[1,2]`-and-`[1,3]` case would falsify the unrestricted claim, and the ASN sidesteps it). R7's insistence on T1-comparability (not merely a shared ancestor) is a real subtlety, correctly identified. R8's subspace-sharing proof (S3★ + SD + S3★-aux) and the link-vacuity (CL-OWN forcing `d=d'`, CL-UNIQ forcing `v=v'`) are complete. The five worked instances all check out arithmetically.

The findings below are the accreted prose this `anti-bloat` cycle is meant to surface: a duplicated/forward-referenced derivation, an essay paragraph about machinery the model lacks, and a cluster of forward-reference micro-accretions.

## REVISE

### Issue 1: `V_S(d)=∅ ⟹ act=∅` is derived twice, the first time out of dependency order
**ASN-0115, §"What a spec-set is, and what delivery is" (V-spec definition)**: "When `V_S(d) = ∅` the constraint is vacuous — any well-formed start of depth `≥ 2` is admissible — but then `act = ∅`, since `⟦σ⟧` lies wholly in subspace `S` (Confinement) and the subspace-`S` slice of `dom(Σ.M(d))` is exactly `V_S(d) = ∅`."

**Problem**: This clause forward-references `act` (defined two paragraphs later) and the Confinement lemma (stated one paragraph later) — a reader following the definition top-to-bottom hits the conclusion `act = ∅` before either ingredient exists. The same fact is then re-derived, in proper order, inside R6: "If `V_S(d) = ∅` the sharpening is trivial: `act = ∅`, every named position is an unbound terminal overrun of the empty active range..." Two passages establishing the identical `V_S(d)=∅ ⟹ act=∅` consequence.

**Required**: Cut the "but then `act = ∅` ..." clause from the V-spec definition, keeping only the admissibility statement ("any well-formed start of depth ≥ 2 is admissible"). R6 already carries the empty-subspace consequence where `act` and Confinement are in scope.

### Issue 2: R6's closing paragraph speculates about authorization/consultability the model does not have
**ASN-0115, §"Partial delivery" (R6), the "Note the boundary R6 does not cover" paragraph**: "An implementation may legitimately refuse a request that names a document it cannot consult; what it may not do is fail a request merely because some named positions within a consultable arrangement are unbound."

**Problem**: "open-document precondition," "authorization," and "a document it cannot consult" name nothing in the substrate. The sole document precondition is `d ∈ dom(Σ.M)`; there is no authorization layer and no notion of consultability beyond allocation. The paragraph distinguishes R6 from a failure mode the ASN deliberately leaves unformalized — and that failure mode is already posed as an open question ("Under what conditions, if any, may a content-delivery operation be permitted to fail outright rather than deliver partially?"). The prose imagines a case the precondition excludes and restates an open question.

**Required**: Trim to a one-line scope note grounded in the model — R6 concerns absence of *binding* within an allocated `d ∈ dom(Σ.M)`, not document allocation itself — and leave the failure question to the open-questions section.

### Issue 3: Forward-reference and justification micro-accretions (batch sweep)
Three small instances of the flagged patterns, none individually load-bearing:

- **§"What a spec-set is", `item`-totality paragraph**: "Hence `item` — and therefore `deliver₁` and `deliver` below — is well-defined on its stated domain." The totality of `item` on `act` is the whole content; the "and therefore `deliver₁` and `deliver` below" is a downstream-consumer enumeration with a forward pointer.
- **Claims table, R9**: "(inline content provenance deferred — see the inline-provenance open question below)" — a deferral pointer occupying a claim slot.
- **§"What a spec-set is" (V-spec definition)**: "This is the same discipline ASN-0058's ContentReference imposes (`#ℓ = #u = m` ...)." — justification-by-precedent of the depth-compatibility constraint (not a *use* of ASN-0058's definition, an appeal to its existence). Lowest priority of the three.

**Problem**: Each makes the reader step past a pointer or precedent appeal to follow the actual claim.

**Required**: Drop the consumer enumeration, the deferral parenthetical, and the precedent aside; the underlying statements stand without them.

## OUT_OF_SCOPE

None. The open-questions section already captures the natural successors (inline provenance, failure conditions, both-store-empty references, channel faithfulness, straddling spans), and no claim defines behavior for a scope-listed sibling operation (R10 delivers a link *reference* and explicitly defers structure-reading to READLINK rather than specifying it).

VERDICT: REVISE
