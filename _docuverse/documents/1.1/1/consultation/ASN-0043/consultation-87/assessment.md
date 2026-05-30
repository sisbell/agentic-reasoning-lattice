# Channel Assignment — ASN-0043 review-87

**Date:** 2026-05-30 10:42

## Issue 1: `home` is used across two sections before it is defined, via a chain of forward pointers
Reason: Pure reorganization — `home(a) = N(a).0.U(a).0.D(a)` depends only on L1 and T4-validity, both already present in the ASN. Moving the definition earlier and stripping provenance prose is fully derivable from the ASN's own content.

## Issue 2: The T7-disjointness discharge is fully restated four times
Reason: De-duplication of an argument the ASN already carries in full at L0a. Collapsing the later instances to citations requires no design intent or implementation evidence.

## Issue 3: L0a carries implementation rationale in a definition slot
Reason: Relocation of existing prose — the Gregory corollary and its Open Question already exist in the ASN; consolidating them is an internal editorial move, not a new evidence claim.

## Issue 4: L1c contains commentary on what the chain "records" rather than content
Reason: The separator-position fact is already stated and reused in the `s = home(a)` postcondition; folding it into the chain and deleting the meta-narration is internal restructuring.

## Issue 5: Repeated "outside this ASN's scope" essay paragraphs in structural slots
Reason: Deletion of redundant scope prose already covered by the Scope section and Open Questions; no external input needed to decide what stays in-scope.

## Issue 6: L9 / L11b preconditions say "all L- and S-invariants" but enumerate lemmas as if they were state invariants
Reason: A precision fix internal to the ASN's own logical structure — FSP already supplies the correct state-local enumeration to copy, and distinguishing lemmas from state-local invariants is determinable from each property's own labeled type.
