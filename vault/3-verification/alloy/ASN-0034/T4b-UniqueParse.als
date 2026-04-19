open util/ordering[Pos]

-- Positions in a tumbler, totally ordered
sig Pos {
  val: Int
}

-- Canonical field identifiers
abstract sig FieldId {}
one sig NodeF, UserF, DocF, ElemF extends FieldId {}

-- A parse: separator positions + field assignment for non-separators
sig Parse {
  seps: set Pos,
  assign: Pos -> lone FieldId
}

-- T4 structural constraints on the tumbler values
pred t4Tumbler {
  some Pos
  all p: Pos | p.val >= 0
  #{p: Pos | p.val = 0} =< 3
  all p: Pos | (p.val = 0 and some p.next) implies p.next.val != 0
  first.val != 0
  last.val != 0
}

-- A valid decomposition of the tumbler into fields
pred validParse[p: Parse] {
  -- Separators have value zero
  all pos: p.seps | pos.val = 0
  -- Field components have strictly positive value
  all pos: Pos - p.seps | pos.val > 0
  -- At most three separators
  #p.seps =< 3
  -- No adjacent separators (non-empty field constraint)
  all pos: p.seps | some pos.next implies pos.next not in p.seps
  -- First and last positions are not separators
  first not in p.seps
  last not in p.seps

  -- Separators are not assigned to any field
  all pos: p.seps | no p.assign[pos]
  -- Every non-separator is assigned exactly one field
  all pos: Pos - p.seps | one p.assign[pos]

  -- Fields appear in canonical order
  all a, b: Pos |
    (p.assign[a] = NodeF and p.assign[b] = UserF) implies lt[a, b]
  all a, b: Pos |
    (p.assign[a] = UserF and p.assign[b] = DocF) implies lt[a, b]
  all a, b: Pos |
    (p.assign[a] = DocF and p.assign[b] = ElemF) implies lt[a, b]

  -- Node field is always present
  some p.assign.NodeF

  -- Field presence determined by separator count
  no p.seps implies no (p.assign.UserF + p.assign.DocF + p.assign.ElemF)
  #p.seps = 1 implies (some p.assign.UserF and no p.assign.DocF and no p.assign.ElemF)
  #p.seps = 2 implies (some p.assign.UserF and some p.assign.DocF and no p.assign.ElemF)
  #p.seps = 3 implies (some p.assign.UserF and some p.assign.DocF and some p.assign.ElemF)

  -- Each field is contiguous (no field straddles a separator)
  all f: FieldId, a, c: Pos |
    (p.assign[a] = f and p.assign[c] = f and lt[a, c]) implies
      (all b: Pos | (lt[a, b] and lt[b, c]) implies p.assign[b] = f)
}

-- T4b: fields(t) is well-defined and uniquely determined by t
assert UniqueParse {
  all p1, p2: Parse |
    (t4Tumbler and validParse[p1] and validParse[p2]) implies
      (p1.seps = p2.seps and p1.assign = p2.assign)
}

check UniqueParse for 7 but exactly 2 Parse, 4 Int

-- Non-vacuity: a valid parse exists for a T4 tumbler
run NonVacuity {
  some p: Parse | t4Tumbler and validParse[p]
} for 5 but exactly 1 Parse, 4 Int
