-- D10-ext — PublicationFrame (FRAME, ensures)
--
--   For any ASN-0026 operation (INSERT, DELETE, COPY, REARRANGE):
--     (A d : d in Sigma.D : Sigma'.pub(d) = Sigma.pub(d))
--
-- Publication status is unchanged by structural operations.

sig Doc {}
sig Element {}

abstract sig PubStatus {}
one sig Private, Published, Privashed extends PubStatus {}

sig State {
  D: set Doc,
  pub: Doc -> lone PubStatus,
  elems: Doc -> set Element
} {
  pub in D -> PubStatus
  all d: D | one pub[d]
  (elems).Element in D
}

----------------------------------------------------------------------
-- ASN-0026 structural operations
----------------------------------------------------------------------

-- INSERT: add an element to a document
pred Insert[s, sPost: State, d: Doc, e: Element] {
  d in s.D
  e not in s.elems[d]
  sPost.D = s.D
  sPost.elems = s.elems + d -> e
  -- frame: pub unchanged
  sPost.pub = s.pub
}

-- DELETE: remove an element from a document
pred Delete[s, sPost: State, d: Doc, e: Element] {
  d in s.D
  e in s.elems[d]
  sPost.D = s.D
  sPost.elems = s.elems - (d -> e)
  -- frame: pub unchanged
  sPost.pub = s.pub
}

-- COPY: copy an element from one document to another
pred Copy[s, sPost: State, src: Doc, dst: Doc, e: Element] {
  src in s.D
  dst in s.D
  e in s.elems[src]
  sPost.D = s.D
  sPost.elems = s.elems + dst -> e
  -- frame: pub unchanged
  sPost.pub = s.pub
}

-- REARRANGE: move an element between documents
pred Rearrange[s, sPost: State, src: Doc, dst: Doc, e: Element] {
  src in s.D
  dst in s.D
  src != dst
  e in s.elems[src]
  sPost.D = s.D
  sPost.elems = s.elems - (src -> e) + (dst -> e)
  -- frame: pub unchanged
  sPost.pub = s.pub
}

-- Any ASN-0026 structural operation
pred StructuralOp[s, sPost: State] {
  (some d: Doc, e: Element | Insert[s, sPost, d, e])
  or (some d: Doc, e: Element | Delete[s, sPost, d, e])
  or (some src, dst: Doc, e: Element | Copy[s, sPost, src, dst, e])
  or (some src, dst: Doc, e: Element | Rearrange[s, sPost, src, dst, e])
}

----------------------------------------------------------------------
-- D10-ext assertion
----------------------------------------------------------------------

assert PublicationFrame {
  all s, sPost: State |
    StructuralOp[s, sPost] implies
      (all d: s.D | sPost.pub[d] = s.pub[d])
}

check PublicationFrame for 5 but exactly 2 State

-- Non-vacuity: a structural operation can occur on a nonempty state
run NonVacuity {
  some s, sPost: State |
    StructuralOp[s, sPost] and some s.D
} for 4 but exactly 2 State
