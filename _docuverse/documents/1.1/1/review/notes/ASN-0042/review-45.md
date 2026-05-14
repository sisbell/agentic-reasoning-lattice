# Review of ASN-0042

## REVISE

### Issue 1: hwm description is technically incorrect in O10 non-coverage analysis

**ASN-0042, "The Fork as Ownership Boundary" (O10 proof, Form B analysis)**: "and therefore U^{(i)}_1 ≤ hwm_0 by definition of hwm (which takes the maximum of the depth-2 component over S(pfx(π), 2) ∩ Σ.B)"

**Problem**: ASN-0040 defines `hwm(B, p, d) = #children(B, p, d)` — the cardinality of the children set, not the maximum of the depth-2 component. The substantive conclusion `U^{(i)}_1 ≤ hwm_0` is correct only via B1 (ContiguousPrefix), which establishes that `children = {c_1, ..., c_{hwm}}` so the max index equals the cardinality. As stated, the citation misrepresents the foundation property.

**Required**: Replace the parenthetical with an explicit citation of B1 (ContiguousPrefix): "by B1, children(Σ.B, pfx(π), 2) = {pfx(π).0.k : 1 ≤ k ≤ hwm_0}, so pfx(π).0.U^{(i)}_1 ∈ children forces U^{(i)}_1 ≤ hwm_0."

### Issue 2: Worked example cites O5 for delegation authority

**ASN-0042, Worked Example, "Account-level permanence"**: "By O5, only π_A (the effective owner of dom(π_A)) can delegate sub-accounts extending [1, 0, 2]."

**Problem**: O5 (SubdivisionAuthority) governs *allocation* of new addresses, not *delegation* of new principals. The ASN explicitly distinguishes these in the Delegation section: "ownership delegation, which introduces a new principal into Π, and allocation, which creates addresses within an existing principal's domain." The authority requirement for delegation is condition (ii) of the `delegated` relation — the delegator must be the most-specific covering principal — not O5.

**Required**: Replace "By O5" with "By condition (ii) of the delegation relation" (or "By the most-specific covering principal requirement for delegation").

### Issue 3: O10 proof references `S'` without formal definition

**ASN-0042, O10 Formal Contract, Unilateral postcondition**: "PrefixBaptismCoupling ensures every sub-delegate's prefix lies in Σ.B, so S' ⊆ {1, …, hwm_0} and hwm_0 + 1 ∉ S' in every reachable state."

**Problem**: The symbol `S'` denotes the set of first user-field components of length-(#pfx(π) + 2) Form B sub-delegate prefixes, but this set is not formally defined anywhere in the ASN. The reader must infer the definition from context.

**Required**: Either define `S'` explicitly when first introduced (e.g., `S' := {U^{(i)}_1 : π_i ∈ Π_Σ, pfx(π_i) = pfx(π).0.U^{(i)}_1}`) or restate the bound in the existing notation: "every length-(#pfx(π) + 2) Form B sub-delegate `π_i` has `U^{(i)}_1 ≤ hwm_0`, so `hwm_0 + 1` is never one of them."

## OUT_OF_SCOPE

### Topic 1: Ownership transfer mechanism

**Why out of scope**: The ASN explicitly notes the tension between Nelson's mention of "someone who has bought the document rights" and the lack of transfer machinery, recording it as Open Question and not claiming the model addresses it. This is correctly deferred — the structural ownership model captures the system as specified, and transfer would require a separate registry overriding address-derived ownership.

### Topic 2: Principal identity binding mechanism

**Why out of scope**: The "Principal Identity and the Trust Boundary" section explicitly records that authentication is exogenous to the ownership model. Properties O0–O10 hold for any consistent identity binding. This is appropriate scoping.

### Topic 3: Cross-node identity federation

**Why out of scope**: O9 (NodeLocalOwnership) establishes that ownership authority is bounded by node prefix; the question of whether the same human can hold standing on multiple nodes via federation is correctly placed in Open Questions, not claimed as a property here.

VERDICT: REVISE
