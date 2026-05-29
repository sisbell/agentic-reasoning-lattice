# Review of ASN-0036

## REVISE

### Issue 1: S8 lists T4 as a dependency it never uses
**ASN-0036, S8 Formal Contract, Depends**: "T4 (HierarchicalParsing) — partitions tumblers into N/U/D/E fields"
**Problem**: The S8 proof operates entirely on V-positions, which have `zeros(v) = 0` (S8a) and are therefore *not* T4-valid field-bearing addresses. Tracing the proof: Existence uses S8-fin/S2/S3; Coverage uses TS4; the within-subspace lemma uses T1, T3, TumblerAdd, NAT-discrete/closure/order; cross-subspace uses T3, OrdinalShift, TumblerAdd, TS4, T5, T10. T4's field-decomposition machinery is never invoked. A dependency the proof does not exercise is exactly the use-site noise the anti-bloat pass targets.
**Required**: Remove T4 from S8's Depends (and from the Properties-table derivation line for S8), or show the step that actually consumes T4.

### Issue 2: "Nat-pos" coins a label for a foundation-derivable fact
**ASN-0036, S8a proof**: "hence `≥ 1` by **Nat-pos** — the elementary fact that for `n ∈ ℕ`, `n ≠ 0 ⟹ n ≥ 1` (immediate from NAT-discrete at `m = 0`)"
**Problem**: This invents a named lemma for something the foundation already supplies via NAT-discrete. Standard 7 forbids reinventing notation a foundation defines; coining "Nat-pos" as if a reusable handle is exactly that, even though it is inline-attributed.
**Required**: Cite NAT-discrete (instantiated at `m = 0`) directly; drop the "Nat-pos" coinage.

### Issue 3: Worked example presents maximal runs as verifying a conjunct the theorem proves only at n = 1
**ASN-0036, Worked example**: "The maximal-run decompositions exhibited by hand below are concrete instances verifying conjunct (b)" — then exhibits `(1.1, 1.0.1.0.1.0.1.1, 5)`, `(1.1, …, 3)`, `(1.4, …, 2)`.
**Problem**: S8 as proved establishes conjunct (b) only under the singleton decomposition (`nⱼ = 1`), where (b) collapses to `M(d)(v) = a`; existence/uniqueness of maximal runs (`nⱼ > 1`) is explicitly deferred to Open Questions. The example silently exercises the deferred `n > 1` case and labels it as verifying the established conjunct, which can lead a reader to believe S8 establishes maximal decomposition.
**Required**: State in the example that the multi-step runs illustrate the *deferred* maximal case (an instance of (b), not a proof of maximal-run existence), keeping the boundary with what S8 proves explicit.

### Issue 4: S8 is titled and framed as "Finite span decomposition" but proves only the trivial partition
**ASN-0036, S8**: "the arrangement … can be decomposed into a finite set of correspondence runs … `(vⱼ, aⱼ, nⱼ)`"
**Problem**: The full correspondence-run apparatus (general `n`, the ordinal-displacement identity over `0 ≤ k < n`) is introduced, but the theorem exercises it only at `n = 1`, where "decomposition into runs" degenerates to "partition into singletons" — true for any finite function. The genuinely structural content (maximal runs) is deferred. The title/statement overstate what is established.
**Required**: Either prove maximal-run existence, or retitle/restate S8 to reflect that what is established is the singleton partition plus disjointness of singleton intervals, with the run apparatus flagged as forward-scaffolding for the deferred question.

### Issue 5: S9 section carries no formal content
**ASN-0036, S9**: "S9 is S0 read directionally … S0 already holds for every transition unconditionally."
**Problem**: The section states outright that it adds nothing beyond S0, then restates it with a quote and a Gregory confirmation. Under the anti-bloat classifier, a structural slot whose own prose declares it formally empty is a candidate for compression.
**Required**: Reduce S9 to the one-sentence directional reading of S0 (it names a Nelson-emphasized property, so a pointer is warranted), and drop the surrounding restatement.

## OUT_OF_SCOPE

### Topic 1: Existence/uniqueness of maximal correspondence runs
**Why out of scope**: Genuinely new territory, already routed to Open Questions; not an error in this ASN's singleton result.

### Topic 2: Whether editing operations preserve D-CTG/D-MIN/S2
**Why out of scope**: Operation-specific frame/postcondition reasoning is excluded by the Scope section and correctly deferred to Open Questions.

VERDICT: REVISE
