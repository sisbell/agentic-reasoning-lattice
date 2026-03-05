include "../TumblerAlgebra/TumblerAlgebra.dfy"

module Foundation {
  import opened TumblerAlgebra

  // Type aliases
  type Addr = nat
  type Pos = nat
  type DocId = nat
  type Content = nat
  type User = nat

  // 2D enfilade displacement (TA8)
  datatype Displacement = Displacement(v: Tumbler, i: Tumbler)
}
