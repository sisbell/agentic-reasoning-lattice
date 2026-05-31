# Review of ASN-0086

## REVISE

### Issue 1: R7a's headline conclusion is largely pre-assumed by the conformance definition it quantifies over
**ASN-0086, R7a + "Definition — substrate-conforming layer" clause (b)**: "for any state-affecting transition `Σ ↝ Σ'` issued by a substrate-conforming layer ... the `Σ.L`-affecting effect ... decomposes into a finite sequence of class-(iii) `→`-steps."

**Problem**: Conformance clause (b) already *requires* the layer to preserve ChainMembershipForOrigin to `Σ'`. That requirement is precisely "every link address lies on some `A_L(d)` sibling-frontier chain" — which is most of what "the change reduces to K.λ" asserts. The proof even concedes this is load-bearing ("Catalog (a) alone is insufficient... catalog (b) excludes it"). So the lemma's distinctive content collapses to the interleaving/ordering and K.σ-prefixing argument; the "no extra class affects `Σ.L`" claim is near-tautological once a layer is admitted only if it preserves chain-membership at every step. Note also that ChainMembershipForOrigin is an ASN-0093 *theorem about →-reachable states*, not a step-local invariant; requiring an arbitrary `↝`-step to "preserve" it is a stronger demand than the foundation proves, and the note never argues such preservation is achievable by any operation other than a literal K.λ replay.

**Required**: State explicitly what R7a adds beyond clause (b)'s assumption (the interleaving and K.σ-prefix construction), and justify treating a reachability-theorem (ChainMembershipForOrigin) as a step-local conformance obligation rather than re-deriving it from the layer's transition structure.

### Issue 2: `⊑` reinvents (and inverts) ASN-0043's `⊒` StateExtension notation
**ASN-0086, "Definition — Extension"**: "`Σ' extends Σ`, written `Σ ⊑ Σ'`, is the reflexive-transitive closure of `→`."

**Problem**: ASN-0043 (foundation) already defines "`Σ'` *extends* `Σ`, written `Σ' ⊒ Σ`." This note reuses the identical phrase "extends" with a flipped symbol (`⊑`) and a different *meaning* (reflexive-transitive reachability vs. store-inclusion-with-agreement). Standard #7 forbids reinventing notation a foundation already defines. The clash is actively confusing: a reader carrying ASN-0043's `⊒` will misread every `⊑` in R6c.

**Required**: Either use ASN-0043's `⊒` if store-extension is meant, or, since reachability genuinely differs from store-inclusion, name the relation distinctly (e.g. `→*`) and state explicitly how it relates to ASN-0043's `⊒` rather than colliding with it.

### Issue 3: "Definition — substrate-conforming layer" clause (b) is a use-site inventory, not a definition
**ASN-0086, Definition — substrate-conforming layer, clause (b)**: the Chain Discipline Catalog enumerates "ChainDiscipline ... and FirstEmission — establish each document's `A_C(d)` and `A_L(d)` chains ...; ChainMembershipForOrigin — every realized homed-set is ...; Supporting chain-structure lemmas: ChainEnumerationInjectivity, ChainPrefixExtension, ..."

**Problem**: This is the flagged "definition's introduction enumerates downstream consumers / use-site inventory" pattern. The definitional content is "preserves the ASN-0093 sub-allocator chain machinery"; the per-lemma gloss is meta-prose a precise reader must skip to reach the actual conformance condition.

**Required**: Reduce clause (b) to the requirement itself ("preserves the ASN-0093 chain-discipline lemmas") and drop the per-lemma descriptions; cite individual lemmas at the proof step that consumes them (R7a discharge (4) already does this).

### Issue 4: M2 "Arrangement modification is out of scope" paragraph is rationale/essay, not load-bearing content
**ASN-0086, "Arrangement modification is out of scope"**: "In Nelson's design a document's arrangement is inherently mutable, and M2 reads as a temporary scaffolding restriction in the current allocation-substrate layer; wiring arrangement mutation in underneath is left to the substrate ASN that relaxes M2."

**Problem**: This explains *why* M2 exists and what Nelson intended rather than what the note relies on (which is the single sentence "this note does not rely on any transition M2 forbids"). It is the flagged "prose explaining why a constraint is needed rather than what it says" pattern, plus a forward deferral to an unnamed future ASN.

**Required**: Keep the operative sentence ("`→` is the complete dom-extending vocabulary under M2; no claim relies on a transition M2 forbids"); cut the Nelson rationale and the forward deferral.

### Issue 5: WP Case 2 develops regimes the relational layer's own discipline excludes, then retracts them
**ASN-0086, WP Analysis, Case 2 regimes (ii)/(iii) + "Relational-layer discharge"**: regime (ii) "Crafted-span retractions admitted" and regime (iii) "Self-nullifying R-typed emission" are spelled out, after which "Relational-layer discharge" states "both regime (ii) and regime (iii) are structurally impossible" under the layer's committed operations.

**Problem**: This is the flagged "imagines a case the claim's carrier/precondition already excludes." Once the relational layer commits Nullify-as-sole-R-producer and unit-depth shape, regimes (ii)/(iii) cannot arise for any layer-initiated state; the prose constructs them only to dismiss them. Relatedly, R0's "*Content-uniformity remark*" sub-paragraph exists primarily to be cited downstream ("R5 invokes R0 at this uniformity directly") — a use-site-anticipating gloss rather than a step that advances R0's proof.

**Required**: Either scope the wp explicitly to direct-K.λ callers (where (ii)/(iii) are live) and drop the "but the layer forbids it" retraction, or collapse the analysis to the relational-layer wp (`d ∈ dom(Σ.M) ∧ K ∈ T_admissible`) with one sentence noting the substrate permits broader retractions. Fold R0's content-uniformity point into the one R5 invocation that needs it.

## OUT_OF_SCOPE

### Topic 1: Concurrency/atomicity of Emit vs. Observe
**Why out of scope**: The consistency model under which `A_K` transitions are observed (open question 5/6) is genuinely new territory; the present note specifies a sequential substrate (SequentialTransitionAxiom) and need not resolve concurrent observation.

### Topic 2: Multi-arity active subsets `A_K^{(n)}`
**Why out of scope**: Extending the active/audit machinery to `|Σ.L(a)| > 3` is correctly deferred; the note's standard-triple restriction is stated up front and self-consistent.

VERDICT: REVISE
