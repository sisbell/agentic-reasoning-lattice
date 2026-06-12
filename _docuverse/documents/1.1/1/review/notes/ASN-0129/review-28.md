# Review of ASN-0129

I checked every numbered claim, traced the worked composition's four-step trace against the upstream contracts step by step (gate verdicts, dedup branches, C2/C3 landing conditions, the nullified-set arithmetic, the UV rewrite at Σ₄), verified the PD0 class rules against the step frames, and tested the ceiling arguments (PC6 converse, C-reach, C-emit) for unhandled routes — including the BH4 `age`-route into the frontier, which C-emit handles correctly. The technical content holds: the trace's value sequences (⊤,⊥,⊤,⊥,⊥ active; ⊤,⊥,⊤,⊥,⊤ default; ⊥,⊥,⊤,⊤,⊤ audit) all compute out as stated, the aggregate polarity classification is correct in both directions, the quantifier rules are sound over grow-only and step-constant domains, the `Observe_K` normalization in PC6's converse is an exact match, and the conjectures are honestly scoped with their proof obligations recorded rather than discharged by unsound citation. The remaining findings are anti-bloat prose items, per this note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Duplicated guidance — PD1's closing sentence vs. the dynamics section's closing clause
**ASN-0129, Predicate dynamics (PD1 and the section's final paragraph)**: PD1 ends: "A protocol that wants a stable gate over active state must either supply the stability *outside* the language (an operating discipline under which the falsifying steps cannot occur — the move DR makes for C3, ASN-0128) or anchor on PD0's audit class instead." The section's closing sentence then ends: "a sound 'stop when Q' wants Q in PD0's class, or wants the discipline that removes PD1's falsifiers stated as an explicit hypothesis."
**Problem**: The same advice — anchor on PD0's audit class or state the falsifier-removing discipline as an explicit hypothesis — is given twice in full, one paragraph apart, in different words. This is the same-thing-said-twice pattern the anti-bloat classifier flags; the closing sentence's unique content is the composition behavior (∧ preserves ⊤-stability, ¬ swaps classes, PC1 over grow-only domains), and its final clause merely restates PD1's last sentence.
**Required**: Keep one site. Either end the closing sentence after the composition facts ("…the classification is the load-bearing input to any termination argument built over this substrate"), or trim PD1's final sentence to a pointer at the section close. The DR cross-reference should survive at whichever site remains.

### Issue 2: Duplicated ⊥-verdict framing with the identical four-item enumeration — PC2 vs. UV
**ASN-0129, PC2 and UV**: PC2 closes: "⊥ is a *verdict*, with meaning fixed by the atom that returns it (a branch, a cycle, multiplicity, inactivity); the guard propagates the verdict, it does not erase it." UV's verdicts clause then restates: "A ⊥ is a verdict with atom-fixed meaning — branch, cycle, multiplicity, inactivity — and a presentation layer must not manufacture one…"
**Problem**: The verdict framing, including the same four-item enumeration of ⊥'s atom-fixed meanings, is written out in full at both sites. Each occurrence does have local work to do (PC2: the guard propagates; UV: presentation must not manufacture), but the shared framing and enumeration are repeated verbatim in content — accreted restatement rather than reference.
**Required**: UV keeps its novel content — the prohibition on manufacturing verdicts and the concrete `target_of`/retirement conflation example — and cites PC2's framing ("⊥ is a verdict, PC2") instead of re-enumerating branch/cycle/multiplicity/inactivity.

## OUT_OF_SCOPE

### Topic 1: A home-projection read (homed-set as a queryable domain)
C-emit's analysis shows PL has no way to regroup `L_dom` by home — `home(a') = d` is exposed by no atom and not characterizable by prefix testing, which is precisely what makes the self-emit test inexpressible at this surface. A future protocol wanting home-scoped queries ("all links homed at d", per-document link budgets, home-relative traffic disciplines beyond BH4's `age`) would need a `homed_at` atom or homed-set base. That is a deliberate exclusion here, correctly fenced by PC6's granularity restriction; adding the atom is future territory, with the explicit cost that C-emit's inexpressibility calculus would have to be redone against the enlarged vocabulary.
**Why out of scope**: The exclusion is load-bearing and intentional in this note (PC6, C-emit); the extension is a registry/vocabulary decision for a future ASN, not an error in this one.

### Topic 2: A temporal layer over the dynamics classification
PD0–PD2 classify how a term's truth behaves across steps, but PL itself has no temporal operators (stated at the dynamics introduction), and nothing here can express step-indexed conditions like "Q has held at every state since P fired" — the form protocol convergence arguments will eventually want. The note correctly defers protocol constructions wholesale; a temporal predicate layer (or a meta-language in which PD0's ⊤-stability certificates become checkable hypotheses, adjacent to Open Question 5) is the natural successor.
**Why out of scope**: The note explicitly scopes dynamics as meta-level classification and defers protocol machinery to the builder; a temporal language is new territory, not a gap in the predicate foundation this note commits.

VERDICT: REVISE
