# Review of ASN-0118

This is a meticulous specification. The transclusion frame (CP1), the displacement tiling, the three-way provenance split in CP8, the self-transclusion and non-contiguous-assembly cases, the worked example, and the non-trivial wp for link discoverability are all rigorously handled. The removal of the ordinal-level requirement is sound: the operation genuinely routes around `actionPoint(ℓ)`, grounding resolution in S3★ over the bound subset and C1a's general (single-subspace) form rather than C0a. I found one completeness gap.

## REVISE

### Issue 1: S8-depth not discharged for the placement (gap-fill) positions
**ASN-0118, displacing-case composite and tiling**: "These placement positions `{p + i : 0 ≤ i < W}` are well-formed by S8a-validity of `p` and OrdShiftHom(b) ... with `p + 0 = p` S8a-valid directly."

**Problem**: The ASN is careful to note that ASN-0082's I3-VP/I3-VD cover only the *shifted* trailing content, and it explicitly patches **S8a** for the gap-fill placement positions via OrdShiftHom(b). But it never discharges the symmetric obligation for the *S8-depth* invariant on those same positions. S8-depth (every `s_C` V-position of `d` shares the common depth `m_{s_C}(d)`) is a per-state invariant COPY must preserve, and the placement positions are freshly introduced `s_C` positions whose depth is asserted nowhere. The tiling argument tacitly treats every position as depth-`m` (it reasons purely about last-component ordinals), so depth-uniformity of the placement positions is in fact *load-bearing* for D-CTG★/D-SEQ as well, not merely S8a — yet it is left implicit. Given that the ASN explicitly carves out and patches S8a for exactly these gap-fill positions, the omission of the analogous S8-depth step is an asymmetric gap, not a harmless elision.

**Required**: Add the one-line discharge: `p` is a valid insertion position, so `#p = m_{s_C}(d)` (ValidInsertionPosition postcondition (a); ValidFirstInsertionPosition (a) in the empty case), and `#(p + i) = #shift(p, i) = #p = m`, so every placement position carries the subspace common depth — preserving S8-depth (establishing it, in the empty case) for the gap-fill exactly as OrdShiftHom(b) preserves S8a. State this for all three branches (empty, append, displacing).

## OUT_OF_SCOPE

### Topic 1: Nominal-extent vs. placed-width relationship under partial binding (C2 loss)
**Why out of scope**: COPY's claims remain consistent under partial binding (it places and shifts by the actual `W`); the unanswered design question of what to guarantee about the nominal/actual divergence is genuinely new territory, correctly logged as an open question rather than an error here.

### Topic 2: Ordering under repeated/overlapping source spans; cross-depth assembly; link undiscoverability after later removal; correspondence relation; link-subspace transclusion
**Why out of scope**: All five are future-ASN territory, and the ASN files them as open questions without making false claims about them.

VERDICT: REVISE
