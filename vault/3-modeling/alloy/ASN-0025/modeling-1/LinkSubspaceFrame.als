-- LinkSubspaceFrame: REARRANGE preserves link-position mappings

abstract sig Tag {}
one sig TextTag, LinkTag extends Tag {}

sig IAddr {}

sig VPos {
  tag: one Tag,
  ord: one Int
} {
  ord > 0
}

sig Doc {}

sig State {
  vmap: Doc -> VPos -> lone IAddr
}

pred isLink[q: VPos] {
  q.tag = LinkTag
}

pred isText[q: VPos] {
  q.tag = TextTag
}

pred Rearrange[s, sPost: State, d: Doc] {
  -- precondition: d has at least two text positions
  some disj q1, q2: VPos |
    isText[q1] and isText[q2] and
    some s.vmap[d][q1] and some s.vmap[d][q2]

  -- postcondition: text-mapped addresses are conserved
  let textPre  = {q: VPos | isText[q] and some s.vmap[d][q]},
      textPost = {q: VPos | isText[q] and some sPost.vmap[d][q]} |
    textPre.(s.vmap[d]) = textPost.(sPost.vmap[d])

  -- frame: link positions in d unchanged
  all q: VPos | isLink[q] implies sPost.vmap[d][q] = s.vmap[d][q]

  -- frame: other documents unchanged
  all d2: Doc - d | sPost.vmap[d2] = s.vmap[d2]
}

-- Property: REARRANGE preserves all link-position mappings in the target document
assert LinkSubspaceFrame {
  all s, sPost: State, d: Doc |
    Rearrange[s, sPost, d] implies
      (all q: VPos |
        (some s.vmap[d][q] and isLink[q]) implies
          sPost.vmap[d][q] = s.vmap[d][q])
}

-- Non-vacuity: a rearrangement that actually changes something exists
run NonVacuity {
  some s, sPost: State, d: Doc |
    Rearrange[s, sPost, d] and not (s = sPost)
} for 5 but exactly 2 State, 4 Int

check LinkSubspaceFrame for 5 but exactly 2 State, 4 Int
