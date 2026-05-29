# Review of ASN-0036

## REVISE

### Issue 1: S4 and S5 prose recapitulate the same postcondition content

**ASN-0036, §Content identity / §Sharing**: S4's prose — "S4 creates a fundamental asymmetry in the system. The content store `C` is oblivious to values… But the arrangement family `M` is sensitive to addresses…" — is then restated in S5's prose: "The combination of S4 and S5 gives the system its distinctive character. S4 says identity is structural — determined by I-address, not by value."

**Problem**: The S5 paragraph re-summarizes S4's asymmetry in different words. This is accreted recap prose: a reader following the S5 claim must skip past a restatement of S4 already given two sections earlier. The carrier of each claim is its Formal Contract; the duplicated essay framing does not advance the argument.

**Required**: Remove the cross-claim recap. State the S4∧S5 consequence (quotation as a first-class structural relationship) once, without re-narrating what each property "says."

### Issue 2: S7a and S7d both restate Nelson's baptism principle

**ASN-0036, §Structural attribution (S7a, S7d)**: S7a — "Nelson's baptism principle establishes it: 'The owner of a given item controls the allocation…'". S7d — "Nelson's baptism principle covers it directly: the user-level allocator baptises documents under the user's prefix in the same way each document's allocator baptises elements…".

**Problem**: Two axioms in the same section invoke and paraphrase the same grounding principle, the second merely shifting it up one hierarchy level. This is the "multiple paragraphs say the same thing in different words" pattern accreting around adjacent design-requirement axioms.

**Required**: Ground the baptism principle once (in S7a or a shared preamble) and have S7d cite it without re-paraphrasing.

### Issue 3: `subspace(v)` definition is over-specified for a first-component projection

**ASN-0036, §Singleton span partition**: the `subspace(v) = v₁` definition carries a signature, preconditions, two postconditions ((a) ℕ-membership "inherits T0's carrier," (b) `≥ 1` "by S8a"), and a Depends block.

**Problem**: For a trivial projection of the first component, the postcondition that the result "inherits T0's ℕ-valued carrier" and a separate S8a dependency are meta-accretion — they explain provenance that is immediate from the projection itself, not properties of `subspace` that downstream proofs consume as the named lemma.

**Required**: Reduce to the definition and signature. Drop the inherited-carrier postcondition.

## OUT_OF_SCOPE

### Topic 1: Whether DELETE/INSERT/COPY/REARRANGE preserve D-CTG, D-MIN, S2
Operation frame/postconditions are explicitly out of scope; the ASN correctly defers these to the Open Questions and an operations-layer ASN.

### Topic 2: Displacement mechanism guaranteeing contiguity preservation under insertion
This is operation-layer machinery (how following positions shift), not a state invariant, and is properly listed as open.

VERDICT: REVISE
