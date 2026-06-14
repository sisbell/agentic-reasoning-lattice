# Review of ASN-0123

## REVISE

### Issue 1: `nextv`'s B2-non-citation footnote is reviewer-defense, not construction, and echoes in three further sites
**ASN-0123, "State and Local Apparatus" (nextv)**: "we are careful *not* to obtain it by citing ASN-0040's B2 (HighWaterMarkSufficiency): B2's stated precondition is the *global* B1 … silent about the other entity-level B6-valid namespaces … namely the document-creation namespace (account, 2) … and the account-creation namespace (node, 2) … Taken as a black box with its stated hypothesis, B2 is therefore unavailable here. No global invariant is needed."

**Problem**: The frontier identity `nextv(E,d) = c_{hwm+1}` is established right there from VN-B1 (proved next) plus S0 — the case split on `m=0` / `m≥1` does the whole job. The ~90-word paragraph adds nothing to that derivation; it pre-empts a "why not just cite B2?" objection, i.e. it explains a *non-action*. The same non-transfer is then re-litigated in V5(a) ("derived above from VN-B1 + S0 without B2's global precondition") and V0 ("B8's same-namespace case, whose B1/B2 preconditions are invariants of ASN-0040's own transition system and do not transfer"). This is justification accreting across cycles. (Distinct from VN-B1's own one-line "B1 … does not transfer … so we prove its analog," which legitimately motivates the *reproof* and should stay.)

**Required**: Drop the B2 footnote from `nextv`; keep only the frontier derivation. Drop the "without B2's global precondition" reminder in V5(a). In V0, the same-allocator distinctness already rests on GlobalUniqueness (stated independently in the same paragraph), so the B1/B2 non-transfer clause is removable.

### Issue 2: V0's count argument analyzes a case P-tier excludes, duplicating the P-tier comment
**ASN-0123, V0 (FreshUniquePermanentIdentity)**: "a node-tier non-owner (zeros(pfx(π)) = 0, which O1a admits into Π) holds no document namespace, so reaching a document from a bare node prefix would first baptize an intermediate account — a second permanent entity (P1) — breaking the single mint, and must instead establish an account first, an out-of-scope prior act."

**Problem**: P-tier's second disjunct (`zeros(pfx(π)) = 1`) places the node-tier non-owner outside the operation's domain, so V0's "exactly one identity" claim only has to count the two *in-domain* branches — one K.δ each. The node-tier paragraph reasons about an input the carrier already excludes. Worse, the P-tier comment already states this exact conclusion: "That restriction is what holds the fork to a single mint and places the node-tier non-owner outside the domain; V0 carries the count." So the exclusion rationale lives in both P-tier and V0, while P-tier simultaneously *defers* the count to V0 — a round trip.

**Required**: Let V0 count the two in-domain branches (owned: one version K.δ; account-tier cross-owner: one document K.δ) and cite P-tier for the domain restriction. If the node-tier→second-mint argument is worth keeping, keep it once, at P-tier where the domain is defined.

### Issue 3: V9 preamble editorializes around the (load-bearing) O5(ii) derivation
**ASN-0123, V9 preamble**: "The account-tier restriction (zeros(pfx(π)) = 1) is precisely what makes π's ownership of the fork *established* rather than assumed — and it establishes it *structurally* … rather than by importing O5 over an allocation whose landing is left unspecified." … "(allocated_by(π, v) also makes the O5 axiom applicable, yielding the same O5(i)/(ii); we give the structural proof because it does not lean on PS's stipulation that O5 governs every K.δ.)" … "the placement detail the identity clause left out of scope (which k) is genuinely not needed".

**Problem**: The structural discharge itself — stream form `[pfx(π),0,k]` ⟹ O5(i) and the Z-mono maximality for O5(ii) — is load-bearing and must stay (it closes the cross-owner soundness gap). What surrounds it is proof-method editorial: "established rather than assumed," "structurally rather than by importing O5," the parenthetical defending the choice of a structural proof over an O5 citation, and the reassurance that the unspecified `k` "is genuinely not needed." These explain *why this proof rather than that one* and *why an omission is harmless* — commentary about the derivation, not the derivation.

**Required**: Keep the O5(i)/(ii) derivation verbatim. Replace the framing with the technical point it carries — one sentence, e.g. "Every member of `S(pfx(π),2)` has the form `[pfx(π),0,k]`, which yields `pfx(π) ≼ v` (O5(i)) and, via Z-mono on the length-`(#pfx(π)+1)` prefix `[pfx(π),0]`, the maximality O5(ii); the within-stream index `k` plays no role." Drop the "established rather than assumed" and the O5-applicability parenthetical.

## OUT_OF_SCOPE

No out-of-scope claims to reclassify. The note's stated scope (fork alone; editing, comparison, link/document creation, delivery, replication excluded) is honored — neighbors are touched only where a frame condition or foundation invariant bears on the fork's guarantees (e.g., V2b's CL-OWN/K.μ⁺_L appeal). The eight open questions correctly externalize genuinely future obligations (concurrent-fork serialization, recovering derivation direction from symmetric provenance, location-fixed windowing) rather than smuggling them into this ASN.

VERDICT: REVISE
