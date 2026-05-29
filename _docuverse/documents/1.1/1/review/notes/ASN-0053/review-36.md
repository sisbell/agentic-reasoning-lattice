# Review of ASN-0053

## REVISE

### Issue 1: Exhaustiveness preamble in SC is meta-prose about clause phrasing
**ASN-0053, SC (*Exhaustiveness*)**: "The SC definition is symmetric in α and β: each case clause is either symmetric (cases (i), (ii), (v) phrase both directions as a disjunction) or carries an explicit 'or symmetrically' rider (cases (iii), (iv)). Swapping α and β maps each case to itself, so the classification is invariant under that swap."
**Problem**: This paragraph describes how the case clauses are *worded* rather than advancing the exhaustiveness argument. The actual proof — "Compare reach(α) with start(β)... Every ordering of the four boundary points... falls into exactly one case" — is self-sufficient and does the WLOG reduction itself. The preamble is the "exhaustiveness claim" / essay-in-structural-slot pattern the anti-bloat pass targets.
**Required**: Delete the symmetry preamble; let the WLOG reduction inside the constructive comparison carry the argument. Drop the trailing "No sixth case exists." as a redundant flourish ("falls into exactly one case" already states it).

### Issue 2: "Denotation, not encoding" is a standalone disclaimer that establishes no property
**ASN-0053, Denotation, not encoding**: "All properties above quantify over the denotation ⟦σ⟧... a width compared by its tumbler representation rather than by the interval it denotes is a separate question, governed by T3's per-tumbler canonical form, not by the span algebra."
**Problem**: This section advances no claim and proves nothing; it is a scope disclaimer demarcating what the ASN does not do. Essay content occupying a top-level structural slot.
**Required**: Remove, or fold a single clause into the Scope/Open Questions material if the distinction must be recorded.

### Issue 3: S6 flat-address-space parenthetical is essay content
**ASN-0053, S6**: "(In a flat address space every interior point would admit a split; the tumbler space stratifies positions by depth, so arithmetic must respect that stratification.)"
**Problem**: The concrete `[1,3,0,1]` example immediately preceding already shows what `level_compat` excludes (acceptable concrete example). The parenthetical adds a hypothetical-world essay aside that does not advance the definition.
**Required**: Delete the parenthetical; keep the concrete divergence example.

### Issue 4: Nelson "no choice as to what lies between" quoted redundantly
**ASN-0053, The reach function** and **S3 proof**: the quote "there is no choice as to what lies between" (LM 4/25) appears in both, supporting the same point (denotation determined by endpoints).
**Problem**: Two paragraphs in the same document deploy the same evidence for the same claim — the duplicate-grounding pattern.
**Required**: Cite once (at first use in "The reach function") and drop the repetition in the S3 conclusion, or vice versa.

### Issue 5: "Properties Introduced" table omits load-bearing cited foundation deps
**ASN-0053, Properties Introduced table**: lists D0, D1, TA-LC as "cited" but omits D2 (DisplacementUnique) and TA-assoc.
**Problem**: D2 is the engine of WR (the first theorem), S4a, S9, and S11; TA-assoc is load-bearing in S5. The table selectively records cited foundation properties but skips two that are at least as central as D1/TA-LC, leaving the summary inconsistent.
**Required**: Add D2 and TA-assoc rows marked "cited," or state explicitly that the table is illustrative rather than an exhaustive dependency list.

## OUT_OF_SCOPE

### Topic 1: Intersection/split across hierarchical levels
The level-uniform restriction is correct for this ASN; the cross-level intersection and finer-level split questions are already routed to Open Questions and belong to a future ASN.

### Topic 2: Span-set difference bound
The tight bound on `normalize(⟦Σ₁⟧ \ ⟦Σ₂⟧)` is correctly deferred to an Open Question; not an error here.

VERDICT: REVISE
