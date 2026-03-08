-- UF — UniversalIFrame (FRAME, ensures)
-- Every operation preserves i-space content for all allocated addresses.
--   (A a : a in Σ.A : Σ'.ι(a) = Σ.ι(a))

sig IAddr {}
sig Value {}

sig State {
  iota: IAddr -> lone Value
}

-- Allocated addresses: dom(ι)
fun allocated[s: State]: set IAddr {
  (s.iota).Value
}

-- The universal i-frame property
pred UniversalIFrame[s, sPost: State] {
  all a: allocated[s] | sPost.iota[a] = s.iota[a]
}

-- Concrete operation: allocate a fresh address with a value.
-- Modifies only the new address; all existing mappings unchanged.
pred Allocate[s, sPost: State, a: IAddr, v: Value] {
  -- precondition: a is not yet allocated
  a not in allocated[s]

  -- postcondition: a maps to v
  sPost.iota[a] = v

  -- frame: all other addresses unchanged
  all a2: IAddr - a | sPost.iota[a2] = s.iota[a2]
}

-- Check 1: Allocate satisfies the universal i-frame
assert AllocatePreservesIFrame {
  all s, sPost: State, a: IAddr, v: Value |
    Allocate[s, sPost, a, v] implies UniversalIFrame[s, sPost]
}

-- Check 2: Frame composes transitively — two consecutive
-- frame-respecting transitions preserve content from the first state.
-- (Holds because the frame implies allocated[s1] ⊆ allocated[s2].)
assert FrameTransitive {
  all s1, s2, s3: State |
    (UniversalIFrame[s1, s2] and UniversalIFrame[s2, s3]) implies
      (all a: allocated[s1] | s3.iota[a] = s1.iota[a])
}

-- Non-vacuity: Allocate can happen from a non-empty state
run AllocateExists {
  some s, sPost: State, a: IAddr, v: Value |
    some allocated[s] and Allocate[s, sPost, a, v]
} for 4 but exactly 2 State

check AllocatePreservesIFrame for 5 but exactly 2 State
check FrameTransitive for 5 but exactly 3 State
