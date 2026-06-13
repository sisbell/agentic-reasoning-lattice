# Review of ASN-0130

The technical core is strong. The substitution-lemma proof in PR3a is a genuine proof (WT-α, WT-W, k-fold PC2 discharge, capture/interference both checked); PR2's acyclicity is run event-wise and handles re-registration; the wp analyses in PR0 and PR5a are real, not trivial; and the PR5 lint derivation earns its conclusion via the prefix-incomparability argument (T10a.2 for same-origin, anchor-comparability contradiction for cross-origin). I found no correctness error and the depth requirements (concrete worked composition, non-trivial wp, derived consequences) are met. The findings below are one exposition-completeness gap in a wp derivation, plus the meta-prose patterns the `review-mode.anti-bloat` classifier directs me to surface.

## REVISE

### Issue 1: PR0 wp first disjunct — the "hits" determination omits the slot-2 step

**ASN-0130, PR0 (success/wp, first disjunct)**: "a `VALID`-passing call hits (I1's branch at the `pdef` class) — the incumbent is I0-equal and canonically shaped, every tuple at one start having entered as a `register_pred` deposit, so `F' = enc({a'})` with `subtree(a') = coverage(F') = subtree(a)` forcing `a' = a` — and returns it at `Σ' = Σ`".

**Problem**: I1's *hit* requires I0-equality, which is coverage equality on **both** slots — `coverage(F) = coverage(F')` *and* `coverage(G) = coverage(G')`. The quoted justification establishes only the slot-1 (F) equality, via `a' = a`. The slot-2 (G) equality — that the presented run `A_def` and the incumbent's registered run have equal coverage — is what actually forces the *hit* rather than a fresh deposit, and it follows from PR-ENC-uniq (both runs are parse-valid and start at `a`, so they coincide), which is not cited here. The wp truth-value survives the omission (a standing active tuple satisfies POST-ref whether the call hits or deposits, since emit does not remove active tuples), so this is an exposition gap, not a correctness error — but the note asserts the hit and returns the incumbent at `Σ' = Σ`, and that conclusion is unjustified without the G-coverage step.

**Required**: Add the slot-2 step — by PR-ENC-uniq the presented run equals the incumbent's registered run, so `coverage(G) = coverage(G')`; with `a' = a` this gives I0-equality, hence the hit.

### Issue 2: Essay content in a proof slot (PR1)

**ASN-0130, PR1 (final sentence)**: "(Contrast every system whose code artifacts are mutable: there, validation of the content-intrinsic part is a cache; here it is a fact.)"

**Problem**: This is a rhetorical contrast against "every system whose code artifacts are mutable," appended after the permanence proof is already complete. It advances no part of the argument — the cache-vs-fact distinction is editorial color. This is exactly the essay-in-structural-slot pattern the anti-bloat pass targets.

**Required**: Delete. The conjunct-division argument (content/signature-intrinsic vs. deposit-time endorsement) already carries the point.

### Issue 3: Triple preview — intro "three foundation facts" ↔ "What this note commits" ↔ the claims

**ASN-0130, intro para 2**: "Content is immutable and permanent … so a validated definition's content can never drift (PR1). Identity is by origin, not value … (PR-ENC). And registration events are totally ordered … can only point backward in first-registration order (PR2 …)."
**ASN-0130, "What this note commits"**: the PR1 / PR-ENC / PR2 bullets restate the same three facts ("permanent proof that its run parse-validated and well-typed"; "identified by the run's start address"; "the reference graph is a DAG").

**Problem**: PR1, PR-ENC, and PR2 are each stated three times before their proof — once as a "foundation fact" in the intro, once as a "commit" bullet, once as the claim. The two summary passages say the same things in different words. A reader following the argument reads the gist twice as preamble, then a third time with the proof. PR5 carries the same internal repetition: "every `Γ_D`-instantiation … is ⊤-stable" is asserted three times within the one claim.

**Required**: Keep one preview layer, not two. Either fold the intro's "three foundation facts" paragraph into the commits bullets or drop the bullets that merely paraphrase a claim; collapse PR5's repeated "every-instantiation ⊤-stable" to a single statement.

### Issue 4: Cross-section mutual deference + defensive justification for the seal

**ASN-0130, PR-DISC**: "This is the note's central scoping hypothesis; the entry-point seal (Standard registrations) discharges it for the shipped surfaces."
**ASN-0130, PS2 (Entry points — the seal)**: "The seal is what makes the registration discipline (PR-DISC) a fact about the shipped surfaces rather than an assumption: without it, a direct `Emit_pdef` call … could mint an unvalidated classifier through a shipped surface. ASN-0128 closed the identical hole for [R] structurally; this note closes its two the same way."

**Problem**: Two paragraphs in two sections assert the same relationship ("the seal discharges PR-DISC"), each deferring to the other's location. The PS2 passage additionally carries a defensive "without it, X could happen" hypothetical and an ASN-0128-precedent note — neither states what the seal *does* (extend the `Emit_K` precondition to `K ≁ R ∧ K ≁ pdef ∧ K ≁ pd_stable`); they argue why it is wanted. The mechanical statement is the load-bearing content; the rest is justification.

**Required**: State the seal once where it is defined (PS2), with the precondition extension as the content. Replace PR-DISC's forward gesture and PS2's "without it / ASN-0128 did the same" with at most a single clause noting the seal discharges PR-DISC.

## OUT_OF_SCOPE

### Topic 1: Dangling live references, cross-substrate portability, naming, certificate classes beyond ST
**Why out of scope**: The note already lists these as Open questions 1–4 and "What this note doesn't cover," and they are correctly placed there — each is a new designated class or a new policy decision, not a defect in the present claims. I raise them only to confirm I am not asking for them here.

### Topic 2: Concurrent and re-registration scenarios in the worked example
**Why out of scope**: The worked composition does not exhibit two writers registering byte-identical runs at distinct addresses, nor a de-register-then-re-register cycle. The underlying behavior is covered (I4 ConcurrentEmitFirstCommit and I2 for the empty-class re-deposit, both ASN-0128), and PR2 already runs its argument event-wise to accommodate multiple deposit events, so this is elaboration for a future worked example, not a gap in the claims.

VERDICT: REVISE
