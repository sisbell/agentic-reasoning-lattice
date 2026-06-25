**S8a (ArrangementDomainRestriction).** The arrangement maps only well-formed V-positions: `dom(Σ.M(d)) ⊆ {t ∈ T : zeros(t) = 0 ∧ #t ≥ 2}` — every active key is a zero-free tumbler of depth at least 2 (a subspace identifier followed by a within-subspace ordinal). By T0 (ASN-0034), `zeros(t) = 0` holds exactly when every component is positive, so equivalently every active V-position has depth at least 2 with all components strictly positive.

A conventional system merges these — "the file" IS the content IS the arrangement. Editing overwrites. Saving destroys the prior state. Nelson rejected this explicitly: "Virtually all of computerdom is built around the destructive replacement of successive whole copies of each current version." The two-component model is his alternative: editing modifies `M(d)` while `C` remains invariant. The separation is the premise; what follows are the invariants it must satisfy.

We call this paired state the *strand*: the two-component object `(Σ.C, Σ.M)` — an immutable content store woven together with the family of mutable arrangements that reference it. The remainder of this ASN derives the invariants that govern a strand.

- *Depends:*
  - T0 (ASN-0034) — supplies the characterization that `zeros(t) = 0` holds exactly when every component is positive, used to restate the domain restriction in terms of strict positivity