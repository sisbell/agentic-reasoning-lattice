# Review of ASN-0085

## REVISE

### Issue 1: OrdAddHom proof omits well-definedness check for the RHS application of TumblerAdd
**ASN-0085, OrdAddHom Proof**: "By TumblerAdd for ord(v) ⊕ w_ord:"
**Problem**: The proof applies TumblerAdd to `ord(v) ⊕ w_ord` without verifying TumblerAdd's precondition `actionPoint(w_ord) ≤ #ord(v)`. The step is: `actionPoint(w_ord) = k − 1` (by w_ord postcondition) and `#ord(v) = m − 1` (by ord postcondition), so the check reduces to `k − 1 ≤ m − 1`, which follows from the given `actionPoint(w) = k ≤ m`. This is one arithmetic step, but a precondition check for the central tool (TumblerAdd) applied in the central proof should be explicit.
**Required**: Before the RHS expansion, state: "The application is well-defined: `actionPoint(w_ord) = k − 1 ≤ m − 1 = #ord(v)`, since `k ≤ m` by precondition."

### Issue 2: Subspace preservation is established in the proof but never stated as a formal postcondition
**ASN-0085, w_ord section**: "position 1 (the subspace identifier) is preserved by any addition v ⊕ w. This is the mechanism by which arithmetic stays within a subspace."
**Problem**: The ASN's introduction promises to formalize the decomposition — "tumbler addition commutes with the decomposition." The ordinal half is formalized (OrdAddHom: `ord(v ⊕ w) = ord(v) ⊕ w_ord`). The subspace half — `subspace(v ⊕ w) = subspace(v)` when `w₁ = 0` — is derived inside the OrdAddHom proof (`r₁ = v₁` since `1 < k`) and described in prose in the w_ord section, but appears in no formal contract. Without it, the decomposition is half-formalized: downstream consumers can cite the ordinal commutation but must re-derive subspace invariance from TumblerAdd each time.
**Required**: Add a formal property (either as a postcondition of OrdAddHom or a separate one-line property) stating: under OrdAddHom's preconditions, `subspace(v ⊕ w) = subspace(v)`. Then derive the full decomposition identity as a corollary: `v ⊕ w = vpos(subspace(v), ord(v) ⊕ w_ord)`, which follows from subspace preservation + OrdAddHom + the inverse property vpos(subspace(v), ord(v)) = v. This is what "addition commutes with the decomposition" means as a single equation.

## OUT_OF_SCOPE

### Topic 1: Subtraction homomorphism and round-trip properties
**Why out of scope**: The ASN correctly identifies these as open questions. TA7a's subtraction closure results are conditional (S-membership depends on action point depth, divergence position, and relative lengths), so the subtraction analog of OrdAddHom requires a multi-case analysis that is genuinely new work, not a missing case in the current proofs.

VERDICT: REVISE
