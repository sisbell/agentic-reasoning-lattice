# Review of ASN-0036

## REVISE

### Issue 1: S7d's rationale paragraph is positioning meta-prose, not content

**ASN-0036, S7d (Document allocation discipline)**: "This is a design requirement parallel to S7a. Nelson's baptism principle covers it directly: the user-level allocator baptises documents under the user's prefix in the same way each document's allocator baptises elements under the document's prefix. Where S7a governs how I-addresses sit beneath their owning document's prefix, S7d governs how the document tumblers themselves are produced."

**Problem**: The final sentence describes the *division of labor* between S7a and S7d — why S7d exists alongside S7a — rather than what S7d asserts. This is exactly the "new prose around an axiom explains why the axiom is needed rather than what it says" pattern. The axiom itself (`zeros(d) = 2`, allocated under T10a, distinct events → distinct documents) is already complete in the Formal Contract.

**Required**: Delete the "Where S7a governs… / S7d governs…" positioning sentence. The baptism quote, if retained, suffices to ground the design requirement; the S7a comparison adds no reasoning.

### Issue 2: Operation-preservation deferred in four separate places

**ASN-0036, D-CTG Frame / post-D-SEQ / concrete-example Violation / Open Questions**:
- D-CTG Frame: "preservation across editing operations is each operation's verification obligation."
- After D-SEQ: "Whether DELETE, INSERT, COPY, and REARRANGE preserve D-CTG is a verification obligation for each operation's ASN."
- Concrete example: "a well-formed deletion must also shift subsequent positions to restore contiguity."
- Open Questions: "Does each well-formed editing operation (DELETE, INSERT, COPY, REARRANGE) preserve D-CTG and D-MIN?"

**Problem**: Four touch-points defer the identical claim (operation-preservation of contiguity belongs to future operation ASNs). This is the "multiple paragraphs defer to the same downstream location" pattern compounding across the note.

**Required**: Keep the deferral in exactly one place — the Open Question is the correct slot. Remove the redundant statements in the D-CTG Frame and the post-D-SEQ sentence; the concrete-example remark may stay only as a concrete illustration of *why* a bare removal violates D-CTG, not as another deferral.

### Issue 3: Within-subspace lemma *Remark* imagines a precondition-excluded case

**ASN-0036, S8 proof, *Remark* after "Application to w"**: "S8-depth is essential. Without it, `dom(M(d))` could contain `s.3` (depth 2) and `s.3.1` (depth 3)…"

**Problem**: The lemma carries S8-depth as a precondition; this paragraph constructs the very state S8-depth forbids in order to argue S8-depth is needed. This is the "imagines a case the precondition already excludes" / "why the axiom is needed" pattern. It does not advance the proof of the lemma — the proof is already complete at "no distinct V-position in the same subspace falls in `v`'s singleton interval."

**Required**: Remove the Remark. The depth-≥3 violation already appears as a concrete example in the "Violation (depth ≥ 3)" block of the worked example section, where an illustrative role is appropriate; here it is duplicated meta-justification.

### Issue 4: The "Corollary" is embedded inside the S8 proof and duplicates ShiftPreservation

**ASN-0036, S8 proof**: the "Corollary (subspace and field-structure preservation across a correspondence run)" sits between the "Existence" and "Non-canonicality" paragraphs of the partition proof, then is restated verbatim in the Formal Contract's Postconditions.

**Problem**: A corollary interrupting the existence/coverage/uniqueness argument breaks the proof's spine — the reader must skip past it to reach "Non-canonicality" and "Coverage." Its content is a pointwise application of ShiftPreservation (conclusions i–iv), already proved above, and is stated a third time in the contract. This is relocated/duplicated content (reviser drift).

**Required**: Move the corollary out of the proof body to a position after the proof concludes (or fold it entirely into the contract, since it is a one-line consequence of ShiftPreservation + S3). State it once.

### Issue 5: ValidInsertionPosition structural claims verified twice

**ASN-0036, Valid insertion position**: the prose block "We verify the structural claims, which apply to both predicates" establishes *Distinctness*, *Depth preservation*, *Subspace identity*, and *S8a consistency*; the two Formal Contracts then re-assert these as postconditions (a)–(d).

**Problem**: The four labeled sub-verifications and the two contracts' postconditions cover the same ground in different words ("two paragraphs in the same document say the same thing"). The free-text verification adds nothing the per-predicate contracts do not already state with their own derivations.

**Required**: Either drop the standalone verification prose and let the contracts carry the postconditions, or collapse the contracts' postcondition derivations into the shared block — not both.

## OUT_OF_SCOPE

### Topic 1: Operation-level preservation of D-CTG, D-MIN, S2

**Why out of scope**: Whether DELETE/INSERT/COPY/REARRANGE re-establish contiguity and the displacement-mechanism invariants is correctly posed in the Open Questions and belongs to the per-operation ASNs (operation frame conditions are excluded by Scope). No error here — only the *count* of deferrals (Issue 2) is a finding.

### Topic 2: Subtraction homomorphism and round-trip for ord/w_ord

**Why out of scope**: The conditions for `ord(v ⊖ w) = ord(v) ⊖ w_ord` and `(ord(v) ⊕ w_ord) ⊖ w_ord = ord(v)` depend on TA7a's conditional S-membership for subtraction; deferring them to a future ASN is appropriate, not a gap in the addition-side homomorphism proved here.

VERDICT: REVISE
