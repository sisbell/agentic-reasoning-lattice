# Review of ASN-0086

I checked the six R-properties, R-Scope, both wp cases, and the worked sketch. The formal content is sound: R0a's cross-home zero-counting argument, the self-emit branch of R-Scope, the wp biconditionals, and the Step 0–4 tumbler arithmetic (`a₁=…2.1`, `b₁=…2.2`, … `a₃=…2.5`) all check out. The findings below are the meta-prose accretion the `review-mode.anti-bloat` classifier flags, plus one clarity point.

## REVISE

### Issue 1: Nullify "Rationale" is why-prose blocking the operation definition
**ASN-0086, Definition — Nullify**: "*Rationale.* Retraction is a destructive withdrawal, which Nelson scopes by *authority* — *"Only the owner has a right to withdraw a document or change it"* … The ownership-at-Σ versus ownership-at-commit distinction is exactly what separates the two branches…"

**Problem**: This paragraph sits between precondition P-tgt and the actual `Nullify(Σ, d_retr, a) ≡ Emit_R(…)` composition, and explains *why* the two P-tgt branches are both owner-authorized rather than *what* the precondition is. It is the "sub-paragraph labeled 'Rationale' that explains why the axiom is needed rather than what it says" pattern. The reader must skip the entire Nelson-quoting essay to reach the operation. The branches are already fully specified by P1 and the self-emit disjunct; the authority gloss adds no checkable content.

**Required**: Cut to at most one sentence ("the self-emit branch is owned-at-commit; the P1 branch owned-at-Σ"), or relocate the design discussion out of the structural slot.

### Issue 2: wp Case 1 carries branch-by-branch realizability essays
**ASN-0086, WP Case 1**: "*The two disjuncts are distinct and each load-bearing.*" followed by "— *P1 branch* … Dropping P1 *while also forbidding the self-emit branch* admits a counterexample…" and "— *Self-emit branch* … Omitting this disjunct would wrongly reject a pre-state…"

**Problem**: The biconditional derivation already proves the formula *is* the weakest precondition (postcondition ⟺ `a ∈ A_rel^{Σ'}` ⟺ `P1 ∨ self-emit`). The follow-on realizability paragraphs are exhaustiveness/defensive justification re-establishing what the biconditional already gives. This is meta-prose the precise reader works around.

**Required**: Delete the load-bearing/realizability essays; the biconditional plus the one-line mutual-exclusivity remark suffices.

### Issue 3: wp Case 2 repeats the same non-redundancy justification
**ASN-0086, WP Case 2**: "*The disjunct is non-redundant.* The second conjunct's escape branch is required for weakestness, not merely sufficient: an `Emit_K` call with `K ~ R` but `a_emit(Σ, d) ∉ coverage(G)` (witness `G = ∅`…)"

**Problem**: Same pattern as Issue 2, in the parallel slot. The "*Derivation (both directions)*" that follows already establishes the biconditional and hence weakestness; the separate non-redundancy paragraph is duplicate justification. Step 4 of the worked sketch then concretely exhibits the false branch a third time.

**Required**: Fold the `G = ∅` witness into the derivation (one clause) and drop the standalone paragraph.

### Issue 4: Same downstream targets cited from multiple sites
**ASN-0086, R0 / Emit_K / Nullify** all defer to "*Value-shape consequence*"; **R0 / R-Scope / wp** all re-state "By RT-closure, Σ' is therefore →*-reachable, and RT-closure's preservation clause carries the full L/S/M/C invariant catalog to Σ'."

**Problem**: This is the "multiple paragraphs in different sections defer to the same downstream location" pattern (Value-shape consequence) and verbatim repetition of the RT-closure preservation sentence across three proofs. The repetition compounds without advancing any individual claim.

**Required**: State the Value-shape consequence and RT-closure preservation once, then cite by name without re-stating the clause body.

### Issue 5: Properties table self-referential suffixes
**ASN-0086, Properties Introduced**: the R6b row (DEF-Consequence) ends "…per R6b"; the Nullify row ends "per Definition — Nullify"; the R-Scope row restates its full statement.

**Problem**: A table row citing "per R6b" *as the R6b row* is circular and conveys nothing. These suffixes are index noise.

**Required**: Drop the self-pointing "per X" tails from the table entries.

## OUT_OF_SCOPE

### Topic 1: wp Case 2 holds only over the layer-reachable subdomain
The wp Case 2 formula is necessary-and-sufficient only because disciplinedness rules out a pre-existing wide-to-span retraction covering the fresh emission address; on a `→*`-reachable-but-not-layer-reachable state (direct K.λ with a subtree-covering `L_R` to-span) the formula is neither necessary nor sufficient. The note scopes the result explicitly and the last Open Question already proposes elevating the unit-depth discipline to a substrate guarantee — that elevation is the proper place to resolve the tension, not this ASN.

### Topic 2: Concurrency, observe-ordering, retraction cardinality bounds
The atomicity of Emit vs concurrent Observe, ordering guarantees on Observe results, and any structural bound on `|nullified(Σ)|` relative to `|dom(Σ.L)|` are new territory, correctly deferred to the Open Questions.

VERDICT: REVISE
