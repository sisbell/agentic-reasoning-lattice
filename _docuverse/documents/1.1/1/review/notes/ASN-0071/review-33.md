# Review of ASN-0071

## REVISE

### Issue 1: Subspace confinement is derived and restated across four sections
**ASN-0071, "The query" / "Resolution" / "The operation" / "Currency"**: The same fact — every `t ∈ ⟦σ⟧` has `subspace(t) = s_C` — is set up in "The query" ("The one consequence both deliver is *subspace confinement*"), proven there as the position-1 instance of PC, then re-derived in Resolution (*Subspace confinement.* "The position-1 instance of prefix confinement (PC, proven in *The query*) applies"), re-cited in "The operation" ("We discharged the source side already — `iaddrs(Q)(Σ) ⊆ dom(Σ.C)` by subspace confinement"), and again in "Currency."
**Problem**: PC subsumes subspace confinement; once PC is proven, the standalone subspace-confinement framing in the opening of "The query" is dead weight, and the re-derivation in Resolution repeats the position-1 step already executed. A reader must skip past three restatements to follow the single load-bearing claim. This is the "multiple paragraphs say the same thing" / forward-deferral accretion the anti-bloat classifier targets.
**Required**: Prove PC once, state its position-1 instance is subspace confinement once, and have Resolution/The operation/Currency cite it by name without re-deriving.

### Issue 2: Defensive justification of the charitable-reading design choice
**ASN-0071, Resolution**: "This is a substantive choice. An alternative specification could reject the entire query as ill-formed if any position is unresolvable. The charitable reading is justified: a position not in the arrangement names no content, so excluding it from the resolution is the natural extension of 'find documents containing the content at these positions'. The price is reduced diagnostic information..."
**Problem**: This paragraph argues *why* the design is defensible against an unchosen alternative rather than stating what the operation does. The preceding paragraph already states the filtering behavior factually ("the intersection drops unresolvable positions, and their absence contributes nothing"). The defense adds no reasoning the spec needs.
**Required**: Delete the justification; keep the factual statement of F-FILT behavior. If the trade-off matters, it belongs in an Open Question, not as inline apologetics.

### Issue 3: Forward-pointer deferral to Open Question in Currency
**ASN-0071, Currency**: "What relationship `find`'s current-state result must bear to `R` is left to the Open Question below." preceded by the paragraph "Recovering the *historically*-containing set ... is a separate concern. `find` does not consult ASN-0047's provenance relation `R` ..."
**Problem**: The Open Questions section already poses "What relationship between FINDDOCSCONTAINING's current-state result and the historical containment relation `R` must the system guarantee?" The Currency paragraph restates the same scoping point and then forward-points to it — a deferral that duplicates the open question rather than advancing the currency argument.
**Required**: State the currency fact (find reads only current `M`/`E_doc`, not `R`) once; drop the "left to the Open Question below" pointer and the duplicated framing.

### Issue 4: "Completeness and soundness" section is meta-prose restating the definition
**ASN-0071, Completeness and soundness**: "F-COMP and F-SOUND are not independent properties of the abstract operation — they are the two halves of its definition. Together they constitute the definition; separately, they name the obligations on any candidate implementation. An implementation that omits any qualifying document realizes a strict subset of `find` ... An implementation that includes a document not satisfying the predicate realizes a strict superset ..."
**Problem**: This advances no reasoning about the operation's guarantees — it unfolds the biconditional into its two trivial directions (already captured in the F-COMP/F-SOUND table rows as "direct from F-find") and then narrates implementation obligations. It is essay content occupying a structural slot.
**Required**: Reduce to the two definitional rows already in the Claims table, or excise the section; the biconditional is the definition of `find` and needs no separate prose to "decompose" it.

### Issue 5: Home/transcluding recovery stated in two places
**ASN-0071, "Discovery through sharing" and "A worked scenario" (Home/transcluding recovery bullet)**: "Discovery through sharing" devotes a paragraph to recovering home-vs-transcluding via `origin(a)` ("This non-distinction is recoverable from the address structure already returned. For each `a ∈ iaddrs(Q)`, `origin(a)` ... Comparing `origin(a)` against each `d ∈ find(Q)` recovers the relationship..."), and the worked-scenario bullet repeats it ("`d_A = origin(a₁)` is `a₁`'s home, while `d_B` and `d_D` ... transclude it").
**Problem**: The abstract recoverability claim and its worked instance are fine individually, but the "Discovery through sharing" paragraph itself states the recovery twice in different words ("This non-distinction is recoverable..." then "The `find` operation does not need to tag its results because tagging is a function the requester can compute"). The two sentences carry one idea.
**Required**: Collapse the two sentences in "Discovery through sharing" into one statement of the recoverability fact.

## OUT_OF_SCOPE

### Topic 1: Relationship to historical containment relation R
Posed correctly as an Open Question; the present-tense semantics are fully specified and the `R`-relationship is future territory.

### Topic 2: Replica freshness and visibility filtering
"What we do not specify" (ii), (iii) correctly defer these to separate specifications; they are not errors here.

VERDICT: REVISE
