module NoDeallocation {
  // NoDeallocation — design requirement
  // The system's operation vocabulary contains no operation that
  // removes an element from the allocated set.

  datatype Tumbler = Tumbler(components: seq<nat>)

  // Design constraint accepted as given: every state transition
  // preserves or grows the allocated set.
  lemma {:axiom} NoDeallocation(before: set<Tumbler>, after: set<Tumbler>)
    ensures before <= after
}
