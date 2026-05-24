# Review of ASN-0094

## REVISE

### Issue 1: Direct cross-ASN references to ASN-0093 and ASN-0036 outside the foundation list

**ASN-0094, multiple sections**: Direct citations by number include:
- "Definition — AllocatorTreeDepth": "ASN-0093's structural chain from `d` to A's base address"
- *Substrate-conforming-layer scaffolding* / SubstrateConformingLayer: "ASN-0093 substrate invariants: M0, M1, C0, C1, C1b, C1c, C-fin", "ASN-0036 content/arrangement invariants: S0, S1, S2, S3, S7a, S7b, S7c, S7d, S8-fin, S8a, S8-depth, D-CTG, D-MIN, D-SEQ"
- R0a proof and *AllocatedAddressAntichain* preamble: "by ASN-0093 L0 (SubspacePartition)"
- *Step D.0*-related arguments and elsewhere: "Under the K.λ contract of ASN-0093", "by ASN-0093's sub-allocator chain axioms"

**Problem**: Only ASN-0034, ASN-0043, and ASN-0086 are listed as foundation ASNs for this review. ASN-0093 and ASN-0036 are cited by number directly, which the review standards flag as a REVISE item. The framework's *Substrate-conforming-layer scaffolding* attempts to consolidate dependencies into 10 named clauses, but several proofs still cite ASN-0093/ASN-0036 invariants directly (notably the AllocatorTreeDepth definition and the chain-of-evidence around K.λ's contract).

**Required**: Either (a) route every ASN-0093/ASN-0036 reference through the named scaffolding clauses (and remove the bare "ASN-0093/0036 invariants" enumeration in SubstrateConformingLayer, replacing it with a clause-by-clause list of what the framework actually consumes), or (b) promote the relevant ASNs to foundation status before publishing. The current mixed regime makes verification depend on facts outside the named foundation.

### Issue 2: Resolution catalog row contradicts its standalone walkthrough

**ASN-0094, Canonical Shape Catalog (Resolution row)**: "a standalone use (registering K at Resolution and consuming the base templates without any NonIdempotentDirectedPair consumer in scope) is admissible under Sh5(b)'s mechanical-derivation rule but **not exhibited at a use site independent of `K_res` in the current draft**."

**Problem**: The *Additional Worked Examples* section contains "Resolution base templates at a standalone K (no `_via` consumer in scope)" — a complete walkthrough with `K = approved_by` registered at the Resolution shape with no `_via` consumer in scope, exercising Emissions AB1, AB2, the AB3 rejection, and the full base-template evaluation table at Σ_2. The catalog row's claim "not exhibited" is factually false at the document level.

**Required**: Update the Resolution catalog row's prose to point at the existing standalone walkthrough (e.g., "exhibited at the 'Resolution base templates at a standalone K' sub-walkthrough in *Additional Worked Examples*"). Either retain the standalone walkthrough and fix the catalog row, or remove the standalone walkthrough and keep the catalog claim as-is.

### Issue 3: Lemma — RetractionTargetNotOnChain naming inconsistent with its generalized statement

**ASN-0094, Lemma — RetractionTargetNotOnChain**: The lemma's statement is "For every `b ∈ dom(Σ.L)` and every `d ∈ dom(Σ.M)`: `b ⋠ a_emit(Σ, d)`", with the *Generality* paragraph explicitly noting "stated about an *arbitrary* link-store address `b ∈ dom(Σ.L)`, not specifically about retraction-tuple slot addresses".

**Problem**: The lemma is consumed at two distinct sites: (1) discharging `NoCraftedSpanReachesD` over prior R-tuples' G-slots (a retraction-specific consumption), and (2) discharging the `K ~ R` disjunct's second arm for the *new* emission's G-slot — and additionally at *Sh4 Case C* (`K ~ R` sub-case ruling out self-nullification of `τ_new`) and *Case D Step D.0* (ruling out self- and cross-nullification of `τ_new`). The latter consumptions are about retraction-typed emissions, but the lemma itself applies uniformly to any link-store address. The name suggests narrower scope than the statement carries, and a future reviewer scanning the lemma index may not realize they can apply it to non-retraction `b ∈ dom(Σ.L)`.

**Required**: Rename the lemma to reflect its general statement (e.g., "LinkAddressNotPrefixOfEmit", "DomLPrefixDisjointFromFreshEmission") and reserve "RetractionTarget…" for use-case prose where the consumption is retraction-specific. Alternatively, restate the lemma's name explicitly with a parenthetical "(uniform across `b ∈ dom(Σ.L)`)".

