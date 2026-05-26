# Review of ASN-0075

## REVISE

No issues identified.

## OUT_OF_SCOPE

### Topic 1: Restoration operation specification
**Why out of scope**: The "Composability with Restoration" section notes that the output's form makes restoration possible but explicitly defers specification. This is appropriately deferred — the ASN's job is SHOWDELETIONS, not the operations that consume its output.

### Topic 2: Concurrency model for SHOWDELETIONS observations
**Why out of scope**: Listed in Open Questions as "what consistency model must SHOWDELETIONS observe to deliver coherent joint snapshots". The current state model (ASN-0047) uses SequentialTransitionAxiom; concurrent observation belongs in a future ASN.

### Topic 3: Multi-document family SHOWDELETIONS
**Why out of scope**: Listed in Open Questions. Generalizing the binary asymmetric pair to families of more than two documents requires structural decisions the binary case doesn't force.

### Topic 4: Within-link-subspace deletion comparison
**Why out of scope**: D-SUBSP rules link-subspace deletion comparison structurally meaningful only per-document (not cross-document) because of CL-OWN. A per-document link-subspace deletion analysis is a different operation belonging in a separate ASN.

---

## Review Notes

The ASN handles the core deliverables well:

- **D-EXH** unpacks the "impossible" row chain via L14 → S3★-aux → S3★ link-clause contrapositive → P4★, with the reachability hypothesis explicitly load-bearing for P4★.
- **D-DISCR** exhibits two reachable states with explicit valid composites; the (C, L, E, M) agreement is verified column-by-column; the J0/J1★ discharge in each composite is justified (including the "K.μ⁺ in some document, not necessarily origin" reading of J0).
- The **worked example** verifies D-EXH, D-IDENT, D-ORIG, D-SYM concretely with an explicit classification table.
- **D-ACT** proves witness-run uniqueness via I-adjacency partitioning, including the structural lemma that no `t ∈ dom(C)` lies strictly between consecutive emissions — with all four cases (same-origin same/short/long length, different-origin) and the three different-origin sub-cases (non-nesting, d≺d', d'≺d) unpacked individually.
- **D-ORD** addresses the multi-valued inverse issue (S5) by using minimum under T1 with explicit injectivity proof.
- Cross-ASN references are confined to foundation ASNs (0034, 0036, 0047, 0053, 0058).

VERDICT: CONVERGED
