# Regional Review — ASN-0034/ActionPoint (cycle 2)

*2026-04-24 03:37*

### Postcondition and derivation bind `i` without a declared carrier
**Class**: REVISE
**Foundation**: (internal — T0, NAT-wellorder)
**ASN**: ActionPoint — Formal Contract *Postconditions:* bullet `wᵢ = 0 for all 1 ≤ i < actionPoint(w)`, and the matching derivation passage "For any i with 1 ≤ i < actionPoint(w), wᵢ = 0. Suppose otherwise, for contradiction: then wᵢ ≠ 0, and to conclude i ∈ S we must also establish the two remaining membership clauses `1 ≤ i` and `i ≤ #w`…"
**Issue**: The postcondition's bound variable `i` has no declared carrier — identical pattern to the S-set-builder gap fixed in the previous cycle, but relocated to the postcondition and its derivation. The derivation's bookkeeping then inherits the gap: S is `{i ∈ ℕ : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0}` (four clauses), but the derivation enumerates only "the two remaining membership clauses `1 ≤ i` and `i ≤ #w`" — it never discharges `i ∈ ℕ`. A downstream consumer reading the Formal Contract sees a postcondition whose quantifier domain is unstated, and a consumer walking the proof sees a membership claim `i ∈ S` justified without checking the carrier clause. Given that the previous-cycle fix made T0/TA-Pos/S all use explicit `i ∈ ℕ`, the postcondition and its derivation are the outlier.
**What needs resolving**: State the postcondition with an explicit carrier for the bound variable (or cite the convention that makes it implicit, applied consistently across the Formal Contract), and have the derivation's `i ∈ S` step discharge every membership clause of S — not only the two picked out here.

### NAT-closure axiom label "distinctness" understates `0 < 1`
**Class**: OBSERVE
**Foundation**: (internal)
**ASN**: NAT-closure — *Axiom:* bullet `0 < 1` (distinctness of the two named constants)
**Issue**: The parenthetical label names `0 < 1` as "distinctness," but `0 < 1` says strictly more than `0 ≠ 1` — it locates `1` strictly above `0` in the order. The prose paragraph above the contract correctly identifies the extra content ("names a second constant in ℕ and locates it in the strict order"); the axiom-slot label is the weaker reading. Purely a labeling/phrasing mismatch; the axiom content itself is correct.
**What needs resolving**: (OBSERVE only)

### TA-Pos notation note references a "separate tumbler ordering" absent from this ASN
**Class**: OBSERVE
**Foundation**: (internal — TA-Pos)
**ASN**: TA-Pos, *Note on notation* — "`>` is reserved for a separate tumbler ordering under which zero tumblers need not all be minimal, so writing `Pos(t)` as `t > 0` would conflate the two relations."
**Issue**: The note's justification invokes an object (a tumbler-level `>` ordering, and the tumbler `0`) that has no definition in this ASN and no dependency arrow pointing to one. The note reads cleanly if the referenced ordering exists downstream, but as written the reader has to accept the justification without a way to check what is being reserved against what. This is notation-choice rationale, not axiom content, so it does not break any proof — it just asks the reader to defer.
**What needs resolving**: (OBSERVE only)

VERDICT: REVISE
