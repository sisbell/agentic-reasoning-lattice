include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module PrefixImmutable {
  import opened TumblerAlgebra

  type Principal(==)

  datatype State = State(
    principals: set<Principal>,
    pfx: map<Principal, Tumbler>
  )

  ghost predicate ValidState(s: State) {
    forall pi :: pi in s.principals ==> pi in s.pfx
  }

  // O13 — PrefixImmutable
  // For any principal present in both pre- and post-state of a transition,
  // its ownership prefix is unchanged.
  ghost predicate PrefixImmutable(s: State, s': State)
    requires ValidState(s)
    requires ValidState(s')
  {
    forall pi :: pi in s.principals && pi in s'.principals
      ==> s'.pfx[pi] == s.pfx[pi]
  }
}
