# Channel Assignment — ASN-0084 review-99

**Date:** 2026-05-30 20:14

```
## Issue 1: Worked examples assert "Canonical partition" using machinery the ASN explicitly defers
Reason: The fix is internal — either prove the bridging lemma (no mergeable adjacent pair ⟹ canonical, via S8 uniqueness already cited in the ASN) or weaken the examples' final line. Both options draw only on definitions and results already present (S8 maximality/uniqueness, Merge adjacency, the examples' own merge checks); no design intent or implementation evidence is needed.

## Issue 2: Properties table lists region non-emptiness as part of the precondition R-PRE, but the body derives it
Reason: The fix is internal — the body already establishes region non-emptiness as the derived "Width positivity" consequence of R-PRE(iii)+(iv)+CS2, so correcting the table to match is a self-contained editorial alignment requiring no external channel.
```
