# Review of ASN-0116

This is a mature note (the K.α/K.μ⁻/K.μ⁺/K.ρ composite decomposition, the I3-citation reconciliation, the bijection-not-inclusion treatment of P4, and the containment-not-emptiness wp in P6 are all carefully done and technically sound). The composite-validity argument discharges each intermediate precondition correctly, and the boundary semantics for the coupling constraints (J0/J1★/J1'★ checked only at the composite boundary) are handled right. My findings are mostly accreted meta-prose plus one boundary the worked section skips.

## REVISE

### Issue 1: Defensive paragraph imagining the excluded S = s_L case
**ASN-0116, "INSERT(...) Precondition"**: "The constraint `S = s_C` is load-bearing, not cosmetic: ... Were `p` to sit in the link subspace (`S = s_L`), I-NEW would map link-subspace positions `shift(p, k)` ... to content addresses `shift(a, k)` ... violating generalized referential integrity (S3★ ...). INSERT-as-content-insertion is well-defined only for the text subspace; link placement is a distinct operation drawing on K.λ, not K.α."
**Problem**: The precondition already fixes `S = subspace(p) = s_C`. This paragraph then imagines the `S = s_L` case the precondition excludes and derives a contradiction — the reviser-drift pattern. The "load-bearing, not cosmetic" framing is defensive justification of why the axiom is needed rather than statement of what it says. A precise reader must skip past an imagined-and-excluded case to follow the precondition.
**Required**: Reduce to the object-level fact in one sentence: "Link placement is a distinct operation drawing on K.λ, not K.α." Delete the hypothetical S3★-violation derivation.

### Issue 2: Defensive exhaustiveness prose in I-NEW
**ASN-0116, Effect clause I-NEW**: "This holds for *every* block position uniformly (occupied and append cases alike), not merely the single instance `i = N+1`."
**Problem**: The per-block-position attribution (I3-V where the position pre-existed, I3-CS otherwise) is legitimate object-level work, but its closing sentences are an exhaustiveness claim phrased as a rebuttal — "not merely the single instance `i = N+1`" reads as a relocated prior finding rather than reasoning that advances the clause. The interval recomputation `i − n ≤ J − 1 < J` is then restated to defend uniformity a second time.
**Required**: State the split rule once (index ≤ N → I3-V; index > N → I3-CS) and the disjointness fact once. Drop the "not merely the single instance" rebuttal framing and the duplicated `i − n < J` re-derivation.

### Issue 3: First-position insertion (J = 1) into a non-empty subspace is never exercised
**ASN-0116, "A worked insertion"**: worked boundaries cover the middle insert (J = 3), append (J = N+1 = 6), and empty subspace (V_S(d) = ∅).
**Problem**: The rubric makes first-position a mandatory boundary. Insertion at `J = 1` into a *non-empty* subspace is the only case that drives the K.μ⁻ branch to full content-subspace clearance (`n'_{s_C} = J − 1 = 0`, strict contraction `0 < N`, prefix empty, the entire suffix shifted and re-installed by K.μ⁺). The general formula covers it, but no worked check or explicit prose confirms the `n'_{s_C} = 0` full-clearance branch — distinct from append (where K.μ⁻ is *dropped*) and from empty-subspace (where there is no suffix to shift).
**Required**: Add a J = 1 front-insertion worked check (or one sentence in the suffix-present sequence noting that J = 1 forces `n'_{s_C} = 0`, clearing the content subspace entirely before K.μ⁺ re-installs the shifted suffix plus block).

### Issue 4: Redundant restatement and repeated downstream deferrals
**ASN-0116, "What we have established"** and Effect clauses I-SHIFT / I-LEFT.
**Problem**: (a) The closing section re-derives P0–P6 and PROV in prose that the claim statements and body already establish — two passages saying the same thing in different words. (b) The Effect clauses I-SHIFT and I-LEFT both defer to "block-disjointness (established below)," and the Effect preamble defers the whole clause-derivation to "the next subsection" — several deferrals to the same downstream location, which the reader must hold open while reading the Effect.
**Required**: Compress the closing section to the two-layer thesis and the claim list rather than re-proving. State the block-disjointness interval fact once, before the Effect clauses that consume it, so I-SHIFT/I-LEFT cite an established fact rather than a forward "below."

## OUT_OF_SCOPE

The four Open Questions (transclusion at a shared insertion point, concurrent insertions without a serializing authority, provenance under transclusion of an already-attributed address, contiguity obligations after later fragmentation) are correctly deferred — they are new territory, not gaps in this ASN, and the note properly lists them rather than claiming them.

VERDICT: REVISE
