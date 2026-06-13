# Review of ASN-0122

This note is unusually rigorous: the proofs show their work, the worked example exercises fan-out/maximality/tie-break/clipping/self-comparison and checks out arithmetically, the X7(iii) injectivity obligation for gap-closing contraction is genuinely discharged (not hand-waved) via D-BJ + D-DP(a), and the X11 path-decomposition (in-degree ≤ 1 via TS2, out-degree ≤ 1, acyclic via TS4) is correct. The findings below are a precision overstatement and accreted prose surfaced under the anti-bloat lens.

## REVISE

### Issue 1: X5's "none of the four is redundant" is false for P, Q and unproven

**ASN-0122, X5 (Locality)**: "any two states agreeing on these four data return the same relation, and none of the four is redundant" … "changing res|P at a single instance p — toward or away from some res(q) — adds or deletes the pair (p, q), so no datum can be dropped."

**Problem**: `res_Σ|P` is a function whose domain *is* `P`, so `P = dom(res_Σ|P)` and `Q = dom(res_Σ|Q)`. Given the two restricted maps, `P` and `Q` are recoverable; they are redundant in the four-tuple. The supporting argument perturbs `res|P` and concludes the *resolution maps* are load-bearing — it establishes nothing about `P, Q`, so the conclusion "none of the four is redundant" / "no datum can be dropped" is both unproven and, for two of the four, false. The note contradicts itself here: the Claims-Introduced table lists X5 as "corr is a function of **the two restrictions**," which is the correct irreducible data.

**Required**: Narrow the claim to the resolution maps — e.g., "corr factors through `(res_Σ|P, res_Σ|Q)`, and neither map can be dropped" — or state explicitly that `P = dom(res_Σ|P)`, `Q = dom(res_Σ|Q)`, so the four-tuple is presentational and the irreducible data are the two maps. Align the prose with the table.

### Issue 2: X6(c) parenthetical recaps X6(b)'s premise rather than adding reasoning

**ASN-0122, X6(c)**: "(Edits that strike an intermediate between its own steps are premise two's case: their position maps join the composite, and what survives them is what transports.)"

**Problem**: X6(b)'s "Interleaved intermediate edits" premise already states exactly this — that an intermediate edit's position map `π_i` is interposed into the composite and the composite carries only survivors. The parenthetical in (c) re-says it at a deferral point ("premise two's case"), advancing no reasoning. This is the forward-reference recap pattern the anti-bloat classifier targets: a paragraph saying in different words what an earlier paragraph already discharged. X6(c)'s own sentence "The middle of the chain can vanish; the correspondence cannot" already states the conclusion the parenthetical gestures at.

**Required**: Delete the parenthetical. (b) discharges the interleaved-edit case once; (c) need not re-narrate it.

### Issue 3 (minor): meta-signpost in the region definition

**ASN-0122, region definition (Spec-set and region)**: "Two design decisions are packed into this definition, and we make them explicit."

**Problem**: Pure signpost — it announces an explanation rather than being one. The two design decisions (domain-clipping; content-subspace confinement) and the concrete `σ = ([1,5], [3])` example that follow stand on their own. The announcing sentence is removable without loss.

**Required**: Delete the sentence; let the clipping rationale and the example carry the point directly.

## OUT_OF_SCOPE

### Topic 1: corr transport under general-depth gap-closing contraction
X7(iii) transports correspondence across the *depth-2* shifting contraction (D-SHIFT/D-L/D-BJ/D-DP, ASN-0082). A deeper gap-closing contraction would need the analogues of those postconditions at general depth before X-T could be instantiated.
**Why out of scope**: This is a missing *foundation* (ASN-0082 is depth-2), not a defect in this ASN. X7 correctly transports across exactly the edit vocabulary the foundations supply.

### Topic 2: the listed open questions
n-way alignment composed from pairwise reports, cached/derived correspondence indices, interoperable pair granularity, and correspondence-bearing-ness of future subspaces are all genuinely future territory.
**Why out of scope**: Already enumerated as Open Questions; correctly deferred, not errors here.

VERDICT: REVISE
