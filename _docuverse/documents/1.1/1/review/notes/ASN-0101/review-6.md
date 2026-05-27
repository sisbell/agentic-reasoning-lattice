# Review of ASN-0101

## REVISE

### Issue 1: Containment precondition reduction skips the lex-order argument

**ASN-0101, "The operation" section, D0 preconditions**: "writing `r := s ⊕ ℓ`, every depth-`m_S` position `v` with `subspace(v) = S` and `s ≤ v < r` lies in `V_S(d)`. Under D-SEQ★ this reduces to `s = [S, 1, ..., 1, p]` for some `p ∈ {1, ..., n_S}` and `p + n − 1 ≤ n_S`, equivalently `p + n ≤ n_S + 1`."

**Problem**: The reduction is correct but its derivation is omitted. A depth-`m_S` position `v` with `subspace(v) = S` could in principle have *any* values in its middle components — not necessarily `1`. The fact that lex-order constraints `s ≤ v < r` (with `s = [S, 1, ..., 1, p]` and `r = [S, 1, ..., 1, p + n]`) *force* `v[2..m_S − 1]` to equal `1` (because any larger middle component would push `v > r`, and S8a forbids smaller) is the load-bearing step that converts the universal containment condition into a counting inequality. Skipping it leaves the reader to reconstruct the argument.

**Required**: A one-paragraph justification showing that for `v` in the half-open interval and at the fixed depth and subspace, T1 case (i) applied at the first divergence position forces `v[j] = 1` for `2 ≤ j < m_S`, reducing the universal to a constraint on the last component alone.

### Issue 2: "K.μ~ exclusively over the content subspace" overreaches

**ASN-0101, "The operation" section**: "Moreover, ASN-0047 defines K.μ~ exclusively over the content subspace — its precondition `|dom_C(M(d))| ≥ 2` ranges over `V_{s_C}(d)`, not over `V_S(d)` for arbitrary S, and the foundation supplies no analogue K.μ~_L over the link subspace."

**Problem**: ASN-0047's K.μ~ effect is over the *full* domain `dom(M(d))` — the bijection equation `(E π : π is a bijection dom(M(d)) → dom(M'(d)) : ...)` is not restricted to the content subspace. Only the cardinality precondition `|dom_C(M(d))| ≥ 2` references the content subspace. The substantive point (that K.μ~ + K.μ⁻ cannot be invoked when `|dom_C(M(d))| < 2`, blocking the composite-substitute strategy for some link-subspace deletions) is correct, but the phrasing as written misdescribes K.μ~'s scope.

**Required**: Rephrase as "K.μ~'s admissibility *precondition* references only content-subspace cardinality" or similar — preserving the substantive argument without overclaiming about the operation's effect.

### Issue 3: Undefined notation `|dom_S(M(d))|`

**ASN-0101, "The operation" section**: "On an interior span with `|dom_S(M(d))| ≥ 2`, one could in principle apply `K.μ~`..."

**Problem**: The notation `dom_S(M(d))` parameterized by subspace `S` is not defined in this ASN or its cited foundations. ASN-0047 uses `dom_C(M(d))` and (implicitly) `dom_L(M(d))` as fixed names. A subspace-parameterized form `dom_S` does not appear in the foundation vocabulary. The reader can guess this means `V_S(d)`, but the notation should match what is used.

**Required**: Either define `dom_S(M(d)) := V_S(d)` once at the operation specification, or rewrite using the existing `|V_S(d)|` notation throughout.

### Issue 4: Boundary cases assert D8 holds without case-by-case verification

**ASN-0101, "Boundary cases" section**: "In each case, D0's effect, D1's gap-closure characterisation, and D8's well-formedness preservation hold. The specification is not specialised by case; the same formulas apply, and degenerate sub-expressions (empty `Λ`, `Ρ`, or `Q`) reduce predictably."

**Problem**: The section enumerates five boundary configurations (empty post-state, deletion at the start, deletion at the end, singleton subspace deletion, singleton interior deletion) and concludes with the unsupported assertion above. The degenerate cases involve real verification work — for instance, when `n_S = n` the empty post-state forces D-CTG★, D-MIN★, D-SEQ★ vacuous, but S8a, S8-fin, S3★, S8-depth are also reduced to vacuous predicates over `V_S(M'(d)) = ∅`; the reader is told this happens "predictably" but is not walked through how each invariant's quantifier degrades. The deletion-at-the-start case is more subtle: D-MIN★ requires the post-state minimum to equal `[S, 1, ..., 1]` of depth `m_S`, and the verification rests on `σ_d(r) = [S, 1, ..., 1, 1]` — mentioned in the section but not connected to the D-MIN★ obligation.

**Required**: For at least the two non-trivial cases (empty post-state and deletion-at-the-start), explicitly trace which D8 invariant clauses degrade to vacuous form, and which clauses receive a non-vacuous witness from `σ_d`. Right now the section reads as "we considered cases; they work" rather than as a proof.

## OUT_OF_SCOPE

### Topic 1: ASN-0098's LP-Comp coverage extension for DEL

ASN-0098's LP-Comp is a documentation note recording that LP4–LP14 form a covering case-analysis on the transition vocabulary established by ASN-0047 + ASN-0093. Adding DEL as a new atomic transition kind means LP-Comp's "every atomic transition is governed by one of [LP4-LP14]" claim no longer fully covers the vocabulary. ASN-0101's D9 supplies a per-document, per-subspace projection characterization for DEL that fills the gap, but the foundation lemma itself would need re-stating with DEL added.

**Why out of scope**: This is foundation-maintenance follow-up, not a correctness gap in ASN-0101's own claims.

### Topic 2: Versioning and recoverability mechanisms

The ASN's "A note on recoverability and historical reconstruction" section observes that DEL supplies the *substrate* for recoverability via D2 + D5 but not the *mechanism* (which is versioning via J4 ForkComposite). Several open questions ask about the interaction between DEL and versioning operations, the conditions under which DEL is fully reversible relative to an observer's view, etc.

**Why out of scope**: Versioning mechanics belong in subsequent ASNs that build the version-graph machinery; DEL's preservation guarantees are stated as necessary but not sufficient.

VERDICT: REVISE
