# Review of ASN-0100

## REVISE

### Issue 1: Reference to a non-existent foundation claim "K.δ-IsDocument"

**ASN-0100, §"Frame Conditions" (INS.frame.E) and §"Post-state V-position well-formedness… and S7 invariants" (P6 argument)**:
- "`E' = E`. The entity set is unchanged: no K.δ fires in the decomposition (`dom(M)` is governed via K.δ-IsDocument under ValidComposite★…)"
- "the ValidComposite★ invariant `E_doc = dom(M)` (every document is allocated with `M(d) = ∅` by **K.δ-IsDocument**, the sole extender of `dom(M)`; **ASN-0047**)"

**Problem**: There is no claim named `K.δ-IsDocument` in ASN-0047 (or any foundation). The second occurrence explicitly attributes it to ASN-0047, which is a dangling/misattributed citation — a precise reader cannot locate it. The mechanism it names is already supplied by the foundation under different names: K.δ's frame for the `Document(e)` case (`dom(M') = dom(M) ∪ {e}` with `M'(e) = ∅`) and M1 (ArrangementMonotonicity), whose prose states `dom(M) = E_doc`. Per standard 7, inventing a label for something a foundation already defines is a REVISE item. (The underlying substance — `dom(M) = E_doc`, extended only by K.δ's Document case — is correctly supported; only the reference is broken.)

**Required**: Replace both uses of `K.δ-IsDocument` with the actual foundation references: K.δ's Document-case arrangement frame (ASN-0047) for "the sole extender of `dom(M)`", and M1 (ArrangementMonotonicity, ASN-0047) for the invariant `dom(M) = E_doc`.

## OUT_OF_SCOPE

(none)

Notes on what was checked and found sound: the three-region disjointness/exhaustiveness (INS.M-exhaustive), the closed-interval D-CTG★ reduction including the arbitrary-pair and off-prefix (`m ≥ 3`) cases, both K.α branches (first-emission and subsequent-emission after full clearance), the append (`Right = ∅`, K.μ⁻ omitted) and empty-document cases, the I3-identification and its restricted inheritance of I3-S2/S3/VP/VD/fin combined with Insertion-region disjointness, the per-intermediate atomicity discharge (including the post-K.μ⁻ contraction state with no I3 counterpart), post-state uniqueness under decomposition freedom, the forced-ordering analysis, and both wp computations. No rigor gaps found in these. The prose in §Background, the Effect One/Two/Three narrative, and §"What is not allocated" is dense but falls within the exempted "what the operation does / concrete example" categories rather than meta-prose.

VERDICT: REVISE
