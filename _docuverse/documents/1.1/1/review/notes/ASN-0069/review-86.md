# Review of ASN-0069

## REVISE

### Issue 1: §"Permanence Across Source and Fork" — three lead-in paragraphs duplicate V12's clauses verbatim

**ASN-0069, §"Permanence Across Source and Fork"**: The three paragraphs "By T8 ... and P1 ...: both `d_src` and `d_new` remain in `E_doc`...", "By P0 ... and S0/S1 ...: every I-address in `dom(C)` ... remains...", and "By P2 ...: the provenance records `(a, d_new)` ... persist...", followed by "We name the combined consequence" → V12 (a)/(b)/(c).

**Problem**: V12(a) restates lead-in paragraph 1 (P1), V12(b) restates paragraph 2 (P0), V12(c) restates paragraph 3 (P2), each carrying the same citation. This is the "two paragraphs say the same thing in different words" accretion the anti-bloat pass targets — the prose paragraphs are the derivation, V12 is the named collection of the identical facts. A reader must read the same three guarantees twice.

**Required**: Delete the three standalone lead-in paragraphs and fold their fuller citations into V12's per-clause parentheticals — V12(a) should cite (T8, P1), V12(b) should cite (P0, S0/S1), V12(c) should cite (P2, V9). V12 then carries the full derivation without the redundant prose preamble.

### Issue 2: V8c instantiates the correspondence set over (d_src, d_new) while V8 establishes fullness only over (d_op, d_new)

**ASN-0069, §"Structural Correspondence", V8c**: "The corresponding-position set `{v ∈ T : v ∈ dom(M'(d_src)) ∩ dom(M'(d_new)) ∧ M'(d_src)(v) = M'(d_new)(v)}` ... V8 records a relationship between two documents in `E_doc`."

**Problem**: V8 (its parent property) is carried over the *content source operand* `d_op`, which equals `d_src` only on a first fork; on a subsequent fork `d_op = d_prev`. The ASN is careful about this distinction everywhere else (V8's own prose, V10b, the worked example's subsequent-fork paragraph which explicitly conditions fullness on "d_new ... has not been edited"). V8c silently switches the operand to `d_src`. The symmetry claim itself is trivially true, but presenting `(d_src, d_new)` as the canonical V8 instance suggests full source↔fork correspondence holds on every fork — which V8 does *not* establish for subsequent forks (only V11, under the unedited-chain premise, does).

**Required**: State V8c's set over `(d_op, d_new)` to match V8's domain, or add one clause noting that on a subsequent fork the V8 correspondence partner is `d_prev`, not `d_src`, so the displayed `(d_src, d_new)` instance is the first-fork specialization.

## OUT_OF_SCOPE

None beyond what the ASN already lists in §"Open Questions"; those questions (concurrency guarantees, descendant enumeration, snapshot-vs-living forks, transcludent sources) correctly defer new territory to future ASNs.

VERDICT: REVISE
