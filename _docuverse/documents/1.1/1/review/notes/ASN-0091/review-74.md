# Review of ASN-0091

## REVISE

### Issue 1: Collapse case of the net-effect split is asserted but never exhibited

**ASN-0091, "REARRANGE_K Realises the Abstract Class" (Net-effect split)**: "when the affected range carries a repeating I-address pattern whose period matches the permutation's displacement, foundation S5 (UnrestrictedSharing) admits an arrangement on which R-P1/R-P2 yield `M'(d) = M(d)` although π is the non-identity rotation."

**Problem**: This is the one distinguished branch of the realisation where the realiser fundamentally changes — from the K.μ~ composite to the *empty* sequence with `Σ' = Σ`. Yet it is the only substantive scenario the ASN never instantiates: four worked examples (WE1–WE4) plus the coalescence and equality witnesses cover fragmentation, swap, interior cuts, non-uniqueness, and every run-cardinality direction, but none exhibits a non-identity REARRANGE_K invocation that yields `Σ' = Σ`. The existence claim rests entirely on an unexhibited appeal. Per the depth/concrete-example standard, a branch this load-bearing (it determines which realiser discharges RA-adm) needs a witness — e.g., `Σ.M(d)` constant `= a` on the affected range, where R-P1/R-P2 reproduce `a` everywhere and π is the non-identity pivot, verified against R-PRE and RA-adm.

**Required**: A concrete collapse-case trace, showing R-P1/R-P2 reproduce `M(d)` and confirming the empty-sequence realiser delivers `Σ' = Σ`.

### Issue 2: Loose citation of S5 for the collapse case

**ASN-0091, same paragraph; and the parenthetical** "(S5/UnrestrictedSharing holds at Σ' as a state-independent theorem of the model class.)"

**Problem**: S5 (UnrestrictedSharing) is an *existential* statement over the model class — "there exists a state with multiplicity > N" — not a per-state fact about a given `Σ`, and not the property actually needed. What the collapse argument requires is merely that the arrangement at hand *may* repeat an I-address across V-positions (permitted because S2 imposes only functionality, never single-image). Citing S5's unbounded-multiplicity theorem to license "an arrangement on which the pivot is net-zero" overreaches the lemma. The parenthetical "S5 ... holds at Σ'" compounds this by treating an existential model-class theorem as a per-state predicate.

**Required**: Justify the collapse case from the absence of a single-image constraint (S2 functionality permits shared images), and either drop the "S5 holds at Σ'" parenthetical or restate it as "S5 is not a per-state invariant, so RA-adm does not range over it."

## OUT_OF_SCOPE

### Topic 1: Whether fragmented transclusion pieces jointly reconstitute the source span
**Why out of scope**: The ASN correctly notes (RE-trans discussion) that it establishes only per-piece origin preservation, not joint reconstitution, and defers this to an Open Question. That is the right boundary; the reconstitution semantics belong in a future note.

### Topic 2: Link-subspace rearrangement semantics
**Why out of scope**: REARRANGE_K fixes the cut subspace at `s_C` (CS3); rearrangement *within* the link subspace is correctly left to a future ASN (listed in Open Questions).

VERDICT: REVISE
