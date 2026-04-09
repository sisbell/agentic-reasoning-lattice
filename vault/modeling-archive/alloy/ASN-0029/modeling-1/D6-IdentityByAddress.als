-- D6-IdentityByAddress.als
-- Property: d1 = d2  iff  fields(d1) = fields(d2)
-- Document identity is fully determined by address fields.

-- Address field values
sig NodeId {}
sig UserId {}
sig DocNum {}

-- Document identifier: a tuple of address fields
sig DocId {
  node: one NodeId,
  user: one UserId,
  doc: one DocNum
}

-- Two DocIds have identical fields
pred sameFields[d1, d2: DocId] {
  d1.node = d2.node
  d1.user = d2.user
  d1.doc = d2.doc
}

-- Design axiom: DocId has value semantics (identity = fields)
fact ValueSemantics {
  all d1, d2: DocId |
    sameFields[d1, d2] implies d1 = d2
}

-- D6: identity iff same fields
assert IdentityByAddress {
  all d1, d2: DocId |
    (d1 = d2) iff sameFields[d1, d2]
}

check IdentityByAddress for 5

-- Non-vacuity: model admits multiple distinct documents
run NonVacuity {
  #DocId > 1
  some d1, d2: DocId | d1.node != d2.node
} for 4
