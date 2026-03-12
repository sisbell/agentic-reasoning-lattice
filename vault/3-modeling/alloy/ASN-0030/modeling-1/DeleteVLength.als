// ASN-0030 A4(c): DeleteVLength
// After deleting k references from document d, |V'(d)| = n_d - k

open util/integer

// Each atom represents a distinct position in a V-list
sig Pos {}

sig Doc {}

sig State {
  vlist: Doc -> set Pos
}

// Delete operation: remove a set of positions from document d's V-list
pred Delete[s, s2: State, d: Doc, removed: set Pos] {
  // precondition: removed positions belong to d's V-list
  removed in d.(s.vlist)
  // at least one deletion
  some removed
  // postcondition: V'(d) is V(d) minus the removed positions
  d.(s2.vlist) = d.(s.vlist) - removed
  // frame: other documents unchanged
  all d2: Doc - d | d2.(s2.vlist) = d2.(s.vlist)
}

// A4(c): delete produces V-list of length n_d - k
assert DeleteVLength {
  all s, s2: State, d: Doc, removed: set Pos |
    let nd = #(d.(s.vlist)), k = #removed |
      Delete[s, s2, d, removed] implies
        #(d.(s2.vlist)) = minus[nd, k]
}

// Non-vacuity: a valid delete instance exists
run NonVacuity {
  some s, s2: State, d: Doc, removed: set Pos |
    Delete[s, s2, d, removed]
} for 5 but exactly 2 State

check DeleteVLength for 5 but exactly 2 State
