# Review of ASN-0130

This is careful work. PR3a's expansion-well-typing is a genuine substitution induction (WT-α + WT-W + the per-step PC2 lowering), the wp analyses in PR0/PR5a argue tightness off-discipline rather than asserting it, and the hard boundary cases — self-reference (PR2(b)), forward/frontier-ghost reference (step 5), born-nullified registration, evaluation surviving de-registration via permanent `sig` and immutable content — are all handled. The proofs hold. The findings below are one real boundary omission and, as the anti-bloat classifier directs, accreted meta-prose.

## REVISE

### Issue 1: Use-site inventory in "Discipline and uniqueness"
**ASN-0130, PR0 / Discipline and uniqueness**: "The note's downstream claims — PR0's wp equivalence (its C3 form needs registration discipline, its reduced form surface discipline besides), PR1, PR2, PR-SIG's `sig` well-definedness and with it WT-ref's groundedness, PR3 with PR3a (... flagged there), PR5's lint reading, PS1's dedup reading — are scoped to derivations that are registration-disciplined and surface-disciplined."
**Problem**: This is a downstream-consumer catalog — eight forward pointers in one sentence — that advances the definition of *registration-disciplined* not at all. Worse, it duplicates information already present at every one of those sites: PR1 opens "At any state Σ reached by a registration-disciplined derivation," PR2 opens "Under PR0's discipline," PR3a opens "On registration-disciplined derivations," PR3 says "on registration-disciplined derivations (PR0's scope list...)." Each claim already declares its own scope. The inventory then becomes a referenced object ("PR0's scope list" is cited from PR3 and PR3a), compounding the redundancy. When the reader reaches PR1 they get the scope locally; the central list is read once and never needed again.
**Required**: Delete the inventory sentence. Keep the substantive content of the paragraph (the definition of registration-disciplined, the I1a discharge, the prefix-freeness sharpening to one-active-registration-per-address). Each downstream claim already states its scope; that is where the scope belongs.

### Issue 2: `register_pred` is undefined on empty `A_def`
**ASN-0130, PR0**: "writing `a := min(A_def)` (T1) and `n := |A_def|`: (i) the run is resident and chain-contiguous — `A_def ⊆ dom(Σ.C)` and `A_def = {shift(a, k) : 0 ≤ k < n}` ..."
**Problem**: `A_def` is caller-supplied, and no precondition or validation clause excludes `A_def = ∅`. On empty input `a := min(∅)` is undefined, so condition (i) cannot even be evaluated, and (ii)'s "parse from `a`" has no start to parse from. PR-ENC's `n ≥ 1` constrains the *artifact*, not the *operation input*; the reader must import it, and even then `min(∅)` blocks (i). The note extends real rigor to adversarial references (step 5's frontier-ghost) and to the born-nullified boundary, but the degenerate empty input — exactly the "empty structure" case the standard demands — is left unspecified.
**Required**: Add an explicit clause — a precondition `A_def ≠ ∅`, or a validation condition (0) "`A_def` is a non-empty finite address set" rejected like any other failure — so the operation's behavior on empty input is stated, not left to `min(∅)`.

### Issue 3: The "bare Multi gate" rationale is stated twice, and the off-discipline failure is narrated four times
**ASN-0130, PR-SIG**: "a raw `pdef`-class deposit — admissible at the bare Multi gate, which reads span counts, never content — can mint an active tuple denoting a start that never validated."
**ASN-0130, Standard registrations**: "a direct `Emit_pdef` call — admissible at the bare Multi gate, which reads span counts, never content — could mint an unvalidated classifier through a shipped surface."
**Problem**: These two passages assert the same fact in near-identical words ("admissible at the bare Multi gate, which reads span counts, never content"). More broadly, the off-discipline failure mode is narrated four times — the two above, plus PR0's two "Off-discipline this direction fails" passages in the wp. The wp instances earn their place (they prove the wp's scoping hypothesis is tight, with the I0a separating pair). The PR-SIG parenthetical and the seal paragraph do not: they describe the same hazard, and the seal paragraph is its natural home (it is where the hazard is closed). A lesser instance of the same pattern: PR-ENC's "typing a reference consults the referent, so it is not a property of one run's content" previews PR-SIG's stratification argument in full.
**Required**: State the raw-deposit hazard once, at the seal (where it is enforced), and have PR-SIG cite it rather than re-narrate. Trim PR-ENC's stratification preview to a bare forward pointer, since PR-SIG carries the argument.

### Issue 4: Essay framing in structural slots
**ASN-0130, opening**: "Three foundation facts make the design nearly free, and the note's work is mostly to compose them."
**ASN-0130, PR0**: "There is no contradiction: validation is an operation, surface-level work whose product is a structural fact (the tuple) that PL can read. The division of labor is the note's central move ..."
**Problem**: "make the design nearly free," "the note's work is mostly to compose them," "the note's central move" are editorial appraisals, not claims. The PR0 paragraph also opens defensively ("There is no contradiction") against an objection the reader has not raised. The substantive content in that paragraph — content is dereferenced only at the operation surface (registration, resolution, expansion), never inside PL evaluation, so ASN-0129's structural-reads-only boundary is untouched — is a real and useful clarification worth one sentence. The defensive opener and the "central move" editorializing are not.
**Required**: Drop the appraisal framing. Reduce the PR0 paragraph to its factual core (one sentence: content is read only at the operation surface, never in PL evaluation). The three foundation facts in the opening are fine; the sentence declaring them "nearly free" is not.

## OUT_OF_SCOPE

### Topic 1: Dangling live references
A definition registered while its referent was active, whose referent is later de-registered (PR0 (iv) only checks the *new* registration). The note raises this as Open Question 3 and shows evaluation still works (content + `sig` permanent). Whether de-registration should be blocked while live referents exist, or checked transitively at evaluation time, is a policy question for a future ASN.
**Why out of scope**: The note's invariants (PR1, PR3 precondition) hold regardless of the resolution chosen; this is new territory, correctly deferred, not a gap in PR0–PR5a.

### Topic 2: Supersession × certification interaction
When `v1` is certified and superseded by `v2`, the certificate does not transfer — `v2` requires its own `certify_pd_stable` (worked example step 4 shows exactly this).
**Why out of scope**: This is the intended behavior (certificates are per-address, PS2), not an omission; no future work is required, but it is worth confirming the note handles it rather than glossing it.

VERDICT: REVISE
