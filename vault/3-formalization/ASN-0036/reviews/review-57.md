# Cone Review — ASN-0036/D-SEQ (cycle 3)

*2026-04-13 19:27*

I've read the entire ASN carefully, tracing every cross-property chain. Most of the structural issues have already been captured. After a thorough pass, I find one new issue:

### D-CTG verification obligation omits MOVE and APPEND despite S8-fin enumerating them as state transitions
**Foundation**: S8-fin (FiniteArrangement) — "Let Σ → Σ' be any state transition produced by an operation (INSERT, DELETE, COPY, MOVE, REARRANGE, or APPEND)" and "every operation specification must individually discharge the obligation"
**ASN**: D-CTG body text — "Whether DELETE, INSERT, COPY, and REARRANGE preserve D-CTG is a verification obligation for each operation's ASN"
**Issue**: S8-fin defines the complete set of arrangement-modifying operations as six: INSERT, DELETE, COPY, MOVE, REARRANGE, APPEND. S8-fin uses universal language ("every operation specification must individually discharge the obligation") and D-MIN does the same ("every operation that populates or modifies V_S(d) must include [S, 1, …, 1]"). D-CTG alone uses an explicit four-operation list that omits MOVE and APPEND. Both MOVE and APPEND modify dom(M(d)) — MOVE removes and re-inserts positions, APPEND adds a new position — so both can break contiguity. A downstream operation ASN for MOVE or APPEND that reads D-CTG's text would see no verification obligation for contiguity, while S8-fin's text imposes a finiteness obligation on the same operations. The formal contracts of D-CTG and S8-fin (stated as universal invariants without operation lists) are consistent; the gap is in the body text that establishes what downstream ASNs must verify.
**What needs resolving**: D-CTG's verification obligation sentence should either use universal language matching D-MIN and S8-fin ("every operation that modifies V_S(d) must preserve D-CTG"), or explicitly list all six operations from S8-fin's enumeration. If MOVE or APPEND are composites of the four listed operations (and therefore inherit D-CTG preservation), this compositional relationship should be stated so the omission is justified rather than silent.
