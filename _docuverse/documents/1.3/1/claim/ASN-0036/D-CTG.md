**D-CTG (VContiguity).** For each document d, V_1(d) (the text subspace) is either empty or occupies every intermediate position between its extremes:

`(A d, u, q : u ∈ V_1(d) ∧ q ∈ V_1(d) ∧ u < q : (A v : subspace(v) = 1 ∧ #v = #u ∧ zeros(v) = 0 ∧ u < v < q : v ∈ V_1(d)))`

In words: within the text subspace, V-positions form a contiguous ordinal range with no gaps. If positions [1, 3] and [1, 7] are occupied, then every position [1, k] with 3 < k < 7 must also be occupied.

For the text subspace at depth m = 2, this is a finite condition: the intermediates between [1, a] and [1, b] are the finitely many [1, i] with a < i < b. Combined with S8-fin (dom(M(d)) is finite), contiguity at depth 2 says V_1(d) occupies a single unbroken block of ordinals.
