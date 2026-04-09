module NoDeallocation {
  // NoDeallocation — design axiom
  // The system's operation vocabulary contains no operation that
  // removes an element from the allocated set.

  datatype Tumbler = Tumbler(components: seq<nat>)

  // Design constraint: every state transition preserves or grows
  // the allocated set. No "deallocate", "free", or "reclaim" exists.
  predicate NoDeallocation(before: set<Tumbler>, after: set<Tumbler>) {
    before <= after
  }
}
