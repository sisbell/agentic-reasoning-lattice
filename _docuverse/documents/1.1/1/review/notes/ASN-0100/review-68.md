# Review of ASN-0100

This is a mature, rigorous note. I verified the three-effect decomposition, the substrate composite (K.α / K.μ⁻ / K.μ⁺ / K.ρ), the invariant discharge (S0/P0, S2, S3★, D-CTG★/D-MIN★/D-SEQ★ including the m≥3 closed-interval reduction, S8★ via C1a, L0's content clause, provenance), the worked examples, and the two wp computations. The correctness is sound and the edge cases (j=0, append, empty document, empty-arrangement-with-nonfresh-allocator) are genuinely covered. All references are to foundation ASNs (0034/0036/0047/0058/0082/0093/0098); no improper cross-references. The findings below are confined to accretion patterns flagged by the review mode.

## REVISE

### Issue 1: Firing-condition stated twice in adjacent text

**ASN-0100, §The Operation: Formal Contract, step 2**: The K.μ⁻ bullet first says "fired iff the pre-state content-subspace Right region `Right := {v ∈ V_{s_C}(d) : v ≥ p}` is non-empty," then adds "The operative condition is single: K.μ⁻ appears in the canonical decomposition exactly when strict s_C contraction is both needed … and admissible while preserving s_L," and then the formal **(INS.μ⁻-fires)** claim restates "K.μ⁻ fires iff `Right ≠ ∅`; it is omitted in exactly two cases…"

**Problem**: The firing condition is asserted three times in one bullet — the lead sentence, the "operative condition is single" sentence, and the named (INS.μ⁻-fires) claim. The middle sentence is meta-prose that re-explains the iff already given and re-stated formally below it; the reader must skip it to reach the carrier claim that downstream text actually cites ("By (INS.μ⁻-fires)…").

**Required**: Keep the named claim (INS.μ⁻-fires) as the single statement of the firing condition and delete the "operative condition is single" restatement.

### Issue 2: Convention-matching justification in the wp section

**ASN-0100, §Weakest-Precondition Analysis, discoverability case**: "We therefore carry INSERT's precondition INS.pre as a standing conjunct, matching the LP12a (ASN-0098) convention, whose wp likewise carries an explicit `enabled(K.μ⁻[d, R])` conjunct."

**Problem**: The total-correctness reason for carrying INS.pre is already given in the preceding sentence ("`wp(S, R)` must entail `S`'s precondition"). The trailing clause justifies the choice by appeal to another document's stylistic convention rather than advancing the computation — a convention-rationale accretion of the kind this review mode targets.

**Required**: Drop the "matching the LP12a convention…" clause; the total-correctness sentence already justifies the standing conjunct.

## OUT_OF_SCOPE

### Topic 1: Link-subspace insertion (K.μ⁺_L)

**Why out of scope**: The note explicitly bounds itself to the content subspace; link-subspace insertion is correctly deferred and not treated as an error here.

VERDICT: REVISE
