include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

// home(a) — Home (DEF, function)
// ASN-0043: home(a) = origin(a) = node.0.user.0.document
module Home {
  import opened TumblerAlgebra
  import TumblerHierarchy

  // Home document: the document-level prefix of a link address
  function HomeDoc(a: Tumbler): Tumbler
    requires TumblerHierarchy.HasElementField(a)
  {
    var node := TumblerHierarchy.NodeField(a);
    var user := TumblerHierarchy.UserField(a);
    var doc := TumblerHierarchy.DocField(a);
    Tumbler(node + [0] + user + [0] + doc)
  }
}
