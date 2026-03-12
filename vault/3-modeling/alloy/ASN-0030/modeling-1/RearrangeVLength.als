// ASN-0030 A4a(b): RearrangeVLength (FRAME)
// After rearranging document d, |V'(d)| = |V(d)|

open util/integer

// Each atom represents a distinct position in a V-list
sig Pos {}

sig Doc {}

sig State {
  vlist: Doc -> set Pos
}

// Rearrange operation: reorder d's V-list (a permutation preserves the set)
pred Rearrange[s, s2: State, d: Doc] {
  // precondition: d has a V-list
  d in s.vlist.Pos
  // postcondition: same set of positions (rearrangement is a permutation)
  d.(s2.vlist) = d.(s.vlist)
  // frame: other documents unchanged
  all d2: Doc - d | d2.(s2.vlist) = d2.(s.vlist)
}

// A4a(b): rearrange preserves V-list length
assert RearrangeVLength {
  all s, s2: State, d: Doc |
    Rearrange[s, s2, d] implies
      #(d.(s2.vlist)) = #(d.(s.vlist))
}

// Non-vacuity: a valid rearrange instance exists with nonempty V-list
run NonVacuity {
  some s, s2: State, d: Doc |
    Rearrange[s, s2, d] and #(d.(s.vlist)) > 1
} for 5 but exactly 2 State

check RearrangeVLength for 5 but exactly 2 State
