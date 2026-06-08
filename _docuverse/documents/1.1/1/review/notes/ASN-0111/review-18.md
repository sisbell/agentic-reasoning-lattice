# Review of ASN-0111

## REVISE

### Issue 1: RL0 states "necessary but not sufficient" twice in adjacent paragraphs
**ASN-0111, RL0 (Definedness)**: The RL0 paragraph says "The link-shape of an address is necessary but not sufficient for definedness: an address may parse as a well-formed link tumbler yet name no allocated link." The very next paragraph repeats: "These conditions are necessary but not sufficient: an address may have link-shaped structure yet name no allocated link."
**Problem**: Two adjacent paragraphs make the identical point in different words — the duplication forces the reader to confirm nothing new was added the second time.
**Required**: Keep one statement. Fold the reader-side structural test (`zeros(a) = 3 ∧ subspace_I(a) = s_L` testable from the address) into a single paragraph that states the necessary-not-sufficient fact once.

### Issue 2: Completeness intro and RL1 both reject the "satisfaction model"
**ASN-0111, Completeness section**: Paragraph 1 — "A search is satisfied by a witness: a link is returned when *one* span of each endset meets the request... It must return the endsets *entire*." RL1 paragraph — "the *content* of the claim is the rejection of the satisfaction model: an alternative implementation that returned only the spans matching some implicit predicate would not be reading the link — it would be searching it."
**Problem**: The read-vs-search contrast via the witness/satisfaction notion is made twice within one short section. The second statement re-argues the first rather than advancing RL1.
**Required**: State the read-vs-search contrast once. RL1's justification can be the one-line "immediate from the definition, `readlink(a, Σ) = Σ.L(a)` componentwise" without re-litigating the satisfaction model.

### Issue 3: RL2 opening prose divides labor between RL1 and RL2 instead of advancing RL2
**ASN-0111, RL2 (Role preservation)**: "Completeness (RL1) already forces per-slot set equality `readlink(a, Σ).eᵢ = Σ.L(a).eᵢ` for every `i`; what RL2 adds is the *structural* status of that equality."
**Problem**: This is meta-prose explaining why RL2 is a distinct claim from RL1 — the reviser-drift pattern (prose justifying a claim's existence relative to a neighbor). The substantive RL2 content (arity preservation, slot index as model primitive per L6) stands on its own without the bookkeeping about what RL1 "already forces."
**Required**: Open RL2 directly with its claim: the read preserves arity and exposes each `eᵢ` under its slot index as a model primitive (L6). Drop the RL1/RL2 division-of-labor sentence.

### Issue 4: RL2's N>3 handling is stated in two places
**ASN-0111, RL2 paragraph and worked-example RL2 bullet**: The RL2 paragraph already establishes "slots 4…N returned faithfully under their own indices and no privileged role assigned by this operation." The worked example then re-derives this: "verifying slots 1–3 establishes the claim for every `N ≥ 3`: an arity-4 value `(F, ∅, Θ, e₄)` returns `e₄` under slot 4 by exactly the same copy, with no slot-count-dependent step to recheck."
**Problem**: The closing tail "with no slot-count-dependent step to recheck" is an exhaustiveness justification duplicating the main RL2 paragraph's all-N point. The concrete arity-4 instance is fine as verification; the defensive exhaustiveness clause is not.
**Required**: Keep the arity-4 concrete check; drop the "no slot-count-dependent step to recheck" defensive clause, since the per-index copy rule was already stated in RL2 proper.

## OUT_OF_SCOPE

(none — the note correctly defers search, follow, count, and creation to their own ASNs without specifying claims for them.)

VERDICT: REVISE
