open util/ordering[Pos]
open util/integer

-- Positions in a tumbler sequence (ordered indices)
sig Pos {}

-- Four hierarchical address levels
abstract sig Level {}
one sig NodeAddr, UserAddr, DocAddr, ElemAddr extends Level {}

-- A tumbler: ordered sequence of integer components
sig Tumbler {
  lastPos: one Pos,
  val: Pos -> lone Int
} {
  all p: Pos | lte[p, lastPos] implies one val[p]
  all p: Pos | not lte[p, lastPos] implies no val[p]
}

-- zeros(t) = #{i : 1 <= i <= #t and t_i = 0}
fun zeros[t: Tumbler]: Int {
  #{p: Pos | lte[p, t.lastPos] and t.val[p] = 0}
}

-- T4 validity: non-negative components, at most 3 zero-valued separators
pred T4Valid[t: Tumbler] {
  all p: Pos | lte[p, t.lastPos] implies t.val[p] >= 0
  zeros[t] =< 3
}

-- Level determined by zero count (the mapping under test)
fun levelOf[t: Tumbler]: lone Level {
  (zeros[t] = 0) => NodeAddr
  else ((zeros[t] = 1) => UserAddr
  else ((zeros[t] = 2) => DocAddr
  else ((zeros[t] = 3) => ElemAddr
  else none)))
}

-- Postcondition: zeros(t) in {0, 1, 2, 3}
assert ZerosInRange {
  all t: Tumbler | T4Valid[t] implies
    (zeros[t] >= 0 and zeros[t] =< 3)
}

-- Postcondition: mapping is injective (distinct zero counts -> distinct levels)
assert LevelInjective {
  all t1, t2: Tumbler |
    (T4Valid[t1] and T4Valid[t2] and not (zeros[t1] = zeros[t2]))
      implies not (levelOf[t1] = levelOf[t2])
}

-- Non-vacuity and surjectivity: all four levels are achievable
run NonVacuity {
  some disj t0, t1, t2, t3: Tumbler |
    T4Valid[t0] and levelOf[t0] = NodeAddr and
    T4Valid[t1] and levelOf[t1] = UserAddr and
    T4Valid[t2] and levelOf[t2] = DocAddr and
    T4Valid[t3] and levelOf[t3] = ElemAddr
} for 5 but exactly 4 Tumbler, 4 Int

check ZerosInRange for 5 but 4 Int
check LevelInjective for 5 but exactly 2 Tumbler, 4 Int
