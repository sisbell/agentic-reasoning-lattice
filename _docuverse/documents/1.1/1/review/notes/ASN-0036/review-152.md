# Review of ASN-0036

## REVISE

### Issue 1: S8a restates its definitional commitment three times
**ASN-0036, S8a (V-position well-formedness)**: the proof opens "A V-position is, by definition, an isolated element field of depth at least 2"; the Formal Contract's *Definition* repeats "A V-position is, by definition, an isolated element field of depth at least 2"; and *Preconditions* repeats it a third time ("The element-field definitional commitment (a V-position is an isolated element field of depth ≥ 2...)").
**Problem**: The same definitional sentence occupies the proof, the Definition slot, and the Preconditions slot — three sayings of one thing. This is exactly the accreted-prose pattern the classifier flags.
**Required**: State the definitional commitment once (the Definition slot), and let the proof and Preconditions reference it without re-paraphrasing.

### Issue 2: S2 postcondition justification is circular and advances nothing
**ASN-0036, S2 (Arrangement functionality), Postconditions**: "ran(Σ.M(d)) = {...} is a well-defined set — single-valuedness makes the image of M(d) depend only on its domain, so the range is determined."
**Problem**: A partial function is single-valued *by definition*, and the range of any function is determined by its domain and mapping regardless. The clause "single-valuedness makes the image depend only on its domain" restates the definition of "function" as though it were an extra property. It explains nothing the axiom above it does not already give.
**Required**: Either drop the justification (the range is well-defined trivially) or replace it with the actual content S2 is buying — that distinct V-positions may collide in the range (which the Frame already states).

### Issue 3: S3 asymmetry stated in prose and again in the Frame
**ASN-0036, S3 (Referential integrity)**: the body says "It does NOT say existence implies arrangement. Content can exist in Istream without being arranged..."; the Frame then says "S3 asserts ran(M(d)) ⊆ dom(C) only; the converse dom(C) ⊆ ⋃_d ran(M(d)) is not asserted."
**Problem**: The directional/non-converse claim appears twice. The prose paragraph carries genuine new content (the persistence-independence consequence, the Nelson "deleted bytes" citation), but its first two sentences duplicate the Frame line.
**Required**: Keep the non-converse statement in one place (the Frame is the natural slot) and let the prose paragraph carry only the persistence consequence.

### Issue 4: S0 prose re-narrates the postconditions and forward-leans into operations
**ASN-0036, S0 (Content immutability)**: "S0 is a strong property. It asserts two things simultaneously: that a remains in the domain..., and that the value at a is unchanged.... It constrains every operation to either leave C(a) unchanged or to operate only on addresses not yet in dom(C)."
**Problem**: The "asserts two things" sentence restates Postconditions (a) domain persistence and (b) value preservation in narrative form — the decomposition is already in the contract. The "constrains every operation to..." sentence reaches into the operations layer, which this ASN scopes out for claims.
**Required**: Cut the re-narration; the postconditions already split S0 into its two conjuncts. Drop or relocate the operation-constraint sentence to an Open Question (one already covers operation preservation obligations).

### Issue 5: S4 proof carries an implementation/complexity aside
**ASN-0036, S4 (Origin-based identity), proof**: "No value comparison is required — the structural test for shared identity is address equality, computable in time proportional to the shorter address."
**Problem**: The abstract property is *decidability from the addresses alone* (T3). "Computable in time proportional to the shorter address" is a complexity/implementation claim that does not advance the abstract guarantee, and the decidability point is already made in the S4 body.
**Required**: Drop the time-bound clause; if retained at all, mark it explicitly as implementation evidence rather than part of the proof.

### Issue 6: scaffolding sentences announcing the next step
**ASN-0036, multiple sections**: "We first restrict S7's domain."; "With S7a, S7b, and S7d established, we can state structural attribution."; "Before stating the partition, we must establish the structure of dom(M(d)) more carefully."
**Problem**: These sequencing announcements describe the document's own structure rather than advancing reasoning. Individually minor, collectively they are the meta-prose the classifier targets.
**Required**: Remove; the section headings and dependency citations already convey order.

## OUT_OF_SCOPE

None to add. Operation-level preservation of D-CTG/D-MIN/S2, subspace alignment, the canonical choice of depth `m`, and the maximal correspondence-run decomposition are already correctly deferred in the Open Questions.

Note on rigor: the substantive proofs (S5 dual construction, S7 four-part attribution, S8 singleton partition with the within-subspace incompatibility lemma and the T5/T10 cross-subspace argument, D-CTG-depth's infinite-intermediate contradiction, D-SEQ's four-step assembly) are case-complete, handle the empty/base cases explicitly, and correctly treat the subspace identifier as `v₁` (first element-field component) rather than the separator. I found no skipped case or hand-wave in the mathematical content; the findings above are prose accretion and clarity, consistent with the anti-bloat classifier.

VERDICT: REVISE
