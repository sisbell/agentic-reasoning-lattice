# Review of ASN-0047

## REVISE

### Issue 1: The `#E(a)` formula in Notation is arithmetically wrong

**ASN-0047, Notation, *I-address (element-level) projections***: "`#E(a)` (ASN-0034): the depth (component count) of `E(a)` — equivalently `#a − zeros(a) − 1` if a has zero separators, or `#a` if a has no zero separators."

**Problem**: For an element-level address the formula does not compute `#E(a)`. Take the ASN's own running example `a₁ = 1.0.1.0.1.0.1.1` (used throughout the fork/insertion traces): `#a₁ = 8`, `zeros(a₁) = 3`, and the element field is `E(a₁) = [1, 1]`, so `#E(a₁) = 2`. The formula yields `#a − zeros − 1 = 8 − 3 − 1 = 4 ≠ 2`. The correct relation is `#E(a) = #a − (#N(a) + #U(a) + #D(a) + 3)`; subtracting only the separator count and one further component silently assumes the preceding three fields are collectively a single component, which T4's non-empty-field constraint (`#N, #U, #D ≥ 1`) forbids. The formula coincides with the truth only when `#N + #U + #D = 1`. The `no separators ⇒ #a` branch is fine; the separator branch is the defect.

**Required**: Either delete the "equivalently …" gloss and refer to T4b's `E` projection directly, or replace it with a correct expression (e.g., `#E(a) = #a − sig-position-of-last-separator`, or state it only as "`#a` minus the length of the node/user/document prefix and its three separators"). As written it is a false identity presented as fact, and `#E(a) ≥ 2` (C1b) cannot be read off it.

### Issue 2: J1/P4 "scaffold" derivations duplicate the operative J1★/P4★ derivations

**ASN-0047, *Coupling and isolation* (J1) and *Scoped coupling constraints* (J1★)**: the J1★ derivation states it is "derived by the same wp computation as J1 with P4 replaced by P4★ and the K.μ⁺ amendment scoping the difference set to the content subspace." Likewise the P4 theorem (full base case + inductive step + per-elementary bullet enumeration) is then superseded wholesale by P4★, whose proof re-runs the same case structure with the content-subspace scoping.

**Problem**: This is the anti-bloat pattern of "two paragraphs saying the same thing in different words." The J1 wp computation and the J1★ wp computation are the identical backward calculation over `Contains(·) ⊆ R`; the P4 inductive proof and the P4★ inductive proof share the same two-case skeleton. The body even instructs the reader how to discount the earlier version ("The scaffold derivation below should not be read as the operative extended-state result"), which is meta-prose telling the reader to skip content the document chose to retain in full.

**Required**: Collapse the duplication. State the wp derivation once (in its operative J1★/P4★ form) and reduce the link-free fragment to a one-line remark that it is the `dom(L) = ∅` specialisation, rather than carrying a parallel full derivation and proof that the text then disavows.

### Issue 3: "Protocol rationale" meta-prose around the node-allocation axioms in the K.δ discharge

**ASN-0047, *K.δ case (ii) discharge and parent-allocator activation*, sub-cases B and C**: e.g. "This is the protocol-layer counterpart to T10a's T2 admissibility, and the T2 discharge form is applied here against the external commitment rather than against any state-bearing component," and "the external registry's role is exhausted at the spawnPt premise, after which the docuverse-layer T10a discipline takes over uniformly."

**Problem**: This is prose explaining *why* NodeUniqueAllocation/NodeRegistryBootstrap are needed and how they relate to T10a's admissibility shape, rather than advancing the discharge itself. The substantive content — "sub-case B/C discharge `e ∉ E` via NodeUniqueAllocation clause (c) / NodeRegistryBootstrap" — is one sentence; the surrounding paragraphs restate the axioms' purpose, their layering against T10a, and the role boundary multiple times. The reader has to skip past the rationale to find the load-bearing step.

**Required**: Reduce sub-cases B and C to the discharge statement (operand `t`'s spawnPt premise is supplied by NodeUniqueAllocation (c) for non-bootstrap nodes and NodeRegistryBootstrap for `n₀`; `e ∉ E` then by T10a GlobalUniqueness on the activated `A_account(t)`). Drop the "protocol-layer counterpart," "role is exhausted," and "takes over uniformly" commentary.

### Issue 4: K.μ~ dependency-order preamble and repeated forward-deferrals are organizational meta-prose

**ASN-0047, *Decomposition of K.μ~***: "We establish the operation's properties in dependency order below, each stated once before it is consumed: Step (A) derives … ; Step (B) shows … consuming Step (A); K.μ~-FIX establishes … ; Steps (C)–(D) establish … ; and the necessity/sufficiency argument, consuming Steps (A), (C), (D), characterises the precondition."

**Problem**: This paragraph advances no reasoning — it is a table of contents for the section that follows, the kind of structural narration the anti-bloat classifier targets. It compounds with several same-target deferrals elsewhere (S3★ matrix cell "see *Decomposition of K.μ~*"; P4★ "proved in *Content-scoped containment and provenance* below"; the K.μ~ precondition "derived at *Necessity and sufficiency of the precondition* above"), where multiple sites point forward/back to the same location.

**Required**: Delete the dependency-order preamble; let the labeled steps stand on their own (they are already named Step (A)/(B)/(C)/(D)). Consolidate the repeated "see/derived at/proved in" pointers so each result is cross-referenced once.

### Issue 5: FrontierEquivalence trailing paragraph is a misplaced justification

**ASN-0047, *FrontierEquivalence (Lemma)*, final paragraph**: "T4b's `parent`/`zeros`/length stratification does not identify `t` as the frontier of its own sub-allocator, since coexisting version sub-allocators `A_v(d₁), A_v(d₂)` can emit same-length outputs under a common T4b parent; the frontier is therefore identified by the operational predicate `inc(t, 0) ∉ E`, not by any structural maximality clause."

**Problem**: This is a defensive justification of why a *rejected alternative* identification method fails — it sits after the lemma's ∎ and explains a design choice rather than supporting the proven biconditional. The note flags exactly this ("a paragraph imagines a case the claim's carrier or precondition already excludes"; defensive justifications). The lemma's statement and proof do not depend on it.

**Required**: If the same-length-version observation is load-bearing anywhere, move it to the single site that consumes it (the k=0 operand-selection rationale in K.δ) and state it once; otherwise remove it. It does not belong as trailing prose on the lemma.

## OUT_OF_SCOPE

None. The ASN stays within state model, elementary transitions, invariants, and coupling; the named composites (K.μ~, fork) are decompositions of elementary transitions, not the out-of-scope named user operations (INSERT/DELETE/COPY/etc.).

VERDICT: REVISE
