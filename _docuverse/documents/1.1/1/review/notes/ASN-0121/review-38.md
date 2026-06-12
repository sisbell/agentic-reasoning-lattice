# Review of ASN-0121

## REVISE

### Issue 1: The preamble's `coverage` gloss contradicts both the foundation definition and this ASN's own home-slot semantics

**ASN-0121, opening section (state paragraph)**: "We use `coverage(e)` (ASN-0043) for the set of I-addresses an endset references"

**Problem**: ASN-0043 defines `coverage(e)` as "the set of all tumbler addresses referenced by the endset" — not I-addresses — and this ASN's residence machinery *depends* on that generality. `athome(a, H) ≡ home(a) ∈ coverage(H)` tests a document-level tumbler (`zeros = 2`) against `coverage(H)`; an I-address is element-level (`zeros = 3`), so under the gloss as written `athome` would be identically false and the entire home slot would be vacuous. The ASN's own subsequent text gets it right ("Every component thus denotes, through `coverage` (ASN-0043), a set of tumbler addresses"), and Trace 6's `H_d`, `H_other`, `H_node` coverages all contain organizational tumblers, as does the wide element-rooted example `[1,0,1,0,2] ∈ coverage((p, ℓ))`. Two statements of the same notation disagree, and the one a reader meets first is the wrong one.

**Required**: Reword the gloss to "the set of tumbler addresses an endset references" (matching ASN-0043's definition and the later sentence). No other use of "I-address" needs to change — the regime name "I-address request" is introduced after the correct phrasing and is fine as a label contrasting with V-spec naming.

### Issue 2: Citation-validity meta-prose in the FTT-notation paragraph

**ASN-0121, "Notation — the FTT subscript"**: "where this ASN routes through ASN-0127's lemmas (F-PRES, F-CIL), each is applied on its own stated hypotheses to `findlinks_FTT`'s defining comprehension"

**Problem**: Anti-bloat finding. This clause defends the validity of citations rather than stating anything about the operation: F-PRES is stated over `Σ.L`-preservation and F-CIL over comprehensions generally — neither mentions the `findlinks` symbol, so no post-rename ambiguity existed for them and the reassurance does no work. By contrast, the adjacent clause ("the second phase of `findlinks_V` (F-V) remains the foundation's bare `findlinks`, not the present operation") resolves a real ambiguity a reader could hit after the rename, and the three-point contrast (i)–(iii) with its non-restriction witnesses is substantive. The paragraph should keep those and drop only the defensive clause.

**Required**: Delete "each is applied on its own stated hypotheses to `findlinks_FTT`'s defining comprehension"; retain the (i)–(iii) disagreements, the two non-restriction witnesses, and the F-V clause.

## OUT_OF_SCOPE

### Topic 1: Result presentation and ordering
Nelson's phrasing is "returns a **list** of all links"; the ASN specifies the answer as a set and is silent on enumeration order. **Why out of scope**: ordering only acquires content with paginated retrieval (FINDNEXTNLINKSFROMTOTHREE), which the scope note explicitly defers; the set-valued answer is the right abstract core for this ASN.

### Topic 2: Constrained search over higher slots (n-set search)
`sat` deliberately leaves `e₄ … e_N` unconstrained, and the ASN notes Nelson's call for n-set support (4/79). A future operation that constrains slots beyond the first three is new territory. **Why out of scope**: FINDLINKS*FROMTOTHREE* is positionally defined over the first three slots; extending the request grammar to higher arities is a different operation, not an error here.

---

The core machinery checks out under detailed verification: the forcing argument for FL-DEF genuinely closes the `R_min`/`R_max` slack; the `nullified`-monotonicity argument correctly splits F-PRES steps (link store fixed, hence `nullified` fixed) from K.λ (R6a); FL-WP's three cases partition exhaustively on retraction-relation membership, the arity-3 cut against ASN-0086's `L_R` is handled correctly (higher-arity retraction-typed links route to case (a) and do not nullify), and both directions of the `nullified(Σ')` membership equation are derived, which is what licenses the "weakest" claim in case (c). All seven traces verify arithmetically, including the straddling-span example `p ⊕ ℓ = [1,0,1,0,2,1,1,1]` containing the document tumbler, the frontier addresses in Trace 7, and the `nullified` computations in Traces 4 and 7. The ghost-pre-coverage and self-retraction hazards are exactly the non-vacuous conjuncts a wp analysis should surface, and both are exercised concretely.

VERDICT: REVISE
