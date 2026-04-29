### Topic 1: V-I subspace correspondence as a system invariant

The invariant `(A d, q : q ∈ dom.poom(d) : sub(q) = sub_i(poom(d).q))` — that a position's V-subspace always matches its I-address's subspace — is a structural property of the system, not specific to INSERT. It would need to be established at document creation and preserved by every operation. Defining and verifying it belongs in a foundational ASN or in the ASN for CREATENEWDOCUMENT, not here.

**Why out of scope**: This is a system-level invariant that spans all operations. INSERT can be shown to preserve S4 without it (per the simpler proof above). Future ASNs introducing cross-subspace operations (e.g., CREATELINK) would benefit from having it stated.

VERDICT: REVISE
