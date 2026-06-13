# Review of ASN-0130

This is a strong, carefully stratified note. The central architectural claim — that the parse layer (content-intrinsic) grounds the registration-order DAG (PR2), which grounds `sig` (PR-SIG), which grounds WT-ref typing — is genuinely non-circular: I checked that PR2 consumes only the parse and the discipline (never `sig`), so the forward reference PR-SIG → PR2 is to an independent result. PR3a's substitution induction (WT-α, WT-W, the `k`-step PC2 discharge) is fully worked, capture-freeness is established, and the wp analyses in PR0/PR5a correctly handle the born-nullified boundary in both directions. The findings below are mostly the meta-prose accretion the `anti-bloat` classifier flags, plus one boundary gap in the certification contract.

## REVISE

### Issue 1: Duplicated "overlapping runs are harmless"

**ASN-0130, PR-ENC-uniq and PR3**: PR-ENC-uniq states "(Runs may still *overlap*: a suffix of a run may itself decode. That is harmless — identity and resolution are start-anchored (PR3), so a definition starting mid-run is a different definition at a different start, never confused with the containing one.)" PR3 then states "overlapping runs are harmless because resolution is start-anchored — a decodable suffix is a different definition at a different start."

**Problem**: The same point — overlap is harmless because resolution is start-anchored — is made twice, and the PR-ENC-uniq instance even forward-references PR3 for the start-anchoring it then asserts, which PR3 re-asserts. This is the "two paragraphs say the same thing in different words" pattern.

**Required**: State the start-anchored-resolution consequence once. Since start-anchoring is PR3's territory, keep it in PR3 and drop the PR-ENC-uniq parenthetical (PR-ENC-uniq's own job — uniqueness from prefix-freeness — stands without it).

### Issue 2: PS1 re-derives PR0's dynamics and inventories the Multi shape's consumers

**ASN-0130, PS1**: The idempotency paragraph re-explains the hit/rejection/re-registration behavior already established in PR0 — "validation runs first on every call (PR0), so a re-presentation whose referents have since been de-registered fails (iv) and is *rejected*, the incumbent untouched — rejection of the call asserts nothing about the standing registration. After de-registration the dedup sees an empty class (I2) and a re-registration deposits afresh at a new address." This restates PR0's "rejection of a call asserts nothing about a standing registration" and its hit/miss/re-deposit semantics. Separately: "The Multi shape is what makes both facts recoverable by denotation: addrs(F) = {a} and addrs(G) = A_def, so condition (iv) tests r ∈ addrs(F), targets_of(a, active) enumerates the run (D3), and M_pdef enumerates the registered definitions (D1)".

**Problem**: A standard-registration catalog entry should carry shape/idem/behaviors/slot-convention plus what is *new* — here, the genuine Multi-vs-merged-span rationale ("a single merged span over the run would denote nothing, AD collecting unit-depth spans only"). The idempotency dynamics duplicate PR0, and the clause enumerating downstream consumers (condition iv, `targets_of`, `M_pdef`) is a use-site inventory rather than content that advances the shape's meaning.

**Required**: Trim PS1's idempotency paragraph to a pointer to PR0's contract. Keep the merged-span rationale; drop the (iv)/`targets_of`/`M_pdef` consumer inventory (those uses appear at their own sites).

### Issue 3: Certification's Boolean-result-sort boundary is not stated

**ASN-0130, PR5a (iii) and PR5**: PR5a's conditions are (i) active registration, (ii) view-independence, (iii) "the checker's verdict `expand(a) ∈ ST` by PD0's rules ... Failure is rejection; the definition stays registered, merely uncertified — unknown, not unstable." PR5 notes "PD0's classes are stated for Boolean state-predicates — terms with a truth value at each reachable Σ".

**Problem**: PR0 (iii) admits any `C_D ∈ Codom` ("Γ_D ⊢ body : C_D"), and WT-ref types `r(e₁,…,e_k) : C_r` at any sort, so non-Boolean definitions are first-class — a `℘_fin(T)`-valued helper is registrable and referenceable. Certifying one: ST is a syntactic class of Boolean terms, so a non-Boolean `expand(a) ∉ ST`, (iii) fails, and the call is rejected. The operation is therefore *safe*, but (a) the contract never states the result-sort requirement (PR0 made its analogous boundary explicit with condition (0)), and (b) the rejection narration "uncertified — unknown, not unstable" miscategorizes a non-predicate definition as a Boolean predicate of unknown stability — a distinct third category from "ill-posed (view-dependent)" and "unknown (not ST)." This is a precondition boundary the operation contract leaves implicit. The note's "predicate" framing throughout sits in tension with the general-term mechanism it actually builds.

**Required**: Add an explicit precondition to PR5a (e.g. condition (0): `sig(a) = (Γ_D, Bool)`), parallel to PR0's (0), and distinguish rejection of a non-predicate definition from rejection of a Boolean predicate whose stability is unprovable. One sentence reconciling "predicate" (the certifiable, Boolean subclass) with the general terms `register_pred` stores would also remove the framing tension.

## OUT_OF_SCOPE

None. The note's own Open Questions (naming, cross-substrate portability, dangling live references, certificate classes beyond ST) correctly fence future work, and the activation/trigger primitive is appropriately left to the protocol layer.

VERDICT: REVISE
