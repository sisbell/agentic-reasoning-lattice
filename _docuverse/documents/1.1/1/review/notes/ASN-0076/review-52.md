# Review of ASN-0076

I checked the two-step composite construction, the precondition discharges in E0, and the proofs of E1–E11 including the wp computation in E11 and the F-structure vacuity argument for the `ℓ_new` disjunct. The mathematics holds: the K.λ precondition discharges are complete at both steps, the freshness/distinctness arguments in E0/E2 are sound, the LP12-based wp in E11 is exact, and the middle-disjunct collapse is correctly justified through LP-Sub + T3. Boundary cases (empty arrangement → orphaning via LP17, `d_new = home(ℓ_old)`, `k=0` base of E5) are handled. No technical gap rises to REVISE.

The findings below are anti-bloat items, which this note's `review-mode.anti-bloat` classifier directs me to surface.

## REVISE

### Issue 1: Redundant summary sentence in the introduction
**ASN-0076, Introduction (consultation-evidence paragraph)**: "Gregory's analysis of udanax-green confirms the same absence at the implementation level: link orgls carry no 'supersedes' field, the spanfilade is append-only... Both authorities arrive independently at the same architectural commitment: there is no operation that mutates an existing link."
**Problem**: The closing sentence ("Both authorities arrive independently at the same architectural commitment: there is no operation that mutates an existing link") restates, in synthesis form, the two preceding sentences that already establish Nelson's and Gregory's independent confirmations of the same absence. The word "independently" is the only added content, and it is already implied by attributing the two observations to two distinct authorities. This is meta-prose summarizing claims the reader has just read.
**Required**: Delete the summary sentence; the two evidence sentences already carry the point.

### Issue 2: Worked example re-derives E0's depth-bound argument rather than instantiating-and-citing
**ASN-0076, A Worked Example, Step 2**: "The element-field depth bound `#E(ℓ_sup) = 2` follows directly: TA5(b) confines the modification to position 8 only ... hence `zeros(ℓ_sup) = zeros(ℓ_new) = 3` ... `#E(ℓ_sup) = 8 - 6 = 2`."
**Problem**: This paragraph re-runs the same TA5(b)/TA5(c)/TA5-SigValid structural argument that E0 already proves abstractly for every `A_L(d_new)` emission. A worked example's job is to instantiate key postconditions on concrete values, not to reproduce an upstream proof on those values. The two passages say the same thing in different words (one abstract, one with positions plugged in).
**Required**: Replace with a citation — e.g., "by E0's depth-bound argument, `#E(ℓ_sup) = #E(ℓ_new) = 2`" — retaining only the concrete values (`ℓ_sup = [4.0.2.0.3.0.2.2]`, zeros at 2/4/6) that the example genuinely contributes.

## OUT_OF_SCOPE

### Topic 1: Supersession-chain invariants, cycle detection, and "current successor" computation
**Why out of scope**: These are correctly deferred to future ASNs in the Open Questions section; the note defines the EDITLINK composite and its single-edit guarantees, which is the right scope boundary.

### Topic 2: Authorization of `d_new` relative to `home(ℓ_old)`
**Why out of scope**: E6's application-layer note appropriately defers executor/capability questions to a future authorization ASN; the link model has no executor field, so this is genuinely new territory rather than a gap in EDITLINK.

VERDICT: REVISE
