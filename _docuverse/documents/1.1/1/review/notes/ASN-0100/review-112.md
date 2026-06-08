# Review of ASN-0100

This is a thorough and largely sound specification. The hard invariants — the closed-interval contiguity reduction with off-prefix exclusion at `m ≥ 3`, the S2 cross-region disjointness via the shared-prefix/last-component argument, the step-by-step projection tracking through the substrate decomposition — are done with real care and backed by concrete worked examples (interior, append, prepend, empty, deep-subspace). The substantive proofs check out. My findings are confined to forward-reference accretion and essay content, which is what the `review-mode.anti-bloat` classifier directs me to surface.

## REVISE

### Issue 1: Duplicated COPY contrast, forward-referencing an out-of-scope operation

**ASN-0100, Effect One (Allocation) and §Identity Through Allocation**:
- Effect One: "COPY (transclusion) is the only operation that aliases existing I-addresses; INSERT, being content creation, never does."
- §Identity Through Allocation: "(COPY introduces V→I references without allocating, so it carries a distinct identity character; that operation is the subject of a future ASN.)"

**Problem**: The same point about COPY — that it aliases rather than allocates, unlike INSERT — is made in two separate locations, and COPY is explicitly out of scope ("the subject of a future ASN"). This is forward-reference accretion: content about a future operation embedded twice in this note. The INSERT-side facts (fresh allocation, identity-by-creation) are fully carried by INS.alloc, INS.C, and INS.identity; the COPY contrast adds nothing those claims do not already establish.

**Required**: State the freshness/identity property of INSERT once (it already is, in INS.identity). Remove the COPY contrast from both sites, or keep at most a single bare clause noting INSERT never aliases, without describing COPY's mechanics.

### Issue 2: Decorative quotation in a proof slot

**ASN-0100, §Atomicity and Canonical Order**: "This is what Nelson calls 'all changes, once made, leave the file remaining in canonical order, which was an internal mandate of the system.'"

**Problem**: This quote closes the atomicity verification after the proof is already complete. The opening framing ("Nelson requires ... canonical order") motivates the section legitimately, but the closing quote is decorative essay content sitting in a verification slot — it restates INS.atomicity in Nelson's words without advancing the argument. The sentence that follows it ("The abstract specification commits to none of the admissible interleavings...") carries the actual conclusion and stands on its own.

**Required**: Drop the closing quotation; keep the substantive concluding sentence.

## OUT_OF_SCOPE

### Topic 1: Link-subspace insertion (`K.μ⁺_L` / `K.λ`)
**Why out of scope**: The note correctly restricts to the content subspace `s_C` and names link-subspace insertion as a distinct future operation. This is a legitimate boundary, not a gap.

### Topic 2: Closure under composition, concurrency, derived document properties
**Why out of scope**: Raised correctly in Open Questions; these are new territory (operation algebra, concurrency model, derived-state accounting), not defects in the INSERT contract as specified.

VERDICT: REVISE
