# Review of ASN-0112

## REVISE

### Issue 1: V8 cross-state depth invariance is not established by the cited invariant
**ASN-0112, V8 / "The origin is permanent" section**: "while the content subspace is non-empty, `origin_d = [s_C,1,…,1]`, invariant under all editing that leaves content present. (The depth `m_C` is fixed throughout any content-present regime, by S8-depth.)"
**Problem**: V8 asserts `origin_d` is a *fixed tumbler* across all content-present edits. For `[s_C,1,…,1]` to denote the same tumbler across states, its length `m_C` must be constant across those states. The parenthetical attributes that constancy to S8-depth — but S8-depth is a *per-state* invariant (within one state, all positions of a subspace share a depth). It says nothing about `m_C` being equal between two distinct content-present states. The actual ground for cross-state constancy is the re-pinning discipline (ASN-0047's `m_S(d)`: re-pinned only after full subspace clearance, hence fixed while non-empty). As cited, the load-bearing step of V8 is unsupported.
**Required**: Cite the re-pinning discipline (the `m_S(d)` definition's "re-pins only after full clearance" clause) as the source of cross-state `m_C` constancy, rather than S8-depth; or derive the cross-state invariance explicitly.

### Issue 2: V17 is implementation mechanics, not a system invariant
**ASN-0112, V17 / "The extent is a well-formed, non-negative displacement"**: "prior deletions may drive intermediate arrangement-tree entries negative, but the root width is recomputed as a max-minus-min reach (Q18) … (abstract positivity is V2's)."
**Problem**: The note itself concedes the abstract guarantee is already V2's. V17's only remaining content — intermediate enfilade entries going negative, root width recomputed by max-minus-min — describes Gregory's tree internals, which no alternative implementation is obliged to reproduce. Stepping back per the review standard: a claim belongs in the spec when "an alternative implementation would also need to satisfy it." An alternative must satisfy V2 (positive extent); it need not have negative intermediate entries or a max-minus-min recomputation. V17, as a numbered claim in the table, specifies implementation mechanics rather than a system guarantee.
**Required**: Remove V17 from the claims table, folding its implementation-confirmation into a remark under V2 (as evidence, not as an introduced guarantee). The abstract obligation is V2 alone.

### Issue 3: Defensive reachability construction inlined into V5
**ASN-0112, "Single subspace: exact cover"**: "the link subspace (`s = s_L`), reachable by `CREATENEWDOCUMENT` then `K.λ` + `K.μ⁺_L` with endsets referencing content elsewhere per L4/L9"
**Problem**: V5 is a claim about exact cover. The parenthetical detours into an operational construction sequence to defend that the link-only sub-case is non-vacuous. This is a defensive justification (a flagged anti-bloat pattern): a reader following the exact-cover argument must skip past a reachability recipe that does not advance V5's reasoning.
**Required**: Trim to a bare assertion that link-only documents are reachable (or drop), without the operation/endset construction.

## OUT_OF_SCOPE

(none — the note stays within whole-document boundary-query territory; per-subspace reporting, content delivery, and link discovery are correctly excluded.)

Minor (not blocking): S3★-aux is invoked for the single-vs-both-subspaces exhaustiveness in two separate sections ("Exact cover…" and the wp derivation). The duplication is mild but worth consolidating to one statement.

VERDICT: REVISE
