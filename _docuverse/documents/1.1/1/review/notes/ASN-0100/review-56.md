# Review of ASN-0100

## REVISE

### Issue 1: Claims table carries near-duplicate rows

**ASN-0100, Claims Introduced table**: Several rows assert the same guarantee twice in different words:
- **INS.inv.immut** ("dom(C) ⊆ dom(C') and pointwise values preserved") vs. **INS.inv.identity** ("∀a ∈ dom(C): a ∈ dom(C'), C'(a) = C(a), origin(a) unchanged") — the second restates the first plus `origin` invariance.
- **INS.frame.subspace** ("non-content subspaces of d unchanged bidirectionally") vs. **INS.inv.cross-subspace** ("V_{s_L}(d') = V_{s_L}(d) with mappings unchanged") — the latter is a strict specialisation of the former.
- **INS.frame.doc** ("∀d' ≠ d: M'(d') = M(d')") vs. **INS.inv.cross-doc** ("arrangements of all d' ≠ d unchanged") — identical content.

**Problem**: Two claim labels saying the same thing in different words is accretion noise; a reader cannot tell whether the duplicate is a distinct obligation or a restatement.
**Required**: Collapse each pair to one claim (fold `origin` invariance into INS.inv.immut; drop INS.inv.cross-subspace and INS.inv.cross-doc, or cite them as corollaries of the frame rows rather than separate claims).

### Issue 2: Statement column of the claims table embeds full proofs

**ASN-0100, Claims Introduced table**: The Statement cell for **INS.chain-shift** reproduces the entire derivation ("Each inc(·,0) step equals shift(·,1) because chain elements are T4-valid (ChainElementT4Validity, ASN-0093), so sig = # (TA5-SigValid)… and composes by TS3"). **INS.M-shift**, **INS.inv.func**, and **INS.proj** likewise carry their justification chains.
**Problem**: The proofs already live in the body (§Effect One, §Arrangement functionality, §Coverage and link discoverability). A status table that re-derives is essay content in a structural slot — the same text in two places.
**Required**: Reduce each Statement to the claim itself; leave the derivation in the body where it is already given.

### Issue 3: Forward-looking aside in a claims-table entry

**ASN-0100, Claims Introduced table, INS.inv.depth**: "A later K.μ⁻ emptying V_{s_C}(d) makes S8-depth vacuous and permits a different depth on the next first-insertion."
**Problem**: This describes the effect of a *future* K.μ⁻ + later INSERT sequence, not INSERT's own invariant preservation. It is editorial speculation about downstream operations in the slot reserved for stating this operation's claim.
**Required**: Remove the trailing sentence; INS.inv.depth's claim is the depth-preservation behaviour of this operation only.

### Issue 4: Multiple sections defer to the same downstream derivation

**ASN-0100, §Effect Two and §Atomicity (step 3, Insertion positions)**: Effect Two says the S8a/S8-depth derivation for `shift(p, k)` "is carried in §Post-state V-position well-formedness (the canonical site)"; §Atomicity then again defers `shift(p, k)`'s S8a/S8-depth "by the canonical derivation in §Post-state V-position well-formedness."
**Problem**: Two separate sections forward-point to the same single location for the same fact — the cross-cycle deferral-accretion pattern. The reader chases the same pointer twice.
**Required**: State the well-formedness derivation once and have the dependent sections cite the claim labels (INS.inv.depth, S8a) directly, rather than narrating a deferral to a "canonical site."

## OUT_OF_SCOPE

### Topic 1: Recovery of canonical order after partial failure mid-composite
**Why out of scope**: The first Open Question rightly defers this to implementation-realisation territory; it is not an INSERT post-state obligation.

### Topic 2: Link-subspace insertion (K.μ⁺_L) semantics
**Why out of scope**: The ASN explicitly bounds itself to the content subspace; link-subspace insertion is a structurally distinct operation, correctly deferred.

VERDICT: REVISE
