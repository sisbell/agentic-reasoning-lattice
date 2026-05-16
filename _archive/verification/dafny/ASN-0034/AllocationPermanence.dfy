include "./NoDeallocation.dfy"

module AllocationPermanence {
  // T8 — AllocationPermanence (INV)
  // Once allocated, an address is never removed from the address space;
  // allocated(s) ⊆ allocated(s') for every state transition s → s'.
  // Theorem from: T1, T2, T4, T10a, TA5, TumblerAdd, TumblerSub, NoDeallocation

  import ND = NoDeallocation

  // The allocation permanence invariant: for every state transition
  // s → s', the allocated set is monotonically non-decreasing.
  ghost predicate AllocationPermanence(before: set<ND.Tumbler>, after: set<ND.Tumbler>) {
    before <= after
  }

  // Operation classification from the formal proof's three-case exhaustion.
  // NoDeallocation ensures these three cases are exhaustive (no removal case).
  datatype OpClass =
    | ReadOnly           // Case 1: T1, T2, T4 — inspect without modifying
    | PureArithmetic     // Case 2: TumblerAdd, TumblerSub — pure functions on T
    | Allocation(a_new: ND.Tumbler)  // Case 3: T10a — insert-only allocation

  // T10a: allocation transitions are insert-only.
  // Sibling allocation via inc(·, 0) and child-spawning via inc(·, k') with k' > 0
  // both satisfy allocated(s') = allocated(s) ∪ {a_new}.
  ghost predicate InsertOnlyAllocation(before: set<ND.Tumbler>, after: set<ND.Tumbler>, a_new: ND.Tumbler) {
    after == before + {a_new}
  }

  // Classifies a state transition by operation type
  ghost predicate ValidTransition(before: set<ND.Tumbler>, after: set<ND.Tumbler>, op: OpClass) {
    match op
      case ReadOnly => after == before
      case PureArithmetic => after == before
      case Allocation(a_new) => InsertOnlyAllocation(before, after, a_new)
  }

  // T8 proof by three-case exhaustion over operation classes.
  // Depends: NoDeallocation (exhaustiveness — no removal case exists),
  //          T10a (Case 3 — allocation is insert-only).
  lemma FromClassifiedTransition(before: set<ND.Tumbler>, after: set<ND.Tumbler>, op: OpClass)
    requires ValidTransition(before, after, op)
    ensures AllocationPermanence(before, after)
  {
    match op {
      case ReadOnly => {}
      case PureArithmetic => {}
      case Allocation(a_new) => {}
    }
  }

  // Permanence composes across sequential state transitions
  lemma Transitive(s0: set<ND.Tumbler>, s1: set<ND.Tumbler>, s2: set<ND.Tumbler>)
    requires AllocationPermanence(s0, s1)
    requires AllocationPermanence(s1, s2)
    ensures AllocationPermanence(s0, s2)
  { }
}
