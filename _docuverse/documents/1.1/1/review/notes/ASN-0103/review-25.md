# Review of ASN-0103

The operation is correctly specified: the place/content seam, the single-K.δ decomposition, the length-restricted frontier `D_A` (with the clean motivating counterexample in the worked example), and the invariant discharge are all sound. The math checks out — `D_A = E ∩ S(A,2)`, freshness via `d ∈ S(A,2)\E`, monotonicity via S0 + FirstForkRoot, and the vacuity/frame routing of `ExtendedReachableStateInvariants` all hold. My findings are anti-bloat (the note carries that classifier), not correctness.

## REVISE

### Issue 1: Stacked "we deliberately do not use X" defensive justifications

**ASN-0103, Effect One (Freshness paragraph)**: "We deliberately do *not* route this through B8 (Uniqueness; ASN-0040): B8's same-namespace branch carries the precondition... S0's injectivity over S(A, 2) needs no single-authority premise at all." Immediately followed by "In particular we do not need GlobalUniqueness (ASN-0034), whose precondition demands... B7 delivers cross-namespace distinctness with no such obligation." Then "Nor do we route through partition independence (T10): its non-nesting premise... B7 sidesteps that premise entirely."

**Problem**: Three consecutive paragraphs explain which foundation lemmas are *not* used and why their preconditions are undischarged. This is defensive negative-space prose — the positive arguments (S0 gives injectivity over `S(A,2)`; B7 gives namespace disjointness) are what carry the claim. The reader must work past three rebuttals to follow a result that stands on two cited lemmas.

**Required**: Keep the positive arguments (S0 for same-chain injectivity, B7 for cross-namespace/cross-account). Delete the B8, GlobalUniqueness, and T10 rebuttals, or compress all three to a single clause if any warning value remains.

### Issue 2: Defensive "we cannot appeal to T9" prose

**ASN-0103, Effect One (subsequent-case version dominance)**: "For a version v we cannot appeal to T9 (ForwardAllocation), which orders only same-allocator pairs: v lives in A_v(d_i), a different allocator from A_doc(A). We argue directly by lexicographic order."

**Problem**: Same pattern as Issue 1 — a paragraph justifying why a tool *doesn't* apply before giving the direct argument. The direct T1 lexicographic argument that follows is self-contained.

**Required**: Open directly with the lexicographic argument; drop the T9 disclaimer.

### Issue 3: CND.A-act prose explains why the axiom is needed and enumerates its consumer

**ASN-0103, "The Operation's Input" (CND.A-act paragraph)**: "This is the account-level analogue of SubAllocatorBundle... we take it as owed by account provisioning — structurally, since owning an account *is* the authority to fork documents beneath it... CND.A-act is what lets Effect One's `d ∈ S(A, 2)` discharge ActivatedEmission for `d` below."

**Problem**: The closing sentence is a downstream use-site inventory ("is what lets Effect One... discharge ActivatedEmission below"), and the surrounding prose argues *why the assumption is needed* rather than stating what it asserts. The assumption itself (`A ∈ E ∧ Account(A) ⟹ Activated(A_doc(A))`) is the content.

**Required**: State the assumption and its provenance (owed by out-of-scope account provisioning) in one line. Remove the use-site pointer and the rationale essay.

### Issue 4: Repeated deferrals to the same downstream location

**ASN-0103**: The effective-owner / O5 deferral appears at least four times: CND.pre ("deferred to the registry-carrying ASN (see Open Questions)"), the "State preconditions" bullet (verbatim repeat), the Ownership section ("we defer them to a registry-carrying ASN (see Open Questions)"), and CND.own ("both deferred — see Open Questions").

**Problem**: Multiple paragraphs in different sections defer to the same downstream location — a flagged accretion pattern. The deferral is a single fact.

**Required**: State the deferral once (the Ownership section is the natural home, since it carries the substantive O1-vs-O5 distinction). Drop the restatements in CND.pre, the preconditions bullet, and CND.own.

### Issue 5: Distinctness argument (S0 + B7) duplicated across four sites

**ASN-0103**: The "same-chain by S0, cross-namespace/cross-account by B7, content/link by zero-count" distinctness argument is given in Effect One's freshness paragraph, restated in CND.monotone, restated again under "Invariants Maintained → Address permanence (T8...)" ("same-chain emissions by S0..., version chains and cross-account documents by B7..., content/link addresses by zero-count"), and a fourth time in the CND.inv table row.

**Problem**: Two paragraphs (Effect One and Invariants Maintained) say the same thing in different words; the proof route is established once and re-narrated. The "Invariants Maintained" restatement adds nothing the Effect One argument did not already establish.

**Required**: Prove distinctness once in Effect One. In "Invariants Maintained," cite it ("distinctness as established in Effect One") rather than re-deriving the S0/B7/zero-count split.

## OUT_OF_SCOPE

### Topic 1: "A Note on Sub-Allocator Activation" forward-looking sentences

**ASN-0103**: "The first INSERT into `d` will draw `[d.0.s_C.1]` from `A_C(d)`; the first MAKELINK will draw `[d.0.s_L.1]` from `A_L(d)`."

**Why out of scope**: INSERT and MAKELINK are explicitly out of scope. The activation-without-emission fact (CND.subAlloc) belongs here; the forward narration of how out-of-scope operations will consume the anchors is borderline essay content. Not an error — but if trimmed under the anti-bloat pass, the INSERT/MAKELINK sentences are the candidates, since CND.subAlloc already carries the load-bearing "available but empty" claim.

VERDICT: REVISE
