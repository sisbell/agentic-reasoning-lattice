**Definition (SubspaceVPositionSet).** For a document d and subspace identifier S, the subspace V-position set V_S(d) is the subset of V-positions in d whose subspace component equals S:

V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S}

where subspace(v) = v₁ extracts the first component of V-position v. The set V_S(d) collects all active V-positions in document d that belong to subspace S. When V_S(d) is non-empty, all its members share a common tumbler depth by S8-depth.

*Definition:* `V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S}` — the set of V-positions in subspace S of document d, where `subspace(v) = v₁`
