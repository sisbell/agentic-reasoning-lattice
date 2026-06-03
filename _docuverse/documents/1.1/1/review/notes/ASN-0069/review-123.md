# Review of ASN-0069

## REVISE

### Issue 1: Defensive "we cite rather than re-derive" commentary in the K.δ verification
**ASN-0069, §"The Fork Composite", K.δ shared-precondition intro and sub-cases**: "`Document(d_new)` (hence `zeros(d_new) = 2`) is V1's identity postcondition; we cite it rather than re-establish it from K.δ-ID.zeros-0/1." / "V1 gives `parent(d_new) = parent(d_src)` (its identity-postcondition consequence, not re-derived here)" / "...so we cite that result rather than re-derive it here."

**Problem**: Three separate instances of process-commentary justifying *why* a citation is a citation rather than a re-derivation. A clean citation ("`Document(d_new)` by V1", "`parent(d_new) = parent(d_src)` by V1", "T4-validity by B6(a)") needs no defense of its citation status. This is residue from the prior Issue-2 revision relocated into prose rather than removed — exactly the accretion the anti-bloat pass targets. The reader must skip past the justification to read the actual discharge.

**Required**: Replace each "we cite X rather than re-establish/re-derive it" with the bare citation. State the fact and its source; drop the meta-commentary about whether it is being re-proved.

### Issue 2: Process commentary "an asserted 'single authority' is not enough"
**ASN-0069, §"Identity by Sub-Allocation"**: "B8's same-namespace clause is the one in force for two forks of `S(d_src, 1)`, and its premises must be discharged in the ASN-0047 model — an asserted 'single authority' is not enough. We discharge them once here."

**Problem**: "an asserted 'single authority' is not enough" and "We discharge them once here" are commentary about the proof process, not content. The discharge itself (B-Seq, B0a, B1, B2, B4) is the substance and stands on its own. The framing clause adds defensive justification for performing the discharge.

**Required**: Open directly with the discharge: B8's same-namespace clause requires B-Seq, B0a, B1, B2, B4 for `S(d_src, 1)`; establish each. Drop the "not enough"/"once here" framing.

### Issue 3: Parallel inductions for `Document(d_new)` and `parent(d_new)` duplicate one skeleton
**ASN-0069, §"Identity by Sub-Allocation"**: the `Document(d_new)` induction (base via K.δ-ID.zeros-0/1, step via IH + P1) and the `parent(d_new) = parent(d_src)` induction (base via K.δ-ID.parent-0/1, step via IH) run over the same induction variable (`A_v(d_src)`'s emission count) with identical base/step structure, differing only in which K.δ-ID identity is invoked.

**Problem**: Two full inductions with the same skeleton. The first/subsequent-fork case split and the P1-carry of `d_prev ∈ E_doc` are stated twice. This is the "same structure in different words" pattern; the parent induction's summary sentence ("the induction chains this per-step preservation across `A_v(d_src)`'s emission count to recover `parent(d_src)`") then restates what its own base/step immediately establish.

**Required**: Run one induction on emission count establishing both `zeros(d_new) = 2` and `parent(d_new) = parent(d_src)` simultaneously (both per-step facts are K.δ-ID identities at the same `k`). Drop the redundant summary sentence.

## OUT_OF_SCOPE

### Topic 1: ≼-transitivity placement
V11a derives transitivity of the foundation prefix relation `≼` inline because ASN-0034's Prefix contract publishes only the definition and `p ≺ q ⟹ #p < #q`. The derivation is correct and self-contained, but a general property of a foundation relation arguably belongs in the foundation (ASN-0034), not in an operation ASN.

**Why out of scope**: This is a foundation-contract gap, not an error in ASN-0069. Deriving the needed lemma locally is acceptable self-containment; promoting it to ASN-0034 is a future foundation revision.

VERDICT: REVISE
