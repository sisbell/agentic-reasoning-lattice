include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module AddressPermanence {

  import opened TumblerAlgebra

  // T8 — AddressPermanence (INV, predicate(State, State))
  // transition invariant

  // Abstract content identifier
  datatype Content = Content(id: nat)

  // I-space state: address-to-content bindings
  datatype IState = IState(bindings: map<Tumbler, Content>)

  // T8: once an address is bound to content, that binding persists
  // across every state transition. No operation removes an address
  // from I-space or changes the content at a bound address.
  ghost predicate AddressPermanence(s: IState, s': IState) {
    forall a :: a in s.bindings ==>
      a in s'.bindings && s'.bindings[a] == s.bindings[a]
  }
}
