# Review of ASN-0040

## REVISE

### Issue 1: B8's concluding sentence overstates the uniqueness guarantee

**ASN-0040, B8 (Uniqueness), end of proof**: "No two distinct baptisms, whether in the same namespace, across sibling namespaces, or at different hierarchical levels, can produce the same address."

**Problem**: This reads as unconditional global uniqueness, but Case 1 (same namespace) is discharged *only* via B-Seq, and B8's own Formal Contract precondition restricts to "a single baptismal authority." The two distinct sub-strengths are conflated. Case 2 (different namespaces) rests on B7, which is purely structural and authority-independent — so cross-authority distinctness holds there. But the same-namespace argument depends entirely on B-Seq's serialization: two concurrent commits reading the same `s.B` with `hwm = m` would both compute `c_{m+1}` and collide. The concluding sentence claims a guarantee the proof does not establish for the same-namespace case across authorities — precisely the gap Open Question 6 acknowledges is unresolved.

**Required**: Qualify the conclusion: same-namespace uniqueness holds *under a single baptismal authority* (B-Seq); cross-namespace uniqueness (B7) is authority-independent. Make explicit which clause of the enumeration requires B-Seq.

### Issue 2: B-Seq carries a "Scope:" sub-field — flagged meta-prose pattern

**ASN-0040, B-Seq (Sequential Commitment), Formal Contract**: "*Scope:* single baptismal authority (one serialized commit path); cross-replica concurrency is out of scope."

**Problem**: The anti-bloat classifier explicitly names sub-paragraphs labeled "Scope" as accreted meta-prose to surface at source. The scoping content is load-bearing (B8 depends on it), but it belongs in the axiom statement itself, not a separate labeled slot. The "*Justification.*" line ("Gregory's udanax-green commits... through a single serialized path") is acceptable grounding, but the duplicate "*Scope:*" framing is the flagged pattern.

**Required**: Fold the single-authority restriction into the *Axiom* line (it already says "under a single baptismal authority"); delete the standalone "*Scope:*" sub-field.

### Issue 3: The single-authority / cross-replica boundary is stated in three places

**ASN-0040, B-Seq Scope + B8 precondition + Open Question 6**

**Problem**: The same cross-replica-out-of-scope boundary recurs as (a) B-Seq's Scope field, (b) B8's precondition qualifier, and (c) Open Question 6's framing. The "multiple paragraphs deferring to the same downstream location" pattern. (b) and (c) are structurally necessary (theorem precondition; open question); (a) is the redundant one.

**Required**: Remove the redundant statement once Issue 2 is addressed; let B8's precondition and Open Q6 carry the boundary.

## OUT_OF_SCOPE

### Topic 1: B3's content-storage interface constraint

**ASN-0040, B3 (Ghost Validity)**: "Content presupposes baptism: any content-storage layer built atop this model may store content at an address only after that address is baptized."

**Why out of scope**: The ghost-element characterization (baptism establishes a permanent anchor independent of content) is squarely in scope for baptism semantics. But the directional constraint imposed on a *content-storage layer* touches "content storage and retrieval," which the Scope section defers. The membership-vs-content distinction is properly baptism's; the storage-ordering rule belongs to whatever ASN specifies the content layer.

META:

VERDICT: REVISE
