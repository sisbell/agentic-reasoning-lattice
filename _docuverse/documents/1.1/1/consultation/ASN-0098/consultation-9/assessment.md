# Channel Assignment — ASN-0098 review-9

**Date:** 2026-05-25 21:22

```
## Issue 1: Ancestor case missing in tightness achievability argument
Reason: Fix is internal — extend the existing case split using T1 trichotomy and the structural form of version-descendant tumblers already cited in the ASN. No design intent or implementation evidence is required; the ancestor argument mirrors the existing non-nesting/descendant arguments using ASN-0034 facts.
```

```
## Issue 2: Displacement notation inconsistent with foundation in worked numerical example
Reason: Fix is internal — δ(n, m) is defined in ASN-0034 and TumblerAdd's length identity is stated there; correcting the example to use δ(3, #s) or a fully concrete tumbler is purely a mechanical application of cited foundations.
```

```
## Issue 3: LP4 hypothesis assumes both sides defined without explicit precondition
Reason: Fix is internal — adding the explicit precondition d ∈ dom(Σ'.M) (justified by M1 of ASN-0093, already cited in downstream applications) is a local statement-tightening with no external dependencies.
```

```
## Issue 4: Non-nesting case argument compresses T1 case analysis
Reason: Fix is internal — expanding the proof to spell out the T1 case (i) analysis at the divergence position parallels the descendant case already worked out in the same section, drawing only on ASN-0034 facts already cited.
```
