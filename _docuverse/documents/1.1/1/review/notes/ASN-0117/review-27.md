# Review of ASN-0117

This is a careful, well-grounded note. The two-layer split is clean, the K.μ⁻ / K.μ⁻+K.μ⁺ case analysis on `R = ∅` is correct, the coupling obligations (J0/J1★/J1'★) are discharged validly, the boundary cases (suffix-delete, delete-everything, leading-span, within-document sharing) are exercised concretely, and the discoverability wp is genuinely non-trivial and correctly quantified per-link. My findings are mostly the accreted prose the anti-bloat classifier targets, plus one rigor point.

## REVISE

### Issue 1: Duplicated summary across Effect section and conclusion
**ASN-0117, end of "DELETE(d,p,w)" Effect section**: "DELETE allocates nothing and frees nothing: the content layer sees *no change whatsoever* (DEL-CIMM). All of DELETE's work is in the arrangement layer, where it shifts the surviving suffix left to close the gap."
**Problem**: This is the same statement as the conclusion §"What we have established": "On the content layer DELETE does *nothing*: `Σ'.C = Σ.C`... On the arrangement layer DELETE is a uniform left-shift." Two paragraphs say the same thing; both restate DEL-CIMM/P0 already given in the claim table. The in-Effect sentence is a premature conclusion summary the reader must skip past.
**Required**: Delete the Effect-section closing sentence; the conclusion carries it.

### Issue 2: Meta-prose around what is/isn't a "distinct claim"
**ASN-0117, §"Content permanence, and address permanence"**: "The question also lists *address permanence*... as a distinct obligation, but it is not a distinct claim: it is read off P0 directly. The equation `dom(C') = dom(C)` is precisely 'frees nothing, allocates nothing'... and `(A b...)` is precisely 'no address is rebound.'"
**Problem**: This is defensive prose parsing an equation into prose synonyms, responding to an anticipated "but you didn't separately prove address permanence." The substantive content is one sentence: address permanence is P0. A related instance: "satisfies the *entire* per-state invariant package... uniformly — every conjunct that theorem closes over, not a hand-picked subset" defends against an imagined cherry-picking objection rather than advancing the argument.
**Required**: Collapse the address-permanence paragraph to one sentence; drop the "not a hand-picked subset" defensive clause.

### Issue 3: Invariant-package appeal assumes reachability without stating it
**ASN-0117, §"The document remains one coherent sequence"**: "Because DELETE is a valid composite of elementary K.μ⁻/K.μ⁺ steps... its post-state satisfies the *entire* per-state invariant package of **ExtendedReachableStateInvariants** (ASN-0047)."
**Problem**: That theorem closes over states *reachable from Σ₀*. The appeal "valid composite ⟹ post-state reachable ⟹ satisfies invariants" requires the pre-state to be reachable, but DELETE's stated precondition is only `d ∈ dom(M)` plus standing well-formedness facts (S8a, D-SEQ). Well-formed is not the same as reachable. As written, the invariant-preservation conclusion has an unstated antecedent.
**Required**: Either add "Σ is →*-reachable from Σ₀" to the precondition, or recast preservation as an inductive step (pre-state satisfies the per-state invariants ⟹ post-state does) rather than routing through the reachability theorem.

## OUT_OF_SCOPE

### Topic 1: Deletion in the link subspace
**Why out of scope**: The precondition fixes `S = subspace(p) = s_C`, matching foundation ASN-0082's text-only (S=1) contraction. Removing a link from a document's arrangement is separate territory, not an error here.

### Topic 2: Depth `m > 2` deletions
**Why out of scope**: The note scopes to `m = #p = 2`, inheriting ASN-0082's depth-2 contraction. Generalizing to arbitrary depth is future work, consistent with the foundation it builds on.

VERDICT: REVISE
