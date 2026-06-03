# Review of ASN-0069

## REVISE

### Issue 1: Defensive "not duplicates" clause in V8a preamble
**ASN-0069, §"Structural Correspondence", paragraph introducing the version stream**: "V8a's version stream is therefore the sibling configuration; V11's chain `d^i_new` (length `#d_src + i`) is the distinct nesting configuration, so the two parallel inductions range over different objects and are not duplicates."

**Problem**: The clause "so the two parallel inductions range over different objects and are not duplicates" advances no reasoning — it is a reviser-facing assertion that V8a and V11 are not redundant, the residue of a prior redundancy challenge rather than content a reader following the proof needs. The genuine distinction (sibling length `#d_src + 1` vs chain length `#d_src + i`) is already stated; the "not duplicates" framing is the meta-layer. The same paragraph also forward-references "the Notation for multiple forks block below" — using `d_new^i` notation before it is introduced — compounding the accretion.

**Required**: Delete the "so the two parallel inductions… are not duplicates" clause. Keep only the substantive length contrast. If `d_new^i` notation is needed at this point, introduce it here rather than pointing forward.

### Issue 2: Defensive S8-run disambiguation in worked example
**ASN-0069, §"Worked Example", *Correspondence (V8)***: "This alignment is a cross-document V-position correspondence: its first two slots are V-positions, distinguishing it from an S8/S8★ correspondence run, whose middle slot is an I-address."

**Problem**: This sentence exists only to forestall a confusion between the `(v_src, v_new, length)` alignment triple and an S8 correspondence run `(v, a, n)`. It does not advance the worked example — the reader computing the example does not consult S8 here. It is meta-prose occupying a concrete-example slot.

**Required**: Remove the disambiguation clause. The triple `([s_C, 1], [s_C, 1], 3)` is self-explanatory in context; if a name is wanted, state it without the comparative defense.

## OUT_OF_SCOPE

None. Scope boundaries (INSERT/DELETE/COPY mechanics, link semantics, version-DAG structure, concurrency beyond the sequential axiom) are respected, and the genuinely-future questions are correctly parked in §"Open Questions" rather than asserted as claims.

VERDICT: REVISE
