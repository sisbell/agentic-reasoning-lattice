# Review of ASN-0043

## REVISE

### Issue 1: Consumer-enumeration meta-prose in lemma/definition introductions
**ASN-0043, L0a (ContentSubspaceScope), closing of the `s_C`-resident paragraph**: "Several results below carry this hypothesis; we name it here and reference it by name rather than restating the quantifier."
**ASN-0043, FSP introduction**: "Several results below extend the store by appending a single fresh sibling link, carrying a given payload, while leaving content and arrangements untouched. We establish once that any such extension preserves conformance, parametric in the payload."
**Problem**: Both sentences justify a definition/lemma by inventorying its downstream consumers ("several results below carry...", "several results below extend...") rather than advancing the content of the definition or lemma. This is the flagged accretion pattern: the meaning of `s_C`-residence and of FSP is fully carried by their statements; the "we name it here so we don't restate it later" and "we establish once" framing is document-management prose the precise reader must skip past to reach the derivation.
**Required**: Drop the consumer-enumeration sentences. State the `s_C`-residence predicate and FSP's hypotheses directly; downstream sites already cite them by name.

### Issue 2: Worked-example setup defers a verification that a later step re-performs in full
**ASN-0043, Worked Example, "Link store" setup**: "We verify `g ∉ dom(Σ.C) ∪ dom(Σ.L)` by direct enumeration in the L9 (TypeGhostPermission) step below — Σ's content store and link store are each enumerable as small finite sets in this state, so the verification proceeds by T7 against each entry."
**Problem**: This sentence does no verification — it is a forward pointer to the later "*L9 (TypeGhostPermission) at Σ*" step, which then performs the actual T7-by-enumeration check. The setup sentence (including the "each enumerable as small finite sets" gloss) is pure deferral to a downstream location, duplicating the framing of the step it points to. Two passages in the same example say the same thing.
**Required**: Delete the setup sentence; let the L9 step carry the disjointness check where it is actually done.

### Issue 3: Defensive "regardless of the size of these domains" guards against a non-issue
**ASN-0043, L9 (TypeGhostPermission), construction of `g`**: "By the L0a discharge ... `g ∉ dom(Σ.C) ∪ dom(Σ.L)`, regardless of the size of these domains."
**Problem**: The L0a discharge is a subspace-separation argument (T7 on distinct first element-field components); it is size-independent by construction, so nothing in the proof could have made domain size relevant. The trailing clause defends against an imagined dependence the argument's structure already excludes — a defensive justification rather than a step that advances the claim.
**Required**: Remove the trailing clause; the T7/subspace argument already makes the conclusion unconditional.

## OUT_OF_SCOPE

### Topic 1: Global content-subspace invariant
The first Open Question (fixing a global `s_C` so disjointness extends from the `s_C`-resident slice to all of `dom(Σ.C)`) is correctly deferred — it is a content-side invariant, not a link-model claim. No action needed.

VERDICT: REVISE

The note is substantively sound: the L1c/CPP chain reasoning, FSP's invariant coverage, the L11a single-tree embedding, and the six-step worked example are all rigorous and complete. The remaining items are accreted meta-prose flagged by the anti-bloat mandate, not correctness gaps.
