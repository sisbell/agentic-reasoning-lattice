# Review of ASN-0070

The mathematics is sound — the inverse-image definition (F0), the subspace correspondence (F-subspace), and the canonical-uniqueness proof (F-canonical) are correct local derivations, and the five worked configurations check the postcondition against concrete state including the cross-subspace straddle. My findings are confined to the forward-reference meta-prose the anti-bloat classifier targets.

## REVISE

### Issue 1: Use-site inventory appended to the vacuous-subspace convention
**ASN-0070, V-Restricted Denotation (Vacuous-subspace convention)**: "This is the single statement of the vacuous case; The Setting, F1, and F-canon-form cite it."
**Problem**: The trailing sentence enumerates the convention's downstream consumers. It advances neither the definition's meaning nor the surrounding reasoning — it is bookkeeping about document structure, the exact pattern flagged ("a definition's introduction enumerates downstream consumers").
**Required**: Delete the sentence. The convention stands on its own; the citing passages already point back to it.

### Issue 2: Meta-commentary on deferral in The Setting
**ASN-0070, The Setting**: "The resolution consequence — that a vacuous subspace forces `Σ_V^S = ⟨⟩` — is fixed once as the *vacuous-subspace convention* (V-Restricted Denotation, below); passages downstream cite it rather than re-derive it."
**Problem**: "is fixed once ... passages downstream cite it rather than re-derive it" is prose about how the document is organized, not about the system. The reader must skip past it to reach the actual fact. This is the "multiple paragraphs defer to the same downstream location" pattern, stated here as explicit narration.
**Required**: State the object-level fact directly (a vacuous subspace `S` has `R(d,e)|_S = ∅`) and drop the meta-narration about where it is "fixed once" and that others "cite rather than re-derive."

### Issue 3: Parenthetical justifying why a clause is needed rather than stating what it does
**ASN-0070, F-canon-form clause (iii)**: "(This convention pins down the family-level ordering, which S9 alone does not address since it operates within a single level-uniform span-set.)"
**Problem**: Clause (iii) already states what it does (s_C first, s_L second). The parenthetical explains *why the clause is needed* by reciting a gap in S9 — "new prose around [a definition] explains why [it] is needed rather than what it says."
**Required**: Remove the parenthetical; the ordering convention is self-explanatory.

## OUT_OF_SCOPE

### Topic 1: Cross-home transclusion resolution relationships
**Why out of scope**: The first Open Question (resolutions against documents transcluding from different home subsets) is genuinely new territory — a relationship between multiple `follow` results, not a property of this single-query operation.

### Topic 2: Concurrency semantics of `follow`
**Why out of scope**: The second Open Question (guarantees under concurrent modification) requires a transition-interleaving model this state-pure query ASN does not establish; it belongs to a future operational-semantics ASN.

VERDICT: REVISE
