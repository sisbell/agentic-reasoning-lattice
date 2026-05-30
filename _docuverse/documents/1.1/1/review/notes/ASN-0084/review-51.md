# Review of ASN-0084

## REVISE

### Issue 1: Dependency-audit paragraph is meta-prose / use-site inventory

**ASN-0084, opening "Dependency audit"**: "No property of ASN-0053 (Span Algebra) is invoked anywhere in the body. The region/interval reasoning that span algebra would otherwise supply — disjointness, coverage, split, and merge of spans (ASN-0053 SC, S1, S3, S4) — is instead grounded in ASN-0036's D-SEQ... ASN-0053 therefore has no use site and is flagged for removal from the inquiry's `depends:` set."

**Problem**: This is housekeeping about the inquiry's `depends:` set, not reasoning that advances the rearrangement argument. It also inventories what each cited foundation supplies ("every region/interval argument... cites one or both (T1, OrdinalShift, TS2–TS5, TA5...)") — a use-site inventory the precise reader must skip past. The anti-bloat classifier on this note specifically targets this pattern.

**Required**: Reduce to the operative fact — "ASN-0053 is unused; remove from `depends:`" — and delete the explanation of what span algebra "would otherwise supply."

### Issue 2: Empty-right-exterior case is stated three times inside R-BLK

**ASN-0084, R-BLK Phase 1**: the "Outside ⋃_k V(bₖ)" bullet (steps (1)–(3)) establishes that only c_{n−1} may fall outside V_S(d); then the immediately following "Explicit trace for the empty right-exterior case" sub-paragraph re-derives the same conclusion ("every run b_k... has V-extent V(b_k) ⊆ V_S(d)... hence max{ord(v)...} ≤ N < ord(c_{n−1})"); and the "Consequences of R-PRE → Empty-exterior boundary cases" paragraph states it a third time.

**Problem**: Two paragraphs in the same lemma say the same thing in different words ("two paragraphs in the same document say the same thing"). The "Explicit trace" sub-paragraph adds no new obligation over the bullet's steps (1)–(3); it restates them with a concrete `c_{n−1} = [S, N+1]`.

**Required**: Keep the steps (1)–(3) justification; delete the "Explicit trace" restatement. The dedicated boundary worked example already supplies the concrete instance.

### Issue 3: R-SP "Q is non-trivial" is defensive meta-prose

**ASN-0084, R-SP**: "*Q is non-trivial.* Singleton-run partitions establish S8 existence on any finite arrangement... so 'M'(d) admits *some* correspondence-run partition' alone is satisfied by *any* M'(d) and discriminates no rearrangements. Q strengthens this in two directions: (i)... (ii)..."

**Problem**: This paragraph argues that the postcondition is worth proving rather than proving it. It is essay content justifying Q, not a step in establishing Q. A reader following the discharge of Q must skip it.

**Required**: Remove, or compress to a one-clause note inside Q's definition that the witness must be the specific R-BLK output rather than an arbitrary partition.

### Issue 4: Duplicated "non-S branch records..." justification in R-PPERM and R-SPERM

**ASN-0084, R-PPERM and R-SPERM** (verbatim in both): "The non-S branch records, in the piecewise definition itself, that π is the identity on positions with subspace(v) ≠ S — exactly the (NS-π) clause of R-NS, which the proof below cites once at the non-case."

**Problem**: This sentence explains why a definitional branch exists and announces that "the proof below cites it once" — a justification of structure plus a forward use-site pointer, duplicated across the two lemmas. The cross-reference to R-NS(NS-π) is already made at the point of use in each proof.

**Required**: Delete the sentence from both formula blocks; the proofs already cite R-NS(NS-π) where the non-S case is discharged.

### Issue 5: R-SP necessity sketches exceed the lemma's declared scope and defer to a downstream open question

**ASN-0084, R-SP**: the lemma "establishes sufficiency only (one direction, ⇐)", yet supplies three full necessity counterexample constructions (R-PRE(iv), CS3, R-PRE(i)/(ii)) plus a "*Why R-PRE(iv) is structural*" / "*Why CS3 is load-bearing*" commentary, and closes: "A full necessity proof... is left as the open question recorded above."

**Problem**: The body carries necessity material the lemma does not claim and then defers the actual result downstream — "multiple paragraphs... defer to the same downstream location." The "Why ... is structural/load-bearing" sub-paragraphs explain significance rather than advancing a proof obligation.

**Required**: Either promote necessity to a claimed postcondition (and prove it), or cut the sketches to a single sentence per conjunct and let the open question stand. The current middle ground inflates a sufficiency lemma with unclaimed, deferred analysis.

## OUT_OF_SCOPE

### Topic 1: k-cut rearrangements for k > 4
**Why out of scope**: Correctly deferred to Open Questions; the n ∈ {3,4} restriction (CS1) is a deliberate scope boundary, not an omission.

### Topic 2: Composition of multiple rearrangements
**Why out of scope**: Whether two rearrangements compose to a single rearrangement is genuinely new territory; the single-operation invariant audit here is self-contained.

### Topic 3: Depth m_1 > 2 and cross-subspace (link) rearrangement
**Why out of scope**: The depth-2 text-subspace restriction is stated up front; lifting it is a future ASN, not a gap in this one.

VERDICT: REVISE
