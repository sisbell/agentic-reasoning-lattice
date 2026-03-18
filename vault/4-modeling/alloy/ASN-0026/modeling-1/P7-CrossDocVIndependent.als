-- P7-CrossDocVIndependent
-- Property: operations on a target document do not alter V-space of other documents.
-- P7: (A d' : d' in Sigma.D /\ d' != target(op) : Sigma'.V(d') = Sigma.V(d'))

sig Addr {}
sig DocId {}

sig State {
  docs: set DocId,
  vspace: DocId -> Int -> lone Addr
}

-- V-space entries exist only for documents in docs
fact VSpaceDomain {
  all s: State, d: DocId |
    (some i: Int | some s.vspace[d][i]) implies d in s.docs
}

-- P7 predicate: cross-document V-independence
pred crossDocVIndependent[s, sPost: State, target: DocId] {
  all d2: s.docs - target | sPost.vspace[d2] = s.vspace[d2]
}

--------------------------------------------------------------
-- Operations (each specifies its target and frame condition)
--------------------------------------------------------------

-- INSERT: writes target document d
pred Insert[s, sPost: State, d: DocId] {
  d in s.docs
  sPost.docs = s.docs
  -- target vspace may change (unconstrained for d)
  -- frame: non-target V-space unchanged
  all d2: s.docs - d | sPost.vspace[d2] = s.vspace[d2]
}

-- DELETE: writes target document d
pred Delete[s, sPost: State, d: DocId] {
  d in s.docs
  sPost.docs = s.docs
  all d2: s.docs - d | sPost.vspace[d2] = s.vspace[d2]
}

-- REARRANGE: writes target document d
pred Rearrange[s, sPost: State, d: DocId] {
  d in s.docs
  sPost.docs = s.docs
  all d2: s.docs - d | sPost.vspace[d2] = s.vspace[d2]
}

-- COPY: writes the target (destination) document; source is read-only
pred Copy[s, sPost: State, src: DocId, tgt: DocId] {
  src in s.docs
  tgt in s.docs
  sPost.docs = s.docs
  -- frame: all docs except tgt unchanged (including src)
  all d2: s.docs - tgt | sPost.vspace[d2] = s.vspace[d2]
}

-- CREATENEWVERSION: creates a new document; writes no existing document
pred CreateNewVersion[s, sPost: State, d: DocId, newDoc: DocId] {
  d in s.docs
  newDoc not in s.docs
  sPost.docs = s.docs + newDoc
  -- frame: ALL existing docs unchanged
  all d2: s.docs | sPost.vspace[d2] = s.vspace[d2]
}

--------------------------------------------------------------
-- Assertions: P7 holds for each operation
--------------------------------------------------------------

assert InsertPreservesCrossDoc {
  all s, sPost: State, d: DocId |
    Insert[s, sPost, d] implies crossDocVIndependent[s, sPost, d]
}

assert DeletePreservesCrossDoc {
  all s, sPost: State, d: DocId |
    Delete[s, sPost, d] implies crossDocVIndependent[s, sPost, d]
}

assert RearrangePreservesCrossDoc {
  all s, sPost: State, d: DocId |
    Rearrange[s, sPost, d] implies crossDocVIndependent[s, sPost, d]
}

assert CopyPreservesCrossDoc {
  all s, sPost: State, src, tgt: DocId |
    Copy[s, sPost, src, tgt] implies crossDocVIndependent[s, sPost, tgt]
}

assert CreateNewVersionPreservesCrossDoc {
  all s, sPost: State, d, newDoc: DocId |
    CreateNewVersion[s, sPost, d, newDoc] implies crossDocVIndependent[s, sPost, newDoc]
}

--------------------------------------------------------------
-- Non-vacuity: confirm operations are satisfiable
--------------------------------------------------------------

run NonVacuityInsert {
  some s, sPost: State, d: DocId |
    Insert[s, sPost, d] and #s.docs > 1
} for 4 but exactly 2 State

run NonVacuityCopy {
  some s, sPost: State, src, tgt: DocId |
    Copy[s, sPost, src, tgt] and src != tgt and #s.docs > 1
} for 4 but exactly 2 State

--------------------------------------------------------------
-- Checks
--------------------------------------------------------------

check InsertPreservesCrossDoc for 5 but exactly 2 State
check DeletePreservesCrossDoc for 5 but exactly 2 State
check RearrangePreservesCrossDoc for 5 but exactly 2 State
check CopyPreservesCrossDoc for 5 but exactly 2 State
check CreateNewVersionPreservesCrossDoc for 5 but exactly 2 State
