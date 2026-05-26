# Review of ASN-0094

## REVISE

### Issue 1: Non-foundation ASN citations in SubstrateConformingLayer definition
**ASN-0094, *Scope and Substrate Scaffolding*, Definition — SubstrateConformingLayer**: The "Invariant Catalog (a)" enumerates "S0, S1, S2, S3, S7a, S7b, S7c, S7d, S8-fin, S8a, S8-depth, D-CTG, D-MIN, D-SEQ" attributed to "ASN-0036 content/arrangement invariants" and "M0, M1, C0, C1, C1b, C1c, C-fin" attributed to "ASN-0093 substrate invariants". Neither ASN-0036 nor ASN-0093 appears in the foundation list (only ASN-0034, ASN-0043, ASN-0086 are foundations). The Chain Discipline Catalog (b) is implicitly from ASN-0093 as well.

**Problem**: The surrounding paragraph asserts "no external invariant catalog is imported by reference," but the definition itself imports these catalogs by name. Each ASN must be self-contained beyond foundations.

**Required**: Either remove the catalog (a) and (b) lists entirely and rely solely on the scaffolding clauses, or restate the invariants in the catalog as additional scaffolding clauses without referencing the source ASNs. The scaffolding clauses already cover the consumed properties; the catalogs are decorative.

### Issue 2: "Coverage class self-identity at R" empty paragraph
**ASN-0094, Retraction shape section, end of walkthrough**: "*Coverage class self-identity at R.* Retraction is the `K ~ R` case in the framework's coverage classes."

**Problem**: One-line paragraph stating the obvious — R is the retraction type by registration. Adds no information beyond its own heading. Meta-prose accretion.

**Required**: Delete the paragraph.

### Issue 3: Meta-prose categorization in single-home commitment
**ASN-0094, *Single-home commitment* paragraph under SHCD**: "The discipline is realized through the *single-home commitment* — the third per-K layer-discipline contract in the framework, distinct from the *Sh4 idempotency contract* and the *FDD functional-dependency contract*. The consolidated commitment reference table in *Scope and Substrate Scaffolding* records this commitment's signature (gate position 1, applicable K's with NonIdempotentDirectedPair shape + per-K SHCD opt-in, discharged theorem SHCD's homed-set commitment) alongside the framework's other named commitments."

**Problem**: Categorization ("the third per-K layer-discipline contract") and cross-reference to the consolidated table are use-site inventory and defensive cross-referencing. Neither advances the protocol; the protocol clauses (i) and (ii) that follow are the load-bearing content.

**Required**: Reduce to one sentence introducing the protocol, or remove the categorization and cross-reference and let the protocol clauses stand on their own.

### Issue 4: Lifetime constancy stated three times
**ASN-0094, TypedRelationCatalog definition**: "*Lifetime constancy of `T_cat`.* `T_cat` is fixed at `Σ_init` and does not change as states evolve, inherited from the lifetime constancy of `T_cat^rep`..."
**ASN-0094, ShapeRegistry definition**: "*Lifetime constancy.* `shape` is fixed across the substrate's lifetime; it does not change as states evolve."
**ASN-0094, ShapeRegistry, post-Registration-interface paragraph**: "Lifetime constancy is a substrate-level commitment, not derivable from R0…R7a... The lifetime constancy at the registry level reads as: the representative list `T_cat / ~` and the function `shape ∘ (·/~)` are both fixed at `Σ_init` and do not change as states evolve."

**Problem**: Three iterations of the same property in adjacent sections, each saying approximately the same thing. The third instance even re-translates the second into "registry level" language.