### Issue 4: "T4(iv)" indexing convention not established in the foundation

**ASN-0094, AllocatedAddressAntichain Step 3.2 and RetractionTargetNotOnChain Case II preamble**: "T4(iv) applied to `x` gives `x_{#x} ≠ 0`"; similarly "by T4(iv)'s `b_{#b} ≠ 0`".

**Problem**: Foundation ASN-0034's T4 lists four positional conditions inline (`zeros(t) ≤ 3`; no-adjacent-zeros; `t₁ ≠ 0`; `t_{#t} ≠ 0`) without numbering them (i)–(iv). The ASN-0094 reference "T4(iv)" relies on a Roman-numeral indexing that does not appear in the foundation; readers must infer which of T4's four clauses is intended.

**Required**: Replace "T4(iv)" citations with explicit clause naming — "T4's `t_{#t} ≠ 0` constraint", or "T4's last-position non-zero clause" — at every site, to remove dependence on a numbering convention not established in the cited foundation.

### Issue 5: Sh-conf rejection sub-types collapsed into a single `⊥` token

**ASN-0094, Sh-conf section**: "The framework does not impose a finer-grained sum type at the substrate boundary; callers wanting that granularity wrap `Emit_K` with their own classification."

**Problem**: The framework returns `⊥` for at least five distinct rejection causes: (a) `K ∉ T_cat`, (b) non-canonical F or G, (c) cardinality mismatch, (d) target-domain miss, (e) per-K-discipline suppression (Sh4, FDD, single-home). The framework provides `C_K(F, G, Σ)` and `C_fd_K(F, Σ)` as layer-callable disambiguation but no analogous query for the structural gates. A consumer cannot, from the bare `⊥` return, distinguish a registry rejection (`K ∉ T_cat`) from a cardinality rejection from a single-home rejection. The text states callers must "wrap `Emit_K` with their own classification", but the framework provides no specification for how that wrapping should look — leaving downstream layers to re-invent the same classification disjointedly.

**Required**: Either (a) make `Emit_K`'s return type a sum (with named rejection tokens per gate), so callers can dispatch without re-discovery; or (b) document, in the Sh-conf section, the standard caller-side classification pattern (call order: registry check → canonical-form check → discipline-suppression check via candidate-set queries → cardinality/target-domain check). The current "wrap it yourself" guidance offloads framework discipline onto every consumer.

## OUT_OF_SCOPE

### Topic 1: Cross-process consistency of the shape registry and per-K disciplines

**Why out of scope**: The framework explicitly commits to single-process substrates by design — *Sh4 idempotency contract* and *FDD functional-dependency contract* atomicity reduces to within-call sequentiality. Extending to multi-process substrates with racing emitters at coverage-equivalent K's would require a coordination protocol (e.g., distributed lock at the `~`-class scope) outside the current framework. The Open Questions section flags this correctly as a scope boundary, and a future ASN would extend the framework's scope rather than fill in an internal gap.

### Topic 2: Higher-arity links (N ≥ 4) and the bipartite catalog's structurally-symmetric gaps

**Why out of scope**: The framework restricts itself to the arity-3 standard-triple slice of `dom(Σ.L)`; higher-arity links (admitted by L3 of ASN-0043 generally) are outside scope. The catalog's bipartite structure also lists potential symmetric rows (e.g., a hypothetical "Tuple-DirectedPair" at `(1, 1, A_rel, A_rel, ⊤)`) as not-yet-enumerated. Extending the catalog along either axis is future catalog-extension work, not an error in the current ASN.

### Topic 3: Ghost-targeting slot semantics

**Why out of scope**: L9 of ASN-0043 admits ghost spans in endsets generally; the shape framework's restriction to allocated slot addresses is a deliberate design choice with articulated rationale. Future shape families admitting ghost-targeting slot semantics — under what state-dependent conformance rule — would be new territory beyond the current framework's commitments.

### Topic 4: Layer composites combining substrate accessors with external data (e.g., `K_is_fresh` with `mtime`)

**Why out of scope**: The Sh5 audit table correctly *rejects* `K_is_fresh` because `mtime` is a layer-supplied accessor outside the discipline's four categories. The framework's design choice to keep external-data composites at the layer level (not the framework catalog) is well-motivated by Sh5(b)'s falsifiability discipline. Composing substrate accessors with external data is future per-layer work.

VERDICT: REVISE
