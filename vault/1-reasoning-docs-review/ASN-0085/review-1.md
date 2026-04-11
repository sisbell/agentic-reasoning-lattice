# Review of ASN-0085

## REVISE

### Issue 1: All three definitions lack formal contracts
**ASN-0085, Ordinal Extraction**: "ord(v) = [v₂, ..., vₘ] — the tumbler of length m − 1 obtained by stripping the subspace identifier."
**Problem**: No precondition/postcondition/frame block on any of the three definitions. The foundations (ASN-0034, ASN-0036) give every definition explicit contracts. These definitions omit:

- **Preconditions**: `ord(v)` requires `#v ≥ 2`, otherwise the result is the empty sequence — not in T (T0 requires length ≥ 1). `vpos(S, o)` requires `S ≥ 1` and `(A i : 1 ≤ i ≤ #o : oᵢ > 0)` for the result to satisfy S8a. `w_ord` requires `#w ≥ 2`.
- **Postconditions**: `ord(v)` produces a tumbler in S (TA7a's domain) when `v` is a valid V-position per S8a — every component of `v` is positive, so stripping the first yields all-positive components. This is the key output guarantee and it's unstated. `vpos(S, o)` should establish that its output satisfies S8a under the right preconditions on `S` and `o`.
- **Frame**: `ord` and `vpos` are pure functions on sequences — no state is read or modified. State it.

**Required**: Add formal contract blocks to all three definitions, following foundation conventions. At minimum: explicit preconditions including depth bounds, postconditions establishing result membership (in T, in S, satisfying S8a as appropriate), and frame conditions.

### Issue 2: The central property is missing — arithmetic does not factor through the decomposition
**ASN-0085, preamble**: "These definitions are the operational bridge between the full V-position space and the ordinal-only arithmetic that TA7a prescribes."
**Problem**: A bridge requires both endpoints connected. The ASN defines the mapping functions but never shows that arithmetic commutes with the decomposition. The property is:

For V-position `v` with `#v = m ≥ 2` and displacement `w` with `w₁ = 0`, `#w = m`, `w > 0`:

`ord(v ⊕ w) = ord(v) ⊕ w_ord`

This follows directly from TumblerAdd: since `w₁ = 0`, `actionPoint(w) ≥ 2`, so position 1 is copied from `v` into `v ⊕ w`. Stripping position 1 from both sides of the equation reduces the full-position addition to ordinal-level addition. The proof is a three-line case analysis on TumblerAdd's definition — the positions before the action point copy from `v` (becoming `ord(v)`), the action point adds, and the tail copies from `w` (becoming `w_ord`).

A corollary for shift: `ord(shift(v, n)) = shift(ord(v), n)`, because `δ(n, m)` has `w₁ = 0` and `w_ord = δ(n, m-1)`.

Without this property, the definitions are inert — they name "strip first component" and "prepend a component" without establishing that the decomposition is structure-preserving. The open question at the end of the ASN asks about exactly these properties, but they should be the main content, not deferred questions.

**Required**: State and prove the arithmetic homomorphism as a lemma. Add it to the statement registry. The shift corollary should be a named consequence.

### Issue 3: No connection to TA7a's domain S
**ASN-0085, Ordinal Extraction**: "Per the ordinal-only formulation of TA7a (ASN-0034), we define the extraction and reconstruction functions."
**Problem**: TA7a defines S = {o ∈ T : #o ≥ 1 ∧ (A i : 1 ≤ i ≤ #o : oᵢ > 0)} and establishes closure of S under addition and (conditionally) subtraction. The ASN references TA7a but never shows that `ord(v) ∈ S` for valid V-positions. The argument is immediate — S8a guarantees all components of `v` are positive, so all components of `ord(v) = [v₂, ..., vₘ]` are positive, placing it in S — but it must be stated as a postcondition of `ord`. Without it, there is no formal warrant for applying TA7a's closure guarantees to extracted ordinals.

**Required**: Add `ord(v) ∈ S` as an explicit postcondition of `ord(v)`, citing S8a. This closes the gap between extraction and TA7a's domain.

### Issue 4: "V-depth displacement" is undefined
**ASN-0085, w_ord**: "For a V-depth displacement w with w₁ = 0 and #w = m"
**Problem**: The term "V-depth displacement" appears without definition. Neither ASN-0034 nor ASN-0036 defines it. The characterization `w₁ = 0 ∧ #w = m` is given inline but not named or motivated. The condition `w₁ = 0` is structurally necessary — it ensures `actionPoint(w) ≥ 2`, which by TumblerAdd means position 1 (the subspace identifier) is copied from the operand, preserving the subspace. This reasoning is absent.

**Required**: Either define "V-depth displacement" formally (a displacement `w` with `#w = m` and `w₁ = 0`, ensuring within-subspace arithmetic by forcing `actionPoint(w) ≥ 2`) or drop the term and state the conditions directly with a one-line justification for why `w₁ = 0` is imposed.

## OUT_OF_SCOPE

### Topic 1: Subtraction homomorphism and round-trip properties
**Why out of scope**: The ASN's open question asks about `(ord(p) ⊕ w_ord) ⊖ w_ord = ord(p)` and generalization to depth > 1. These are natural follow-ons once the addition homomorphism (Issue 2) is established, but they involve TA7a's conditional subtraction results (where S-membership of the result depends on the specific operands). A separate section or extension can address these without blocking convergence of the core definitions and addition homomorphism.

### Topic 2: Interaction with span operations
**Why out of scope**: How ordinal decomposition interacts with span splitting, span coverage, and POOM operations is downstream of this ASN. The definitions here are prerequisites; the span-level consequences belong in the operation ASNs.

VERDICT: REVISE
