# Review of ASN-0042

## REVISE

### Issue 1: Delegation condition (v) is redundant with the O17b coupling
**ASN-0042, O15 / O17b**: condition (v) requires `pfx(π') = next(Σ.B, p, d) = c_{hwm(Σ.B,p,d)+1}`; O17b's sharpening states "every transition that admits a new principal `π'` ... `Σ'.B = Σ.B ∪ {pfx(π')}`."
**Problem**: O17b's principal-introduction clause already forces the baptism branch, whose general form is `Σ'.B = Σ.B ∪ {next(Σ.B, p, d)}`. Composing the two pins `pfx(π') = next(Σ.B, p, d)` — exactly condition (v). So (v) and O17b independently determine the same fact; one is redundant over-determination of the admission gate. Moreover, no ownership theorem (O1a, O1b, O2, O3, O8, NestingByDelegation) consumes the full next-reachability form — every use routes through *Freshness-(v)*, which extracts only `T4(pfx(π'))` and `pfx(π') ∉ Σ.B`. The hwm/`next` machinery is therefore imported into the ownership model without ownership-level necessity.
**Required**: Either weaken (v) to `T4(pfx(π')) ∧ pfx(π') ∉ Σ.B` and let O17b supply the baptism-stream form, or derive (v) from O17b rather than positing both. State explicitly which of the two is primitive.

### Issue 2: O17 imports B10 without the reachability that licenses it
**ASN-0042, O17 (AllocatedAddressValidity)**: "This is ASN-0040's B10 (T4ValidityInvariant), imported as a load-bearing fact ... every address in `Σ.B` satisfies T4."
**Problem**: B10 is an invariant over *ASN-0040-reachable* registries. Applying it to the ownership registry `Σ.B` requires that `Σ.B` be such a registry — precisely RegistryReachability, which is derived separately and not cited here. The one-line "imported" derivation skips the licensing step. O17 is load-bearing for AccountPrefix, O6, and O9, so the gap propagates.
**Required**: Have O17 invoke RegistryReachability (no circularity — RegistryReachability's derivation does not use O17) before importing B10.

### Issue 3: The O1a/O1b/T4 shared induction cannot be checked in reading order
**ASN-0042, "The Account-Level Boundary" and O1b**: O1b is stated in *Ownership as a Structural Predicate* with "It is established by the shared induction in *The Account-Level Boundary*," and that induction's non-delegation/delegation steps cite O12, O13, O14, O15, *Freshness-(v)*, and delegation conditions (i)–(iii) — all defined two sections later in *State Axioms*.
**Problem**: This is the forward-reference accretion the note flags: a proof deferred forward, then discharged with premises defined still further forward. The reader must resolve a chain of forward dependencies to verify the base/step cases.
**Required**: Either relocate the shared induction after the state axioms it depends on, or hoist the axioms (O12–O15, O14) ahead of the first invariant proof so the induction reads in dependency order.

### Issue 4: Essay/meta-prose in structural slots
**ASN-0042, O14**: "The formalization permits both cases: the existential quantifier ranges over all of `Π₀`, not a single distinguished element."
**ASN-0042, O7(c)**: the postcondition body grants "`π'` may delegate a sub-prefix `p''` with `pfx(π') ≺ p''`," with the actual restriction (next-reachable single-step extension only) deferred to obligation (v) and the Formal Contract.
**Problem**: The O14 sentence is commentary on the formalization rather than an axiom clause. The O7(c) body overstates the right and forces the reader to reconcile it against (v) downstream.
**Required**: Drop the O14 meta-sentence (the multi-node clause-check already carries the content). State O7(c)'s restriction inline ("a next-reachable first child `p''`") rather than as a generality later narrowed.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer and provenance/effective-owner divergence
**Why out of scope**: The system as specified has no transfer mechanism (O3 confirms refinement-only); the divergence between O6 provenance and O2 effective owner under transfer is correctly deferred to the Open Questions, not an error here.

VERDICT: REVISE
