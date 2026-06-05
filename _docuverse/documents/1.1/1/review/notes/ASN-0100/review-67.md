# Review of ASN-0100

## REVISE

### Issue 1: Worked example cites INS.proj instead of computing the projection directly

**ASN-0100, §A Worked Example (interior, "Projection-shift correspondence")**: "We now read the post-state projection off INS.proj rather than re-tracing the composite."

**Problem**: INS.proj is stated and proven later, in §Verifying the Invariants → Coverage and link discoverability. The worked example precedes that section, so it consumes a not-yet-established claim. Worse, a worked example is supposed to be *evidence* for the claims, not a citation of them. The result `{[1,2],[1,5],[1,6]}` is directly computable from the exhibited post-state: `coverage(e_1) ∩ ran(M'(d)) = {a₂,a₃,a₄}`, and the V-positions of `M'(d)` mapping to those are `[1,2]↦a₂, [1,5]↦a₃, [1,6]↦a₄`. Reading it "off INS.proj rather than re-tracing the composite" makes the example circular (it leans on the claim it ought to corroborate) and forward-referential.

**Required**: Compute the post-state projection directly from `M'(d)` and `coverage(e_1) ∩ ran(M'(d))` in the example, reserving INS.proj for §Coverage. The example should verify INS.proj, not assume it.

### Issue 2: e_1's tightness construction is not load-bearing for the example's conclusion

**ASN-0100, §A Worked Example (interior)**: A full paragraph constructs `Σ_{e_1}`, discharges the three tightness conditions, concludes `tight(e_1, Σ_{e_1})`, and invokes LP19a to obtain `N_I = ∅`. The very next paragraph ("Non-tight alternative") then states: "For the tight e_1 above, `N_I = ∅` holds for a structural reason that outlives tightness... both lie strictly above coverage(e_1)'s ceiling `a_5 = [d.0.s_C.5]` under T1 (last components 6, 7 > 5), regardless of any tightness assumption."

**Problem**: The text concedes that for `e_1` the conclusion `N_I = ∅` follows from chain-frontier ordering alone (`a_{new}` last components 6,7 > 5), so the elaborate tightness/LP19a apparatus built around `e_1` does not advance the example's reasoning. The tightness mechanism is genuinely needed only to *contrast* with the non-tight `e_1'` (where `N_I ≠ ∅`); attaching the full tightness derivation to `e_1` — whose numbers make it moot — is accretion that the precise reader must work past.

**Required**: Drop or radically shorten the `e_1` tightness derivation; demonstrate the tight/non-tight distinction through the `e_1` (structural `N_I=∅`) vs. `e_1'` (`N_I≠∅`) pair, invoking LP19a/tightness only where it is actually decisive.

## OUT_OF_SCOPE

(none — INS.identity.version concerns INSERT's allocation behavior when the target is a version document, not version creation, so it stays in scope.)

VERDICT: REVISE
