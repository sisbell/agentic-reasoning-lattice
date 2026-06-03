# Review of ASN-0069

I checked the identity allocation (V1), the transclusion/no-content claims (V3, V4, V4b), source isolation (V5/V5a), the correspondence and chain induction (V8, V11, V11a), provenance (V9, V12), the empty-source case (V7), and the full ValidComposite★ verification in §"The Fork Composite". The proofs hold — the sub-case dispatch, the freshness discharges via ChildSpawnFreshness/FrontierEquivalence, the P4★-at-composite-boundary use in V12(d), and the V11 induction are all sound, and the empty-source K.δ-alone composite is verified separately and correctly. Boundary cases (empty source, subsequent fork of an edited prior version, fork-of-empty-fork, zeros bound on the version chain) are covered. No correctness defect found.

The note carries `review-mode.anti-bloat`. The remaining findings are duplication/accretion, not correctness.

## REVISE

### Issue 1: The first-fork/subsequent-fork operand formulas are reproduced four times
**ASN-0069, §"What Must Be Constructed"**: "First fork of `d_src` (when `A_v(d_src)` has emitted no prior version): `d_new = inc(d_src, 1)` and `d_op = d_src`. Subsequent fork ...: `d_new = inc(d_prev, 0)` and `d_op = d_prev = max(dom(A_v(d_src)))`."

The same allocation formula recurs as a full claim in **V1** ("First fork of `d_src` ...: `d_new = inc(d_src, 1)`, produced by K.δ case (ii) with `k = 1`..."), a third time in **§"Identity by Sub-Allocation"** item (i) ("`inc(d_src, 1)` when no prior version exists, `inc(max(children), 0)` otherwise"), and a fourth time in the **V0** effects block ("`d_new = inc(d_src, 1)` on first fork ... `d_new = inc(d_prev, 0)` on subsequent fork").

**Problem**: V1 is the canonical identity claim and V0 legitimately restates the effect for the composite assembly. But the §"What Must Be Constructed" bullets and the §"Identity by Sub-Allocation" parenthetical reproduce V1's formulas verbatim in substance before V1 is even stated — the "two paragraphs say the same thing in different words" pattern. A reader following the argument re-encounters the identical formula in motivation, in sub-allocation transfer, and in the claim.

**Required**: In §"What Must Be Constructed", introduce only the `d_src` vs `d_op` *distinction* (identity source vs content source) without reproducing the `inc(d_src, 1)`/`inc(d_prev, 0)` formulas; let V1 carry them. Drop the redundant formula parenthetical from §"Identity by Sub-Allocation" item (i) and cite V1.

### Issue 2: The Worked Example re-derives V10(a) instead of exhibiting it
**ASN-0069, §"Worked Example", subsequent-fork paragraph**: "both `d_new = inc(d_src, 1)` and `d_new² = inc(d_new, 0)` have length `#d_src + 1` (the first by TA5(d) at `k = 1`, the second by TA5(c) at `k = 0` inheriting `d_new`'s length), so they share a length ... and differ in that single trailing component (TA5(c) at the subsequent fork modifies position `sig(d_new) = #d_new` only ...)."

**Problem**: This reproduces the TA5-based length-and-distinctness derivation already given in V10(a) and §"Independence Among Forks". A worked example should *exhibit* that `d_new` and `d_new²` are distinct addresses and check the postconditions against concrete values — not re-run the general proof with full TA5 citations. The re-derivation is proof content relocated into a structural slot meant for illustration.

**Required**: Replace the in-line TA5 derivation with a citation to V10(a) and a concrete exhibition (e.g., show the two sibling tumblers differing only in the trailing component), so the example checks the claim rather than re-proving it.

## OUT_OF_SCOPE

### Topic 1: Counterpart correspondence for typed-but-equal content; value-equal distinct I-addresses
The final two Open Questions ("relate independently-typed but textually identical content"; "distinguish two distinct I-addresses holding equal byte values") concern COPY-style typed content and value-vs-identity semantics. Correctly raised as future work, not claimed here.

**Why out of scope**: COPY operation mechanics and link/typed-content semantics are excluded from this ASN; posing them as open questions for a future ASN is appropriate.

META: (none — the ASN defines an operation abstractly as a state transition with invariants an alternate implementation must satisfy; it has not drifted into implementation mechanics.)

VERDICT: REVISE
