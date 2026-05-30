# Review of ASN-0042

## REVISE

### Issue 1: B1 / hwm / next / B_fin preconditions never discharged on `Σ.B`

**ASN-0042, O10 (Non-coverage analysis)**: "By B1 (ContiguousPrefix), `children(Σ.B, pfx(π), 2) = {pfx(π).0.k : 1 ≤ k ≤ hwm_0}`" — and earlier "`hwm_0 := hwm(Σ.B, pfx(π), 2)`", "`a' = next(Σ.B, pfx(π), 2)`".

**Problem**: The ASN imports ASN-0040's B10 explicitly and carefully (O17: "imported as a load-bearing fact of the ownership model"), but it then invokes B1, `hwm`, `next`, and `B_fin` on `Σ.B` without the analogous justification. Those foundation results are invariants/operations over ASN-0040-*reachable* registries (states reached by `Bop`). The ownership transition relation `→` includes delegation (O18), allocation (O5/O16), and "every other op" — and nothing in the ASN establishes that an ownership-reachable `Σ.B` is an ASN-0040-reachable registry. `hwm`'s own contract requires "B satisfies B1 for (p, d)"; `next` requires "B ⊆ T finite (discharged by B_fin when B = s.B for a reachable s)". Both preconditions are simply assumed. The O10 construction (hence Unilateral O10★) rests on B1 giving the exact `children` set, so this is load-bearing, not cosmetic.

**Required**: Either state a coupling axiom — every ownership transition that modifies `Σ.B` does so by an ASN-0040 baptism, so B0, B1, B10, and B_fin transfer to every ownership-reachable state — or discharge B1/B_fin/`hwm`/`next` preconditions at each use site (notably O10), matching the rigor already applied to B10 in O17.

### Issue 2: Triplicated "forevermore" / parental-sovereignty argument

**ASN-0042, Permanence and Refinement intro; OwnershipDomainPermanence prose; O10 closing prose**: the Nelson "once assigned a User account... full control over its subdivision forevermore" quote and the "parent controls baptism, child controls content, parent cannot regain it" point are developed three times across three sections.

**Problem**: This is the named anti-bloat pattern "two paragraphs say the same thing in different words." The formal content is carried by O3 (refinement-only) and O8 (irrevocability); the repeated narrative gloss in OwnershipDomainPermanence and again at the end of O10 restates it without advancing the argument.

**Required**: State the design intent once (at O3/O8), and let OwnershipDomainPermanence and O10 cite the property rather than re-prosecute the "forevermore" reading.

### Issue 3: "Principal Identity and the Trust Boundary" is essay content in a structural slot

**ASN-0042, Principal Identity and the Trust Boundary**: "This is not a deficiency in the ownership *model* — it is a gap in the ownership *enforcement*... O1 through O10 hold regardless of how principal identity is established (the binding is treated in the *Summary of the Model*)."

**Problem**: The section defines no claim and advances no property. Its one substantive assertion — that O1–O10 are independent of the identity-binding mechanism — is restated verbatim in the Summary ("Principal identity... is exogenous to this model"). It is meta-prose that the reader must skip to follow the formal chain, with a forward pointer to the Summary that itself repeats the point.

**Required**: Delete the section and keep the single exogeneity sentence in the Summary, or fold its content there. Concrete authentication is already OUT OF SCOPE per the Scope block.

### Issue 4: Forward-reference deferral prose

**ASN-0042, Subdivision Authority corollary; O10 Field-opening boundary case**: "...the effective-owner outcome at the baptized prefix is `π'`... and that case is captured by O7(a) rather than this corollary." / "...are the `hwm_0 = 0` case of the O10 *Construction*, *B6 verification*, and *Non-coverage analysis*, discharged there in full generality; no re-derivation is repeated here."

**Problem**: Both are use-site deferrals ("captured by X rather than here," "discharged there... not repeated here") of the kind the anti-bloat classifier flags. The first sub-paragraph exists only to say the corollary does *not* cover delegation; the second narrates where an argument lives rather than making one.

**Required**: Drop the corollary's "introducing transitions" sub-paragraph (its scope is already fixed by the hypothesis `Π_{Σ'} = Π_Σ`). In the field-opening case, exhibit the one branch-specific value (`inc([1,0,2,3],2) = [1,0,2,3,0,1]`, `hwm = 0`) and cite O10, without the "discharged there in full generality / no re-derivation repeated" narration.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer and provenance/owner divergence
**Why out of scope**: Raised correctly as an Open Question. The system as specified has no transfer mechanism (O3 describes refinement-only); the invariants relating O6 provenance to O2 effective owner under transfer are new territory, not a defect here.

META: not needed — the ASN remains squarely on system-guarantee territory (an ownership predicate, an effective-owner function, and their invariants), stated abstractly enough to bind any conforming implementation.

VERDICT: REVISE
