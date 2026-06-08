# Review of ASN-0111

I read the note as a specification of a pure read of a link by its own address, evaluated against the foundation invariants (L0–L14, LP12/LP13, L2/L6/L8, etc.). The core operation and RL0–RL7 are clean: the operation is honestly a `Σ.L` lookup, completeness/role-preservation/determinacy follow immediately or from cited foundations, and the single-step-vs-`→*` distinction in RL7 is handled correctly via LP13. The two gaps below are both in the orphaned-instance derivation — which the note itself bills as verifying its most subtle postcondition (RL8).

## REVISE

### Issue 1: Orphaned-instance slot-1 argument silently widens the supposition
**ASN-0111, "A worked read" / orphaned instance**: the supposition is "no document arrangement maps any V-position to *the three content I-addresses* lying within `coverage(F)`," but the slot-1 conclusion reads "by the supposition, no arrangement range reaches *any I-address in coverage(F)*, so `coverage(F) ∩ ran(Σ.M(d)) = ∅`."
**Problem**: `coverage(F)` is infinite (it contains the entire subtrees beneath the span starts, as the note itself stresses). The step from "those three are unarranged" to "`coverage(F) ∩ ran(Σ.M(d)) = ∅`" requires that the three addresses *exhaust* `coverage(F) ∩ (dom(Σ.C) ∪ dom(Σ.L))`. That exhaustiveness is asserted ("are the element-level content I-addresses lying within `coverage(F)`") but never derived, and it is the load-bearing premise of the slot-1 case.
**Required**: show the exhaustiveness — content addresses have `#E = 2` (ChainDiscipline/FirstEmission, ASN-0093), so no deeper `dom(Σ.C)` member lies in the subtrees, leaving exactly the three; and every address in `coverage(F)` has `subspace_I = s_C` while `dom(Σ.L) ⊆ s_L` (L0), so `coverage(F) ∩ dom(Σ.L) = ∅` (T7). Then `ran(Σ.M(d)) ⊆ dom(Σ.C) ∪ dom(Σ.L)` (S3★) closes the case.

### Issue 2: Orphaned-instance slot-3 "meets neither store" under-argued for the link store
**ASN-0111, orphaned instance, slot 3 (type)**: "the ghost document `[1.0.1.0.9]` hosts no content, so `coverage(Θ) ∩ dom(Σ.C) = ∅`; … `coverage(Θ)` meets neither store here, so `coverage(Θ) ∩ ran(Σ.M(d)) = ∅`."
**Problem**: only the `dom(Σ.C)` half is argued (via the ghost document). The `dom(Σ.L)` half — needed for "meets neither store" — is merely asserted. It does not follow from "hosts no content."
**Required**: supply the subspace argument: every address in `coverage(Θ) = {t : [1.0.1.0.9.0.1.1] ≼ t}` carries `subspace_I = s_C` (the start's element field begins with `1`), while every `dom(Σ.L)` address carries `s_L` (L0), so the two are disjoint by T7 — independent of whether `[1.0.1.0.9]` hosts anything.

## OUT_OF_SCOPE

None. The note correctly confines itself to direct read and defers following/searching/counting/creation to their own ASNs.

VERDICT: REVISE
