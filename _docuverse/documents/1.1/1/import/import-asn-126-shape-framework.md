---
create_note: 126
title: "Substrate Shape Framework"
source_doc: "_workspace/asn-new-shape-framework-draft.md"
depends: [86]
---

# Why I'm importing this doc

ASN-0086 commits the substrate to typed relations of arity three over
`(F, G, K)` and provides the operational vocabulary `Emit_K`, `Observe`,
`Nullify`. It does not narrow the cardinalities of the F and G slots,
nor does it specify the registration surface an app must use to declare
a concrete type.

The lattice's usage pattern is uniformly single-source — classifiers,
citations, supersession chains, holdings, retractions — so the open
arity-3 vocabulary in ASN-0086 is paying for generality the substrate
never exercises. The right level of commitment for apps to register
against is a finite shape vocabulary with a static well-formedness
check on every emit.

This note supplies that and only that: F cardinality fixed at 1, three
shape categories by G cardinality (Unary, Binary, Multi), a
shape-conformance predicate `Sh-conf` evaluable from the tuple and the
registry entry alone, a registry that is a component of `Σ_init` and
invariant across every `→`-step, and an idem flag whose structural
presence is committed here with operational semantics deferred to a
successor. Five named properties (P1–P5) record the structural
commitments.

Importing now because:

- Operations layer specs (the typed-relation classifiers used by the
  reasoning lattice — citation.depends, supersedes, retired, holdings,
  etc.) need a stable shape vocabulary to register against.
- The behavior catalog, default predicates, and standard registrations
  are operational concerns that can layer on top of this framework
  without revisiting the structural commitments here.
- The note explicitly defers everything operational (idem semantics
  at emit, behavior catalog, default predicates, standard
  registrations, predicate composition, extension beyond F=1/N=3) to
  successor notes via the Open Questions section.

Direct dep `[86]` — no transitivity assumption. ASN-0086 R0–R7 supply
the typed-relation framework this note narrows.
