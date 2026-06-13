# Review of ASN-0123

I checked the load-bearing proofs in full: SA (the stored-address antichain argument from LP-Sub + the zero-count contradiction), VN-B1 (the K.δ case analysis showing only frontier arrivals into a version namespace), the `nextv` frontier identity derived from VN-B1 + S0 without B2, the PS coverage derivation (`n₀ ≼ e` propagated through K.δ, making `ω` total on E), V8's coverer-set equality, and — most carefully — V9's structural O5(i)/O5(ii) discharge and the severance proof, V9w's P4★/P-bdy step, and both worked instances (the arithmetic checks: `a₁ ⋠ a₂`, `|R'∖R| = |A| = 2`, the position-4 divergence in the cross-owner instance). The mathematics is sound. I found no correctness or missing-case defects. The remaining issues are residual forward-reference/meta-prose accretion (the note's anti-bloat classifier) plus one self-containment nit.

## REVISE

### Issue 1: Cross-owner identity clause carries a proof-obligation roadmap and a duplicated domain line
**ASN-0123, The Operation / identity clause (cross-owner branch)**: "*The branch presupposes an account-tier forker (zeros(pfx(π)) = 1, so pfx(π) ∈ E carries that namespace by PS incumbency); the node-tier case lies outside the operation's domain (P-tier). Validity and freshness of this K.δ are discharged at V-WF; the stream form [pfx(π), 0, k] and its consequences — Document(v), pfx(π) ≼ v (O5(i)), and the maximality (O5(ii)) — at V9.*"

**Problem**: Two accretion patterns in a definitional slot.
- The node-tier exclusion is already stated, with its full rationale, in the P-tier explanation block above ("*A node-tier non-owner … satisfies neither disjunct and lies outside the domain: reaching a document from a node prefix would first baptize an intermediate account …*"). The branch's "*the node-tier case lies outside the operation's domain (P-tier)*" is a back-pointer restating it — two paragraphs saying the same thing.
- The final sentence is a proof-obligation roadmap ("discharged at V-WF; … at V9"), and it is echoed downstream in **V-WF**: "*The stream form's ownership-facing consequences — pfx(π) ≼ v (O5(i)) and coverer-maximality (O5(ii)) — are established at V9.*" V-WF consumes only `Document(v)` (for the K.μ⁺ precondition); the O5(i)/O5(ii) sentence advances nothing in V-WF and only points to V9. So the same Document(v)/O5 deferral to V9 appears in two sections.

**Required**: In the branch, keep the load-bearing account-tier presupposition (`zeros(pfx(π)) = 1`, `pfx(π) ∈ E` carries A_doc) and the definition of `v`; drop the redundant node-tier restatement and the proof-location inventory. In V-WF, drop the O5(i)/O5(ii) pointer (it consumes only `Document(v)`). **This is not the declined dep-audit finding, and is not about the protected discharge**: V9's O5(ii) maximality proof and V-WF's AllocatorHierarchy/ChildSpawnFreshness/FrontierEquivalence machinery stay intact — only the cross-referencing pointers and the duplicated line are at issue.

### Issue 2: Use-site inventory around the B=E identification
**ASN-0123, State and Local Apparatus (baptism-apparatus paragraph)**: "*The version-allocation arguments below use only the document tier of this identification; PS's incumbency clause (iv) draws on the account tier.*" — paired with PS(iv)'s forward reference "*the entity-level B=E identification (below)*".

**Problem**: This is a downstream-consumer enumeration ("X below uses the document tier; PS(iv) uses the account tier") wrapped in a bidirectional cross-reference (PS(iv) → "below", apparatus → "PS(iv)"). It does not advance the B=E identification; it only routes the reader to where each tier is later consumed.

**Required**: State the entity-level B=E identification once where it is established; let PS(iv) cite it inline rather than forward-reference "(below)", and drop the consumer-inventory sentence. A reader meets the document-tier and account-tier uses at their sites.

### Issue 3: Process-artifact reference breaks self-containment
**ASN-0123, V11 (snapshot/window discussion)**: "*On the snapshot question, the design record (Q8 of the consultation) draws a line our model makes precise.*"

**Problem**: "Q8 of the consultation" points at an internal elaboration artifact an implementer reading this spec does not have. The substantive grounding for the same line is already present in the sentence via Nelson [LM 2/37].

**Required**: Drop the "(Q8 of the consultation)" parenthetical; the Nelson citation already carries the design point.

## OUT_OF_SCOPE

Scope is well-managed: the cross-owner branch performs document-level allocation but stays squarely within versioning (one K.δ transcribing the source), not ASN-0103 document-creation; version comparison and the editing/link/delivery operations are correctly named out of scope and only touched where a frame condition bears (V9w's provenance, V12's correspondence). The eight Open Questions defer genuine future territory (concurrent-fork serialization, supersession vs. permanence, derivation-direction recovery from symmetric provenance) without leaving gaps in the current contract. Nothing to relocate.

VERDICT: REVISE
