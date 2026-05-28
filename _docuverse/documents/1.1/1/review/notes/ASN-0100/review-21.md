# Review of ASN-0100

## REVISE

### Issue 1: S8★ single-run merge relies on an unstated inc/shift identification
**ASN-0100, §Per-subspace span decomposition (S8★)**: "the Insertion region `{(shift(p, k), a_k) : 0 ≤ k < n}` forms a single correspondence run `(p, a_0, n)` … The I-adjacency `a_{k+1} = a_k + 1` (in ordinal-shift notation, identifying `inc(·, 0)` on a T4-valid same-length successor with the ordinal-shift operation) is the M-adjacency required by M7's merge condition (ASN-0058)."

**Problem**: This packs three foundation facts into a parenthetical "identifying":
- The mapping-block run `(p, a_0, n)` denotes `{(shift(p,k), a_0 + k)}` (OrdinalShiftBase). For this to equal `{(shift(p,k), a_k)}` you need `shift(a_0, k) = a_k`, i.e. `inc^k(a_0, 0) = shift(a_0, k)`. That holds only because each `a_k` is T4-valid (so `sig(a_k) = #a_k` by **TA5-SigValid**, making `inc(·,0)` bump the last component, matching `shift(·,1)`) and because `inc(·,0)` **preserves T4** (TA5a) so the identity iterates.
- The V-adjacency `shift(p, k+1) = shift(shift(p, k), 1)` is **TS3 (ShiftComposition)**.

None of TA5-SigValid, TA5a, or TS3 is cited at this step. "The I-adjacency is the M-adjacency by identifying inc with shift" is a claim, not a derivation (Standard 6).

**Required**: Show the chain explicitly: cite TA5-SigValid (a_k is T4-valid, so `sig = #`, so `inc(a_k,0)` modifies only the last component, equal to `shift(a_k,1)`), TA5a (T4 preservation, so the iterate `a_0 + k = a_k` holds for all `k`), and TS3 for the V-side. Then the M7 merge condition is established rather than asserted.

### Issue 2: The `a_k + k` run-denotation is reused without derivation across sections
**ASN-0100, §Worked example (interior, single correspondence run `(p, a_0, n)`)** and **§S8★**: the run `(p, a_0, n)` is treated as denoting `{(shift(p,k), a_k)}` throughout.

**Problem**: Same gap as Issue 1, surfacing wherever the Insertion region is described as one block. The equivalence `a_0 + k = a_k` (OrdinalShiftBase `+`) versus the allocation fact `a_{k+1} = inc(a_k, 0)` is load-bearing for the "single block" / "single run" claim and for the M7-mergeability that underwrites the canonical decomposition's uniqueness. It is never proven, only gestured at.

**Required**: Establish the lemma once (Insertion addresses satisfy `a_k = shift(a_0, k)` because `A_C(d)`'s chain elements are T4-valid same-length successors) and reference it at both sites.

## OUT_OF_SCOPE

### Topic 1: Link-subspace insertion (`K.μ⁺_L` / `K.λ` analogue)
**Why out of scope**: The ASN explicitly bounds itself to the content subspace and flags the link-subspace operation as structurally distinct; the Open Question about link-subspace insertion invariants belongs in a future ASN, not here.

### Topic 2: COPY / version-creation mechanics
**Why out of scope**: The INSERT-vs-COPY section and the `INS.identity.version` corollary contrast INSERT's allocation identity against COPY and versioning only to fix INSERT's identity character; they do not specify COPY or K.δ version-derivation mechanics, and the ASN states these are out of scope. This is acceptable framing, not drift.

VERDICT: REVISE
