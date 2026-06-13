# Review of ASN-0108

The proof work here is strong. The wp analysis in W2 is genuinely non-trivial and correct — I verified the three-way nesting (membership-identity ⊊ frozen-prefix ⊊ `wp(R)`) and the closed form `j' = j ∨ (j ≥ m' ∧ j' ≥ m')` against the rank arithmetic, including the past-the-end corner. The edge-case walks (empty set `m=0`, exact multiple `m=4`, non-divisible `m=5`, first-window-short `N>m`) all check out against W4/W9/W9a including the `[N divides m]` term. The orphaned-cursor survival (W8), the no-re-delivery cursor-advance induction (W5), and the cumulative-inflow charging argument (W9b) are sound sketches with acyclic dependencies (no-re-delivery ← clause 1; termination ← no-re-delivery + finite inflow; no-skip ← clause 1 + termination — I checked there is no vicious circularity). I found no correctness error.

The findings below are all anti-bloat: the coherence result has accreted restatement across W5/W9/W9b, exactly the pattern this note's classifier targets, and the recent W5 revision left overlapping scope statements behind.

## REVISE

### Issue 1: W5 states its scope three times

**ASN-0108, W5**: The claim box, the "**Claim:**" paragraph, and the "sufficient but not necessary" paragraph each carry the continuously-matching scope and the termination asymmetry.

- Box: "*no skip* of a continuously-matching tail matcher (under a termination hypothesis), *no re-delivery* of a continuously-matching matcher … sufficient but not necessary".
- Claim para: "*No re-delivery* (**unconditional** — needs no termination hypothesis): … matches *continuously* … *No skip* (**under the hypothesis that the pass terminates**): …" — this is where the two guarantees are actually *defined*, with precise scope. Substantive.
- Third para: "The two guarantees share one matching-scope — both range over links matching *continuously* across the intervening states … and differ only in the genuine asymmetry: *no skip* needs the pass to terminate, *no re-delivery* does not."

**Problem**: The third paragraph's middle sentence restates the continuous-matching scope and the termination asymmetry that the box and the Claim paragraph already establish. A precise reader following the claim hits the same scoping three times. The genuinely additive content of the third paragraph is only "sufficient but not necessary / whole-pass" and the boundary clarification "A link matching in only one of the relevant states … falls outside both."

**Required**: Keep the box (summary) and the Claim paragraph (definitions). Trim the third paragraph to its additive content — the whole-pass / sufficiency point and the one-state-only boundary clarification — and drop the re-statement of scope+asymmetry.

### Issue 2: the coherence result is split across W5, W9, and W9b with mutual deferral

**ASN-0108, W9 global guarantee**: "scoped exactly as W5's coherence is — not a terminal-state fact: **every link that is an undelivered tail matcher at some visited call … and that *remains* matching … is delivered exactly once; none such is skipped.**"

**Problem**: This bolded sentence is W5's no-skip + no-re-delivery (delivered exactly once) restated in full in W9's slot — the note itself flags it as "scoped exactly as W5's coherence is." Combined with W5's two forward references into W9b ("…kept from re-delivery only under a *permanent* key … (W9b)" and "(W5's discipline, supplying W9b's termination condition (i))"), and W9b's repeated back-references re-deriving "W5's cursor-advance induction (no re-delivery)" and re-explaining why `(i′)` is distinct from `(i)` via W8, the single coherence property and its acyclic dependency on termination are scattered across three claims that defer to one another. The reader must assemble "no-skip needs termination (W5) → termination needs clause-1 + finite-inflow (W9b) → which closes no-skip" by hand from cross-pointers.

**Required**: State coherence once (W5) and have W9 *cite* it for the global reading rather than restate the full property — W9's own contribution is the local cardinality fact (`After(next-cursor) = ∅` under computability) and the short-window terminator, which can stand on a one-line reference to W5 for the "everything delivered" half. Likewise, W9b should reference W5's no-re-delivery for the injectivity step rather than re-explaining the cursor-advance induction and the clause-1-vs-computability distinction in fresh prose.

### Issue 3: the "ladder of key conditions" is a forward-looking taxonomy lodged inside W5

**ASN-0108, W5**: "The conditions on the key split into two families. One concerns *whether `κ(c)` can be evaluated at all*, and divides in turn: **computability** … and its unconditional strengthening **value-totality** …. The other family concerns *whether comparisons move under evolution* — W5's clause 1, clause 2, and state-stability, as defined above."

**Problem**: `computability` and `value-totality` are introduced here but first *used* in W8 (and then W9, W9b). Sitting inside W5 — which is about clause 1/clause 2, not about evaluability — the ladder reads as an inventory of conditions for downstream claims rather than as content advancing W5. Placement, not existence: the evaluability family belongs where W8 first needs it.

**Required**: Move the computability/value-totality definitions to W8's vicinity (their first use), leaving W5 to define only the comparison-stability family it actually consumes.

## OUT_OF_SCOPE

### Topic 1: address-key resurrection below the cursor

Under the address key (allocation-monotone for *fresh* links, W6), a link allocated early, orphaned before delivery, and *resurrected* (LP18) at a state where the reader's cursor has already paged past its low, permanent address re-enters `Match` *behind* the cursor and is never delivered — a blind spot the address key shares for resurrected (not fresh) links. W6 correctly scopes its append-at-tail guarantee to "*fresh* addresses," and W5's no-skip is correctly scoped to *continuously*-matching links, so this is excluded by construction, not an error. W9b also correctly excludes behind-cursor resurrections from the termination inflow count.

**Why out of scope**: This is the completeness question the open questions already gesture at (OQ2 on non-allocation-monotone keys, OQ3 on cross-call matching-set invariants). No claim over-promises here; surfacing the guarantee for resurrected-below-cursor links is future territory, not a defect in W6/W5/W9b as scoped.

VERDICT: REVISE
