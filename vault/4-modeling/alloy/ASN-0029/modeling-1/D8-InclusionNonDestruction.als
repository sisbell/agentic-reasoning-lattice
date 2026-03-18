-- D8 — InclusionNonDestruction (LEMMA)
-- Derived from P7 (CrossDocVIndependent, ASN-0026).
--
--   target(COPY) = d2 ∧ d1 ≠ d2  ⟹  Σ'.V(d1) = Σ.V(d1)
--
-- A COPY targeting one document does not alter the version set
-- of any other document.

sig Doc {}
sig Version {}

sig State {
  versions: Doc -> set Version
}

-- COPY operation: incorporates content into a target document.
-- The target's version set may change; all others are preserved.
pred Copy[s, sPost: State, target: Doc] {
  -- frame: documents other than target are unchanged
  all d: Doc - target | sPost.versions[d] = s.versions[d]

  -- effect: target gains at least one new version (non-trivial copy)
  some sPost.versions[target] - s.versions[target]
}

-- D8: InclusionNonDestruction
-- A COPY targeting d2 preserves the version set of every other document d1.
assert InclusionNonDestruction {
  all s, sPost: State, d1, d2: Doc |
    (Copy[s, sPost, d2] and d1 != d2) implies
      sPost.versions[d1] = s.versions[d1]
}

-- Non-vacuity: a valid Copy exists
run FindCopy {
  some s, sPost: State, target: Doc |
    Copy[s, sPost, target]
} for 4 but exactly 2 State

check InclusionNonDestruction for 5 but exactly 2 State
