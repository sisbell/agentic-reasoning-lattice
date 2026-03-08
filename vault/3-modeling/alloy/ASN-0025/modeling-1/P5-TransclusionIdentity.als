-- P5 — TransclusionIdentity (POST, ensures)
-- Applies to COPY. After COPY, every I-address in the source span
-- is visible in the destination document.
--
-- S = (s₁, ..., sₘ) is the I-address sequence of the source span,
-- where sᵢ = Σ.v(d_s)(qᵢ).
-- Property: (A a : a ∈ S : visible(a, d, Σ'))

sig IAddr {}
sig VPos {}

sig State {
  docs: set IAddr,
  vmap: IAddr -> VPos -> lone IAddr     -- Σ.v(d) : VPos ⇸ IAddr
} {
  -- vmap only defined for documents
  all d: IAddr - docs | no vmap[d]
}

-- visible(a, d, Σ) ≡ ∃ q ∈ dom(Σ.v(d)) : Σ.v(d)(q) = a
pred visible[a: IAddr, d: IAddr, s: State] {
  some q: VPos | s.vmap[d][q] = a
}

-- Source span I-addresses: S = {Σ.v(d_s)(q) | q ∈ span}
fun spanAddrs[s: State, d_s: IAddr, span: set VPos]: set IAddr {
  (d_s.(s.vmap))[span]
}

-- COPY operation: transclude source span into destination document.
-- Operationally: for each source I-address, a fresh position in d
-- is created that maps to that same I-address (transclusion, not duplication).
pred Copy[s, sPost: State, d_s: IAddr, d: IAddr, span: set VPos] {
  -- Preconditions
  d_s in s.docs
  d in s.docs
  some span
  all q: span | one s.vmap[d_s][q]

  -- Operational: each source I-address gets a fresh position in d
  let S = spanAddrs[s, d_s, span] |
    all a: S | some q: VPos {
      no s.vmap[d][q]              -- position is fresh
      sPost.vmap[d][q] = a         -- maps to source I-address
    }

  -- Existing mappings in d preserved
  all q: VPos | some s.vmap[d][q] implies
    sPost.vmap[d][q] = s.vmap[d][q]

  -- Frame: docs unchanged
  sPost.docs = s.docs

  -- Frame: other docs' vmaps unchanged
  all d2: sPost.docs - d | sPost.vmap[d2] = s.vmap[d2]
}

-- P5: After COPY, every source span address is visible in destination
assert TransclusionIdentity {
  all s, sPost: State, d_s, d: IAddr, span: set VPos |
    Copy[s, sPost, d_s, d, span] implies
      (all a: spanAddrs[s, d_s, span] | visible[a, d, sPost])
}

-- Non-vacuity: a COPY producing visible transclusion exists
run NonVacuity {
  some s, sPost: State, d_s, d: IAddr, span: set VPos |
    Copy[s, sPost, d_s, d, span]
    and some spanAddrs[s, d_s, span]
} for 5 but exactly 2 State

check TransclusionIdentity for 5 but exactly 2 State
