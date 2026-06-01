# Review of ASN-0086

## REVISE

### Issue 1: R0's invariant-preservation step mis-attributes the discharge of L14/L14a
**ASN-0086, R0 proof, "L-invariant preservation across the K.λ-step"**: "Every catalog invariant (the full L/S/M/C catalog of ASN-0036, ASN-0043, ASN-0093) holds at the fresh key `a` by K.λ's own ASN-0093 invariant-preservation contract. The one obligation not closed structurally by that contract is the match between the emitted value and K.λ's value-shape precondition…"

**Problem**: ASN-0093's published catalog (M*, C*, L0–L3, L12, SD, L-fin, C-fin) does **not** contain ASN-0043's L14 (DualPrimitive) or L14a (NonTranscludability). So K.λ's ASN-0093 contract cannot be the mechanism that preserves L14/L14a, yet R0 claims the *full* ASN-0043 catalog is discharged by it and names value-shape (L3) as the *only* non-structural obligation. The note itself introduces **FreshLinkKeyDisjointness** precisely to discharge L14/L14a at a fresh key, and R5's proof correctly invokes it ("the L14/L14a fresh-key obligation is the FreshLinkKeyDisjointness sub-lemma") — but R0 never cites it. R0 thus leaves L14/L14a either unhandled or wrongly attributed, and renders FreshLinkKeyDisjointness orphaned at its primary intended use site.

**Required**: In R0, invoke FreshLinkKeyDisjointness to discharge L14/L14a (as R5 does), and narrow the blanket claim so it covers only the invariants ASN-0093's K.λ contract actually proves. Alternatively, if FreshLinkKeyDisjointness is genuinely redundant, delete it and justify why ASN-0093's contract covers L14/L14a.

### Issue 2: Defensive scope-prose argues against a hypothetical the note already excludes
**ASN-0086, Working domain**: "We do not quantify over hypothetical higher-layer operations. The substrate of this note admits no transition other than K.σ/K.α/K.λ, so there is no operation against which a separate 'categorical' reachability or a layered conformance taxonomy would range. The question of which nullification guarantees survive operations beyond K.σ/K.α/K.λ is deferred to the ASN that actually introduces such operations."

**Problem**: This paragraph explains why an alternative apparatus ("categorical reachability," "layered conformance taxonomy") is unnecessary — apparatus the note's own `→ ≡ K.σ ∪ K.α ∪ K.λ` definition already excludes. It is residue arguing against a removed design rather than advancing any claim. The deferral is already captured by the final Open Question.

**Required**: Delete the paragraph; the transition definition and the Open Question carry its content.

### Issue 3: Definitional choice justified by a downstream use-site inventory
**ASN-0086, "A_rel^Σ names the whole link store, not only the tuples"**: "We keep the broader `A_rel^Σ = dom(Σ.L)` because the substrate-level guarantees stated over it — SD-disjointness here, R0a's antichain, R-Scope's single-address scope — are genuinely arity-independent; where a result concerns tuples specifically we say so…"

**Problem**: The definition's justification enumerates its downstream consumers rather than advancing the definition's meaning — the "consumed by X, Y, Z" anti-pattern. The arity-independence of R0a/R-Scope is established (and noted) at those sites; restating the roster here is meta-prose the reader must skip.

**Required**: Reduce to the definitional fact (`A_rel^Σ = dom(Σ.L)` includes higher-arity links not in any `L_K`) without the consumer roster.

### Issue 4: "Harmless" paragraph imagines a case the claim's carrier already excludes
**ASN-0086, Definition — Nullified**: "Because `A_rel^Σ = dom(Σ.L)` holds higher-arity link addresses as well as arity-3 tuple addresses, `nullified(Σ)` may collect a higher-arity link address; such an address indexes no `L_K`-tuple … so the active-subset exclusion `a ∉ nullified(Σ)` in `A_K^Σ` simply never references it — the collection is harmless."

**Problem**: This is defensive prose proving a non-issue: since `A_K^Σ` ranges only over `L_K^Σ` (arity-3) members, a higher-arity entry in `nullified(Σ)` is unreachable by construction. The paragraph reassures against a case the `A_K` definition structurally cannot encounter.

**Required**: Cut, or compress to a one-clause note that `nullified` and `A_K`'s exclusion are arity-restricted by their carriers.

## OUT_OF_SCOPE

### Topic 1: Concurrency/atomicity of Emit vs. Observe, and Observe ordering
**Why out of scope**: The substrate here is sequential (SequentialTransitionAxiom). A consistency model for concurrent Emit/Observe and an ordering guarantee on Observe results require operations and a concurrency semantics this note does not introduce. Correctly deferred (Open Questions).

### Topic 2: Higher-arity typed relations `L_K^{(n)}` and multi-arity projections
**Why out of scope**: This note deliberately restricts to standard triples (`|Σ.L(a)| = 3`). The relational treatment of `|Σ.L(a)| > 3` is new territory, not a defect here. Correctly deferred (Open Questions).

VERDICT: REVISE
