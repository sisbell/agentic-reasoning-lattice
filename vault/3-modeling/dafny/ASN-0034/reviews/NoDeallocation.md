# NoDeallocation — Contract FLAG

*2026-04-09 08:57*

Axiom encoded as predicate instead of axiom/assume

The formal contract specifies:
  *Axiom:* The system's operation vocabulary contains no operation
  that removes an element from the allocated set.

The Dafny code has:
  predicate NoDeallocation(before: set<Tumbler>, after: set<Tumbler>) {
    before <= after
  }

Missing/extra/wrong:
  Wrong construct. The contract marks this as an *Axiom:* — a design
  constraint taken as given. A predicate merely defines a checkable
  condition; it does not assert that the condition holds for every
  state transition. The encoding should use `lemma {:axiom}` with
  `ensures before <= after` so that Dafny treats it as an assumed
  truth rather than a callable boolean function.
