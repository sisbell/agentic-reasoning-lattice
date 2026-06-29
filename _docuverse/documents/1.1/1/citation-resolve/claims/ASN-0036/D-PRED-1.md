# Citation Resolve — ASN-0036/D-PRED — run 1

*2026-06-29T13:36:14Z*
*Model: sonnet*

## Output

D-INJ exists and its `depends` list (line 39) confirms it consumes D-PRED in its above-k₀ surjectivity sub-case. From D-PRED's perspective, D-INJ is the downstream consumer — D-PRED names it to explain the scope of the exported result. That's a `forward` reference.

No currently-classified entries need retraction (NAT-closure, NAT-wellorder, NAT-zero all appear and are correctly directional).

```
CLASSIFICATIONS:
- label: D-INJ
  direction: forward
  bullet: "- D-INJ (InjectiveImageCardinality) — downstream consumer of this lemma; its above-k₀ surjectivity sub-case draws the predecessor `i` from D-PRED and is the motivating use that bounds the lemma to existence alone"

RETRACTIONS: []
```
