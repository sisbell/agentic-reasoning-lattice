// home(a) — LinkHome (DEF, function)
// ASN-0043: home(a) = origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)

include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

module Home {
  import opened TumblerAlgebra
  import TumblerHierarchy

  function Home(a: Tumbler): Tumbler {
    Tumbler(
      TumblerHierarchy.NodeField(a) + [0] +
      TumblerHierarchy.UserField(a) + [0] +
      TumblerHierarchy.DocField(a)
    )
  }
}
