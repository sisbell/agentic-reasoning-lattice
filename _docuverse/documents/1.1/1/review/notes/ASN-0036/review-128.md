# Review of ASN-0036

## REVISE

### Issue 1: S7c Depends mismatch — unjustified TA7a citation
**ASN-0036, S7c Properties table vs. Formal Contract**: The Properties table row reads "design; uses S7b, T4, T4b, TA7a, T10a.4, S0 (ASN-0034)", but the S7c Formal Contract Depends lists only "S7b (element-level I-addresses) — provides E(a); T4b (UniqueParse) — defines element-field projection."
**Problem**: T4, TA7a, T10a.4, and S0 appear in the table but not in the contract. TA7a in particular has no visible role — S7c is a pure design axiom asserting `#E(a) ≥ 2`; nothing in its statement or any nearby reasoning consumes TA7a's ⊕/⊖ subspace-closure results. The citation is noise.
**Required**: Reconcile the two Depends lists. Remove TA7a unless a use is shown; either add T4/T10a.4/S0 to the contract or drop them from the table.

### Issue 2: S7a Depends mismatch
**ASN-0036, S7a Properties table vs. Formal Contract**: Table says "uses T4, T4b, T10a, T10a.4, S0"; contract Depends lists "T4, T4b, S7b, T10a, T10a.4."
**Problem**: The table cites S0 (absent from the contract) and omits S7b (present in the contract). One of the two is wrong about what S7a actually rests on.
**Required**: Make the table and contract agree on S7a's dependency set.

### Issue 3: Repeated T10a.4 "surrounding T4-validity" boilerplate
**ASN-0036, S7a/S7b/S7c/S7d/S7/ShiftPreservation Depends**: The clause "T10a.4 (T4PreservationUnderDiscipline) — supplies the surrounding T4-validity (no adjacent zeros, positive endpoint components ...) on which T4b's projections rely" recurs near-verbatim across six contracts.
**Problem**: This is use-site/justification accretion. The same explanatory paragraph repeated across contracts is prose the reader must skip past at each occurrence; a single citation suffices once the rationale is stated once.
**Required**: State the T10a.4→T4b rationale once (e.g., at S7b, the first element-level claim) and reduce the later citations to the bare "T10a.4 — T4 preservation."

### Issue 4: Triple deferral to the same downstream location
**ASN-0036, Span decomposition intro / S8 postcondition / S8 proof**: "deferred to the open question on unique maximal decompositions"; "(Coalescing deferred — see open questions.)"; "minimality is not claimed."
**Problem**: Three paragraphs in the same section defer the identical question (run coalescing) to the identical downstream location — the flagged "multiple paragraphs defer to the same downstream location" pattern.
**Required**: Keep one deferral (the S8 postcondition note) and remove the redundant forward pointers.

### Issue 5: Reviser-drift in S5 cross-document construction
**ASN-0036, S5 proof**: "the index range `i ∈ {1, …, N + 1}` is required so that the `D(dᵢ) = [i]` field has a strictly positive component ... at `i = 0` the trailing component would be a zero, which T4 reads as a field separator rather than a content component."
**Problem**: The construction binds `i ∈ {1, …, N+1}`, so `i = 0` is already excluded. Explaining why the excluded `i = 0` would violate T4 imagines a case the construction's own range rules out — defensive prose around a witness, not advancing the proof.
**Required**: State the witness range; drop the `i = 0` failure analysis.

## OUT_OF_SCOPE

### Topic 1: Operation-level preservation of D-CTG, D-MIN, S2
The ASN correctly defers (open questions) whether INSERT/DELETE/COPY/REARRANGE preserve the contiguity invariants and subspace alignment. Operations are out of scope; no error.

### Topic 2: Subtraction homomorphism `ord(v ⊖ w)` and round-trip conditions
Listed as open questions; the additive homomorphism (OrdAddHom) is the in-scope content, and the subtractive analogue belongs to a future ASN.

VERDICT: REVISE
