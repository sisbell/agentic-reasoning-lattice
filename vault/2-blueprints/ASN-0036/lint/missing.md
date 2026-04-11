# Missing Dependencies — ASN-0036

*Last scanned: 2026-04-11 11:42*

- **D-CTG**: MISSING: T1(i) — "since v₁ < v₂ by T1(i)", "By T1(i), w > v₁", "By T1(i), w < v₂"
- **D-CTG-depth**: MISSING: T1(i) — "by T1(i), since j is the first disagreeing component and j ≤ min(m, m)"
- **D-SEQ**: MISSING: T1(i) — "By T1(i) (TumblerOrdering, ASN-0034), v₁ < v₂" and "again by T1(i)"
- **S8**: MISSING: TA5(b) — "TA5(b) gives `(v + 1)ᵢ = vᵢ` for all `i < sig(v)`"
- **S8**: MISSING: TA5(c) — "By TA5(c), `v + 1 = inc(v, 0)` satisfies `#(v + 1) = m` and differs from `v` only at position `m`"
- **S8-depth**: MISSING: TA5(c) — "TA5(c) guarantees the successor has the same depth as the predecessor"
- **S8a**: MISSING: LM 4/30 — "per T4 and LM 4/30" in the Remark on link-subspace
- **vpos(S, o)**: MISSING: subspace — referenced in postcondition inverse: "subspace(v) = v₁" and "vpos(subspace(v), ord(v)) = v"
- **vpos(S, o)**: MISSING: zeros — referenced in postcondition S8a satisfaction: "zeros(vpos(S, o)) = 0"

*28 files scanned.*
