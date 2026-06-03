# Review of ASN-0071

## REVISE

### Issue 1: The `d_s ∈ E_doc` precondition is stated three times

**ASN-0071, *The query* / *Resolution* / *The operation***: The vspec definition says "`d_s ∈ Σ.E_doc` names a source document"; *Resolution* re-establishes it ("For `Σ.M(d_s)` to be a defined arrangement — `dom(Σ.M) = Σ.E_doc` (M1) — we require `d_s ∈ Σ.E_doc`; under that condition…"); and *The operation* formalizes the identical condition again as `wp-defined`.

**Problem**: The same membership requirement carries its own explanation in three slots. The *Resolution* gating prose and `wp-defined` are evaluated at the same (evaluation) state and are pure duplicates. The vspec-definition copy additionally conflates a *syntactic* pair `(d_s, σ)` with a *semantic* state-membership fact against an unfixed `Σ` — leaving ambiguous which state's `E_doc` the vspec definition refers to.

**Required**: Pick one home for the semantic precondition (`wp-defined`) and make the vspec a syntactic object whose well-definedness against `Σ` is established solely there. Remove the redundant gating sentence in *Resolution* (just reference `wp-defined`).

### Issue 2: Two paragraphs in *Home versus transcluding documents* say the same thing

**ASN-0071, *Home versus transcluding documents***: Paragraph 1 already states the query "discovers every document referencing `a` at once: `a`'s home document `origin(a)` … and every transcluding document, all reported as equally-qualifying." Paragraph 2 restates this in different words ("The find operation does not distinguish home from transcluding document: both reference `a`, both satisfy the predicate … the distinction is nonetheless recoverable … `origin(a)` names `a`'s home document, and comparing it against each `d ∈ find(Q)` recovers the relationship").

**Problem**: Both paragraphs make one point — home and transcluder both qualify, and `origin(a)` recovers the distinction. F-ORIGIN already records the recoverability claim. This is duplicated prose around a single forward-stable fact.

**Required**: Collapse to one paragraph stating the fact once; let F-ORIGIN carry the recoverability claim.

### Issue 3: Meta-prose justifying the F-COMP / F-SOUND labels

**ASN-0071, *The operation***: "Neither is a result beyond the definition; the labels name the halves of the iff for downstream reference."

**Problem**: This sentence advances no reasoning about the operation; it justifies *why the labels exist* and enumerates a downstream use ("for downstream reference"). That is exactly the use-site/defensive meta-prose this note should shed. The preceding sentence already states the biconditional is its own soundness/completeness statement.

**Required**: Delete the sentence. Keep the iff and the two label assignments; drop the justification for labeling.

### Issue 4: Cross-depth width-dependence argued twice around PC-RANGE

**ASN-0071, *A cross-depth query* / *Cross-depth capture, in general***: Before the derivation: "This is the *width-1* instance of cross-depth capture (PC-RANGE, derived below) … The width dependence is essential: a width-2 span … would denote `v_{#u} ∈ {1, 2}`, capturing *two* sibling subtrees, not 'the' subtree. PC-RANGE makes the dependence explicit." After the derivation: "The width-1 case `ℓ_{#u} = 1` pins `v_{#u} = u_{#u}` … There is no blanket 'prefix names subtree' guarantee: the subtree reading is exactly the width-1 specialisation of PC-RANGE."

**Problem**: The "width dependence is essential / no blanket prefix-names-subtree" point is made both before (with a forward "derived below" pointer) and after the PC-RANGE derivation. The width-2-captures-two-subtrees observation and the width-1-specialisation observation are the same content split across the forward reference.

**Required**: State the width-dependence consequence once, after the derivation, where PC-RANGE's `ℓ_{#u}` parameter is in hand. Remove the pre-derivation duplicate and the "derived below" forward pointer.

## OUT_OF_SCOPE

### Topic 1: Relationship between current-containment result and the historical relation `R`
**Why out of scope**: The ASN correctly defers the current-vs-ever-containing question to Open Questions; `R`-coupling is a future ASN, not a defect here.

### Topic 2: Rejecting versus silently filtering unresolvable vspec positions
**Why out of scope**: F-FILT fixes the silent-drop semantics; whether the system should instead reject is a policy question deferred to Open Questions.

VERDICT: REVISE
