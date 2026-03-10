-- A5.new — VersionNewDoc (POST, ensures)
-- Property: d' in Sigma'.D and d' not in Sigma.D
-- A new document appears in the post-state that was absent from the pre-state.

sig Doc {}

sig State {
  docs: set Doc
}

-- VersionNewDoc operation: creates a fresh document
pred VersionNewDoc[s, sPost: State, dNew: Doc] {
  -- POST: the new doc is in post-state
  dNew in sPost.docs

  -- POST: the new doc was not in pre-state
  dNew not in s.docs

  -- frame: existing docs preserved, only dNew added
  sPost.docs = s.docs + dNew
}

-- A5.new: VersionNewDoc guarantees d' in Sigma'.D and d' not in Sigma.D
assert A5_VersionNewDoc {
  all s, sPost: State, dNew: Doc |
    VersionNewDoc[s, sPost, dNew] implies
      (dNew in sPost.docs and dNew not in s.docs)
}

-- Non-vacuity: a valid VersionNewDoc instance exists
run FindVersionNewDoc {
  some s, sPost: State, dNew: Doc |
    VersionNewDoc[s, sPost, dNew]
} for 4 but exactly 2 State

check A5_VersionNewDoc for 5 but exactly 2 State
