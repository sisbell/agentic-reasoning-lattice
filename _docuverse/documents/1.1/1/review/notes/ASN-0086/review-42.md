# Review of ASN-0086

## REVISE

### Issue 1: Three-field tag convention is pure infrastructure
**ASN-0086, Setup section**: "Each R-claim and named operation below carries a headline tag of the form `[setup: req|free, discipline: req|free|N/A, stipulation: req|free|N/A]`"
**Problem**: Tags appear at every R-claim and operation, plus the Properties table. They record dependency tracking that belongs *in* proofs, not in claim headlines. Tags don't help understand what the claim says; they're inventory. R0 tagged `[setup: req, discipline: N/A, stipulation: N/A]` requires the reader to verify the claim, then walk Step 4's L14a-preservation step to discover why Setup is consumed — the tag is then redundant with the proof.
**Required**: Remove the tag system. Where a hypothesis is consumed, state it at the consumption site in the proof.

### Issue 2: FramePreservation lemma over-formalizes input substitution
**ASN-0086, Setup section**: A named LEMMA with five specializations stating "if predicate doesn't read X, substituting X doesn't change predicate value."
**Problem**: This is input substitution — `P(Σ) = P(Σ')` when `Σ.X = Σ'.X` and `P` doesn't read X. It's trivially true and the proof is "by definitional identity of inputs." Stating it as a named lemma with five "specializations (a)–(e)" and then citing it as "FramePreservation specialization (a)" at R0 Step 4 turns a one-line substitution into a multi-paragraph citation network.
**Required**: Delete FramePreservation. Where it's invoked, write directly "Σ'.C = Σ.C and Σ'.M = Σ.M by Frame, so [the predicate] holds trivially."

### Issue 3: The substrate primitive vs. discipline tension is restated repeatedly
**ASN-0086, multiple locations**: The same observation — "the substrate primitive admits broader emissions than the discipline; R0a holds only under the discipline; udanax-green realizes the discipline" — appears in (a) Substrate emission primitive paragraph, (b) "Breadth of the primitive vs. the discipline R0a names" paragraph, (c) Definition of Sibling-frontier discipline, (d) R0a's preamble, (e) R0a's Remark on substrate evidence, (f) Emit_K's "Why the construction is bound" paragraph, (g) Appendix B.
**Problem**: Seven separate statements of the same conditional relationship. Each one explains why R0a fails without the discipline, why udanax-green satisfies it, and why a hypothetical alternative emission policy would falsify it.
**Required**: State it once at the Definition of Sibling-frontier discipline. R0a's preamble can cite. The other locations should reference, not restate.

### Issue 4: Worked Sketch is over-instantiated
**ASN-0086, Worked Sketch**: Six numbered steps with concrete L-invariant verification at every fresh emission.
**Problem**: Steps 1 and 2 establish the active/audit distinction concretely — this is the worked sketch's payoff. Steps 3 (cross-document retraction), 4 (Observe with both views), 5 (R6c persistence across two transitions), and 6 (R6b non-recursion under second-order retraction) each re-exercise the same verification machinery (L-invariant check at a fresh address, coverage computation, set-difference for `A_K`). The 6-step worked example certifies what the schematic proofs already established; it should illustrate, not re-verify.
**Required**: Keep Steps 1–2 as the worked sketch. Move Steps 3–6 to a numbered Examples section if they're needed at all; most could be deleted.

### Issue 5: Appendices A and B are commentary
**ASN-0086, Appendix A** ("Coarsening of ASN-0034's transition relation"): explains how this ASN's `→` relates to ASN-0034's transitions.
**ASN-0086, Appendix B** ("Failure modes: necessity of the sibling-frontier discipline"): catalogs what breaks when the discipline is violated.
**Problem**: Both are commentary about the specification, not specification. Appendix A is meta-prose justifying an abstraction choice. Appendix B catalogs what's already explicit in the body (R0a's discipline-conditional form together with L12 + L12a entail permanent failure of the antichain after one non-disciplinary step).
**Required**: Delete both appendices. The substantive content from Appendix B (the concrete `a' = a₁.1` instantiation) can be folded into a single sentence in R0a's discipline-conditional remark.

### Issue 6: R7/R7a/R7b/"NullifyIsEmit" naming is convoluted
**ASN-0086, Properties Introduced and R7 area**: R7a is a substantive lemma; R7b is named as "the legacy label" for the relational layer's Definition; R7 (no subscript) is a "legacy alias" for the consequence; the consequence is also called "NullifyIsEmit"; the Properties table doesn't include R7 or R7b as separate entries.
**Problem**: Four labels (R7, R7a, R7b, NullifyIsEmit) for what amounts to one lemma plus one definitional consequence. Readers trying to cite "R7" must determine which alias is meant. The "legacy" framing suggests prior cycles renumbered.
**Required**: One label per claim. R7a (the substantive lemma) and R7 (the definitional consequence) should be the only labels; drop R7b and "legacy alias NullifyIsEmit."

