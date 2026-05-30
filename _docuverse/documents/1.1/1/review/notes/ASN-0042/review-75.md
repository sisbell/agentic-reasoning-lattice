# Review of ASN-0042

## REVISE

### Issue 1: O14 — prose paragraph restates the formal clauses verbatim
**ASN-0042, State Axioms (O14)**: "The second clause asserts bootstrap finiteness... The third clause requires every initial principal to have a node-level or account-level prefix. The fourth clause requires that no two initial principals share a prefix. The fifth clause requires every initial principal's prefix to be a valid tumbler address."
**Problem**: This paragraph walks clause-by-clause through a formal statement that was just given symbolically directly above. Clauses two through six add nothing the formulas do not already say — this is the "two paragraphs say the same thing in different words" anti-bloat pattern. Only the seventh-clause gloss (independence from the coverage conjunct) carries reasoning.
**Required**: Delete the restatement of clauses 2–6; keep only the seventh-clause independence argument, which is load-bearing.

### Issue 2: O15 — "reading of the conjuncts" restates conditions (i)–(vi)
**ASN-0042, State Axioms (O15)**: "The reading of the conjuncts: (i) the delegate's prefix strictly extends the delegator's, (ii) the delegator is the most-specific covering principal... (iii) the delegate is newly introduced, (iv) the delegate's prefix is at node or account level, (v) the delegate's prefix is a valid tumbler..."
**Problem**: Same restatement pattern as Issue 1 — the formal conditions are immediately above, and (i),(iii),(iv),(v) are pure paraphrase. The genuinely non-obvious gloss is on (ii) (authorization) and (vi) (top-down order), which is also developed at length later in the *Delegation* section. The intermediate paraphrase is noise the reader skips.
**Required**: Drop the paraphrase of (i),(iii),(iv),(v); retain only the (ii)/(vi) intent, and only if not already covered by the *Delegation* section's discussion of the same two conditions (it is — consider deleting here entirely).

### Issue 3: Identity scope stated twice; labeled "Scope note" sub-paragraph
**ASN-0042, Principal Identity section** ("*Scope note (Identity is exogenous).*") **and Summary** ("Principal identity ... is exogenous to this model — see the Scope note in the *Principal Identity and the Trust Boundary* section.")
**Problem**: The same scoping claim ("identity binding is exogenous; O1–O10 hold for any mechanism") appears in three places: the section prose, the labeled "Scope note" sub-paragraph, and the Summary with a cross-pointer back. The explicitly labeled "Scope note" is the flagged labeled-sub-paragraph pattern, and the Summary's "see the Scope note" is a deferral to content already stated inline.
**Required**: State the exogeneity claim once (the section prose suffices). Remove the labeled "Scope note" wrapper and the Summary's back-pointer.

### Issue 4: Self-contradictory notation sentence for `Σ.B`
**ASN-0042, State Axioms (Notation)**: "We adopt the foundation's notation rather than introducing a separate `Σ.B` symbol."
**Problem**: The ASN uses `Σ.B` throughout — which *is* a renaming of the foundation's `s.B` (state `s` → `Σ`). The sentence claims not to introduce `Σ.B` while the whole ASN depends on it. As written it asserts the opposite of what the ASN does, forcing the reader to reconcile the contradiction.
**Required**: State the relation plainly: the ASN reuses ASN-0040's `.B` registry accessor on its own state symbol `Σ`, writing `Σ.B` for what ASN-0040 writes `s.B`.

### Issue 5: Forward-pointer cluster in the Exclusivity motivation
**ASN-0042, The Exclusivity Invariant (closing) / Ownership as a Structural Predicate**: "who is entitled to subdivide the space beneath it (O5 below), who originated the content (O6 below), or whose delegation created the address... Every downstream property depends on O2."
**Problem**: A cluster of "(O5 below)/(O6 below)" use-site forward pointers plus a generic "every downstream property depends on O2" — the latter is an unfalsifiable importance-assertion rather than a step in the argument. These are the forward-reference-accretion patterns flagged for this note.
**Required**: Drop the parenthetical forward pointers (the labels appear in their own sections) and the "every downstream property depends on O2" sentence; if O2's load-bearing role needs stating, name the specific dependents once where they are defined.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer invariants and provenance/authority divergence
**Why out of scope**: The ASN correctly records this as an Open Question rather than a claim. The divergence between inalienable provenance (O6) and effective authority (O2) under a hypothetical transfer regime is genuinely new territory requiring its own state machinery (an external deed registry), not a defect in this ASN's refinement-only model.

VERDICT: REVISE
