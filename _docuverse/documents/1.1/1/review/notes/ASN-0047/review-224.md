# Review of ASN-0047

## REVISE

### Issue 1: S8★ contradicts itself about S8 condition (c)
**ASN-0047, *Amendments to existing transitions*, S8★ (per-subspace span decomposition)**: "It intentionally does *not* carry ASN-0036's S8 condition (c) — uniqueness of the maximal-run decomposition. For the content subspace, the partition together with conditions (a) and (b) is exactly ASN-0036's S8."

**Problem**: The umbrella statement says S8★ drops (c) entirely. But the content-subspace route is described as "a direct application of ASN-0036's S8," and S8 (foundation) explicitly asserts "(c) the maximal-run decomposition is unique." So either content-subspace S8★ inherits (c) (and the umbrella "does not carry (c)" is over-broad), or it does not (and "exactly ASN-0036's S8" is wrong, since S8 includes (c)). As written the two sentences cannot both hold.

**Required**: Scope the (c)-dropping to the link subspace only. State that content-subspace S8★ is the full ASN-0036 S8 (including uniqueness, since the projection's range is `dom(C)` and S3 holds), while only the link-subspace projection — discharged by the trivial length-1 decomposition — omits (c). Remove the unqualified "S8★ does not carry condition (c)."

### Issue 2: Defensive consistency-restatement in the K.μ~ decomposition (Step B.3)
**ASN-0047, *Decomposition of K.μ~*, Step (B), sub-claim (B.3)**: "*(B.3) The realised post-state is consistent with S3★(Σ').* The decomposition's post-state must not *contradict* the admissibility-stipulated S3★(Σ'); we check it does not."

**Problem**: B.3 derives nothing beyond re-aggregating B.1 (S3★ at the intermediate state) and B.2 (new content positions target dom(C)). It restates the union of (i) framed survivors and (ii) new positions and re-asserts `dom(C') = dom(C)`, `dom(L') = dom(L)` already fixed by the composite frame. This is the "two paragraphs say the same thing in different words" pattern: B.1 + B.2 already establish S3★(Σ'); B.3 is a defensive "we check it does not contradict" paragraph that the precise reader must skip. The carrier (clause-(i) admissibility) already stipulates S3★(Σ'); Step (B) only needs to show the decomposition realises it, which B.1+B.2 do.

**Required**: Delete B.3, or compress to a one-line conclusion ("B.1 and B.2 jointly establish S3★(Σ') over `dom(M'(d))`; framed arrangements `d' ≠ d` carry S3★ from the pre-state").

### Issue 3: Open question references the superseded non-star invariants
**ASN-0047, *Open Questions***: "What invariants must the link subspace satisfy beyond those inherited from D-CTG, D-MIN, and S8-depth ... that D-SEQ does not capture?"

**Problem**: This ASN supersedes D-CTG/D-MIN with D-CTG★/D-MIN★ (dropping the link-subspace exemption) and establishes D-SEQ★ as a system-wide invariant covering the link subspace. The open question frames the link subspace as governed by the base (exempted) forms, which is exactly what this ASN replaced. A reader cannot tell whether the question asks about a gap the ASN already closed.

**Required**: Reframe against the starred forms actually in force (D-CTG★/D-MIN★/D-SEQ★), so the question scopes genuine future territory rather than the superseded baseline.

## OUT_OF_SCOPE

### Topic 1: Link inheritance under forking
**Why out of scope**: J4 explicitly leaves "a mechanism for link inheritance under forking" to a future ASN; the fork composite copies only the content subspace, and the link-subspace-empty fork is correctly within this ASN's contract.

### Topic 2: Tombstoning / interior link withdrawal
**Why out of scope**: The tension between Nelson's tombstoning (LM 4/9) and D-CTG★/D-MIN★ suffix-only contraction is correctly deferred to a separate withdrawal-mechanism ASN (open question), not an error in this ASN's K.μ⁻ contract.

VERDICT: REVISE
