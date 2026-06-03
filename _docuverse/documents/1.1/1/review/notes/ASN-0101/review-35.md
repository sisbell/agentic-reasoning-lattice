# Review of ASN-0101

## REVISE

### Issue 1: LP-family extension catalogue claims exhaustiveness but omits LP-Sub, LP-Fin, and LP-Fin Corollary

**ASN-0101, D10 ("LP-family extension under DELETE")**: "ASN-0098's projection apparatus — both LP-Comp's per-step lemmas LP2 through LP14 and the discoverability/tightness lemmas LP16 through LP21 — carries to the DEL-extended vocabulary intact." and "LP-Comp's case-analysis, together with this catalogue of the discoverability and tightness lemmas, remains exhaustive over the extended vocabulary once the present cataloguing is taken as the DEL row."

**Problem**: ASN-0098 contains three further lemmas — LP-Sub (SubstrateContainment, `dom(Σ.C) ∪ dom(Σ.L) ⊆ F`), LP-Fin (IntervalFinitude), and LP-Fin Corollary (CanonicalIntervalCharacterisation) — that the catalogue neither enumerates nor dispatches. These are part of ASN-0098's projection apparatus (they underwrite the tightness lemmas LP12b, LP19, LP19a that the catalogue *does* address), so an explicit exhaustiveness claim that ranges only over "LP2 through LP14 and LP16 through LP21" leaves them unaccounted for. The catalogue handles the lemmas these three support (LP12b supplanted by D11; LP19/LP19a since DEL allocates nothing) but never states the status of the supporting lemmas themselves. A claim of exhaustiveness over the apparatus must either cover them or scope itself to exclude them.

**Required**: Add a catalogue row for LP-Sub, LP-Fin, and LP-Fin Corollary, noting that each is state-relative and purely tumbler-structural (LP-Sub reads off `dom(C') = dom(C)` and `dom(L') = dom(L)` via D2/D3; LP-Fin and its Corollary depend only on canonical-span structure over F, with no transition-vocabulary dependence), so each holds at any post-DEL state without requiring extension — or narrow the exhaustiveness sentence to disclaim them explicitly.

## OUT_OF_SCOPE

### Topic 1: Full historical reconstruction of arbitrary prior states
The ASN's "recoverability and historical reconstruction" section correctly defers the full versioning/backtrack mechanism to the broader transition vocabulary, treating DEL as supplying only the non-destruction substrate. This is the right boundary; the reconstruction machinery itself belongs to a future ASN.

### Topic 2: DELETE-then-INSERT round-trip recovery
The open question on whether DELETE followed by insertion at the same V-position recovers the pre-DELETE arrangement depends on INSERT mechanics, which are out of scope per the scope list. Correctly left open.

VERDICT: REVISE
