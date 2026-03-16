include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

// O11 — IdentityAxiomatic
// The ownership model treats principal identity as given.
// session.account = pfx(π) is an axiom of the session,
// not a theorem of the ownership model. Authentication is external.
module IdentityAxiomatic {
  import opened TumblerAlgebra

  datatype Principal = Principal(prefix: Tumbler)
  datatype Session = Session(account: Tumbler, principal: Principal)

  // The axiomatic binding: a session's account tumbler equals
  // the ownership prefix of its associated principal.
  // This is a precondition for downstream properties, never proved.
  ghost predicate ValidSession(s: Session) {
    s.account == s.principal.prefix
  }

  // DIVERGENCE: O11 is a meta-property — it asserts that identity
  // binding is assumed (axiomatic), not derived from the ownership
  // model. Dafny represents this as a predicate that downstream
  // modules require as a precondition. There is no proof obligation.
}