**Required**: State once at the introduction of `T_cat`, derive once for `shape` (it inherits from `T_cat^rep`'s lifetime). Delete the re-translations.

### Issue 5: "As a corollary of the *Representative list...* paragraph above" re-explanation
**ASN-0094, ShapeRegistry definition, *Registration interface***: "*Registration interface.* As a corollary of the *Representative list as layer-supplied configuration parameter* paragraph above, the layer's pre-`Σ_init` configuration consists of two paired fixed lists..."

**Problem**: The paragraph re-explains the configuration-parameter idea immediately after the TypedRelationCatalog section established it. The "as a corollary" forward-reference is the very pattern flagged in the addendum ("multiple paragraphs in different sections defer to the same downstream location").

**Required**: Combine with the original paragraph or remove. The shape-side registration mechanics can simply state the function as a list lookup without re-deriving from prior prose.

### Issue 6: Hand-curation conventions in structural slots
**ASN-0094, head of *The Canonical Shape Catalog***: Three numbered "hand-curation conventions" — per-shape uniformity, signature derivation rule, citation convention. Each is referenced obliquely in the per-shape walkthroughs ("Bodies follow the catalog's three hand-curation conventions").

**Problem**: The conventions disclaim what the framework cannot enforce. The disclaimer takes a structural slot (introduction to the catalog) that would otherwise carry the catalog's load-bearing content. The "Citation convention" enumerates allowed citation sources — a use-site inventory rather than a derivation.

**Required**: Either reduce the disclaimer to one sentence ("template signatures are derived from shape components; bodies are author-curated"), or move the elaboration to an Open Question. Keep the catalog's structural slot for catalog content.

### Issue 7: EffectiveWpSimplification mutual-exclusivity table re-derivation
**ASN-0094, Corollary — EffectiveWpSimplification**: The table enumerating four K-registration combinations with their `Π_K` conjuncts is followed by the prose "In every row, at most one antecedent is true, so `Π_K` is well-defined as the single active conjunct..." and "`Π_K` is necessary for the postcondition's *fresh-deposit* reading..."

**Problem**: The mutual-exclusivity argument before the table already proves the property structurally (idem flag pins down which discipline can co-register). The table then re-derives the same conclusion by enumeration. The trailing necessity-of-`Π_K` paragraph adds a third pass on the same point.

**Required**: Either remove the structural argument and keep the table as the proof, or remove the table and keep the structural argument with one worked case. Don't do both.

### Issue 8: AllocatedAddressAntichain — variable rename muddles the case-3 argument
**ASN-0094, Lemma — AllocatedAddressAntichain, Case 3 / Step 3.1**: The lemma is stated and proved using variables `x` (the slot address) and `a` (the candidate descendant). Case 3 is well-organized, but in Step 3.1 the proof says "enumerate its elements as `n_1 < n_2 < n_3` under T0's strict ℕ-order" without first establishing that `|Z_x| = 3` follows from `zeros(x) = 3`. The cardinality argument is implicit and depends on the reader noticing `Z_x` is the set of zero positions, distinct values in `1..#x`.

**Problem**: Each step in a multi-case proof should be self-contained at the cited level. The proof skips from "T4-valid at element level" to "cardinality 3" without naming `zeros(·) = 3` and its set-cardinality consequence. A reader unfamiliar with T4c's identification of zeros-count and level has to reconstruct it.

**Required**: Add one sentence: "Since `zeros(x) = 3` and the zero positions are distinct natural numbers, `|Z_x| = 3`; symmetric for `|Z_a|`." Same gap appears in Step II.1 of LinkAddressNotPrefixOfEmit and should be tightened there too.

## OUT_OF_SCOPE

### Topic 1: Composite shapes (relations whose slot constraints depend on other relations' content)
**Why out of scope**: The ASN already flags this in Open Question 6 with the [refinement candidate] tag. Treating composite shapes would require either a sixth shape-tuple component or a separate composability layer, both substantial extensions.

### Topic 2: Multi-process shape registry consistency
**Why out of scope**: Open Question 7 flags this with [scope boundary]. The Sh4/FDD/SHCD contracts presume sequential `↦`-transitions; distributed coordination is a separate problem.

### Topic 3: Container-level link targeting (`A_M` symbol for `dom(Σ.M)`)
**Why out of scope**: Open Question 8 explicitly defers this with [scope boundary]. The current catalog deliberately restricts to `A_doc`, `A_rel`, `A`.

### Topic 4: Higher-arity links (beyond standard-triple)
**Why out of scope**: The *Arity scope* paragraph in Scope and Substrate Scaffolding explicitly restricts to the arity-3 slice `L^Σ`. Extension to higher arities is correctly deferred.

VERDICT: REVISE
