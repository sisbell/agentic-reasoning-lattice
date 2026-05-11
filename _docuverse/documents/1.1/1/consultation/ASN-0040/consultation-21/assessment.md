# Channel Assignment — ASN-0040 review-21

**Date:** 2026-05-11 09:29

## Issue 1: B₀ non-emptiness justification is inconsistent with the deferred parent prerequisite
Reason: Resolving this requires design intent on whether the system was meant to bootstrap from an empty registry or always begin with a root anchor, and evidence on what the implementation actually does at genesis.
Nelson question: Was the tumbler hierarchy designed to require a non-empty seed (e.g., a root node) at genesis, or is bootstrapping from an empty B₀ consistent with the design?
Gregory question: At system genesis, does udanax-green initialize the address space with seed addresses already present, or does it start from an empty registry and baptize the root via the normal mechanism?

## Issue 2: The unconditional inclusion allocated(Σ) ⊆ Σ.B is asserted but not derived
Reason: The fix is a cross-ASN bridge axiom identifying ASN-0034's (T1)/(T2) allocator events with ASN-0040's baptismal Op transitions; this is derivable from the two ASNs' own content by making the identification explicit.

## Issue 3: The B0-from-T8 chain is incomplete as stated
Reason: Purely a logical-derivation gap; the missing step (allocated(Σ') ⊆ Σ'.B) is the unconditional inclusion already named in the same paragraph, so the fix is internal expository repair.

## Issue 4: B4 is miscast as a per-operation precondition in Bop's PRE
Reason: A presentation/categorization fix internal to the ASN — separating caller-discharged obligations (B6) from structural framework assumptions (B4) requires no external input.

## Issue 5: B1's proof of preservation for non-target non-B6 namespaces does not present an exhaustive case structure
Reason: The four ways B6 can fail and their disposition are already implicit in the proof; the fix is to surface the taxonomy as an explicit partition, entirely internal.

## Issue 6: B0a's "Equivalently" claim presumes every transition is op-associated
Reason: Citation/cross-reference fix to the framework section already present in the ASN; no external evidence or intent needed.
