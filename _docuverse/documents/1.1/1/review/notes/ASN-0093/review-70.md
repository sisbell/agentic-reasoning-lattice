# Review of ASN-0093

## REVISE

### Issue 1: Worked-example Steps 6–7 re-derive arguments the note itself labels identical to earlier steps

**ASN-0093, Worked example, Steps 6–7**: Step 6 — "The per-step TA5a admissibility … is identical to Step 2 under `d → d'`." Step 7 — "The per-step TA5a admissibility … is identical to Step 3 under `d → d'`."

**Problem**: After declaring the chain construction and admissibility identical to Steps 2–3, both steps re-exhibit the full chain `(t₀,t₁,t₂)` / `(t₀,t₁,t₂,t₃)` and re-run the per-step TA5a discharge anyway. The branch coverage they would add (first content/link emission) is already established by Steps 2–3; the only genuinely new material is the multi-component document field `D(d') = [5,3]` and the resulting position-6 divergence. The new cross-document branch (prefix-incomparable documents) is delivered separately by Step 9. So Steps 6–7 re-run an argument the note marks as identical, which is exactly the "two paragraphs say the same thing in different words" pattern.

**Required**: Keep the genuinely new material in Steps 6–7 (the `D(d') = [5,3]` projection and the position-6 divergence demonstrating origin extraction with a multi-component document field), and cite Steps 2–3 for the identical chain and admissibility rather than re-exhibiting them.

### Issue 2: ChainMembershipForOrigin and StoreT4Validity are proved by transition-induction twice

**ASN-0093, Address sub-allocators (lemma proofs) vs. Discharge of stated invariants (lemma-preservation matrix)**: The standalone "Lemma (ChainMembershipForOrigin)" carries a full *"Induction on transition sequences from `Σ₀` … Base … Step"* proof with per-transition cases; the Discharge section's "Simultaneous-induction framing" then states the inductive step "is recorded as a per-(invariant, transition) matrix," and the lemma-preservation matrix re-lists ChainMembershipForOrigin and StoreT4Validity as rows whose cells mostly say "see lemma proof above."

**Problem**: Two competing canonical homes for the same induction. Either the standalone lemma proof is the induction (and the matrix rows are pointers that add nothing), or the simultaneous-induction matrix is the induction (and the standalone proof duplicates it). The matrix rows for these two lemmas carry no content beyond back-pointers — "see lemma proof above," "Symmetric to K.α (content↔link); see lemma proof above."

**Required**: Pick one location. If the standalone proofs are canonical, drop the two lemma rows from the matrix; if the matrix is canonical, reduce the standalone statements to the lemma claim without re-proving by induction.

### Issue 3: Tautological clause in the opening paragraph

**ASN-0093, opening paragraph**: "ASN-0043 introduced the link store and its structural invariants (L0/L1/L1a/L1b/L1c/L3/L12), of which this note restates those listed"

**Problem**: "of which this note restates those listed" is circular — it asserts that the note restates the very invariants it just listed, conveying no information. The Properties Introduced table's Source column already records, per invariant, which ASN it comes from and whether it is restated; the clause duplicates that accounting in vaguer form.

**Required**: Strike "of which this note restates those listed"; the parenthetical naming the inherited invariants is sufficient, and the Source column carries the restatement provenance.

## OUT_OF_SCOPE

### Topic 1: Disjointness of `dom(M)` from `dom(C)`/`dom(L)`

The note proves `dom(C) ∩ dom(L) = ∅` (SD) but never states the document/element separation `dom(M) ∩ (dom(C) ∪ dom(L)) = ∅`.

**Why out of scope**: It is trivially forced by zero-counts (`zeros = 2` for documents, `zeros = 3` for content/links) and nothing in this substrate depends on it; if a higher layer needs it, it can be stated there. Not an error in this ASN.

VERDICT: REVISE
