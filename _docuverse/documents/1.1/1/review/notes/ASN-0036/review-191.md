# Review of ASN-0036

## REVISE

### Issue 1: S8a carries reviser-directed meta-prose
**ASN-0036, S8a (V-position componentwise positivity and depth)**: "The `S8a` label names this unfolded reading for downstream citation; a reviser cannot tighten one form without the other, since the two are equivalent by T0."
**Problem**: The second sentence does not advance the claim. "names this unfolded reading for downstream citation" enumerates a downstream consumer of the label, and "a reviser cannot tighten one form without the other" is reviser-drift meta-prose — it instructs future editors rather than stating what S8a says. The substantive content (S8a is the per-component unfolding of the domain-restriction axiom, equivalent by T0) is fully carried by the first sentence.
**Required**: Delete the second sentence. Keep only "S8a is the per-component unfolding of the domain-restriction axiom via T0, not an independent obligation."

### Issue 2: S8a stated twice in identical substance
**ASN-0036, S8a section vs. Properties Introduced table**: prose says "notational alias of the domain-restriction axiom ... equivalent by T0"; the table row repeats "notational alias of the domain-restriction axiom (not an independent obligation), equivalent by T0."
**Problem**: Two locations assert the same alias-equivalence in different words — the "two paragraphs say the same thing" pattern. The table is the index slot; the parenthetical editorializing belongs in neither.
**Required**: Reduce the table row to a bare statement of the alias (e.g., "per-component unfolding of the domain-restriction axiom, T0") and drop the "(not an independent obligation), equivalent by T0" duplication.

### Issue 3: D-CTG guard-purpose gloss is meta-commentary
**ASN-0036, D-CTG (VContiguity)**: "The guard `zeros(v) = 0` restricts the consequent to S8a-conforming tumblers, so the contiguity demand ranges only over intermediates that could be V-positions."
**Problem**: This explains *why a clause of the axiom is present* rather than stating what the axiom requires — the "new prose around an axiom explains why the axiom is needed" pattern. Since `zeros(v) = 0` over T0's carrier is definitionally "all components positive," the quantifier already speaks for itself.
**Required**: Remove the sentence, or fold a one-clause note ("zeros(v)=0 ⟺ S8a positivity, by T0") into the formal contract's Preconditions if the linkage is load-bearing.

### Issue 4: "(applies wherever D-CTG holds)" scope-justification on D-CTG-depth
**ASN-0036, D-CTG-depth heading and Properties Introduced table**: "Shared prefix reduction (applies wherever D-CTG holds)."
**Problem**: This is a placement/scope justification appended to a corollary title, repeated in two slots. Its applicability is already fixed by its Depends on D-CTG; the parenthetical adds nothing the dependency does not.
**Required**: Drop the parenthetical from both the heading and the table row.

## OUT_OF_SCOPE

### Topic 1: Contiguity for the link subspace (S = 2)
D-CTG, D-MIN, D-SEQ are stated only for the text subspace. Link-position contiguity (Nelson, LM 4/31) is governed by the links/endsets ASN and is correctly deferred — listed OUT OF SCOPE here.

### Topic 2: Operation-layer preservation of D-CTG/D-MIN/S2 and subspace alignment
The Open Questions correctly route INSERT/DELETE/COPY/REARRANGE preservation obligations and the `subspace(v) = v₁` alignment obligation to the operations layer; these are not defects in the strand model.

Note on rigor: the S8 correspondence-run proof (injective-acyclic-succ → maximal-chain partition, with the i=0 convention handled separately from TS3's n₁≥1 precondition), the D-SEQ four-step derivation, and the D-CTG-depth infinite-intermediate contradiction are all complete and case-covered, and the worked example exercises S0/S3/S5/S7/S8/D-SEQ across create/transclude/delete. The remaining findings are prose accretion, not gaps in the argument.

VERDICT: REVISE
