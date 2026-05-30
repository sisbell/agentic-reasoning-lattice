# Review of ASN-0042

## REVISE

### Issue 1: O5 (a necessary condition) used as a sufficient authorization grant
**ASN-0042, O7 postcondition (b) proof and O10 "Per-baptism authorization"**: "Hence `π'` satisfies O5's authorization condition for allocating within `odom(π')`." / "The single baptism is performed by `π`, the most-specific covering principal of `a'` at `Σ` (by the non-coverage analysis). O5 (SubdivisionAuthority) is satisfied. … The baptism is authorized."
**Problem**: O5 is stated purely as a necessary condition — `allocated_by_{Σ'}(π,a) ⟹ pfx(π) ≼ a ∧ (most-specific)`. Showing the two consequent conjuncts hold for `π` does not establish that `π` *may* allocate, nor that `allocated_by(π, a')` holds. Reading O5 as granting permission affirms the consequent. The Unilateral O10★ claim ("performed by `π` alone") asserts `allocated_by(π, a')`, which the general proof never derives. Notably, the **worked example does this correctly** ("since O16 gives the fresh prefix some allocator … O5 and delegation condition (ii) both identify that allocator … and O1b makes it unique: `π_A`"), so the general proofs are simply missing the chain their own example uses.
**Required**: In O7(b) and O10, derive the allocator identity explicitly: ASN-0040's `Bop(pfx(π),2)` is applicable (B6 holds); by O16 the fresh `a'` has some allocator in `Π_Σ`; by O5 that allocator is a most-specific cover; by the non-coverage analysis + O1b it is uniquely `π`. Then "performed by `π`" is established rather than asserted.

### Issue 2: Forward-reference / defensive meta-prose around NestingByDelegation
**ASN-0042, OwnershipDomainPermanence (statement paragraph)**: "This is the formal consumer of NestingByDelegation: the 'sub-delegate' reading is not informal commentary but the `covers_Σ*` conjunct, discharged in Step 4 below."
**Problem**: This sentence advances no reasoning — it is a defensive justification of why a conjunct exists plus a forward pointer ("discharged in Step 4 below") to the proof that follows immediately. The reader must skip past it to reach the claim. This is the forward-reference accretion the anti-bloat classifier targets.
**Required**: Delete. The `covers_Σ*` conjunct stands on its own in the formula; Step 4 discharges it without an announcement.

### Issue 3: Axiom-role annotations explain "why needed" rather than what the conditions say
**ASN-0042, O15**: "Condition (ii) is the *authorization* clause — the delegator `π` must be the most-specific covering principal of `pfx(π')` in `Π_Σ`, so no principal may delegate within a sub-domain it has already delegated away. Condition (iv) enforces *top-down delegation order* … Condition (v) is the *next-reachability* gate …"
**Problem**: These are rationale paragraphs attached to an axiom, explaining the motivation/consequence of each clause rather than stating content. The clauses (i)–(v) are already written formally above; the "so no principal may delegate…" gloss is downstream-consequence prose that belongs in the property that consumes it (O7/O8), not at the axiom.
**Required**: Either fold the role-names inline as one-word labels in the formula, or move the consequence sentences into the proofs that actually use them.

### Issue 4: Back-reference deferral inside a Formal Contract slot
**ASN-0042, O7 Formal Contract, postcondition (c)**: "(the entry-state versus per-state discharge of these conditions is established in the proof of postcondition (c) above)."
**Problem**: A Formal Contract should state the postcondition, not point back to its own proof. This is the "defer to a downstream/adjacent location" pattern in a structural slot.
**Required**: State the condition the contract guarantees (the right is to next-reachable single-step stream extensions, satisfiable when O15 (ii),(iv),(v) hold at the prospective state); drop the pointer.

## OUT_OF_SCOPE

(No improperly-scoped claims found. The Open Questions correctly defer ownership transfer, cross-node federation, and accessibility-on-principal-removal to future ASNs.)

VERDICT: REVISE
