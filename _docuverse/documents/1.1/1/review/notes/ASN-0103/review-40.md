# Review of ASN-0103

The mathematics is sound. I verified the length-filter construction (`D_A = E ∩ S(A,2)`, both inclusions), the document-level/validity/freshness/distinctness sub-proofs, the cross-chain exhaustiveness derivation via ActivatedEmission + AllocatorHierarchy + B7, and the worked example demonstrating why the length filter averts the version-collision. All check out. The remaining issues are prose accretion around the standing assumption and frame, consistent with this note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: CND.A-act rationale repeated four times
**ASN-0103, multiple sections**: The standing assumption `A ∈ E ∧ Account(A) ⟹ Activated(A_doc(A))` is accompanied by the same "exists-the-instant-the-account-does" gloss in four locations:
- input section: "an activated document sub-allocator exists whenever the account does";
- Formal Contract precondition: "the account's document sub-allocator being live the instant the account exists";
- claims table CND.A-act: "an account carries an activated document sub-allocator the instant it exists, with no separate activation step";
- Invariants Maintained (ActivatedEmission): "its activation is supplied by the standing assumption CND.A-act."

**Problem**: This is the flagged pattern — prose around an assumption re-explaining *why it is owed / that there is no separate activation step* rather than stating its content, repeated across sections. The "owed by out-of-scope account provisioning" rationale and the "instant it exists" gloss compound across slots.
**Required**: State CND.A-act once with its content; cite it by label at the three use-sites without re-glossing the rationale.

### Issue 2: State frame restated verbatim in Effect Three and Formal Contract
**ASN-0103, "Effect Three" and "The Operation: Formal Contract"**: The full frame (`C' = C`, `L' = L`, `R' = R`, `E' = E ∪ {d}` with `d ∉ E`, `M'(d) = ∅`, and `(A d' ∈ E_doc : M'(d') = M(d'))`) is given as display equations in Effect Three and then re-listed identically as the Formal Contract's Effect bullets.
**Problem**: The same equations appear twice as canonical statements (the per-conjunct restatement in Invariants Maintained is legitimate verification, but these two are duplicate declarations). A reader must reconcile two identical specifications.
**Required**: Keep the frame equations in the Formal Contract (the canonical contract) and reduce Effect Three to the prose that motivates them, or vice versa — do not carry the equations in both.

### Issue 3: CND.no-sharing largely restates CND.empty
**ASN-0103, Claims table**: "CND.no-sharing | At creation the fresh document references no I-address at all: ran(M'(d)) = ∅ (CND.empty), so at Σ' it shares no I-address with any document."
**Problem**: This is `ran(M'(d)) = ∅` (CND.empty) plus a scope deferral to S5/transclusion. It adds a trivial consequence and an out-of-scope pointer rather than independent content.
**Required**: Fold the "shares no I-address" observation into CND.empty's consequences, or justify CND.no-sharing as a distinct guarantee; drop the standalone claim if it is only CND.empty restated.

## OUT_OF_SCOPE

The note correctly confines forking, content/link allocation, node/account provisioning, and effective ownership to citations or Open Questions, and defines no claims for them. Nothing to flag.

VERDICT: REVISE
