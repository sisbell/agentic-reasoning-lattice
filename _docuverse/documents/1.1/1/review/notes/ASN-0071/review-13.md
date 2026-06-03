# Review of ASN-0071

## REVISE

### Issue 1: find-predicate interaction with the link subspace is never discharged

**ASN-0071, "The operation" / F-find**: `find(Q)(Σ) := { d ∈ Σ.E_doc : ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅ }`

**Problem**: `ran(Σ.M(d))` contains both content-subspace images (in `dom(C)`) and link-subspace images (in `dom(L)`, by S3★ + CL-OWN). The ASN proves the *source* side meticulously — `iaddrs(Q)(Σ) ⊆ dom(Σ.C)` via subspace confinement — but never connects this to the *target* side to establish the operation's stated purpose ("tracks transclusion of byte content"). The intended semantic guarantee — that a document is returned because it shares *content*, never because it shares a *link* address — is left implicit. A reader cannot tell from the text why the link-subspace portion of `ran(Σ.M(d))` cannot contribute a spurious match.

**Required**: Add the one-line discharge: link-subspace entries of `ran(Σ.M(d))` lie in `dom(L)`, which is disjoint from `dom(C)` (ASN-0047 L14), and `iaddrs(Q)(Σ) ⊆ dom(C)`; therefore `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ⊆ dom(C)`, so only content sharing can satisfy the predicate. This is the dual of the source-side confinement argument and is what justifies calling the operation content-transclusion discovery.

### Issue 2: worked scenario never verifies the exclusion (negative) direction of the predicate

**ASN-0071, "A worked scenario"**: the constructed state has `Σ.E_doc ⊇ {d_A, d_B}`, and both documents reference `a₁`, so both are in `find(Q)(Σ)`. The exclusion line reads: "All other `d ∈ E_doc`: `a₁ ∉ ran(M(d))` ... so `d ∉ find(Q)(Σ)`."

**Problem**: In the state as built, the only documents are `d_A` and `d_B`, both of which match. "All other `d`" quantifies over the empty set, so the F-SOUND-style exclusion case is verified vacuously. The concrete example exercises only inclusion (F-SHARE, F-PART, F-FILT); it never demonstrates the membership predicate evaluating to *false* against a concrete arrangement. The hardest half of a biconditional membership test goes untested by the worked scenario.

**Required**: Add a third document `d_C ∈ E_doc` to the scenario with an arrangement referencing a distinct I-address `a₂ ≠ a₁` (e.g., a second K.α/K.μ⁺ under `d_C`), and show `ran(M(d_C)) ∩ {a₁} = ∅`, hence `d_C ∉ find(Q)(Σ)`. This verifies the exclusion direction against a concrete non-containing document.

## OUT_OF_SCOPE

### Topic 1: an R-based "ever-contained" historical query
The ASN cleanly separates current containment (`find`) from the permanent provenance relation `R`, and the first Open Question asks what relationship the system must guarantee between them. Defining the `R`-based historical query operation is genuinely new territory — `find` commits to currency by design, and the historical operation is a separate operation with its own completeness semantics.

### Topic 2: visibility/access-control filtering of the result
The ASN explicitly defers Nelson's private-document filtering (LM 2/59) as a policy layer overlaid on the unfiltered `find`. The filtering operation and the completeness it must preserve over the requester-visible subset belong in a future ASN; specifying them here would conflate the abstract basis with policy.

VERDICT: REVISE
