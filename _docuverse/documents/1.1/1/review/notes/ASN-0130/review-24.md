# Review of ASN-0130

The mathematics here is sound. I worked the hard cases — self-reference (PR2b), de-registration and re-registration (PR2 event-wise + I2), born-nullified registration (PR0 + C3), the `k = 0` / `n = 1` boundaries, and the full substitution induction in PR3a — and each holds. PR2's acyclicity-by-construction is genuinely airtight (a cycle's second member cannot validate before the first deposits), the wp derivations partition correctly, and PR3a's WT-α/WT-W lemmas discharge expansion well-typing rule-for-rule. The exact-coverage argument for the lint (`t ∈ subtree(t') ⟹ t' = t` between definition starts) is correct. I found no correctness defect.

What follows is on the dimension this note's `review-mode.anti-bloat` classifier asks for: meta-prose and duplication accreted across cycles.

## REVISE

### Issue 1: One insight ("evaluation keys on ever-registration, not active") is fully articulated in three places
**ASN-0130, PR1 / PR3 / PR5a**:
- PR3: "A de-registered definition therefore still evaluates: evaluation keys on *ever-registration*, not active registration (PR1)." (and, two sentences earlier, "Active registration is *not* required, of `a` or of any referent…").
- PR1: "evaluation (PR3) keys on *ever-registration*, not (iv)-currency — a de-registered referent still resolves and expands, its deposit-state validity proved once and preserved in the audit slice…".
- PR5a (0)/(i): "ever-registration is all `sig(a)` and `expand(a)` need (PR-SIG, PR3)".

**Problem**: PR1 and PR3 each say the same thing in full — "de-registered definitions still resolve/expand/evaluate because evaluation keys on ever-registration" — and cite *each other* doing it. This is the circular cross-reference + restated-claim pattern. The point is PR3's evaluation contract; PR1 and PR5a are downstream beneficiaries, not co-authors of it.
**Required**: State the contract once at PR3 ("evaluate's precondition is ever-registration, not active registration; a de-registered definition still resolves, expands, and evaluates"). In PR1, replace the full restatement with a bare citation ("harmless: evaluation keys on ever-registration, not (iv)-currency — PR3"); PR5a already does the right thing by citing, so leave it.

### Issue 2: PR0 (iii) re-derives PR-SIG's signature-grounding inside the validation list
**ASN-0130, PR0, condition (iii)**: "the decoded signed term well-types, `Γ_D ⊢ body : C_D`, under WT plus WT-ref (PR-SIG) — each reference node's `sig(r)` defined exactly because (iv) holds — an entailment registration discipline supplies (PR-SIG, PR-DISC) — PR-SIG having fixed a registered referent's signature at its first registration, the surface checking (iii) and (iv) jointly".

**Problem**: PR-SIG already establishes this exact grounding ("condition (iv) requires each referenced r actively registered, so — on the registration-disciplined derivations — `sig(r)` is defined and immutable"). PR0 (iii) re-proves it with three nested em-dash asides mid-list, so the bare claim — "(iii): the body well-types under WT + WT-ref" — is buried under relocated PR-SIG content. A reader has to skip past the justification to read the validation condition.
**Required**: Reduce (iii) to the condition plus a citation: "(iii) the decoded term well-types, `Γ_D ⊢ body : C_D`, under WT + WT-ref — decidable because (iv) makes each referent's `sig(r)` defined (PR-SIG)." Drop the "an entailment registration discipline supplies… the surface checking (iii) and (iv) jointly" chain.

### Issue 3: PR-SIG's least/greatest-fixed-point gloss is rationale, not definitional content
**ASN-0130, PR-SIG**: "Allocate two runs, each referencing the other's start, neither registered: whether either well-types needs the other's signature first — a loop with no ground, where a least-fixed-point reading calls both invalid, a greatest calls both valid, and content decides nothing."

**Problem**: The concrete example (two mutually-referencing runs) is legitimate and carries the point. The trailing lfp/gfp sentence is the meta part — it explains *why* "no ground" is unfixable rather than advancing what the stratification *is*, and is removable without loss to the argument. Same paragraph's "the induction below — with every claim that consumes `sig` — is scoped to…" gestures at downstream consumers rather than stating the scope.
**Required**: Keep the mutual-reference example and the conclusion ("registration order grounds the type layer"); cut the "least-fixed-point reading calls both invalid, a greatest calls both valid, and content decides nothing" clause and the "with every claim that consumes `sig`" aside.

## OUT_OF_SCOPE

I found no future-ASN gap the note has not already fenced. Its Open Questions correctly place the genuinely-deferred territory — human-facing naming (Q1), cross-substrate portability (Q2), dangling live references (Q3), and certificate classes beyond ST (Q4) — and "What this note doesn't cover" correctly defers the concrete byte encoding (a substrate parameter), activation/triggers (protocol layer per ASN-0129's fence), and the certifier's checking algorithm (ASN-0129 Open Q5). These are placements, not errors. Concurrent `register_pred` of the same run is adequately inherited through the wrapped `Emit_pdef`'s idem-⊤ contract (I4, ASN-0128) and needs no restatement.

VERDICT: REVISE
