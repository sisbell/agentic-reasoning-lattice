# Review of ASN-0131

I worked through every claim in the table against its supporting prose and the foundation contracts. The core mathematics is sound: RE-DEF factors cleanly through `Avail(Σ)` (so `RE = {(i,e) ∈ Avail(Σ) : touch_W(e)}`, the key step that makes union-distributivity and the wp derivations go through); RE-ADDR's antichain argument is correct; the worked instance genuinely exercises RE-OVL/RE-CLIP/RE-WHOLE/RE-UNIT; the intersection counterexample (RE-UDIST-∩) is a real refutation, not an assertion; RE-CWP's `Δ`-condition is equivalent to the full "nothing dropped" condition; and the RE-RET iff is correctly split (forward needs the type hypothesis, backward rests on R-Scope alone). I found one genuine over-claim and one accretion pattern.

## REVISE

### Issue 1: "settled, not assumed" overstates the insert/delete M-only lift

**ASN-0131, "Stability… Under editing of the queried document"**: "And this is *settled*, not assumed. ASN-0082 models these primitives over a `(C, M)` state… and proves they write only `Σ.M(d)` and frame `Σ.C` (I3-C, D-I)… so the unique lift to the full state writes `Σ.M(d)` and frames `L`, `E`, `R` — there is nothing else for such a lift to write."

**Problem**: ASN-0082 establishes the M-only property *over its 2-store `(C, M)` model*. It cannot prove anything about `Σ.L`, `Σ.E`, `Σ.R` — those stores do not exist there. A `(C, M)`-primitive's behavior on the three added stores is therefore *unconstrained* by its `(C, M)`-spec, so "frame `L, E, R`" is a stipulation (the conservative lift), not a derivation. "The unique lift… there is nothing else for such a lift to write" smuggles in exactly this choice, and "settled, not assumed" then misreports a modeling assumption as a theorem. RE-EDIT's stability-under-insert/delete is the claim a downstream consumer would build on, so the distinction matters: a builder reading "settled" would not know an assumption is in play. The companion claim — that the bare shift's I3-V vacancy is "a non-queryable intermediate of the *non-atomic* full edit" — rests on the same informal footing (that the gap state is not a reachable query point), since ASN-0082's I3 is a standalone postcondition family, not an ASN-0047 elementary transition guaranteed to land in a D-CTG★-satisfying state.

**Required**: Either (a) state the conservative-lift framing explicitly as a modeling assumption ("we treat shift-based insert/delete as edits touching no store but `Σ.M(d)`"), dropping "settled, not assumed"; or (b) realize insert/delete as ASN-0047 composites, where the M-only property *is* settled by the K.μ frame conditions, and scope out the cases ASN-0047's frontier-only K.μ⁺/K.μ⁻ cannot express. The core RE-EDIT result over ASN-0047's own vocabulary is rigorous and does not depend on this passage, so deferral costs nothing.

### Issue 2 (anti-bloat): cross-foundation reconciliation re-derived at use sites

**ASN-0131, "Under retraction"**: "(R-Scope SingleTupleScope, ASN-0086, arity-independent — carried to this ASN-0047 state by the `Σ.L`-evolution bridge, R-Scope's `d_retr ∈ dom(Σ.M)` hypothesis meaningful here because `dom(Σ.M) = E_doc` (M1, ASN-0047) is the same ASN-0093 document substrate ASN-0086 names)."

**Problem**: The `Σ.L`-evolution bridge is established once up front ("every ASN-0086 lemma whose conclusion constrains `Σ.L` or `nullified` holds at every ASN-0047-reachable state"). This parenthetical re-confirms the substrate identity ("the same ASN-0093 document substrate ASN-0086 names") that the bridge already covers. It is paired with two other defensive asides that the precise reader must traverse — "And this is *settled*, not assumed" (Issue 1) and "settles this for an output of *any* arity, with **no appeal to triple structure**" in the RE-ADDR derivation. These are the justification-accretion the review mode targets: prose defending the validity of a cross-foundation transfer rather than advancing the argument. The bridge itself is load-bearing and should stay; its re-application is what has accreted.

**Required**: Establish the bridge once, then cite it tersely at use sites (e.g. "R-Scope, arity-independent, via the `Σ.L`-evolution bridge"); drop the inline substrate re-confirmation and the "settled"/"no appeal to triple structure" asides.

## OUT_OF_SCOPE

(none — the note correctly *cites* ASN-0127's image machinery and existence/discovery taxonomy rather than rebuilding them, contrasts the excluded operations by name only, and defers genuinely new territory to Open Questions 1–7 rather than claiming it.)

VERDICT: REVISE
