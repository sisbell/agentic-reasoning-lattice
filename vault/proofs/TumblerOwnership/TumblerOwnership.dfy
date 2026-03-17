include "../TumblerAlgebra/TumblerAlgebra.dfy"
include "../TumblerAlgebra/TumblerHierarchy.dfy"

// TumblerOwnership — shared definitions for ASN-0042 Tumbler Ownership
// Principal, State, common predicates, O1, O9, O11, O12, T8
module TumblerOwnership {
  import opened TumblerAlgebra
  import TumblerHierarchy

  // O1 — Principal identity: distinguished by ownership prefix
  datatype Principal = Principal(prefix: Tumbler)

  // Ownership state
  datatype State = State(principals: set<Principal>, alloc: set<Tumbler>)

  // O1 — owns(pi, a) = pfx(pi) <= a
  ghost predicate Owns(pi: Principal, a: Tumbler) {
    IsPrefix(pi.prefix, a)
  }

  // Principal pi covers address a
  ghost predicate Covers(pi: Principal, a: Tumbler, principals: set<Principal>) {
    pi in principals && IsPrefix(pi.prefix, a)
  }

  // Effective owner: most-specific covering principal (omega from ASN-0042)
  ghost predicate IsEffectiveOwner(pi: Principal, a: Tumbler, principals: set<Principal>) {
    Covers(pi, a, principals) &&
    forall pi' :: Covers(pi', a, principals) && pi' != pi ==>
      |pi.prefix.components| > |pi'.prefix.components|
  }

  // Strict prefix relation
  ghost predicate StrictPrefix(p: Tumbler, a: Tumbler) {
    IsPrefix(p, a) && |p.components| < |a.components|
  }

  // O12 — PrincipalPersistence
  ghost predicate PrincipalPersistence(s: State, s': State) {
    s.principals <= s'.principals
  }

  // T8 — AddressPermanence
  ghost predicate AddressPermanence(s: State, s': State) {
    s.alloc <= s'.alloc
  }

  // acct(a): account-field truncation
  // zeros(a) = 0 -> acct(a) = a
  // zeros(a) >= 1 -> acct(a) = a truncated through user field
  function Acct(a: Tumbler): Tumbler {
    var z0 := FindZero(a.components, 0);
    if z0 >= |a.components| then
      a
    else
      var z1 := FindZero(a.components, z0 + 1);
      Tumbler(a.components[..z1])
  }

  // Delegation preconditions from ASN-0042 Delegated definition
  ghost predicate DelegationPrecondition(
    s: State, delegator: Principal, delegate: Principal
  ) {
    delegator in s.principals &&
    delegate !in s.principals &&
    // (i) pfx(delegator) < pfx(delegate)
    StrictPrefix(delegator.prefix, delegate.prefix) &&
    // (ii) delegator is most-specific covering principal for pfx(delegate)
    (forall pi :: pi in s.principals && IsPrefix(pi.prefix, delegate.prefix)
      ==> |pi.prefix.components| <= |delegator.prefix.components|) &&
    // (iv) zeros(pfx(delegate)) <= 1
    TumblerHierarchy.ZeroCount(delegate.prefix.components) <= 1 &&
    // (v) T4(pfx(delegate))
    TumblerHierarchy.ValidAddress(delegate.prefix) &&
    // (vi) no existing principal has delegate's prefix as strict prefix of theirs
    (forall pi :: pi in s.principals ==>
      !StrictPrefix(delegate.prefix, pi.prefix))
  }

  // Two covering prefixes of the same address nest by length
  lemma CoveringPrefixesOrdered(p1: Tumbler, p2: Tumbler, a: Tumbler)
    requires IsPrefix(p1, a)
    requires IsPrefix(p2, a)
    requires |p1.components| <= |p2.components|
    ensures IsPrefix(p1, p2)
  { }

  // O11 — IdentityAxiomatic
  // The ownership model treats principal identity as given.
  // session.account = pfx(pi) is an axiom of the session,
  // not a theorem of the ownership model. Authentication is external.
  datatype Session = Session(account: Tumbler, principal: Principal)

  ghost predicate ValidSession(s: Session) {
    s.account == s.principal.prefix
  }

  // O9 — NodeLocalOwnership
  // (A pi in Pi, a in T : owns(pi, a) ==> nodeField(pfx(pi)) <= nodeField(a))
  lemma NodeLocalOwnership(p: Tumbler, a: Tumbler)
    requires IsPrefix(p, a)
    requires TumblerHierarchy.ZeroCount(p.components) <= 1
    ensures TumblerHierarchy.SeqIsPrefix(TumblerHierarchy.NodeField(p), TumblerHierarchy.NodeField(a))
  { }
}
