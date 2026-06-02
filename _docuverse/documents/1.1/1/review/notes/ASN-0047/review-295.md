# Review of ASN-0047

I read the full transition model. The technical core is sound: I checked the K.δ case-split (i/ii, k∈{0,1,2}) against the K.δ-ID identities, the K.μ~ bijection-realisation chain (admissibility (i)–(v), K.μ~-FIX, K.μ~-RANGE, Step (A)/(B)), the K.μ⁻ constructive/post-state equivalence, the D-SEQ★ derivation (both m=2 and m≥3 cases), and every worked example's arithmetic (tumbler `inc`, `origin`, `zeros`, anchor construction). I found no correctness defect. My findings are confined to the anti-bloat / forward-reference accretion patterns this note's classifier directs me to surface.

## REVISE

### Issue 1: The K.μ~ correctness argument is fragmented across sections with forward deferrals to the same location
**ASN-0047, *Decomposition of K.μ~* (Step (A), Case `s_L`)**: "Pointwise link fixity (clause (v), `π(v) = v`) for these sources is established once below in *Link-subspace fixity and realisation* step (4); we cite it here rather than re-derive."

**Problem**: One argument — that the K.μ⁻+K.μ⁺ full-clearance decomposition realises exactly the admissible π — is split across *Full-clearance form*, *LRP*, *bijection equation*, *Step (A)*, *Step (B)*, *K.μ~-FIX*, *K.μ~-RANGE*, *Link-subspace fixity and realisation*, *Necessity and sufficiency*, and *Decomposition*, with forward deferrals among them (Step (A) → "step (4)"; *Decomposition* → "the clause-(v) discharge (Step (A), Case s_L)"; *Necessity* → "Link-subspace fixity"). This is exactly the flagged pattern: "multiple paragraphs in different sections defer to the same downstream location." A reader cannot follow the realisation claim without jumping between non-adjacent subsections. (LRP itself — proved once, then cited — is *not* the problem; the forward deferrals that precede the proof are.)

**Required**: Order the K.μ~ argument so that LRP and link-subspace fixity are established before they are first used, and remove the "established once below … we cite it here rather than re-derive" deferrals by stating the fact at its first use.

### Issue 2: Step (A) dresses a trivially one-directional fact as a class equivalence
**ASN-0047, *Decomposition of K.μ~*, Step (A)**: "Subspace preservation … and link-subspace fixity … hold for every *admissible* π directly by admissibility clauses (iv) and (v). Conversely, every admissible π is *realisable* … and every realisable π is subspace-preserving and link-subspace fixing (hence admissible), so the two classes coincide …"

**Problem**: The forward direction ("every admissible π is subspace-preserving and link-fixing") is true *by definition* — clauses (iv) and (v) are admissibility hypotheses. The text's own sentence admits this ("directly by admissibility clauses (iv) and (v)"). Wrapping a definitional triviality plus the one substantive direction (realisable ⟹ admissible) into "the two classes coincide" inflates the structure without advancing the argument. The only content is the reverse direction.

**Required**: Drop the "two classes coincide" framing; state only the substantive claim (the full-clearance decomposition produces a subspace-preserving, link-fixing — hence admissible — π, and realises every admissible π).

### Issue 3: Epistemic-status meta-prose around J1★/J1'★ explains why rather than what
**ASN-0047, *Scoped coupling constraints***: "Both J1★ and J1'★ are forced by a *design choice*, not by the calculus alone: the wp computation motivates each coupling but does not force it; Nelson's commitment to a permanent reverse index, confirmed by Gregory's implementation accumulating entries 'from every content addition,' is what forces both directions."

**Problem**: This paragraph (and its near-duplicate appearing after each wp derivation — "We *impose* this as the composite-scoped coupling J1'★") argues about the *epistemic status* of the couplings rather than stating or using them. It matches the flagged pattern: prose around a constraint explaining why it is needed rather than what it says. The wp derivations above it already establish the motivation mechanically; the "design choice not calculus" commentary is redundant meta-prose.

**Required**: Reduce to a single clause noting the couplings are imposed (not derived), or fold the provenance-permanence motivation into J1★'s one-line preamble and delete the repeated commentary.

## OUT_OF_SCOPE

### Topic 1: Interior link/content withdrawal with renumbering
Already correctly deferred — the ASN's K.μ⁻ models suffix-only contraction, and the Open Questions list flags interior `DELETEVSPAN` compaction as future work. No action; raised only to confirm it is appropriately scoped out, not a gap in this ASN.

META does not apply: the ASN specifies state components (C, L, E, M, R), elementary transitions, and reachable-state invariants abstractly, with implementation evidence (Nelson/Gregory) cited as grounding rather than as the object of specification. It has not drifted into implementation mechanics.

VERDICT: REVISE
