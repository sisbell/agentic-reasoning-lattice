# Review of ASN-0126

## REVISE

### Issue 1: "No fourth shape" completeness claim ignores lower-bound G-disciplines
**ASN-0126, Three shapes by G span count**: "The claim 'no fourth shape' is accordingly modest: no recurring lattice pattern needs a G-discipline outside `{empty, singleton, unrestricted-finite}`, nor a multi-span F."

**Problem**: The catalog covers only an *upper* taxonomy of G — `|G|=0`, `|G|=1`, `|G|<∞`. It has no shape for a *lower-bounded* G, i.e. `1 ≤ |G| < ∞` (non-empty Multi). This bites against the note's own descriptive intent. The table glosses Multi as "a single source connected to finitely many target spans" and the prose names "citations, fan-outs, multi-target connections" — but a fan-out or citation with zero targets is not a fan-out. Yet `Sh-conf(citation, [c₁], ∅) = ⊤` under Multi (`|G| = 0 < ∞`), so the gate structurally admits a zero-target "citation." The note never reconciles the gap between the descriptive ≥1-target usage and the structural shape that permits 0. A "≥1 finite" discipline is precisely a G-discipline *outside* `{empty, singleton, unrestricted-finite}`, so if any enumerated pattern requires it, the completeness claim is false as stated.

**Required**: Either (a) argue explicitly that zero-target instances of Multi-typed relations are structurally acceptable (so the lower bound is genuinely never needed at the shape level, deferring any "must-cite-something" rule to the operational successor), or (b) weaken the "no fourth shape" claim to acknowledge a possible non-empty-Multi (`1 ≤ |G| < ∞`) shape as deferred. As written, the enumeration argument addresses span-count *caps* but is silent on span-count *floors*, and the note's own usage descriptions imply a floor.

## OUT_OF_SCOPE

### Topic 1: General scope characterization of range-G Binary retractions
The framework registers R as Binary, which (correctly, per Nelson/Gregory single-span semantics) admits a single G-span of non-unit width; the born-nullified example shows such a tuple nullifies all of `coverage(G_rng)`, not a single tuple, so ASN-0086's R-Scope (`{t : a ≼ t} ∩ A_rel^{Σ'} = {a}`) does not transfer under `→_sh`.

**Why out of scope**: The note explicitly defers operational retraction semantics (Open questions; "what `idem = ⊤` implies ... is the operational successor's concern"). A general range-scope property for Binary retraction belongs there, not here. The note already discharges its structural obligation by showing R-Scope rests on operational unit-depth, not on Binary registration.

META: (none — the ASN defines a fourth state component, a shape-gated transition relation, and state-invariant structural properties; it remains squarely in abstract-specification territory.)

VERDICT: REVISE
