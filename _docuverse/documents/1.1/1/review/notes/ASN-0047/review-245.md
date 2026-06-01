# Review of ASN-0047

I checked the elementary transition definitions, the K.μ⁻ contraction equivalence, the K.μ~ decomposition (Steps A–D, necessity/sufficiency), the D-SEQ★ derivation, the cross-layer derivations, and the verification matrices. The object-level proofs I traced hold up. The findings below are the prose-accretion patterns flagged by the active `review-mode.anti-bloat` classifier — duplicated arguments with cross-deferral and use-site inventory in structural slots.

## REVISE

### Issue 1: Full-clearance form stated twice, with the second occurrence deferring to the first

**ASN-0047, *Decomposition of K.μ~*** and **ASN-0047, *Necessity and sufficiency of the precondition***: The first site states "**Full-clearance form (canonical statement).** K.μ⁻ clears the entire content subspace — content-only removal — while retaining every link-subspace position, and K.μ⁺ rebuilds the content subspace at fresh positions... it is the realisation invoked wherever a K.μ~ argument needs to realise an arbitrary admissible π." The second site (*Decomposition*) restates the same construction — "K.μ⁻ removes V_{s_C}(d) entirely... and K.μ⁺ then adds..." — then adds "the full-clearance form whose canonical statement and no-per-π-check property are given in §*Necessity and sufficiency of the precondition* above. It is the form invoked by every K.μ~ verification argument below."

**Problem**: The same construction is described in two sections, and the second both re-describes it and points back to the first. This is the duplication + cross-deferral pattern the anti-bloat note names ("two paragraphs in the same document say the same thing in different words"; "multiple paragraphs defer to the same downstream location"). The clause "It is the form invoked by every K.μ~ verification argument below, which therefore needs to name no cut point" is a use-site inventory rather than a step in the argument.

**Required**: State the full-clearance form once (in *Decomposition*, where K.μ~'s realisation belongs), and have the *Necessity and sufficiency* sufficiency construction cite it by name without re-describing it. Drop the "invoked by every verification argument below" inventory sentence.

### Issue 2: The "other cut points" parenthetical describes a realisation the ASN never uses

**ASN-0047, *Decomposition of K.μ~***: "(Other cut points `n'_{s_C} = k₀ − 1` with `1 ≤ k₀ ≤ n_{s_C}` realise π when π preserves M(d)-values below the cut, but the verification arguments use only the always-available full-clearance form.)"

**Problem**: This introduces an alternative decomposition only to state that it is never used. It does not advance any claim — it is essay content about what the document chooses not to do. (The single exception, *Worked example: interior content replacement*, reuses the cut-point *notation* for a distinct range-changing composite, not for K.μ~, so the parenthetical's K.μ~ use-case is genuinely vacant.)

**Required**: Remove the parenthetical. If the cut-point notation is needed by the interior-replacement worked example, introduce it there.

### Issue 3: The "unscoped P4 unsatisfiability" argument is given twice with a cross-deferral

**ASN-0047, *Coupling and isolation* (P4 box)** and **ASN-0047, *Scoped coupling constraints* (opening)**: The P4 box derives that the unscoped bound is unsatisfiable — "Since `ℓ ∈ dom(L)` and `dom(L) ∩ dom(C) = ∅` (L14), `(ℓ, d) ∉ R` — P4 is unsatisfiable for the unscoped relation once any link-subspace mapping exists" — and closes "We retain the P4 label only to name the unscoped bound that P4★ below refines." The *Scoped coupling constraints* opening repeats the conclusion — "an unscoped coupling and P7 are mutually unsatisfiable once any link-subspace mapping exists, by the same L14/P7 disjointness argument that makes the unscoped P4 unsatisfiable (see *Definition (Current containment)* above)."

**Problem**: The same L14/P7 unsatisfiability argument is stated in two sections, the second explicitly deferring back ("see ... above"). P4 is introduced solely to be refuted and renamed, and the "We retain the P4 label only to name..." sentence is meta-prose justifying why a discarded property is kept around. This matches the "introduce a claim only to refute it" and "defer to the same location" patterns.

**Required**: Make the unsatisfiability argument once. Either state P4★ directly with a one-line note that an unscoped bound fails under L14/P7, or keep the P4 box and have the *Scoped coupling* opening reference it without restating the conclusion. Remove the label-retention justification sentence.

### Issue 4: "Locus of contraction" adds a derived elaboration without a new claim

**ASN-0047, K.μ⁻ amendment**: "*Locus of contraction.* A one-line consequence of the strict-contraction clause: an empty subspace admits only the trivial empty removal, so whenever exactly one of `V_{s_C}(d)`, `V_{s_L}(d)` is non-empty, that subspace is the sole locus of contraction and must shrink strictly; when both are non-empty, the strict-subset requirement may be met by contracting either or both."

**Problem**: This is labeled a "one-line consequence" and restates the strict-contraction clause's content as a case enumeration that no later argument consumes. It is elaboration in a structural slot rather than a load-bearing step.

**Required**: Remove, or fold into the strict-contraction clause as a half-sentence if a downstream argument actually relies on the single-non-empty-subspace case.

## OUT_OF_SCOPE

None. The ASN stays within state/operation/invariant territory and does not drift into named-operation specifications, authority, concurrency, or enfilade internals.

VERDICT: REVISE
