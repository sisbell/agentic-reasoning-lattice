# Review of ASN-0100

## REVISE

### Issue 1: Empty-arrangement case is verified only for the pristine sub-case

**ASN-0100, A Worked Example (empty-document first insertion)**: "Let `d` have `V_{s_C}(d) = ∅` and additionally `V_{s_L}(d) = ∅` ... and stipulate further that no content has ever been allocated under `d` — `{a' ∈ dom(Σ.C) : origin(a') = d} = ∅`."

**Problem**: The empty-arrangement precondition (ValidFirstInsertionPosition) is `V_{s_C}(d) = ∅`, which is *independent* of whether `dom(C)` holds residual `d`-origin addresses. The substrate permits full content-subspace clearance — K.μ⁻ with `n'_{s_C} = 0` — after which `V_{s_C}(d) = ∅` but the document's prior content addresses persist in `dom(C)` by S0/P0 (precisely the Istream/Vstream asymmetry the Background section emphasizes; ASN-0047's `m_S(d)` note explicitly anticipates re-pinning "after full clearance"). In that pre-state, K.α fires its **subsequent-emission** branch (`a_0 = inc(a_prev, 0)`), not first-emission — because the branch keys on `dom(C)`, not on `V_{s_C}(d)`. The Substrate Decomposition step 1 acknowledges both branches generically, but the only empty-document example stipulates away the very sub-case where empty-V and empty-content-for-`d` diverge, and no prose states that the empty-V precondition admits the subsequent-emission branch with `m_C` re-pinning. Standards require a concrete example for non-trivial cases; the post-clearance re-insertion is the non-trivial one and is unillustrated.

**Required**: Add a concrete example (or an explicit note) for the empty-`V_{s_C}(d)`-but-residual-content sub-case: confirm K.α's subsequent-emission branch, `m_C := #p` re-pinning that may differ from the cleared depth, and that the invariant discharges (D-SEQ★, S8★, INS.chain-shift over the continued chain) go through.

### Issue 2: Downstream-consumer pointer in the composite-boundary premise (anti-bloat)

**ASN-0100, INS.pre (Composite-boundary premise)**: "These hold only at composite boundaries, not at arbitrary elementary-reachable states; carrying the premise makes pre-state P4★/P4a/P7a available to the post-state discharges of those same properties (§Provenance)."

**Problem**: The middle clause enumerates where the premise is consumed (`§Provenance`) rather than advancing what the premise states — the flagged "definition's introduction enumerates downstream consumers" pattern, freshly accreted (per the recent `add composite-boundary premise` revision). The non-vacuity sentence and the "Σ' is again a composite boundary" sentence are substantive and should stay.

**Required**: Keep the premise statement and its non-vacuity ("hold only at composite boundaries"); drop the use-site pointer to §Provenance.

## OUT_OF_SCOPE

### Topic 1: Link-subspace insertion (K.μ⁺_L)
**Why out of scope**: The ASN correctly bounds itself to the content subspace and defers link-subspace insertion to a future ASN (Open Questions, Bounding the Scope). No claims are defined for it — no action needed.

The "INSERT vs. COPY" section uses COPY only as a contrast to fix INSERT's identity character; it defines no COPY claims (INS.identity* are INSERT properties), so it is not an OUT_OF_SCOPE violation — though the contrast prose could be tightened.

VERDICT: REVISE
