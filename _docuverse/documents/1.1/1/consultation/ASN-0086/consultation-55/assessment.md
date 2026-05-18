# Channel Assignment — ASN-0086 review-55

**Date:** 2026-05-18 06:35

```
## Issue 1: R7a's class-(i) replay frame is asserted, not derived
Reason: The reviewer has already cited T10a's text from ASN-0034 showing runtime preconditions (parent activation, spawnPt admission). The fix is to either extend the replay vocabulary to include hierarchy-construction primitives or rewrite the proof to discharge runtime preconditions explicitly — both derivable from re-reading ASN-0034's T10a axiom carefully.
```

```
## Issue 2: Notation error in R7a statement
Reason: Simple notation error — `Σ_n'` is undefined and the body uses `Σ_m` consistently. Internal fix: drop the `= Σ_n'` clause.
```

```
## Issue 3: ASN-0036 P3 mis-attribution
Reason: P3 (ArrangementMutability) is in ASN-0047, not ASN-0036. The reviewer has identified the correct replacement citations (ASN-0036's S9 + ASN-0043's L12 + L12a). Internal fix verifiable against the cited specs.
```

```
## Issue 4: "Substrate emission primitive" terminology is inconsistent
Reason: Pure terminology consistency fix — distinguish the broad class-(iii) primitive from the disciplined `Emit_K` subset throughout the note. Internal fix.
```

```
## Issue 5: Forward-reference accretion patterns (anti-bloat classifier)
Reason: Each pattern (a)–(i) is meta-prose or organizational justification that should be trimmed per the anti-bloat classifier. Internal exposition fix; no design or implementation question is at stake.
```

```
## Issue 6: R6b META framing
Reason: Meta-meta-prose can be folded into the Definition of `nullified` or restated as a direct LEMMA reading off the Definition's quantifier range. Internal restructuring.
```

```
## Issue 7: Concrete consequence for non-disciplined emissions missing
Reason: Constructing an L1c-admissible non-disciplined address with `#E = 3` (e.g., `1.0.1.0.1.0.2.1.5`) is derivable from L1c's literal admissibility conditions in ASN-0043. The reviewer has already proposed the example. Internal fix.
```

```
## Issue 8: SharedDepthOneAllocator lemma placement
Reason: Pure organizational fix — promote the lemma out of the Setup section to separate derived material from given material. Internal restructuring.
```
