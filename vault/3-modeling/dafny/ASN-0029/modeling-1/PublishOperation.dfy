include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module PublishOperation {
  import opened Foundation

  // D10a — PublishOperation (POST, ensures)

  datatype PubStatus = Private | Published | Privashed

  // DIVERGENCE: account(d) = actor(op) precondition omitted. Authorization
  // is a protocol-layer constraint; the state transformation is independent
  // of account structure.

  // Publish operation on pub map. The base State (D, I, V) is unchanged —
  // captured by this function operating on pub alone; the caller retains
  // the original State for the frame.
  function Publish(
    s: State,
    pub: map<DocId, PubStatus>,
    d: DocId,
    status: PubStatus
  ): (pub': map<DocId, PubStatus>)
    // pre
    requires d in s.docs
    requires pub.Keys == s.docs
    requires pub[d] == Private
    requires status == Published || status == Privashed
    // well-formedness preserved
    ensures pub'.Keys == s.docs
    // post: target gets requested status
    ensures pub'[d] == status
    // frame: other documents' pub unchanged
    ensures forall d' :: d' in s.docs && d' != d ==>
      pub'[d'] == pub[d']
  {
    pub[d := status]
  }
}
