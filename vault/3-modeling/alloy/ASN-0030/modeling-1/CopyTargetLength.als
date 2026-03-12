// ASN-0030 A5(c): CopyTargetLength
// After COPY(d_s, p_s, k, d_t, p_t), |Σ'.V(d_t)| = n_{d_t} + k

open util/integer

// Each atom represents a distinct position in a V-list
sig Pos {}

sig Doc {}

sig State {
  vlist: Doc -> set Pos
}

// Copy operation: insert a set of fresh positions into d_t's V-list
pred Copy[s, s2: State, ds, dt: Doc, inserted: set Pos] {
  // precondition: source has content
  some ds.(s.vlist)
  // precondition: both documents have V-lists (possibly empty for target)
  // inserted positions are fresh to the target
  no inserted & dt.(s.vlist)
  // at least one position copied
  some inserted
  // inserted positions come from source (modelling address sharing)
  #inserted =< #(ds.(s.vlist))
  // postcondition: target gains exactly the inserted positions
  dt.(s2.vlist) = dt.(s.vlist) + inserted
  // frame: other documents unchanged
  all d2: Doc - dt | d2.(s2.vlist) = d2.(s.vlist)
}

// A5(c): copy produces target V-list of length n_{d_t} + k
assert CopyTargetLength {
  all s, s2: State, ds, dt: Doc, inserted: set Pos |
    let ndt = #(dt.(s.vlist)), k = #inserted |
      Copy[s, s2, ds, dt, inserted] implies
        #(dt.(s2.vlist)) = plus[ndt, k]
}

// Non-vacuity: a valid copy instance exists
run NonVacuity {
  some s, s2: State, ds, dt: Doc, inserted: set Pos |
    Copy[s, s2, ds, dt, inserted]
} for 5 but exactly 2 State

check CopyTargetLength for 5 but exactly 2 State
