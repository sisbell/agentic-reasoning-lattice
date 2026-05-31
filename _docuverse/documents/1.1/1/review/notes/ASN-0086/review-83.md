# Review of ASN-0086

## REVISE

### Issue 1: Arrangement-modification frame derivation repeated three times verbatim
**ASN-0086, "Two Foundational Sets" (↦ paragraph), "Definition — BroadExtension," and "Lemma — LinkStoreInvarianceUnderArrangement" proof**: each independently reconstructs `Σ'.L = Σ.L` along `↦ \ →` from "(i) L12 value-preservation, (ii) L12a no-removal, (iii) link-store extension partitioned into K.λ-steps."
**Problem**: The same (i)/(ii)/(iii) derivation from the same three premises appears three times in three different sections. This is the "multiple paragraphs say the same thing in different words" pattern the anti-bloat classifier flags. The reader must re-verify the identical argument at each site.
**Required**: State the derivation once (the LinkStoreInvarianceUnderArrangement lemma is the natural home), and have the `↦` definition and BroadExtension cite it rather than re-deriving.

### Issue 2: R7a proof-intro use-site inventory plus name mismatch to its own block
**ASN-0086, R7a proof, opening paragraph**: "The monotonicity argument consumes four directly (L12, L12a, S0, S1); the per-iteration replay discharges each step's preconditions (enumerated in the (1)–(4) bullets below) and preserves the remaining catalog by step type and mechanism (enumerated in the *Per-step substrate-invariant discharge* block below)."
**Problem**: Two defects. (a) This is a roadmap/use-site inventory that advances no reasoning — it pre-announces which invariants later paragraphs will cite. (b) It names the target block "Per-step substrate-invariant discharge," but the actual block is titled "Per-step substrate-invariant preservation." A forward pointer that doesn't match its target degrades navigability.
**Required**: Delete the inventory sentence (the bullets and block below carry their own citations); if a pointer is retained, fix the name to match the block.

### Issue 3: "Load-bearing site for catalog (b)" stated twice in R7a
**ASN-0086, R7a proof, bullet (4)(iii)** ("This is the load-bearing step relying on catalog (b) being strictly stronger than catalog (a)") **and the paragraph following the case analysis** ("This is the load-bearing site for catalog (b) — Chain Discipline Catalog — of substrate-conformance ... without ChainMembershipForOrigin preserved to Σ', R0a-Cor1 would not pin down a unique chain enumeration").
**Problem**: The same point — that catalog (b) is the load-bearing assumption and catalog (a) alone is insufficient — is made twice, once inline and once again after the cases, including the `a*` remark. Duplicated emphasis.
**Required**: Keep the single most complete statement (with the `a*` counterexample) and remove the inline restatement.

### Issue 4: Catalog-membership justifications in the substrate-conforming layer definition are meta-prose
**ASN-0086, "Definition — substrate-conforming layer," sub-blocks "L5/L6/L8 discharge" and "L-permissions omitted"**: "The catalog above deliberately excludes the ASN-0043 *permissions* L4(c), L7, L9, L10, L11b: these license endset-content or non-injectivity patterns but constrain no state-bound value, so they carry no preservation obligation and are never re-cited as discharge targets at any emission site in this note."
**Problem**: "L-permissions omitted" explains *why something is not in the catalog* rather than defining the catalog — the exact "explains why X is needed/excluded rather than what it says" reviser-drift pattern. The catalog is a definition; a definition does not need to justify its own complement.
**Required**: Drop "L-permissions omitted" entirely (an unlisted invariant is simply not required — no prose needed). Collapse "L5/L6/L8 discharge" to a one-line note that these three are value-shape commitments discharged by K.λ's value-shape precondition.

### Issue 5: R7a "categorical across all layers" framing oversells what is proved
**ASN-0086, R7a and preceding `↝` definition**: "R7a quantifies over `↝` to make its claim categorical across all layers that conform to substrate invariants."
**Problem**: R7a's load-bearing precondition (catalog (b), specifically ChainMembershipForOrigin preserved at Σ') already forces every fresh link to be a sibling-frontier chain element — which is most of the conclusion. The proof's own `a*` remark concedes catalog (a) alone is insufficient. So R7a is not "categorical across all conforming layers"; it is categorical across layers that already produce chain-discipline-conforming states. The framing should not advertise more generality than the precondition delivers.
**Required**: Either weaken the prose to state that R7a characterizes layers preserving the chain-discipline catalog (and note this is automatic for any K-operation-only layer), or make explicit that catalog (b) is the substantive hypothesis and "categorical" refers to that restricted class.

### Issue 6: DEF-Consequence label rationale is justificatory padding
**ASN-0086, "Properties Introduced," type-labels paragraph**: "DEF-Consequence marks tautological consequences of a Definition's quantifier-range or argument-shape commitment whose downstream implications ... warrant separate naming as substantive properties even though their content follows directly from the Definition."
**Problem**: A table legend should name the label, not argue for the label's existence. The clause "warrant separate naming ... even though their content follows directly" is a defense of a taxonomy choice, not legend content.
**Required**: Reduce to "DEF-Consequence: a direct consequence of a Definition's quantifier range or argument shape (e.g., R6b)."

## OUT_OF_SCOPE

### Topic 1: Concurrency, atomicity, and Observe ordering
**Why out of scope**: The Open Questions correctly defer Emit/Observe atomicity, the consistency model for `A_K` transitions, and Observe result ordering. These require a concurrency model this note does not introduce; deferring them is appropriate.

### Topic 2: Higher-arity active subsets `A_K^{(n)}`
**Why out of scope**: Restricting `L_K`/`A_K` to standard-triple links is stated explicitly, and the multi-arity extension is listed as an open question. Not an error in this note's stated scope.

VERDICT: REVISE
