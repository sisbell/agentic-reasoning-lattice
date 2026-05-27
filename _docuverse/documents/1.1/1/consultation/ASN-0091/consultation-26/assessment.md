# Channel Assignment — ASN-0091 review-26

**Date:** 2026-05-26 21:37

## Issue 1: Unified-state identification E_doc = dom(M) derivation is interpretive
Reason: The fix requires reconciling the effect clauses of ASN-0093's K.σ and ASN-0047's K.δ-IsDocument under unification — a cross-ASN formal reconciliation internal to the spec system. Neither Nelson's design intent nor udanax-green's implementation bears on how two ASNs' effect clauses compose under unification; the resolution is to either find the unified-state operation semantics in the spec system or supply explicit verification from each source ASN's clauses.

## Issue 2: M0 and M1 from ASN-0093 omitted from per-invariant discharge enumeration
Reason: Both M0 and M1 are named in ASN-0093 with discharges derivable from RA-frame plus structural facts. The fix is to add them to the enumeration with their discharges; no external channel input is needed.

## Issue 3: Abstract subspace-preservation of π lacks its own labeled claim
Reason: The subspace-preservation property is already proved in prose using RA-adm + S3★ + L14; extracting it as a labeled claim is a pure restructuring of existing ASN content. No external channel needed.

## Issue 4: RE-frag★/RE-coal★/RE-eq★ existential claim is too informal
Reason: The fix requires constructing a concatenation of the existing single-step witnesses (RE-frag, RE-coal, RE-eq) and verifying that one witness's post-state can serve as the next witness's pre-state. This is mathematical work on witnesses already in the ASN; no external channel input is needed.

## Issue 5: Bijection signature in RA-π overconstrains and creates dependency on RA-dom
Reason: This is a formal/typing choice between two equivalent signatures, with the dependency structure between RA-π and RA-dom already discussed in the ASN. The fix is an internal definitional clean-up; neither design intent nor implementation evidence bears on which signature to adopt.

## Issue 6: Density of per-invariant discharge paragraph impedes verification
Reason: Pure prose restructuring — breaking one large paragraph into subsections, with no new content required. The discharges themselves are already in the ASN; only their organization changes.
