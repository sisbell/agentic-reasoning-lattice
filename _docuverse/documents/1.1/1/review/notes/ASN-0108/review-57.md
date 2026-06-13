# Review of ASN-0108

I read this as windowed (resumable) enumeration of a state-dependent matching set under a total order, with the choice of ordering key left as a parameter and each guarantee tagged with the key-property it needs. I stress-tested the load-bearing claims and the boundary coverage; both hold. The note also carries the anti-bloat classifier, so I checked the prose against the accretion patterns separately. My findings on that axis came up empty *after* applying the review's own protections — detail below.

## What I verified (the hard claims)

- **W2 (offset-vs-identity wp).** I recomputed the offset window `[j+1, min(j+N,m')]` against `R`'s target `[j'+1, min(j'+N,m')]` and confirm `wp(resume_offset, R) ≡ j'=j ∨ (j ≥ m' ∧ j' ≥ m')`. The strict nesting **membership-identity ⟹ frozen-prefix (`j'=j`) ⟹ genuine wp** is real: the heavy-orphaning corner (`Match(q,Σ')={a_2}`, both windows empty, `R` holds, `j'=1≠2=j`) genuinely separates frozen-prefix from the wp, and the orphan-one/insert-one corner genuinely separates membership-identity from frozen-prefix. Sound.
- **W4 (partition, variable schedule).** The cumulative-cut-point induction `W_i =` ranks `[S_i+1, min(S_{i+1},m)]` is correct, and only W9a's closed form depends on the constant schedule. Sound.
- **W5 (coherence).** The cut-point walk (clause-1 violation → genuine skip of a never-orphaned link), the tail-reorder walk (clause-2 violation, harmless), and the cancellation walk (clause-1 failures cancel → sufficient-not-necessary) are each internally consistent and exhibit *distinct* phenomena. I reconstructed the one-sentence "cursor-advance induction" for unconditional no-re-delivery (delivery gives `a ⪯ c_k`; clause 1 transfers it across the transition; `c_k ≺ c_{k+1}` advances; iterate) — it works, and it correctly relies on computability being *presupposed* by clause 1, which W9b then unfolds as (i′). The W5/W9b treatment of clause-1-vs-computability is consistent (W5's "unconditional" is scoped to *termination*, not to needing only clause 1).
- **W9b (termination).** The per-link charge argument is sound: every delivery charges to the initial-tail base or to its most-recent inflow event; re-delivery requires leave-and-re-enter, so distinct deliveries of one link have distinct contributions (injective), giving deliveries `≤ |initial tail| + |events|`. The "bounded instantaneous size insufficient" and "zero-inflow non-termination via re-ascension" (W9c) counterexamples correctly isolate cumulative inflow and cut-point preservation as the operative quantities.
- **W6a (creation bridge).** The `K.λ`-frame argument freezing `image(W,d_q,·)` and lifting ASN-0127's F-LAMBDA from fixed-`I` `findlinks` to the discoverability `Match` is correct, including disjointness from `K.λ`-freshness.
- **W9a count.** `⌈m/N⌉ + [N divides m]` checks against all four walks (`m=4→3`, `m=5→3`, `m=0→1`, `N=3,m=2→1`) and spot cases I added.

**Boundary coverage is complete:** empty set (`m=0`, the only walk exercising "next cursor `c` unchanged"), first-window-already-short (`N>m`), exact multiple (the degenerate empty terminator + the non-termination overrun if a reader stops only on strictly-positive short windows), single matcher, cursor-leaves-the-set (W8), new-link-mid-pass (W6/W6a), orphan-mid-pass (W7/W8), multi-document spread (W6 caveat). Foundation usage is correct and no foundation notation is reinvented (`Match` is an explicit local alias for `findlinks_V`, not a competing definition).

## On the anti-bloat mandate

I examined the flagged patterns and am deliberately not raising them, because each candidate is either protected by the review's own rules or load-bearing:

- The three concrete walks in W5 and the walks in W8/W9c, plus the four termination walks — **concrete examples are explicitly not meta-prose**, and each exercises a *distinct* failure (skip vs. cursor-collapse vs. non-termination vs. the four boundary counts).
- The udanax-green key archaeology (`onlinklist` dedup, the matched-slot/`LINKFROMSPAN` description) is a **statement of what the implementation does** — also protected — and the matched-slot contrast does work: it establishes that `κ` is fixed *a priori* as a function of the immutable link value rather than query-dependent, which W5/W8 lean on.
- The three-key sorting recurs in W5 (stability), W6 (allocation-monotonicity), W8 (computability), W9b (permanence) — but each sorts on a *different* property, which is the note's substantive spine, not repetition.
- Cross-claim references use "(established above)" to refer back to the permanence derivation rather than re-deriving it; the one apparent restatement (W8 re-noting that orphaning leaves the endset intact) is in service of W8's genuine computability-vs-invariance distinction.
- The W9b source-(3) enumeration (resurrection / born-ghost) is an **exhaustiveness** demonstration of the inflow taxonomy — which the rigor standard wants, not bloat.

In short, the current revision's prose is load-bearing once the protected categories are set aside; the accretion the classifier warns of appears to have been trimmed.

## OUT_OF_SCOPE

### Topic 1: Multi-document enumeration discipline (Open Question 1)
**Why out of scope**: `Match` spans multiple home documents, so the address key is allocation-monotone only within a single document and W6's append-at-tail (and its blind-spot closure) is document-local. The note scopes W6 correctly to a single allocator chain and defers the global discipline to OQ1 — this is future-ASN territory, not an error here.

### Topic 2: Eventual-delivery guarantee under a non-allocation-monotone key (Open Question 2)
**Why out of scope**: When the key is not allocation-monotone, a between-call creation can land permanently behind the cursor (the W6 blind spot). What the protocol must additionally guarantee to prevent permanent skip is correctly left open.

### Topic 3: Scope-fenced operations
**Why out of scope**: Count-only retrieval, full-set retrieval (FINDLINKS/ASN-0099), MAKELINK, FOLLOWLINK, and BEBE define no claims here, as required. W10 correctly fences the companion cardinality query (the "k of m" source) outside the windowed protocol, and OQ5 correctly flags the delivery-vs-counting-order correspondence as a separate concern.

VERDICT: CONVERGED
