include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "ISpaceMonotone.dfy"
include "CrossDocVIndependent.dfy"
include "ReferentiallyComplete.dfy"

module RefStabilityModule {
  import opened Foundation
  import ISpaceMonotone
  import CrossDocVIndependent
  import ReferentiallyComplete

  // ASN-0026 REF-STABILITY — RefStability (LEMMA, lemma)
  // derived from P7 (CrossDocVIndependent), P1 (ISpaceMonotone), P2 (ReferentiallyComplete)
  //
  // After any operation on d_s, a distinct document d_t retains all
  // V-space references in the I-space domain.
  lemma RefStability(s: State, s': State, ds: DocId, dt: DocId)
    requires ReferentiallyComplete.ReferentiallyComplete(s)
    requires ISpaceMonotone.ISpaceMonotone(s, s')
    requires CrossDocVIndependent.CrossDocVIndependent(s, s', ds)
    requires ds != dt
    requires dt in s.docs
    requires dt in s.vmap
    ensures dt in s'.vmap
    ensures forall q :: q in s'.vmap[dt] ==> s'.vmap[dt][q] in Allocated(s')
  { }
}