### Issue 7: Edit-history meta-prose
**ASN-0086, Properties Introduced**: "Note: the prior R6 'ActiveSubsetWellDefinedness' entry has been folded into the Definition of ActiveSubset (well-definedness check is one line of set-difference accounting against Σ.L); no separately numbered R6 exists"
**Problem**: This is edit-history that the reader doesn't need. Just present R6a/R6b/R6c, or renumber to R6/R7/R8.
**Required**: Remove the "folded in" note. Either renumber or accept that R6a/R6b/R6c stand without explanation.

### Issue 8: SharedDepthOneAllocator preamble is essay-length
**ASN-0086, Setup section**: The SharedDepthOneAllocator lemma is preceded by paragraphs labeled "Naming convention for unnumbered lemmas," "Allocator-naming convention," with a "Depth-notation caveat" inside the lemma itself, then a 3-step proof, then "Subspace-routing and allocator-tree-depth-2 independence" remarks, then "Status" remarks, then "This corollary is consumed at..." use-site enumeration, then "Reconciliation with Nelson's design" prose.
**Problem**: Essay content occupies a structural slot. The lemma's statement is buried in three paragraphs of scaffolding before the proof and three after. The "Consumed at" use-site listing is exactly the "use-site inventory" pattern flagged in the bloat criteria.
**Required**: State the lemma. Give a 3-step proof. Delete the surrounding essay material; downstream sites can cite by name when they consume.

### Issue 9: Defensive justifications around hypotheses
**ASN-0086, Setup section** (Setup hypothesis): "Setup is not derivable from ASN-0036's class-(ii) emission primitive, which permits content emission at any T4-valid c..."
**ASN-0086, Setup section** (Subspace distinctness): "This is adopted as an explicit hypothesis of this note, parallel to the s_C-resident content hypothesis above. The distinctness is *presupposed* by ASN-0043's L0/L0a partition and L14's scoped disjointness (both collapse... if s_C = s_L), but ASN-0043 does not state it as one labeled fact."
**Problem**: Both axioms are accompanied by paragraphs explaining *why* the axiom is needed rather than *what* the axiom says. The "Maintenance protocol" sub-paragraph for Setup is another instance: "Tightening ASN-0036's class-(ii) primitive to require subspace_I(c) = s_C would discharge it at every reachable state" — this is design discussion, not specification.
**Required**: State each axiom in one line. Delete the rationale paragraphs.

### Issue 10: Multiple paragraphs defer to the same downstream location
**ASN-0086, Scoping note, R6c statement, BroadExtension definition, R6c-Corollary**: Each defers (in different words) to R6c-Corollary's role of lifting from `⊑` to `⊑̂`.
**Problem**: The R6c/R6c-Corollary split is justified four separate times. Each justification re-explains the `→` vs `↦` distinction. The substantive proof of R6c-Corollary is two sentences (`A_K` depends only on `Σ.L`; arrangement-modifying transitions hold `Σ.L` identical) and could be a one-line corollary stated immediately after R6c.
**Required**: State R6c once, with the corollary as a one-line attachment. Delete the Scoping note's anticipation of R6c-Corollary; remove BroadExtension's deferral; collapse R6c's three-paragraph preamble about scope into one sentence.

### Issue 11: R0 Step 4 enumerates L-invariants individually after declaring uniform discharge
**ASN-0086, R0 Step 4**: "Routine L-invariants discharged uniformly via FramePreservation" splits into "(a) value-preservation under class-(iii) frame," "(b) definitional/existential claims," "(c) enabling permissions" — then *also* lists L0, L1, L1a, L1b, L1c, L11a, L14, L14a as "Substantive L-invariants requiring analysis."
**Problem**: After declaring the routine cases discharged uniformly, the proof then enumerates each of the substantive cases at length (multi-paragraph discharge of L11a's Case A vs Case B, etc.). The split between "uniformly via FramePreservation" and "substantive analysis" doesn't reduce verbosity — the substantive cases consume most of the section.
**Required**: Either (a) discharge all L-invariants in a single uniform paragraph citing Frame conditions + the construction's freshness, or (b) verify the substantive cases without the prior "uniformly discharged" preamble.

## OUT_OF_SCOPE

### Topic 1: Higher-arity active subsets
**Why out of scope**: Open Questions correctly identifies this as a future extension; `A_K^(n)` machinery would require its own ASN.

### Topic 2: Concurrency / atomicity of Emit vs Observe
**Why out of scope**: Open Questions correctly identifies this as needing a separate consistency-model treatment.

### Topic 3: Native scoped L14 (without Setup hypothesis)
**Why out of scope**: Open Questions correctly identifies the reformulation work that would be needed.

META: The ASN's substantive specification content — the active/audit distinction with R6a/R6b/R6c, Observe_K, Nullify, and the relational-layer reduction — is legitimate and worth keeping; the surrounding infrastructure (tag system, FramePreservation lemma, appendices, repeated discipline-conditionality discussion, over-instantiated worked sketch) has accumulated to many times the volume of the substantive content and should be pared back, not terminated.

VERDICT: REVISE
