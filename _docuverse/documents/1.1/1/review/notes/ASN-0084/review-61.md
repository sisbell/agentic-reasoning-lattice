# Review of ASN-0084

## REVISE

### Issue 1: Dangling reference to a non-existent "Scope note"
**ASN-0084, R-BLK, Phase 2 (Classify)**: "non-S runs are entirely contained in their subspace by OrdShiftHom (a) of ASN-0036 *as cited in the Scope note*."
**Problem**: There is no paragraph or sub-label named "Scope note" anywhere in this ASN. The fact being invoked is actually the *V-extent confinement* clause of R-NS(NS-run). The cross-reference is broken — a reader cannot follow it. (This appears to be residue from a removed sub-paragraph; the prior-cycle declined-findings list itself refers to an "R-BLK Scope note" that no longer exists.)
**Required**: Replace "as cited in the Scope note" with the actual carrier — "by R-NS(NS-run), *V-extent confinement*" — or delete the parenthetical, since OrdShiftHom (a) is self-sufficient.

### Issue 2: The "post-state S8 follows from foundation S8" claim is stated four times
**ASN-0084, Invariant preservation ("Foundation-S8 transport"), R-SP statement, R-SP proof (S8 paragraph), and R-SP table row**: e.g. "post-state S8 ... follows from foundation S8 (ASN-0036), whose preconditions ... are all preserved above ... none of them references the pre-state partition," restated nearly verbatim in R-SP ("No designated pre-state partition is required; post-state S8 follows from foundation S8") and again in the table.
**Problem**: Four paragraphs in different sections assert the identical claim in different words — the precise reader must verify they are the same statement, not a refinement. This is the duplication pattern the anti-bloat classifier flags.
**Required**: State it once (in Invariant preservation) and have R-SP and the table point to it without re-deriving.

### Issue 3: R-SP largely re-walks the "Invariant preservation" paragraph it cites
**ASN-0084, R-SP proof**: "Every clause of Q except S8 ... is therefore discharged generically by the *Invariant preservation* paragraph above," followed by a re-enumeration (C-transport, bijectivity for S2, R-RI for S3, multiset preservation for S5, dom-equality for the D-* family).
**Problem**: The proof's body restates the mechanism already given in Invariant preservation, adding nothing but the S8 step. The lemma's only new content is the S8 discharge; the rest is a second copy of an earlier list.
**Required**: Collapse R-SP's body to the S8 step plus a single pointer; do not re-enumerate per-invariant mechanisms.

### Issue 4: R-NS(NS-run) "Phases 2 and 3" duplicates R-BLK's non-S handling
**ASN-0084, R-NS proof (NS-run), "Phases 2 and 3"**: "Phase 2 classifies b into the dedicated non-S region ... Phase 3 applies displacement zero to non-S runs ... The resulting B' contains the triple (v_b, a_b, n_b) unchanged."
**Problem**: This restates R-BLK Phase 3's non-S bullet, which in turn cites back to R-NS(NS-run) ("as also recorded by R-NS(NS-run)"). The two passages describe the same mechanism with mutual deferral, so the reader bounces between them without either being authoritative.
**Required**: Let R-NS(NS-run) state the verbatim-carry result; have R-BLK Phase 3's non-S bullet cite it once without re-describing the phases.

### Issue 5: Disclaimer meta-prose about claim posture
**ASN-0084, R-CS3 statement and R-SP table**: "This is the one necessity result we retain; we make no claim of exhaustiveness for the other conjuncts"; "(sufficiency only; necessity not claimed)".
**Problem**: These sentences describe what the ASN does *not* assert rather than advancing any argument — essay-style scope hedging in structural slots. The lemma statements (R-CS3 proves CS3 necessity; R-SP proves sufficiency) already carry their own scope.
**Required**: Remove the disclaimers; the lemma names and postconditions already delimit what is claimed.

### Issue 6: Cancellation citation does not cover the zero shift amount
**ASN-0084, "Identification of singleton tumblers with natural numbers"**: "`c + a = c + b ⟹ a = b` by TS5 (ShiftAmountMonotonicity, ASN-0034)."
**Problem**: TS5's preconditions require shift amounts `n₁ ≥ 1`, but the identified domain is extended to ℕ (including 0) by the local identity convention. For `a = 0` or `b = 0`, TS5 does not apply; injectivity there rests on TS4 (ShiftStrictIncrease) ruling out `shift(v,0) = shift(v,n)` for `n ≥ 1`. The citation omits this.
**Required**: Either restrict the cancellation statement to the positive sub-domain actually used, or add the TS4 step covering the zero case, matching the per-step citation discipline used elsewhere in the same paragraph.

## OUT_OF_SCOPE

### Topic 1: k-cut rearrangements for k > 4 and composition of rearrangements
**Why out of scope**: The ASN explicitly fixes n ∈ {3,4} (CS1) and defers generalization and composition to the Open Questions; these are new territory, not defects here.

### Topic 2: Cross-subspace and depth-m₁>2 rearrangements
**Why out of scope**: The text-subspace, depth-2 restriction is a declared scope boundary; lifting it is a separate ASN.

### Topic 3: Operational recovery of the canonical (maximal) partition from B'
**Why out of scope**: R-BLK produces a valid-but-not-maximal partition and defers the merge-reduction process to a future ASN; the existence/uniqueness of the maximal partition is correctly delegated to foundation S8.

VERDICT: REVISE
