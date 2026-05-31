# Review of ASN-0093

## REVISE

### Issue 1: SubAllocatorAxiom.Exists is tautological given the definition of "active"

**ASN-0093, Address sub-allocators / SubAllocatorAxiom.Exists**: The *Active sub-allocator chains* paragraph defines "a sub-allocator chain `A_C(d)` ... is *active at state* `Σ` iff `d ∈ dom(M)` at `Σ`." SubAllocatorAxiom.Exists then asserts: "For every `d ∈ dom(M)`, the content sub-allocator chain `A_C(d)` ... and the link sub-allocator chain `A_L(d)` ... are active (per the *Active sub-allocator chains* definition above)."

**Problem**: This clause states `d ∈ dom(M) ⟹ active`, where `active` is *defined* as `d ∈ dom(M)`. It is a restatement of the definition and carries no content. The only non-vacuous reading — that the stream objects `A_C(d) = S(b_C(d),1)`, `A_L(d) = S(b_L(d),1)` exist — is already unconditional from ASN-0040's SiblingStream (defined for any `B6`-valid parent, and `(b_·(d),1)` is shown `B6`-valid from M0). So Exists postulates nothing an axiom is needed for.

**Required**: Either delete the Exists clause, or restate the actual content it is meant to carry (and if that content is "the streams exist," cite ASN-0040 and drop it from the axiom — it is derived, not postulated).

### Issue 2: SubAllocatorAxiom.FirstEmission is derivable, not axiomatic

**ASN-0093, SubAllocatorAxiom.FirstEmission**: "the first address produced by `A_C(d)` is `t_1^C(d) := [d.0.s_C.1]` ... and T4-valid by direct inspection" (and the link analog).

**Problem**: ChainDiscipline already commits each chain to be the ASN-0040 sibling stream `S(b_·(d),1)` rooted at `inc(b_·(d),1)`. The first element's structural form `[d.0.s_C.1]` follows from ASN-0040's SiblingStream postcondition `cₙ = [p₁,…,p_{#p},0…0,n]`, and its T4-validity follows from TA5a (`k=1` unconditional on T4-valid input) given M0. The note itself re-derives both — in the C1c/L1c chain exhibitions and in worked-example Steps 2–3. A clause that the document proves elsewhere is a lemma, not an axiom. Stating it as a third axiom clause is over-axiomatization and creates a redundant entanglement (ChainDiscipline cites "FirstEmission's `t_1^C(d) = inc(b_C(d),1)`," which is circular against an axiom that should be a consequence).

**Required**: Demote FirstEmission to a lemma discharged by ChainDiscipline + the ASN-0040 SiblingStream postconditions + TA5a, or identify what independent content (not derivable from ChainDiscipline) justifies axiom status.

### Issue 3: Use-site inventories and forward-reference meta-prose in structural slots

**ASN-0093, multiple locations**:
- After SubAllocatorAxiom: "The substrate's freshness obligations decompose as: (i) ... (ii) ... (iii) ... Together these cover the full sub-allocator chain lifecycle from activation through arbitrary emission."
- ChainPrefixExtension's "*Quantifier scope*" sub-paragraph: "The K.α and K.λ subsequent-emit derivations exploit this by citing the prefix relation at a freshly emitted address ... *before* it is committed."
- After the ChainMembershipForOrigin proof: "This lemma is the inductive invariant that licenses application of ChainEnumerationInjectivity to `(a_prev, a)` ..."
- After M1: "M1 underwrites every 'remains in dom(M)' claim used downstream and is what allows SubAllocatorAxiom.Exists's ... to be read as a permanent activation."

**Problem**: Each enumerates downstream consumers of a claim rather than advancing the claim's content — the forward-reference accretion pattern the review mode flags. A reader following the definition/lemma does not need its future call sites listed at the definition site.

**Required**: Remove the use-site inventories; the disciplines and lemmas stand on their stated content, and the consuming derivations already cite them where used.

### Issue 4: Reviser-drift prose justifying definition-vs-consequence structure

**ASN-0093, *Active sub-allocator chains***: "Across-state permanence — once a sub-allocator chain is activated it remains active at every successor state — is not part of this definition; it is a *consequence* of M1 ... The per-state activation condition stated here is the load-bearing notion; the across-state corollary is derived rather than postulated."

**Problem**: This is prose explaining *why the structure is chosen* (per-state definition vs derived corollary) rather than stating content. The substantive fact (permanence follows from M1) can be stated in one clause; the surrounding "is the load-bearing notion / is derived rather than postulated" commentary is meta-justification.

**Required**: Reduce to the operative statement: "active at `Σ` iff `d ∈ dom(M)`; permanence of activation follows from M1." Drop the commentary.

### Issue 5: Duplicate prose

**ASN-0093, discharge matrix and front matter**:
- The parenthetical "(`E(·)` is T4b's structural projection on the address alone, depending on no state component, so prior keys' `#E(a) ≥ 2` transfers unchanged ...)" appears verbatim-equivalent in the C1b/K.σ, L1b/K.σ, and L1b/K.α matrix cells.
- The "factoring is downward from a fuller transition model ... `E_doc` → `dom(M)`" claim is stated in the opening paragraph, again in *Scope*, and again across *Properties Introduced* rows.

**Problem**: Two (or more) paragraphs/cells saying the same thing in different words — the duplicate-prose pattern flagged for this note.

**Required**: State each once (the E-projection-is-structural fact once, e.g., at C1b's definition; the `E_doc → dom(M)` factoring once in the intro) and reference it rather than restating.

## OUT_OF_SCOPE

### Topic 1: Link withdrawal / tombstoning
**Why out of scope**: The Open Questions section's three-path discussion (arrangement-layer withdrawal, value tombstone, embedded marker) is correctly deferred; withdrawal is explicitly out of scope per the substrate's stated boundary, and the note commits to none of the paths.

### Topic 2: Arrangement mutation, entity stratification, provenance
**Why out of scope**: The K.μ family, `Σ.E`, and `Σ.R`/`K.ρ` are deferred to higher-layer ASNs; the vacuous holding of S2/S3/S8a/D-CTG under `M(d)=∅` is the correct substrate-layer treatment.

VERDICT: REVISE
