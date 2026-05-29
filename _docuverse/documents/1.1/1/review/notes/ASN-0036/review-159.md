# Review of ASN-0036

This note carries `review-mode.anti-bloat`. The mathematical core is sound — I checked the S8 partition proof (within-subspace lemma both cases, cross-subspace via T5/T10), the S5 existence constructions, the S7 attribution chain, and the D-CTG-depth / D-SEQ derivations, and found no rigor gaps. The findings below are accreted meta-prose and duplication, which is exactly what the classifier asks me to surface.

## REVISE

### Issue 1: Scope-defensive trailing sentence in the contiguity preamble
**ASN-0036, Arrangement contiguity**: "The properties below (D-CTG, D-MIN, D-CTG-depth, D-SEQ) bind `S = 1` in their formal statements and constrain only the text subspace; contiguity semantics for other subspaces are out of scope for this ASN."
**Problem**: Every formal statement already binds `S = 1` (e.g., D-CTG quantifies over `V_1(d)`). The clause "contiguity semantics for other subspaces are out of scope for this ASN" advances no reasoning — it is a scope disclaimer that restates what the `S = 1` binding already enforces, and it overlaps the document's own Scope section. This is the "defensive justification / essay content in a structural slot" pattern.
**Required**: Drop the out-of-scope clause; the `S = 1` binding in each property carries the restriction.

### Issue 2: "Conjunct (b) is a definition, not a theorem" stated three times
**ASN-0036, S8**: statement — "Conjunct (b) is a definition of the labeled partition, not a theorem."; proof — "this is the labeled partition of conjunct (b), well-defined precisely because S2 makes the label unique and S3 places it in `dom(Σ.C)`"; postconditions — "yielding the labeled partition (b)".
**Problem**: The same status claim ("(b) is a definitional labeling discharged by S2 + S3") appears in the property statement, the proof, and the Formal Contract. Two of the three are restatement; only the proof sentence does work.
**Required**: Establish (b) once (in the proof), and let the statement/postcondition reference it without re-asserting its definitional status.

### Issue 3: ValidInsertionPosition derivation block duplicates the Formal Contract postconditions
**ASN-0036, Valid insertion position**: the prose block beginning "By D-MIN, `min(V_1(d)) = [1, 1, ..., 1]` of depth `m`..." derives, in order: the explicit form `[1, ..., 1+j]` (= postcondition (d)), `zeros(v) = 0` + positivity (= postcondition (b)), and "the predicate is satisfied by exactly `N + 1` distinct positions" (= postcondition (c)).
**Problem**: These three results then reappear verbatim as postconditions (b), (c), (d) of the non-empty Formal Contract. The block sits awkwardly between the two Definitions and the two Formal Contracts and re-states content that belongs in one place. Sentences like "This is the canonical minimum position required by D-MIN." and "In both predicates, `v₁ = 1` is the text subspace identifier." are scattered restatements of the same facts.
**Required**: Keep the derivation attached to the postconditions in a single location; remove the standalone prose duplication.

### Issue 4: Essay/defensive fragments in structural slots
**ASN-0036, S8a Formal Contract**: "(Motivating reading: an isolated element field of depth at least 2 — the within-document arrangement coordinate, carrying no field separators.)" — interpretive essay inside a Definition slot.
**ASN-0036, S5 Frame**: "S5 ranges over S0–S3 only; the witnesses are not claimed to satisfy later invariants." — defensive scope note about an existence claim.
**Problem**: Neither advances the formal content of its slot; both are the "essay content in structural slot" / "defensive justification" patterns flagged by the anti-bloat mode.
**Required**: Move the S8a motivating reading into the surrounding prose (or cut), and cut the S5 frame disclaimer (the existence claim's `S0–S3` scope is already explicit in its statement).

## OUT_OF_SCOPE

### Topic 1: Operation frame conditions preserving D-CTG/D-MIN/S2
The final Open Question ("What must each well-formed editing operation ... guarantee in order to preserve the contiguity invariants ... including the case where insertion coincides with an occupied V-position?") is correctly deferred — INSERT/DELETE/COPY/REARRANGE postconditions belong to the operation ASNs, not the strand model.

### Topic 2: Subspace alignment as an operations-layer obligation
The Open Question on `subspace(v) = v₁` matching the I-address's first element-field component is appropriately left to the operations layer; the strand model only needs the structural typing it already states.

VERDICT: REVISE
