# Review of ASN-0087

## REVISE

### Issue 1: M1 dual-attribution prose is citation bookkeeping, not reasoning

**ASN-0087, Inputs**: "M1 is stated identically — as the inclusion `dom(Σ.M) ⊆ dom(Σ'.M)` — in both ASN-0047 and ASN-0093; the two coincide on that inclusion clause... Uses below that need only the inclusion cite 'M1' without re-attributing; the `E_doc` identity, used here, is the ASN-0047-specific clause."

**Problem**: The final sentence is pure citation-convention bookkeeping — it tells the reader *how the author will cite M1*, not what M1 establishes. A precise reader needs only "`dom(M) = E_doc` (M1, ASN-0047)." The remaining apparatus (identical statements, coincidence on the inclusion, "ASN-0093 has no entity layer," the no-re-attribution convention) is defensive meta-prose anticipating a citation-ambiguity objection. The wp Case 2 paragraph then re-litigates the same point ("M1 (the inclusion clause, common to ASN-0047 and ASN-0093 per *Inputs*) supplies only the inclusion..."), so two paragraphs in different sections carry the same attribution argument.

**Required**: Reduce the Inputs note to the single load-bearing fact (`dom(M) = E_doc` from ASN-0047's M1; the inclusion clause is the shared part). Drop the "uses below cite M1 without re-attributing" convention sentence and the duplicate attribution in wp Case 2.

### Issue 2: L1c discharge conflates `A_L(d)` with L1c's chain-from-`d`

**ASN-0087, Invariant Preservation (Per-State Invariants)**: "ℓ is produced by `A_L(d)`, so by ChainDiscipline (ASN-0093) ℓ lies on d's link sub-allocator chain `A_L(d) = S(b_L(d), 1)`, whose elements are exactly the inc-chain emissions."

**Problem**: L1c requires an inc-chain seeded at `origin(ℓ) = d` with `k₁ = 2`. That chain is `d →[inc(·,2)]→ b_C(d) = [d,0,1] →[inc(·,0)]→ b_L(d) = [d,0,2] →[inc(·,1)]→ [d,0,2,1] →[inc(·,0)]*→ ℓ`. Its intermediate emissions include the anchors `b_C(d)` and `b_L(d)`, which have `#E = 1` and are **not** elements of `A_L(d) = S(b_L(d), 1)` (whose elements all have `#E = 2`). So `A_L(d)`'s elements are *not* "exactly the inc-chain emissions" of L1c's chain — the chain from `d` additionally traverses two anchors that `A_L(d)` excludes. The argument leans on a `k₁ = 2` first step that `A_L(d)`'s sibling-stream framing does not exhibit.

**Required**: Either discharge L1c the clean way — ℓ enters `dom(L)` via K.λ, and ASN-0093 maintains L1c over all of `dom(L)`, so L1c holds at ℓ at Σ' — or exhibit the actual `d`-seeded chain (through `b_C(d)`, `b_L(d)`, first emission, then sibling advances) rather than identifying it with the `A_L(d)` stream.

## OUT_OF_SCOPE

### Topic 1: Well-formedness of forward-reaching endsets
The Open Questions raise constraints on endsets covering not-yet-allocated I-addresses. The ASN correctly bounds its own claims with `StandardAuthoring`; a general theory of forward-reaching endset well-formedness is future territory, not a defect here.

VERDICT: REVISE
