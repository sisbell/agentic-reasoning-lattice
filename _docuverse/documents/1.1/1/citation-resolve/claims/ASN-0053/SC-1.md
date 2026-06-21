# Citation Resolve — ASN-0053/SC — run 1

*2026-06-20T23:45:23Z*
*Model: sonnet*

## Output

I found it. `T1` is `(LexicographicOrder, ASN-0034)` — confirmed from S7's depends list. Now I have everything needed.

The SC claim prose references exactly one external label: `T1`. It appears in the opening sentence ("under T1"), the second sentence ("Since T1 is a total order"), and the Axiom ("Axiom: T1 — positions are totally ordered"). The claim's exhaustiveness proof and mutual-exclusivity argument rest entirely on T1 supplying a total order over positions, making every pair of boundary points comparable. That is a `depends`.

No other claim labels appear in the SC prose.

```
CLASSIFICATIONS:
- label: T1
  direction: depends
  bullet: "- T1 (LexicographicOrder, ASN-0034) — supplies the total order on positions whose comparability of any two boundary points makes the five-case split exhaustive and mutually exclusive"

RETRACTIONS: []
```
