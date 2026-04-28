The cardinality operator |·| is postulated as a primitive total function on subsets
of every initial segment {j ∈ ℕ : 1 ≤ j ≤ n} ⊆ ℕ (n ∈ ℕ), with codomain ℕ. For such S,
|S| ∈ ℕ is the unique k for which there exists a strictly increasing function
f : {j ∈ ℕ : 1 ≤ j ≤ k} → ℕ with image S (at k = 0 the domain is empty, f is the
empty function, vacuously strictly increasing with image ∅, forcing S = ∅ and
|∅| = 0 without recourse to a convention on empty lists), and |S| ≤ n.
NAT-order's strict-total-order discipline keeps the "strictly increasing function"
predicate well-formed. NAT-card is the foundation
citation for every claim that invokes |·| — in particular the definition
zeros(t) = |{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}| in T4 and its downstream consumers T4a,
T4b, T4c.
