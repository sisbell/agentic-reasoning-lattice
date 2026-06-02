# Review of ASN-0047

## REVISE

### Issue 1: CrossDocEntityDisjoint handles a case its own precondition excludes
**ASN-0047, *Allocator hierarchy under documents*, Lemma (CrossDocEntityDisjoint)**: The lemma's *Statement* is scoped to distinct parent accounts — "For documents `d₁, d₂` with `parent(d₁) = A₁`, `parent(d₂) = A₂`, and `A₁ ≠ A₂`: `d₁ ≠ d₂`." But the closing *Same-parent pairs* paragraph then reasons about the opposite configuration: "Within a single parent account, two distinct documents need not inhabit the same sub-allocator chain... Distinctness across such cross-chain same-parent pairs is discharged by SSGU... or, equivalently for the document/version pair, by T10a.6."

**Problem**: This is reviser drift — a paragraph discharging the case `A₁ = A₂` that the lemma's hypothesis `A₁ ≠ A₂` explicitly rules out. The same-parent argument is load-bearing somewhere (document-vs-version distinctness is real), but it does not belong inside a lemma stated only for distinct parents. The trailing "or, equivalently... by T10a.6" also supplies two discharge routes for one fact — pick one.

**Required**: Either widen the lemma's statement to cover all distinct-document pairs (same- and cross-parent) and update the precondition accordingly, or move the same-parent argument to wherever document/version distinctness is actually consumed (S7d's distinctness obligation) and drop it here. Remove the redundant second discharge route.

### Issue 2: K.μ~ admissibility clause (v) — defensive prose conflicts with the proof that derives it
**ASN-0047, *Decomposition of K.μ~*, "Necessity and sufficiency of the precondition"**: "(v) being the explicit fifth admissibility criterion, which K.μ~ realizes via LRP under the full-clearance form (Step (A), Case s_L), **not a property deduced from (i)+(iv)+CL-UNIQ**."

**Problem**: Step (A), Case `s_L` does in fact *derive* clause (v): "the bijection equation together with LRP gives `M(d)(π(v)) = ... = ℓ` ... CL-UNIQ at Σ ... forces `π(v) = v`." The derivation uses (iv) + CL-UNIQ + **LRP**. The preamble's disclaimer drops LRP from the list it denies deduction from, so the literal claim is true but reads as contradicting Step (A). A reader must reconstruct that LRP is the missing ingredient to reconcile the two passages. This is exactly the defensive meta-prose the reader has to skip past to follow the claim.

**Required**: Either delete the disclaimer (Step (A) already proves the relevant fact) or state plainly that LRP is the extra premise — "(v) is derived in Step (A) from (iv), CL-UNIQ, and LRP; it does not follow from (i)+(iv)+CL-UNIQ for an arbitrary π, as the link-swap transposition shows."

### Issue 3: Elementary K.μ⁺ definition pre-announces its own amendment
**ASN-0047, *Elementary transitions*, K.μ⁺ precondition**: "the K.μ⁺ amendment strengthens this to D-CTG★/D-MIN★ — contiguity and minimum-position pinned within *each* subspace `V_s(d)` rather than only the text subspace `V_1(d)` (D-CTG★/D-MIN★ are defined in *Amendments to existing transitions*)."

**Problem**: The elementary definition reaches forward into the extended-state amendment, naming symbols defined in a later section, and the same strengthening is then restated in full at *K.μ⁺ amendment (ContentSubspaceRestriction)* ("where the elementary definition required ... D-CTG and D-MIN ... the extended-state precondition requires ... D-CTG★ and D-MIN★"). This is forward-reference accretion — amendment content occupying the elementary slot and duplicated across two sections.

**Required**: Let the elementary K.μ⁺ state only the elementary (ASN-0036 D-CTG/D-MIN) precondition; confine the D-CTG★/D-MIN★ strengthening to the amendment section, which already carries it.

### Issue 4: Cross-reference housekeeping in the S3★ discharge
**ASN-0047, Class (a) verification, *S3★ ... and S3★-aux***: "The two invariants are discharged together here — the authoritative per-transition discharge for both (the *Generalized referential integrity* section states the invariants; this entry proves their preservation)."

**Problem**: The parenthetical narrates the division of labor between two document locations rather than advancing the discharge. It is bookkeeping prose of the kind that compounds across cycles.

**Required**: Drop the parenthetical; the discharge stands on its own.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link withdrawal
**Why out of scope**: K.μ⁻ models suffix-only contraction; interior withdrawal with compaction/renumbering is a distinct operation. The ASN already flags this in its Open Questions, which is the correct disposition — not a defect in the present model.

VERDICT: REVISE
