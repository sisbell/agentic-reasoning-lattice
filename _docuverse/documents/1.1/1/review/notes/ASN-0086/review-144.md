# Review of ASN-0086

## REVISE

### Issue 1: R6b's formal statement does not capture the "non-fixpoint" claim its name and prose assert

**ASN-0086, R6b (SingleDepthRetraction)**: name/prose — *"Retraction-of-retraction is not a fixpoint operation: nullifying a retractor b does not 'undo' b's nullifying effect on its prior targets"*; formal — `(A Σ, a, b, F', G' : a ∈ A_rel^Σ ∧ (b, F', G') ∈ L_R^Σ ∧ a ∈ coverage(G') : a ∈ nullified(Σ))`.

**Problem**: The substantive guarantee — that `a` stays nullified *even when its witnessing retractor `b` is itself nullified* — is carried entirely in prose ("L_R^Σ retains b's tuple regardless of b's active-subset status"). The formal statement never mentions `b ∈ nullified(Σ)`; it is the plain `⟸` direction of the definition of `nullified`, with `b`'s status simply absent rather than discharged. As written the lemma is a trivial definition-unfolding and does not formally establish the non-fixpoint property the name advertises. This is the "derived guarantee stated without derivation" pattern: the consequence is named but not derived.

**Required**: Add `b ∈ nullified(Σ)` to the hypotheses (the conclusion still follows, since the witnessing `L_R` tuple is consulted independently of `b`'s status), so the formal statement actually expresses "a retractor nullifies its targets even while itself nullified." Alternatively, relabel R6b explicitly as the definitional `⟸` and move the non-fixpoint reading to a separately-derived corollary.

### Issue 2: Duplicated prose — "K.λ fixes address but not endset shape" stated twice

**ASN-0086, Definition — Unit-depth retraction discipline**: "a direct K.λ caller can emit a crafted-span retraction that is L-invariant-conforming yet violates it — K.λ fixes emission *address* but not endset *shape*."
**ASN-0086, WP Case 2 ("Substrate-conformance alone is insufficient")**: "K.λ constrains every emission *address* to the sibling frontier but leaves a link's endset *shape* unconstrained, so a substrate-conforming Σ may still carry a crafted (non-unit-depth) retraction span…"

**Problem**: Two paragraphs in different sections make the identical point in different words ("address fixed / shape unconstrained"). This is the "two paragraphs say the same thing" accretion pattern; the reader must reconcile the two to confirm they are the same claim.

**Required**: State the address-vs-shape distinction once (at the discipline definition, where it belongs) and have the wp paragraph cite it rather than re-prosify it.

### Issue 3: Forward-reference / use-site inventory prose that does not advance reasoning

**ASN-0086, Foundation**: "Each chain lemma (ChainDiscipline, FirstEmission, ChainMembershipForOrigin, ChainEnumerationInjectivity) is cited at its use site below."
**ASN-0086, State transition relation**: "the K.α/K.λ emission forms are recalled where needed, e.g. in R0 and a_emit."

**Problem**: Both are use-site inventories — promises about where things will be cited later, not content. They are exactly the "definition's introduction enumerates downstream consumers" / forward-reference patterns the anti-bloat classifier targets. Each lemma is in fact cited where used; the inventory adds nothing.

**Required**: Delete both sentences. Citations at the use sites are self-documenting.

### Issue 4: Pure-rename lemmas occupy proof slots with no added reasoning

**ASN-0086, R4 (TupleAddressDisjointness)**: "`A_doc^Σ ∩ A_rel^Σ = ∅` — which is SD (StoreDisjointness, ASN-0093) under the partition aliases." (Similarly R2 = L12, R3 = L12a + R2.)

**Problem**: R4's entire content is alias-substitution into a foundation lemma; it states a numbered lemma whose proof is the single word "SD." This is acceptable as a vocabulary bridge inside a definition, but as a standalone numbered claim with a derivation slot it adds a name and no reasoning. R2/R3 are nearly the same (R2 is verbatim L12 "in tuple vocabulary").

**Required**: Either fold R2/R4 into the partition/permanence definitions as one-line aliases (no separate lemma slot), or — if they must remain numbered for the relational vocabulary — drop the proof slots and mark them inline as definitional aliases of the named foundation lemmas, so they are not mistaken for results requiring verification.

## OUT_OF_SCOPE

### Topic 1: Retraction stability under the categorical relation ↝, not only →
R6a and R6c are proved for the dom-extending `→` (and `→*`). The note introduces `↝`/`↝*` precisely to model higher-layer operations, and the active/audit distinction's value depends on retractions being permanent. Whether `a ∈ nullified(Σ)` persists across arbitrary invariant-preserving `↝`-steps (not just the three K-ops) is the natural strengthening, but it requires characterizing which higher-layer transitions preserve L12/L12a — territory for a later ASN, not an error here.

VERDICT: REVISE
