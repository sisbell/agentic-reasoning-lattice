# Review of ASN-0108

This note is unusually careful — the W2 weakest-precondition analysis (identity vs. offset cursor, with the three strictly-nesting preconditions and the past-the-end corner), the W4 partition proof, and the four W9 termination walks all hold up under checking. The findings below are where the rigor lapses, plus the accreted forward-reference prose the anti-bloat classifier flags.

## REVISE

### Issue 1: W9b's termination derivation assumes cursor-monotonicity that clause 1 alone does not supply — and the note's own W8 supplies the counterexample

**ASN-0108, W9b (CumulativeInflowSufficiency)**: "a delivered link cannot climb back above a later cursor by a key shift alone, and its only way back into the tail is to leave Match and resurrect — kind 3. Distinct deliveries of one link have distinct most-recent contributions (between two deliveries the link must drop out of and re-enter the tail …)". Hypotheses stated: "(i) the cursor's cut-point is preserved at each successive cursor — W5's clause 1 … and (ii) the total inflow … is finite."

**Problem**: The charge-injectivity step rests on "a delivered link cannot climb back above a *later* cursor" — i.e., the cursor sequence `c_{i+1} ≼ c_{i+2} ≼ … ≼ c_j` is `≺`-monotone *at the resume state* `Σ_j`. But clause 1, as defined in W5, preserves a cursor's ordering of a link only when **both** are "matching across the cursor's transition." To propagate `c_{i+1} ≺ c_{i+2}` (established at `Σ_{i+1}`) forward to `Σ_j`, every intermediate cursor must itself remain in `Match` at each subsequent transition. The note's *own W8* establishes precisely the opposite is possible: a cursor can be orphaned — `c ∉ Match(q, Σ')` — and resumption still proceeds. An orphaned intermediate cursor is not a both-states link, so clause 1 at the next transition does not transport its ordering, the chain `c_{i+1} ≼ … ≼ c_j` breaks, and a continuously-matching delivered link can re-enter `After(c_j, Σ_j)` *without* dropping out and resurrecting. Charge-injectivity, and with it termination, is then not secured by (i)+(ii). Under a value-total key (address key, frozen keys) cursor-monotonicity is trivial and W9b holds — but W9b is stated as a general criterion over clause-1 keys, and the note does not restrict it.

**Required**: Either add the missing hypothesis to W9b (value-totality, or that visited cursors do not orphan), or prove the cursor sequence is `≺`-monotone at the resume state from (i) — explicitly handling the orphaned-intermediate-cursor case that W8 admits. As written, (i)+(ii) is asserted to be sufficient and is not.

### Issue 2: "Orphaned (LP17)" over-states single-document Match-loss

**ASN-0108, "State, the Matching Set," (M-mut)**: "it may lose members — a link whose matched endpoint content is removed from a consulted arrangement (D-NONMONO's K.μ⁻ case), the link then orphaned: still resident in dom(Σ.L) (ASN-0098 LP13) but no longer discoverable (LP17)." Echoed in W7 ("thereby orphaned") and W8's walk: "a_2 is orphaned — its matched endpoint content is removed from every consulted arrangement (ASN-0098 LP17), so a_2 ∉ Match(q, Σ')."

**Problem**: `Match` is fixed by the note as the *single-document* `findlinks_V(W, d_q, Σ)`, reducing at full region to `{a : discoverable_from(a, d_q, Σ)}` (F-FULL). A link leaves this set by losing discoverability *from d_q alone* — D-NONMONO's K.μ⁻ case, i.e., `coverage ∩ ran(Σ.M(d_q)) = ∅` (LP12). LP17 (GhostProjection) is the strictly stronger condition that *no* document in `dom(Σ.M)` reaches the coverage — global ghosthood. A link can drop out of `Match` (no longer discoverable from `d_q`) while remaining discoverable from some `d' ≠ d_q`, hence **not** orphaned per LP17. The proofs (W7, W8) need only the weaker per-`d_q` loss; LP17 is both gratuitous and a misattribution of the mechanism.

**Required**: Cite the per-document mechanism (D-NONMONO's K.μ⁻ / LP12) for Match-loss, and either drop the LP17 citation or explicitly define "orphaned" here to mean "no longer discoverable from the queried region `d_q`," distinct from LP17's global ghost.

### Issue 3: W5's claim statement buries its content under a four-way forward-reference tour

**ASN-0108, W5 (OrderStability)**: "Because clause 1 quantifies only over links matching in *both* states, its scope excludes two kinds of link, neither a coherence concern: a *newly-created or newly-discoverable* matcher landing below the cursor (the separate W6 blind spot) and a delivered link that *left* `Match` and *resurrected* above a later cursor (W7; ASN-0098 LP18), whose re-delivery is the W9b cumulative-inflow phenomenon the present-tense semantics (ASN-0127 D-ZERO) counts as a fresh tail arrival, not a repeat."

**Problem**: The load-bearing content is one clause — *clause 1 is scoped to both-states links*. Everything after the colon is justification-by-deferral to four downstream locations (W6, W7/LP18, W9b, D-ZERO), placed inside the claim slot of a definitional invariant. This is the "multiple paragraphs defer to the same downstream location" / "essay content in a structural slot" pattern the anti-bloat pass targets; the reader must navigate a tour of the rest of the note to read W5's statement.

**Required**: State the scope (clause 1 ranges over links matching in both states) and stop. The downstream handling of out-of-scope link kinds is established where those claims live; it does not belong in W5's statement.

### Issue 4: The "W6 blind spot" and the value-totality/state-stability point are each re-explained across multiple sections

**ASN-0108, multiple sites**: The "W6 blind spot" is re-explained in W2 ("that is the separate W6 blind spot, an omission of a newly created link"), in W5 ("the separate W6 blind spot"), and in the post-W9d paragraph ("the W6 blind spot: under a non-allocation-monotone key a newly created link can land behind the cursor and is never reached"). Separately, the value-totality-vs-state-stability distinction is stated in the "ladder of key conditions" ("the converse fails, and the failure is precisely what the cursor-survival argument (W8) turns on — a content-position key with frozen values but removable content is state-stable … yet not value-total") and then again as the substance of W8 ("value-totality … not state-stability … is what makes κ(c) computable through the disappearance").

**Problem**: Each concept is delivered once at its home claim and then re-paraphrased elsewhere — the "two paragraphs say the same thing in different words" and "a definition's introduction pre-explains a downstream consumer" patterns. The ladder's pre-staging of W8 ("precisely what the cursor-survival argument (W8) turns on") is the clearest instance: it spends W8's argument before W8.

**Required**: State the blind spot once (W6) and the value-totality/state-stability gap once (W8); elsewhere reference by label without re-explaining. The ladder may name the five conditions without anticipating which downstream claim turns on which.

## OUT_OF_SCOPE

### Topic 1: Windowing over a union of consulted document-regions

The note fixes `Match` to a single `findlinks_V(W, d_q, Σ)`. A query whose matching set spans several consulted documents (distinct `d_q`'s) is not addressed here. This is genuinely future territory and the note already routes the closely-related multi-allocator ordering problem to Open Question 1; no revision is owed.

### Topic 2: The companion cardinality operation

W10 correctly states that "k of m" requires `m` from "a separate cardinality query — a distinct operation, out of scope here." That operation (FINDNUMOFLINKSFROMTOTHREE) is scoped out by the harness, and the correspondence between its count order and this note's delivery order is properly left to Open Question 5. Correct handling, not an error.

VERDICT: REVISE
