# Review of ASN-0036

## REVISE

### Issue 1: S8 postcondition (b) is a tautology

**ASN-0036, S8 (Singleton span partition)**: The statement binds `aⱼ = Σ.M(d)(vⱼ)` in its preamble, then asserts as postcondition (b) "Each singleton carries its own image: `Σ.M(d)(vⱼ) = aⱼ`." The proof discharges it with "Conjunct (b) is `M(d)(v) = a`, which holds by construction."

**Problem**: Since `aⱼ` *is defined* as `Σ.M(d)(vⱼ)`, conjunct (b) reduces to `M(d)(vⱼ) = M(d)(vⱼ)`. It is true by definition and establishes nothing — it is not a proved postcondition. A reader looking for the partition's content (which is entirely in the coverage/uniqueness argument for (a)) is given a placeholder that "holds by construction."

**Required**: Either drop (b), or restate it as something with content — e.g., that the singleton labeling is well-defined because `M(d)` is a function (S2) and `aⱼ ∈ dom(Σ.C)` (S3), connecting the partition to the two invariants it actually relies on — and present it as a definition of the labeled partition rather than a theorem.

### Issue 2: S8a prose conflates subtree-contiguity with V-position contiguity

**ASN-0036, S8a (V-position well-formedness), prose**: "Since all V-positions in subspace `s` extend the single-component prefix `[s]`, T5 (ContiguousSubtrees, ASN-0034) guarantees they form a contiguous interval under T1."

**Problem**: T5 guarantees that the *prefix subtree* `{t : [s] ≼ t}` is order-convex — not that the V-positions occupying it are contiguous. V-positions can have gaps; eliminating gaps is precisely what D-CTG separately requires as a design constraint. As written, "they form a contiguous interval" asserts the D-CTG conclusion for free, which is false in general. The remark is also extraneous to S8a, whose proof establishes only `zeros(v)=0` and componentwise positivity; the subtree fact is used later (S8 across-subspace uniqueness), not here.

**Required**: Either correct the antecedent ("the prefix subtree `{t : [s] ≼ t}` is order-convex," not "the V-positions form a contiguous interval") and move it to the S8 across-subspace argument where it is actually consumed, or delete it from S8a.

### Issue 3: S5 queryability paragraph is implementation-concern essay duplicating an Open Question

**ASN-0036, S5 (Unrestricted sharing), prose**: "We observe that the state `Σ = (C, M)` makes the sharing relation computable... Nelson requires this to be queryable... The state model supports this — the information is present; only the efficiency of its extraction is an implementation concern."

**Problem**: The load-bearing content is one clause — the set `{d : ∃v M(d)(v)=a}` is determined by the state. The remainder (Nelson queryability quote, "efficiency... is an implementation concern") is essay that the note itself flags as implementation territory, and it restates the Open Question "What must the system guarantee about the computability of the sharing inverse... what is the cost bound." Under the note's `review-mode.anti-bloat` mandate, this is prose that defers to a downstream location while the substantive claim already lives elsewhere.

**Required**: Reduce to the single derivable consequence (sharing relation is a function of `Σ`); drop the efficiency tangent and the duplicate of the Open Question.

## OUT_OF_SCOPE

### Topic 1: Whether DELETE/INSERT/COPY/REARRANGE preserve D-CTG, D-MIN, S2

Already correctly parked in the Open Questions and excluded by the Scope section (operation-specific effects). The Σ₃ DELETE in the worked example only *checks* the post-state, which is appropriate; proving preservation belongs to operation ASNs.

### Topic 2: Constraints on the value domain `Val` (heterogeneity, type uniformity)

A genuine question, correctly listed as open. `Val` is deliberately opaque at this abstraction level; constraining it is future territory, not a defect here.

VERDICT: REVISE
