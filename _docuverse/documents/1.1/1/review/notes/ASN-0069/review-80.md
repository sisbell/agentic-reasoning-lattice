# Review of ASN-0069

## REVISE

### Issue 1: V9a restates its own preamble paragraph
**ASN-0069, §"Provenance Recording"**: The paragraph beginning "We observe what V9 does *not* record... It does *not* record that `d_new` obtained `a` from `d_src`... What is recoverable is the fork-tree lineage and the content origin, not the per-address acquisition route." is immediately followed by V9a: "the relation does not distinguish whether `d_new` acquired `a` via fork from `d_src`, via transclusion... The relation reports *who has it*; the I-address tells you *who made it*; the parent prefix tells you *who you came from*."

**Problem**: The prose paragraph and the V9a body make the same three-part point (R records containment; `origin(a)` gives the maker; prefix gives the parent; the acquisition path is not stored). This is the anti-bloat pattern "two paragraphs say the same thing in different words" — the precise reader must read the claim twice to confirm nothing new was added.

**Required**: Delete the prose preamble; let V9a carry the claim. If the "three pieces recoverable independently" gloss is wanted in prose, fold it into V9a's body rather than duplicating it above the label.

### Issue 2: The `d_op` operand gloss is re-stated at nearly every property
**ASN-0069, V4 / V8 / V12(d) / V0 / "The Arrangement Layer" / Properties table**: The parenthetical "the content source operand `d_op` (`= d_src` on the first fork, `= d_prev` on a subsequent fork)" recurs verbatim or near-verbatim at V4, V8, V12(d), V0's effects block, the §"The Arrangement Layer" opener, and four rows of the Properties table — after the rule is already fully stated once in §"What Must Be Constructed".

**Problem**: The operand-tracking rule is fixed once by J4 and restated in §"What Must Be Constructed". The repeated parenthetical does not advance any individual proof; it is accreted self-containment boilerplate that the reader skips. This is the repetition the anti-bloat classifier targets.

**Required**: State the `d_op` convention once (the §"What Must Be Constructed" statement is the right site), then write the downstream claims against the bare symbol `d_op`. Drop the inline "(= d_src on first fork, = d_prev on subsequent fork)" glosses from V4, V8, V12(d), V0, and the table rows.

## OUT_OF_SCOPE

### Topic 1: V6a link-discoverability apparatus
**ASN-0069, §"Subspace Selectivity" (V6a and the local `coverage` / `project` / `discoverable_from` definitions)**

**Why out of scope**: The scope list excludes *link semantics*. V6 already discharges the fork's structural obligation on links (`V_{s_L}(d_new) = ∅`; the shared I-addresses keep references to common content). V6a goes further, introducing a query apparatus — coverage of an endset, projection of a link slot onto a document's V-positions, and a discoverability predicate — and proving a three-part inheritance lemma over it. That machinery is link-query semantics, not a fork guarantee, and per the scope instruction a claim defined for an excluded topic should be flagged rather than expanded here. The boundary is genuinely close (link *survivability* under editing is a central Nelson promise), so this is a scoping call, not a correctness defect: if V6a stays, it should be the minimal "shared I-addresses preserve existing references" observation, with the predicate apparatus deferred to the link-semantics ASN.

VERDICT: REVISE
