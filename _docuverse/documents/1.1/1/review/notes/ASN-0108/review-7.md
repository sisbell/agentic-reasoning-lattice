# Review of ASN-0108

## REVISE

### Issue 1: W5's necessity is asserted abstractly but its failure mode is never exhibited

**ASN-0108, W5 (OrderStability)**: "Resumption past a cursor `c` is well-defined across `Σ → Σ'` only if the ordering key preserves the cursor's *cut-point* and the relative `≺`-order *among the links in `After(c, ·)`*."

**Problem**: W5 is the linchpin of the entire note — it is the claim that discriminates the address key (invariant for free, T8) from the content-position key (invariant only conditionally). Yet the *necessity* direction is supported only by abstract reasoning plus the uniform-shift example (which shows absolute invariance is *too strong*). What is never shown is the thing that makes tail-order preservation genuinely *necessary*: a concrete instance where a tail reorder between calls causes an actual skip. The mechanism is real — if the reader sits at cursor `c` after delivering `a` from tail `{a ≺ b}`, and the key then shifts so `κ(b) < κ(c)`, then `b ∉ After(c, Σ')` and is silently lost — but no numeric walk demonstrates it. Compare W2 (concrete offset-failure walk), W8 (concrete orphan walk), and W9a (four boundary walks): every other load-bearing discrimination gets a worked scenario. W5, the most central, does not. This is exactly the skipped case the standard on concrete examples names.

**Required**: Add a concrete walk (à la W2/W8) showing a tail-order violation under a content-position key producing a skip of a genuinely-matching, never-orphaned link — establishing necessity, not merely the address-key sufficiency.

### Issue 2: W6's blind spot is described but not walked

**ASN-0108, W6**: "a new link `a_new` … whose endpoint content sorts *below* `κ(c)`. Then `κ(a_new) <_K κ(c)`, so `a_new ∉ After(c, Σ')`: the new link lands permanently behind the cursor and is never delivered."

**Problem**: This is a key consequence — the silent-skip hazard that distinguishes the non-allocation-monotone key — and is the subject of Open Question 2. It is given a semi-formal description but no numeric instance, while the *dual* phenomenon (cursor survival under orphaning, W8) receives a full five-link walk. The treatment is asymmetric for two phenomena of equal weight.

**Required**: A concrete walk (fixed `Match`, fixed `N`, a content-position key) in which a freshly created matching link lands behind the cursor and is provably never delivered in the pass — verifying W6's blind-spot claim against a specific scenario.

## OUT_OF_SCOPE

### Topic 1: Multi-document global ordering
The behaviour when the matching set spans multiple home documents whose link allocators advance independently (no globally allocation-monotone key) is correctly deferred to Open Question 1, not an error here.

### Topic 2: Cross-state partition preservation
Whether W4's partition survives state evolution is correctly held as Open Question 6; W4 is honestly scoped to fixed `(Match, κ)`.

### Topic 3: The satisfaction predicate
Which links match `q`, and the count/full-set operations, are explicitly deferred and belong to the count-only and FINDLINKS operations.

VERDICT: REVISE
