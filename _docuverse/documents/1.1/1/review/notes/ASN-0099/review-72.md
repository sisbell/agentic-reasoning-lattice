# Review of ASN-0099

## REVISE

### Issue 1: "What We Have Not Specified" contradicts the total comprehension definition
**ASN-0099, "What We Have Not Specified"**: "The semantics of querying with I-addresses outside `dom(Σ.C) ∪ dom(Σ.L)`."
**Problem**: `findlinks(I, Σ) = {a ∈ dom(Σ.L) : (E i : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅)}` is a *total* function of `I ⊆ T` — the comprehension is defined for every I, with no restriction to allocated addresses. F8 explicitly asserts `findlinks` is a function of `(Σ.L, I)` for arbitrary I, the Empty Query section handles `I = ∅`, and LP17 (ghost projection) shows endsets may cover non-allocated addresses. A query with addresses outside `dom(Σ.C) ∪ dom(Σ.L)` simply returns the (possibly ghost-covering) links whose coverage meets I — fully specified. Listing this alongside genuinely-unspecified items (procedure, caching, replication) is incorrect.
**Required**: Either delete the bullet, or reword it to name what is actually unspecified (e.g., "the *interpretation* a reader should attach to such a result"), not its semantics, which are pinned by the comprehension.

### Issue 2: Chronological-reading paragraph is self-disclaiming interpretive prose
**ASN-0099, "Result Ordering" (after F10)**: "*Chronological reading (interpretive).* The T1 presentation order carries a chronological reading within each home document … but across home documents T1 sorts by document tumbler, not by K.λ event history. This interpretation plays no role in F10's ordering claim."
**Problem**: The paragraph ends by admitting it "plays no role in F10's ordering claim." It is essay content occupying a structural slot under a formal ordering claim, advancing no reasoning the claim depends on.
**Required**: Remove the paragraph. If the chronological observation is worth keeping, it belongs in commentary, not appended to a load-bearing ordering lemma.

### Issue 3: "non-allocating" terminology forces a defensive clarification
**ASN-0099, "Arrangement Independence"**: "Throughout this ASN we call an operation *non-allocating* … The term names link-store inertness specifically and does *not* exclude content allocation: K.α (ContentAllocation) is non-allocating in this sense because it extends `dom(C)`, never `dom(L)`."
**Problem**: The second sentence exists only to defend a poorly-chosen term against the obvious misreading that an operation which *does* allocate content is called "non-allocating." This is defensive justification, not argument. The ASN already supplies the unambiguous synonym "link-store-inert."
**Required**: Drop "non-allocating," use "link-store-inert" throughout, and delete the defensive clarification sentence. (The neighbouring A1a/A1 pair also restates the same fact twice — "every op of V∖{K.λ} preserves Σ.L" and "K.λ is the unique operation that modifies the link store"; keep one statement of the equivalence.)

### Issue 4: F17/F18 say "atomic K.μ-family step" but include the non-atomic K.μ~
**ASN-0099, F17/F18**: "findlinks_filtered(C, Σ) = findlinks_filtered(C, Σ') across an **atomic** K.μ-family step." Justification: "F9 (V ∖ {K.λ} steps preserve Σ.L, **K.μ~ included**) + F15."
**Problem**: ASN-0047 defines K.μ~ as "a *named composite* of K.μ⁻ + K.μ⁺" — explicitly not atomic. The statement's qualifier "atomic" excludes K.μ~, yet the justification asserts K.μ~ is included. The scope of the claim is internally inconsistent.
**Required**: Drop "atomic" (the claim holds for every K.μ-family step, composite included, via F9's transitive composition), or, if the claim is meant to be per-atomic-step, exclude K.μ~ and correct the justification.

## OUT_OF_SCOPE

### Topic 1: Latency/freshness bound between K.λ commit and FINDLINKS visibility
**Why out of scope**: Raised in the Open Questions, this is a timing-guarantee question about the abstract handle ("next query after K.λ"). It introduces a new class of obligation (bounded propagation) not needed to specify the operation's set-theoretic semantics, and belongs to a future ASN on consistency/latency, not a revision here.

### Topic 2: Combined `findlinks_filtered_scoped(C, S, Σ)`
**Why out of scope**: The ASN correctly defers this and notes the intended naive-intersection composition. A full treatment (with its own conformance/monotonicity claims) is future territory, not an error in this ASN.

VERDICT: REVISE
