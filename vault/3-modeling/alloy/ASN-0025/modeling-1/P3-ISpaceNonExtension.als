-- P3 — ISpaceNonExtension (FRAME, ensures)
-- Applies to DELETE, REARRANGE, COPY.
-- Property: Σ'.A = Σ.A ∧ Σ'.ι = Σ.ι

sig IAddr {}
sig Value {}
sig VPos {}

sig State {
  iota: IAddr -> lone Value,         -- Σ.ι : IAddr ⇸ Value
  docs: set IAddr,                   -- Σ.D ⊆ Σ.A
  vmap: IAddr -> VPos -> lone IAddr  -- Σ.v(d) : VPos ⇸ IAddr
}

-- Σ.A = dom(Σ.ι)
fun allocated[s: State]: set IAddr {
  s.iota.Value
}

pred wellFormed[s: State] {
  -- D ⊆ A
  s.docs in allocated[s]
  -- vmap only maps docs to allocated addresses
  all d: IAddr, q: VPos |
    some s.vmap[d][q] implies
      (d in s.docs and s.vmap[d][q] in allocated[s])
}

-- DELETE: remove a v-position from a document's v-space
pred Delete[s, s2: State, d: IAddr, q: VPos] {
  d in s.docs
  some s.vmap[d][q]
  -- effect: remove the mapping at q
  s2.vmap[d] = s.vmap[d] - (q -> IAddr)
  -- frame: other documents unchanged
  all d2: IAddr - d | s2.vmap[d2] = s.vmap[d2]
  s2.docs = s.docs
  -- P3 frame: i-space unchanged
  s2.iota = s.iota
}

-- REARRANGE: swap two v-positions in a document
pred Rearrange[s, s2: State, d: IAddr, q1, q2: VPos] {
  d in s.docs
  some s.vmap[d][q1]
  some s.vmap[d][q2]
  q1 != q2
  -- effect: swap the two mappings
  let a1 = s.vmap[d][q1], a2 = s.vmap[d][q2] |
    s2.vmap[d] = s.vmap[d] ++ (q1 -> a2) ++ (q2 -> a1)
  -- frame: other documents unchanged
  all d2: IAddr - d | s2.vmap[d2] = s.vmap[d2]
  s2.docs = s.docs
  -- P3 frame: i-space unchanged
  s2.iota = s.iota
}

-- COPY: copy content from one document position to another
pred Copy[s, s2: State, src: IAddr, qSrc: VPos, dst: IAddr, qDst: VPos] {
  src in s.docs
  dst in s.docs
  some s.vmap[src][qSrc]
  no s.vmap[dst][qDst]
  -- effect: add mapping in destination pointing to same i-address
  s2.vmap[dst] = s.vmap[dst] + (qDst -> s.vmap[src][qSrc])
  -- frame: other documents unchanged
  all d2: IAddr - dst | s2.vmap[d2] = s.vmap[d2]
  s2.docs = s.docs
  -- P3 frame: i-space unchanged
  s2.iota = s.iota
}

-- P3: i-space non-extension for DELETE
assert DeleteNonExtension {
  all s, s2: State, d: IAddr, q: VPos |
    (wellFormed[s] and Delete[s, s2, d, q]) implies
      (allocated[s2] = allocated[s] and s2.iota = s.iota)
}

-- P3: i-space non-extension for REARRANGE
assert RearrangeNonExtension {
  all s, s2: State, d: IAddr, q1, q2: VPos |
    (wellFormed[s] and Rearrange[s, s2, d, q1, q2]) implies
      (allocated[s2] = allocated[s] and s2.iota = s.iota)
}

-- P3: i-space non-extension for COPY
assert CopyNonExtension {
  all s, s2: State, src, dst: IAddr, qSrc, qDst: VPos |
    (wellFormed[s] and Copy[s, s2, src, qSrc, dst, qDst]) implies
      (allocated[s2] = allocated[s] and s2.iota = s.iota)
}

-- Non-vacuity: a well-formed Delete transition exists
run NonVacuity {
  some s, s2: State, d: IAddr, q: VPos |
    wellFormed[s] and Delete[s, s2, d, q] and wellFormed[s2]
} for 5 but exactly 2 State

check DeleteNonExtension for 5 but exactly 2 State
check RearrangeNonExtension for 5 but exactly 2 State
check CopyNonExtension for 5 but exactly 2 State
