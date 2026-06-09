# Review of ASN-0126

I worked through the framework's mathematical content carefully — the shape catalog, the `Sh-conf` predicate, the `K.λ_sh` gate, the projection bridge, and the wp refinement. The reasoning is sound. The projection bridge `π(Σ) = (Σ.C, Σ.M, Σ.L)` correctly carries ASN-0086's lemmas to the four-component state; P3/P5 are a clean safety/liveness pair; the gate-vs-landing separation (gate clears → audit slice `L_K`; C2/C3 govern active subset `A_K`) is correct; the born-nullified worked illustration checks out arithmetically (`a = g = ...2.4 ∈ coverage(G_rng) = [...2.4, ...2.7)`, so the citation is nullified at birth). RegisteredAdmissible's `coverage(K) ≠ ∅ ⟹ K ≠ ∅` step is valid. I found no correctness gap.

The note carries `review-mode.anti-bloat`, and the residual findings are accumulated restatement, not unsound argument.

## REVISE

### Issue 1: "Properties established" restates P1–P6 already stated at their establishing sites
**ASN-0126, Properties established**: "**P3 (Sh-confWellFormedness).** Every value a `→_sh`-step adjoins to `dom(Σ.L)` is a standard triple `(F, G, K)` with K registered and `Sh-conf(K, F, G) = ⊤`. (The shape-gated emit.)"

**Problem**: Every one of P1–P6 is given a full formal statement at the section that establishes it *and* a second prose restatement here. Compare the inline P3 ("...whose K is registered and for which `Sh-conf(K, F, G)` holds") against the gloss above — same claim, different words. The same doubling holds for P1 (Registry permanence), P2/P4 (Registration entries), P5 (The shape-gated emit), P6 (Reachable conformance). The section makes the reader re-read six claims they have already read; only the parenthetical section-pointers add anything.

**Required**: Deduplicate. Keep the canonical formal statement at each establishing site and reduce "Properties established" to a compact index (label + one-line gloss + section pointer), or move the formal statements here and leave the establishing sites to prove the result without re-labelling. The full statement should live in exactly one place.

### Issue 2: The "Binary is strictly weaker than the unit-depth discipline" consequence is explained twice
**ASN-0126, Single-source ¶3**: "Binary registration is strictly weaker than ASN-0086's UnitDepthRetractionDiscipline: Binary gates G by span count alone, so a single G-span of non-unit length ... is equally Binary-conformant, hence a legal `→_sh`-step that withdraws a whole region at once."

**ASN-0126, The shape-gated emit**: "This framework gates R by Binary alone (Single-source), strictly weaker than the unit-depth discipline, so `→_sh` admits non-unit retraction to-spans whose coverage can include a fresh address, and C3 becomes live."

**Problem**: Both passages derive the identical fact — Binary counts G-spans only, so non-unit G-spans are conformant and a whole region can be withdrawn. The second passage already cites "(Single-source)"; the clause "strictly weaker than the unit-depth discipline, so `→_sh` admits non-unit retraction to-spans" then re-explains exactly what that citation points to. The reader must notice the repetition and confirm it is the same claim.

**Required**: State the fact once (Single-source, where the Binary retraction wrapper is introduced) and let the C3-liveness paragraph rely on the citation alone — e.g., "By Single-source, `→_sh` admits non-unit retraction to-spans, so C3 becomes live" — without re-deriving the weakness.

## OUT_OF_SCOPE

### Topic 1: Gating on target validity / coverage, not just span count
`Sh-conf` deliberately "consults no state-indexed address set" and counts spans only, so a Binary edge may point its one G-span at a ghost address or pre-emptively cover not-yet-allocated link addresses (the born-nullified illustration). Whether typed relations should additionally constrain *targets* (residence, type-target compatibility, no pre-emptive range coverage) is genuinely new territory.

**Why out of scope**: The no-residence-check decision is intentional and grounded in L4/L9, and the note already routes target-behavior questions to its successor (Open Questions #2, behavior catalog). This is a policy for the operational-semantics layer, not an error in the shape framework.

VERDICT: REVISE
