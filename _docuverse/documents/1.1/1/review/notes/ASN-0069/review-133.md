# Review of ASN-0069

This ASN is in strong shape. The proofs cover the edge cases the operation demands (empty source, first vs. subsequent fork, fork-of-fork chains, sibling forks), the foundation citations are confined to declared dependencies (34, 36, 40, 47), and where a foundation gap exists (≼-transitivity is not published by ASN-0034's Prefix contract) the ASN proves it inline rather than assuming it. I found no substantive rigor errors. One proof-step justification is circular and should be repaired.

## REVISE

### Issue 1: The composite verification discharges `d_op ∈ E_doc` by citing the precondition it is supposed to be establishing
**ASN-0069, §"The Fork Composite", K.μ⁺ discharge**: "with `M^{(1)}(d_op) = M(d_op)` by K.δ's frame condition ... applied to `d_op ≠ d_new` — the inequality holds because V1 places `d_new ∉ E_doc` pre-fork while `d_op ∈ E_doc` pre-fork, **as J4's precondition requires `d_op ∈ E_doc`**."

**Problem**: This verification exists to show the fork composite *is* a valid J4 instance; it may not lean on "J4's precondition requires `d_op ∈ E_doc`" to supply that very fact — that is circular within a validity check. For a first fork the fact is trivial (`d_op = d_src ∈ E_doc`, V0's precondition). For a subsequent fork `d_op = d_prev`, the fact is genuinely non-trivial and *is* independently established two paragraphs earlier in K.δ sub-case B ("Per-sub-case `d_prev ∈ E` holds by P1 ... applied to `d_prev`'s earlier K.δ event", together with `Document(d_prev)`). The discharge cites the wrong ground.

**Required**: Replace "as J4's precondition requires `d_op ∈ E_doc`" with the actual derivation: `d_op = d_src ∈ E_doc` (first fork) or `d_op = d_prev ∈ E_doc` via the K.δ sub-case B P1-argument (subsequent fork). This keeps the validity check non-circular.

## OUT_OF_SCOPE

### Topic 1: K.μ⁻ expressiveness aside in the worked example
**ASN-0069, §"Worked Example"**: "A middle-only deletion such as removing `[s_C, 2]` while keeping `[s_C, 3]` is not expressible as a K.μ⁻ at all."
**Why out of scope**: DELETE mechanics are out of scope; the worked example's legitimate purpose here is demonstrating source isolation (V5a), which it does. The expressiveness claim about K.μ⁻ retention is a characterization of the deletion operation, not of the fork, and belongs with the K.μ⁻ contract. It is an aside, not a fork claim, so this is a placement note rather than a defect.

VERDICT: REVISE
