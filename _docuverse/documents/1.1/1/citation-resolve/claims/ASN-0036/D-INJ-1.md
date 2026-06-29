# Citation Resolve — ASN-0036/D-INJ — run 1

*2026-06-29T10:25:30Z*
*Model: sonnet*

## Output

Scanning the prose for claim-label references not yet classified.

The only unclassified label in the prose is **D-CTG-depth**, named in the closing remark: *"D-CTG-depth consumes the lemma at `P := N + 1`, `n := N`…"* — D-CTG-depth is the downstream consumer; D-INJ's correctness does not rest on it. Direction: `forward`.

All five currently-classified `depends` entries (NAT-card, NAT-wellorder, NAT-order, NAT-closure, NAT-addcompat) remain in the prose and their directions are correct.

```
CLASSIFICATIONS:
- label: D-CTG-depth
  direction: forward
  bullet: "- D-CTG-depth — downstream consumer of this lemma; instantiates it at P := N + 1, n := N to derive the pigeonhole contradiction that closes its finiteness step"

RETRACTIONS: []
```
