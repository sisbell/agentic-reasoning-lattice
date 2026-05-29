# Review of ASN-0053

## REVISE

### Issue 1: Self-citation by the ASN's own number

**ASN-0053, S11d proof**: "By SC (SpanClassification, ASN-0053), exactly one of five cases holds" — and the table row "(iii) Proper overlap ... By S11c", with S11d itself tagged citing internal claims as "(SpanClassification, ASN-0053)".

**Problem**: SC, S11, S11a–c are all defined *in this document*. Tagging them with "ASN-0053" treats the note as if it were an external dependency. This is the self-contained-ASN convention inverted: foundation citations carry a number (ASN-0034), in-document claims must not.

**Required**: Drop the "ASN-0053" tag everywhere it labels an in-document claim. Write "By SC", "by S11c", etc.

### Issue 2: Repeated boilerplate well-formedness verification (anti-bloat)

**ASN-0053, S1, S3, S4, S8 (×2), S11, S11c (Case 1 and Case 2)**: each proof re-runs the identical paragraph — "since s < r and #s = #r, the divergence k is of type (i) with k ≤ #s, the width r ⊖ s has a positive component at position k, so it is positive with action point k ≤ #s — T12 is satisfied; #width = max(#r,#s) = #s, so level-uniform."

**Problem**: This is one lemma instantiated seven-plus times with only the names changed — exactly the compounding redundancy the anti-bloat classifier targets. The reader must re-verify identical reasoning at every site, and any correction must be made in seven places.

**Required**: Hoist a single named lemma — e.g., "WF: for s, r ∈ T with s < r and #s = #r, the pair (s, r ⊖ s) is a well-formed level-uniform span with reach r" — and cite it at each construction site instead of re-deriving.

### Issue 3: S11 asserts the containment boundary characterization without derivation

**ASN-0053, S11 proof**: "Containment means start(α) ≤ start(β) and reach(β) ≤ reach(α)."

**Problem**: This is stated as a definitional equivalence, but deriving reach(β) ≤ reach(α) from ⟦β⟧ ⊆ ⟦α⟧ in tumbler space is non-trivial — it requires the non-emptiness argument (if reach(β) > reach(α), then reach(α) ∈ ⟦β⟧ since start(β) < reach(α), forcing reach(α) ∈ ⟦α⟧, i.e. reach(α) < reach(α), contradiction). S11d explicitly derives the *symmetric* reverse-containment boundary chars one section later, so the asymmetry is conspicuous: one direction is hand-waved, the mirror direction is proved.

**Required**: Supply the short derivation in S11 (or cite the S11d derivation), so both containment directions are established at the same rigor.

### Issue 4: Implementation-mechanic citations inside abstract claims

**ASN-0053, S1**: "the function `spanintersection` always produces at most one output span (Q10, `correspond.c:210-265`)"; similarly S4a/S5 cite `tumblerlength(cut) = tumblerlength(width)` aborts (Q14, Q15).

**Problem**: File-and-line and function-name citations are implementation mechanics, not system guarantees. The abstract claims (S1 single-span intersection, S4 exact partition) stand on T1/T12/D1 alone; the `correspond.c` line range adds nothing to the proof and pins the abstract law to one implementation. This is borderline drift, not termination-level — the claims themselves remain properly abstract.

**Required**: Keep the abstract proof; demote the file:line confirmations to brief evidentiary notes or remove them. Do not let an abstract law's justification rest on a concrete source location.

## OUT_OF_SCOPE

### Topic 1: Span-set–level difference bound

**Why out of scope**: The tight bound on |normalize(⟦Σ₁⟧ \ ⟦Σ₂⟧)| for normalized span-sets is correctly deferred to the Open Questions, not asserted here. S11d closes only the two-span difference; the set-level generalization is a future ASN, not a gap in this one.

### Topic 2: Population-dependent re-normalization

**Why out of scope**: The note correctly flags (citing Nelson) that the canonical form is unique only "at a given instant" and that allocation between addresses may force revision — and correctly leaves the minimal-update problem as an open question rather than attempting it here.

VERDICT: REVISE
