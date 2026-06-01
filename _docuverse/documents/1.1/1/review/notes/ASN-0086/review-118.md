# Review of ASN-0086

## REVISE

### Issue 1: R6b's universal omits the `a ∈ A_rel` restriction, so the stated lemma is false for non-link `a`

**ASN-0086, R6b (SingleDepthRetraction)**: 

`(A Σ → Σ', a, b, F', G' : (b, F', G') ∈ L_R^Σ ∧ a ∈ coverage(G') : a ∈ nullified(Σ'))`

**Problem**: The conclusion `a ∈ nullified(Σ')` requires, by the Definition of `nullified`, that `a ∈ A_rel^{Σ'} = dom(Σ'.L)` — `nullified(Σ) = {a ∈ A_rel^Σ : (E …)}` carries that membership conjunct. The guard supplies only `(b, F', G') ∈ L_R^Σ` and `a ∈ coverage(G')`. But R6a's own proof stresses that `coverage`'s codomain is `℘(T)`, not `A^Σ`, and "may include addresses outside `dom(Σ.C) ∪ dom(Σ.L)` (L9, TypeGhostPermission)." So `a` may be a ghost or content address in `coverage(G')`; then `a ∉ A_rel^{Σ'}` and `a ∉ nullified(Σ')`, falsifying the conclusion.

The proof asserts "`a ∈ coverage(G')` still witnesses `a ∈ nullified(Σ')`" but never discharges the `a ∈ A_rel^{Σ'}` conjunct. By contrast, R6a *does* discharge it explicitly ("By L12a … `a ∈ dom(Σ.L) ⊆ dom(Σ'.L) = A_rel^{Σ'}`, discharging the `a ∈ A_rel^{Σ'}` predicate required by Definition of `nullified(Σ')`"). R6b is missing exactly the step its sibling lemma performs. The worked example only ever applies R6b to link addresses (`a₁`, `b₁`), confirming the intended-but-unstated restriction.

**Required**: Restrict the quantifier to `a ∈ A_rel^Σ` (then `a ∈ A_rel^{Σ'}` follows by L12a, mirroring R6a), or otherwise establish the membership conjunct in the proof body. As written, the lemma is false for ghost/content `a`.

### Issue 2: Derivation inventories and triplicated forward-references (anti-bloat)

**ASN-0086, Properties Introduced table, R0 and R7a rows**: the "Statement" cells carry paragraph-length dependency inventories — e.g. R7a's "(= L12 + L12a + L-fin + L1a + S7d + ASN-0093 K-op frame conditions + ChainDiscipline + FirstEmission + ChainMembershipForOrigin + ChainEnumerationInjectivity for replay determinism + conforming-layer clause (b) …)". A summary table is a structural slot; a full premise list belongs in the proof, not restated here.

**ASN-0086, R7a lemma statement / proof / table row**: the clause-(b) contingency is stated three times — inline in the lemma ("*under conforming-layer clause (b) … which the discharge (4)(iii) below consumes*"), again in the proof, and again in the table ("the clause-(b) contingency … is stated in the R7a lemma"). The inline forward pointer to "(4)(iii) below" is a deferral embedded in the claim itself.

**Problem**: This is the forward-reference accretion the anti-bloat classifier targets — use-site/dependency inventories in structural slots, and multiple passages deferring to the same downstream location.

**Required**: Move premise lists into proofs; state the clause-(b) contingency once (in the lemma) and drop the duplicate restatements and the inline "(4)(iii) below" pointer.

### Issue 3: Notational slip in the worked sketch

**ASN-0086, Worked Sketch, Step 2**: "the only `L_R` tuple is still at `b₁`, whose `coverage(G')` contains `a₁` but not `a₂` since `a₁` and `a₂` are distinct siblings in `A_{a₁}`."

**Problem**: `A_{a₁}` is undefined; the chain is `A_L(d)`. The same slip recurs implicitly where the sketch reasons about sibling chains.

**Required**: Replace `A_{a₁}` with `A_L(d)`.

## OUT_OF_SCOPE

### Topic 1: Higher-arity typed relations `L_K^{(n)}`
The note restricts `L_K` to standard-triple links (`|Σ.L(a)| = 3`) and explicitly defers the higher-arity construction (and the binary-projection question) to the Open Questions. Defining `L_K^{(n)} ⊆ A_rel × ℘(A)^n` is new territory, not a defect here.

### Topic 2: Concurrency/atomicity of Emit vs. Observe
The consistency model under which `A_K` transitions are observed (Open Questions) is genuinely future work; this ASN fixes only the sequential-transition semantics inherited from ASN-0093.

VERDICT: REVISE
