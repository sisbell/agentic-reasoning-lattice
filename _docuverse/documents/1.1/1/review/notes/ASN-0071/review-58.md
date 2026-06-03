# Review of ASN-0071

## REVISE

### Issue 1: S8-depth misquoted — `m_C` is not the depth of *every* arrangement position

**ASN-0071, *Resolution* (PC-RANGE discussion)**: "PC-RANGE's range condition at component `#u` couples to the arrangement's content-subspace depth `m_C` (S8-depth, which fixes `#v = m_C` for every `v ∈ dom(M(d_s))`)"

**Problem**: S8-depth fixes a common depth *per subspace*, not across the whole arrangement. A document carrying link-subspace positions has those at depth `m_L`, which need not equal `m_C`. So "fixes `#v = m_C` for every `v ∈ dom(M(d_s))`" is false in general. The conclusion you actually use (content-subspace positions have depth `m_C`) is correct because PC confines `⟦σ⟧` to `s_C`, but the stated reason overclaims. Note F-DEEP gets this right ("every content-subspace `v ∈ dom(M(d_s))`"); this parenthetical is the inconsistent one.

**Required**: Restrict the parenthetical to content-subspace positions: "S8-depth fixes `#v = m_C` for every *content-subspace* `v ∈ dom(M(d_s))`."

### Issue 2: Anti-bloat — `wp-defined` is established twice

**ASN-0071, *The operation* (*Well-definedness precondition*)**: "The type signature presents `Q` and `Σ` as independent arguments, but `iaddrs(Q)(Σ)` consults `Σ.M(d_s)` ... meaningful only when `d_s ∈ Σ.E_doc` — exactly the precondition `wp-defined` named in *Resolution*."

**Problem**: *Resolution* already named and motivated `wp-defined` ("Resolution consults `Σ.M(d_s)` for each source `d_s`, so it is meaningful only at a state Σ where each named arrangement is defined"). This paragraph re-derives the same conclusion in different words and even acknowledges it ("exactly the precondition ... named in *Resolution*"). Two paragraphs in two sections saying the same thing.

**Required**: Collapse to a one-line pointer — state that `find` inherits `wp-defined` as its domain — rather than re-deriving the definedness argument.

### Issue 3: Anti-bloat — F-CONTENT over-justifies a trivial set identity

**ASN-0071, *The operation* (*Only content sharing can satisfy the predicate*)**: "`ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ⊆ (dom(Σ.C) ∪ dom(Σ.L)) ∩ dom(Σ.C) = dom(Σ.C)`, where the left factor ... is S3★ ∧ S3★-aux and the right factor ... is the subspace-confinement subset claim above; the product set evaluates to `dom(Σ.C)` since `dom(Σ.C) ⊆ dom(Σ.C) ∪ dom(Σ.L)`."

**Problem**: `(C ∪ L) ∩ C = C` is trivially true; the trailing clause spells out the membership reasoning for an identity no reader needs walked through. Essay content padding a one-line step.

**Required**: State the two inclusions and the result; drop the "where the left factor ... product set evaluates to" gloss.

### Issue 4: F-DEEP and the empty-source case have no concrete trace

**ASN-0071, *Resolution* / *A worked scenario***: F-DEEP (`#u > m_C ⟹ iaddrs_one = ∅`) and the empty-source case (`V_{s_C}(d_s) = ∅ ⟹ ∅`) are asserted with derivation, but the worked scenario only exercises the *shallow* cross-depth case (`#u = 2 < m_C = 3`).

**Problem**: The deep-anchor and empty-source results are the counterintuitive corner of the operation (a well-formed-looking vspec resolves to nothing). Per the rigor standard, key postconditions should be checked against a concrete scenario; the dual of the cross-depth example is exactly where a reader wants to see the empty result land.

**Required**: Add a short trace — e.g. submit a depth-3 anchor against `d_A` (where `m_C = 2`) and show `⟦σ⟧ ∩ dom(M(d_A)) = ∅`, hence `iaddrs_one = ∅`.

## OUT_OF_SCOPE

### Topic 1: Relationship between current result and provenance relation `R`
Properly deferred in *Currency* and Open Questions. The current/ever-containing distinction belongs in a future ASN; not an error here.

### Topic 2: Rejection vs. silent filtering of unresolvable positions
F-FILT fixes the silent-filter semantics; whether the system should instead reject is an Open Question, correctly out of scope.

VERDICT: REVISE
