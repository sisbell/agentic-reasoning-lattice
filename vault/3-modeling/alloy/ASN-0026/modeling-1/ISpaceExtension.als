-- ISpaceExtension (+_ext lemma, ASN-0026)
-- For any operation, I-space is only ever extended: old mappings are
-- preserved and new addresses (if any) are fresh.

sig Addr {}
sig Byte {}
sig Doc {}

sig State {
  ispace: Addr -> lone Byte,
  docs: set Doc,
  vmap: Doc -> Addr
}

-- Domain of I-space (allocated addresses)
fun allocated[s: State]: set Addr {
  (s.ispace).Byte
}

-- Well-formedness: V-space references only allocated addresses;
-- vmap defined only for existing docs
pred wellFormed[s: State] {
  all d: s.docs | d.(s.vmap) in allocated[s]
  all d: Doc - s.docs | no d.(s.vmap)
}

-- The extension property
pred ISpaceExtends[s, s2: State] {
  s.ispace in s2.ispace
}

---------- Operations ----------

-- DELETE: remove V-space references, I-space unchanged
pred Delete[s, s2: State, d: Doc] {
  d in s.docs
  s2.ispace = s.ispace
  s2.docs = s.docs
  d.(s2.vmap) in d.(s.vmap)
  all d2: Doc - d | d2.(s2.vmap) = d2.(s.vmap)
}

-- INSERT: allocate fresh addresses, extend I-space, add to V-space
pred Insert[s, s2: State, d: Doc] {
  d in s.docs
  let fresh = allocated[s2] - allocated[s] {
    some fresh
    -- Frame: old I-space mappings preserved
    all a: allocated[s] | s2.ispace[a] = s.ispace[a]
    -- Fresh addresses each get exactly one byte
    all a: fresh | one s2.ispace[a]
    -- V-space: doc keeps old addresses and gains some fresh ones
    d.(s.vmap) in d.(s2.vmap)
    d.(s2.vmap) - d.(s.vmap) in fresh
    -- Other docs unchanged
    all d2: Doc - d | d2.(s2.vmap) = d2.(s.vmap)
    s2.docs = s.docs
  }
}

-- REARRANGE: reorder within a doc; I-space and address set unchanged
pred Rearrange[s, s2: State, d: Doc] {
  d in s.docs
  s2.ispace = s.ispace
  s2.docs = s.docs
  d.(s2.vmap) = d.(s.vmap)
  all d2: Doc - d | d2.(s2.vmap) = d2.(s.vmap)
}

-- COPY: share existing addresses to another doc, I-space unchanged
pred Copy[s, s2: State, src, tgt: Doc] {
  src in s.docs
  tgt in s.docs
  s2.ispace = s.ispace
  s2.docs = s.docs
  tgt.(s.vmap) in tgt.(s2.vmap)
  tgt.(s2.vmap) - tgt.(s.vmap) in src.(s.vmap)
  all d2: Doc - tgt | d2.(s2.vmap) = d2.(s.vmap)
}

-- CREATENEWVERSION: new doc sharing addresses from original, I-space unchanged
pred CreateNewVersion[s, s2: State, orig, ndoc: Doc] {
  orig in s.docs
  ndoc not in s.docs
  s2.ispace = s.ispace
  s2.docs = s.docs + ndoc
  ndoc.(s2.vmap) in orig.(s.vmap)
  all d2: Doc - ndoc | d2.(s2.vmap) = d2.(s.vmap)
}

---------- Combined operation ----------

pred AnyOp[s, s2: State] {
  (some d: Doc | Delete[s, s2, d])
  or (some d: Doc | Insert[s, s2, d])
  or (some d: Doc | Rearrange[s, s2, d])
  or (some src, tgt: Doc | Copy[s, s2, src, tgt])
  or (some orig, ndoc: Doc | CreateNewVersion[s, s2, orig, ndoc])
}

---------- Assertion ----------

assert ISpaceExtension {
  all s, s2: State |
    (wellFormed[s] and AnyOp[s, s2]) implies ISpaceExtends[s, s2]
}

---------- Checks ----------

check ISpaceExtension for 5 but exactly 2 State

---------- Non-vacuity ----------

run NonVacuity {
  some s, s2: State |
    wellFormed[s] and AnyOp[s, s2] and s != s2
} for 4 but exactly 2 State
