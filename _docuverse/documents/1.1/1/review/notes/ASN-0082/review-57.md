# Review of ASN-0082

## REVISE

### Issue 1: I3-S7 / S7-post misstate the foundation's S7 dependency set
**ASN-0082, I3-S7 (and identically S7-post)**: "S7 (StructuralAttribution) is a derived theorem whose dependencies are S7a, S7b, S7d together with S0, S4, and the foundation lemmas T4, T4b, T3, T10a.4, GlobalUniqueness (ASN-0034)".
**Problem**: ASN-0036's S7 contract states its preconditions as "S7a, S7b, S7d, T4, T4a, T4b, T0, T10a, T10a.4". The ASN-0082 enumeration adds S0, S4, T3, GlobalUniqueness and silently drops T4a, T0, T10a. The proof then leans on the spurious entries ("S0 holds by I3-C"), as if S7 required S0. The conclusion (post-state satisfies S7) survives because every relevant lemma is state-independent, but the *named premise chain* does not match the foundation theorem it cites — a precision defect in an ASN whose value is precise dependency tracking.
**Required**: Cite S7's actual ASN-0036 dependency set, or, if the author believes S7 genuinely consumes S0/S4, justify that against the foundation contract rather than asserting a divergent list.

### Issue 2: Duplicated wp prose — the rhetorical "Why…?" paragraphs restate discharges already shown
**ASN-0082, Weakest-precondition analysis (S8a-post)**: the conjunct-2 discussion ("From `v ∈ R` … OrdinalExceedsDisplacement (iii) … the `v ∈ R` precondition combined with `p ∈ V_1(d)` …") is then repeated in full by "*Why the obligation sits at both v and p, not at v alone?*" ("The wp obligation `v₂ − c > 0` cannot be discharged from v's pre-state invariants alone …"), which closes with a cross-reference re-explaining I3-VP ("This is the structural counterpart to insertion's I3-VP …").
**Problem**: Two paragraphs in the same section say the same thing in different words (the anti-bloat "same thing twice" pattern). The I3-VP wp analysis carries the parallel redundancy ("*Why componentwise positivity of v on positions 1..m−1 specifically?*" re-derives conjunct 1). This is essay content in a proof slot — the wp computation already exhibits the dependency structure the prose claims to "make visible."
**Required**: Keep the wp obligation table and its one-line discharges; delete the rhetorical-question recapitulation paragraphs in both wp sections.

### Issue 3: The "ordinal-level" definition enumerates its downstream consumer instead of advancing its meaning
**ASN-0082, Span Width Preservation intro**: "We call a span *ordinal-level* when its width acts purely at the deepest component: actionPoint(ℓ) = m. This is the precondition I3-S requires … We state I3-S as the general ordinal-level span fact and invoke it within the shifted region where I3 applies."
**Problem**: A definition's introduction enumerating its use-site ("the precondition I3-S requires," "invoke it within the shifted region") is the flagged "definition enumerates downstream consumers" pattern. The definitional content is the single clause `actionPoint(ℓ) = m`; the rest is rationale prose the reader must skip to reach the lemma.
**Required**: State the definition; drop the use-site narration. The Statement Registry already records "ordinal-level" cleanly.

### Issue 4: Use-site inventories preview lemma labels that the lemmas themselves establish
**ASN-0082, "Structural preservation"**: "We derive that S8-depth, S8a, S8-fin, and S2 hold for the post-state M'(d), and that referential integrity (S3) is preserved, enabling composition with subsequent operations." And **"Arrangement invariants not preserved," S ≠ 1 case**: "The arrangement-typing invariants — S8-depth, S8a, S2, S3, S8-fin — are preserved (I3-VD, I3-VP, I3-S2, I3-S3, I3-fin), and that is the full obligation on the post-state."
**Problem**: Both are inventory restatements of the lemma block that immediately follows (or precedes) them, plus rationale ("enabling composition with subsequent operations," "that is the full obligation"). The labels carry their own statements; the preview adds no reasoning.
**Required**: Remove the inventory sentences; let the lemmas stand.

### Issue 5: Repeated forward references to D-SHIFT before it is stated
**ASN-0082, ThreeRegions** ("The set Q₃ … is defined in D-SHIFT below, once the shift function σ is in hand") and **OrdinalDisplacementProjection** ("At the restricted depth m = 2 (see D-SHIFT below), w = [0, c] …").
**Problem**: Multiple paragraphs in different sub-sections defer to the same downstream location (D-SHIFT) — the flagged forward-reference-deferral pattern. The σ/Q₃ machinery could be introduced once at its point of use rather than pointed at twice from upstream.
**Required**: Drop the "(see D-SHIFT below)" deferrals; introduce Q₃ at D-SHIFT without the upstream promissory notes.

## OUT_OF_SCOPE

### Topic 1: Depth > 1 generalization of gap-closure and dense partition
**Why out of scope**: Already correctly carried as an Open Question. The depth-scoping axiom `#p = 2` is a deliberate restriction, not a gap; lifting it (preserving the round-trip and shift/increment commutativity) is genuine new territory for a future ASN.

### Topic 2: External-reference update after a shift
**Why out of scope**: Listed in Open Questions. What the system must surface to let an external recorder re-anchor a repositioned V-position is a protocol concern beyond this arrangement-layer ASN.

VERDICT: REVISE
