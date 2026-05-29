# Review of ASN-0036

This note carries the `review-mode.anti-bloat` classifier, and the underlying mathematics is sound — the S8 partition proof (within-subspace incompatibility lemma + cross-subspace T10 argument), D-CTG-depth, and D-SEQ all hold under inspection, and the worked example checks out component-by-component. The remaining findings are accreted meta-prose and one framing/precision issue.

## REVISE

### Issue 1: S7d postcondition annotates its downstream consumer and duplicates S7's derivation
**ASN-0036, S7d Postconditions**: "By GlobalUniqueness (ASN-0034), distinct documents have distinct document-level tumblers — the cross-document uniqueness premise for S7's identification argument."
**Problem**: The trailing clause names where the fact gets consumed (S7) rather than advancing S7d. The identical fact is then re-derived in S7's own proof under "Uniqueness across documents" ("S7d supplies the required premise — distinct allocation events — and GlobalUniqueness then guarantees... distinct"). The same inference is stated in two places, once with a use-site annotation.
**Required**: Drop the "— the cross-document uniqueness premise for S7's identification argument" clause. Let S7's proof cite S7d's postcondition directly; do not restate the GlobalUniqueness derivation in both slots.

### Issue 2: the `m ≥ 2` deferral to Open Questions is restated across multiple slots
**ASN-0036, ValidFirstInsertionPosition** — definition body: "the strand model fixes only the lower bound `m ≥ 2` (the choice of specific value is deferred to the Open Questions)"; Signature line: "The strand model fixes only the lower bound `m ≥ 2`."; and the Open Question itself ("What operation-layer constraints determine the canonical choice of m...").
**Problem**: Two paragraphs in different slots defer the same choice to the same downstream location, with the Open Question carrying it a third time. This is the multiple-deferral pattern.
**Required**: State `m ≥ 2` once in the definition; let the Open Question stand as the single forward pointer. Remove the Signature-line restatement.

### Issue 3: implementation evidence for S7a parked in the S7 proof section
**ASN-0036, S7 (prose before the proof)**: "Gregory's implementation corroborates S7a: the I-address prefix itself encodes the originating document, used during allocation to scope the search range."
**Problem**: This is corroborating evidence for S7a, sitting inside the S7 section. S7a already carries its own evidence (Nelson's baptism principle and "You always know where you are"). The sentence is relocated support, not content advancing S7.
**Required**: Move to S7a if the evidence is wanted, or drop it — S7a is already substantiated.

### Issue 4: `subspace_I` carries a full formal contract but is load-bearing in no proof
**ASN-0036, subspace_I definition** (Signature/Preconditions/Definition/Postconditions/Depends).
**Problem**: `subspace_I` appears only in S7c's motivation, the worked example, and the properties table — no claim's proof depends on it. Its sibling `subspace(v)` is genuinely consumed (S8, D-CTG, D-SEQ). A four-clause contract for a projection used once in an example is weight without a proof obligation behind it.
**Required**: Either inline `subspace_I(a) = E(a)₁` at its single use, or cite a proof that depends on it. If the symmetry with `subspace` is the only justification, that is a comment, not a contract.

### Issue 5: S8's conjunct (b) is vacuous in the exhibited witness, so the named theorem over-promises
**ASN-0036, S8 Postconditions**: "(b) `(A j, k : 0 ≤ k < nⱼ : M(d)(shift(vⱼ, k)) = shift(aⱼ, k))`. The proof exhibits the singleton decomposition (every `nⱼ = 1`), for which conjunct (b) reduces to the base case."
**Problem**: The real content the proof establishes is that the per-position half-open intervals are pairwise disjoint and cover `dom(M(d))` (this is where the lemma, T5, and T10 do work). Conjunct (b) — the only clause that gives "correspondence run" non-trivial meaning — is satisfied trivially and never exercised. The contract presents (b) as a co-equal postcondition when the proof renders it decorative.
**Required**: Foreground the established result (finite disjoint partition of `dom(M(d))` into per-position intervals) as the theorem's content, and state plainly that (b) holds only at the base case under the singleton witness — existence of any `nⱼ > 1` run is not established here. (Whether maximal runs exist/are unique is correctly left to Open Questions; the contract wording is the fix.)

## OUT_OF_SCOPE

### Topic 1: existence and uniqueness of maximal (non-singleton) correspondence runs
**Why out of scope**: Already captured in the Open Question on whether the decomposition has a unique maximal form. This is the natural successor to Issue 5's reframing, not a defect in the present ASN.

### Topic 2: preservation of D-CTG/D-MIN/S2 under INSERT/DELETE/COPY/REARRANGE
**Why out of scope**: Operation frame conditions are explicitly excluded by the Scope section and correctly deferred to the Open Questions; the strand model establishes the state invariants those operations must preserve, which is its proper remit.

VERDICT: REVISE
