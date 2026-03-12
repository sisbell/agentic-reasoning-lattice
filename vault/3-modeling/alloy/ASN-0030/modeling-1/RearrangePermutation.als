// ASN-0030 A4a(c): RearrangePermutation (POST)
// After Rearrange, V' is a permutation of V.
// Exists bijection pi on [1..n_d] such that V'(p) = V(pi(p)).
// Modeled per-document: State.V is one document's V-list.

sig Addr {}

sig State {
  V: Int -> lone Addr,
  perm: Int -> lone Int       // Skolem witness for the bijection
}

fun positions[s: State]: set Int {
  (s.V).Addr
}

// V-list occupies contiguous positions 1..n
pred wellFormed[s: State] {
  all p: Int | some s.V[p] implies p >= 1
  all p, q: Int | (some s.V[q] and p >= 1 and p < q) implies some s.V[p]
}

// A4a(c): exists bijection perm on [1..n] s.t. V'(p) = V(perm(p))
pred Rearrange[s, sPost: State] {
  let posns = positions[s] {
    // same position domain
    positions[sPost] = posns

    // perm is a bijection on posns
    all p: posns | one sPost.perm[p]
    all p: posns | sPost.perm[p] in posns
    all p: Int | p not in posns implies no sPost.perm[p]
    all disj p1, p2: posns | sPost.perm[p1] != sPost.perm[p2]

    // postcondition: V'(p) = V(perm(p))
    all p: posns | sPost.V[p] = s.V[sPost.perm[p]]
  }
}

// Consequence: the set of referenced addresses is preserved
assert RearrangePreservesAddrSet {
  all s, sPost: State |
    (wellFormed[s] and Rearrange[s, sPost]) implies
      Int.(sPost.V) = Int.(s.V)
}

// Consequence: well-formedness is preserved
assert RearrangePreservesWF {
  all s, sPost: State |
    (wellFormed[s] and Rearrange[s, sPost]) implies wellFormed[sPost]
}

// Consequence: V-list size is preserved
assert RearrangePreservesSize {
  all s, sPost: State |
    (wellFormed[s] and Rearrange[s, sPost]) implies
      #(sPost.V) = #(s.V)
}

// Non-vacuity: a non-trivial rearrange exists
run FindNontrivialRearrange {
  some s, sPost: State |
    wellFormed[s] and Rearrange[s, sPost] and s.V != sPost.V
} for 5 but exactly 2 State, 4 Int

check RearrangePreservesAddrSet for 5 but exactly 2 State, 4 Int
check RearrangePreservesWF for 5 but exactly 2 State, 4 Int
check RearrangePreservesSize for 5 but exactly 2 State, 4 Int
