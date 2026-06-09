# Review of ASN-0126

## REVISE

### Issue 1: Property numbering skips P3
**ASN-0126, Properties established**: the section lists "P1, P2, **P4**, P5, P6, P7" — and every in-text citation does the same (`(P5)`, `(P7)`, "Derived in The shape-gated emit (P4)...").
**Problem**: There is no P3 anywhere — not defined, not referenced. A precise reader hits "P4" and must hunt for a P3 that does not exist, suspecting a dropped property or a dangling reference. Either a property was removed and the gap left uncauterized, or the numbering is simply wrong.
**Required**: Renumber to a contiguous P1–P6, or, if P3 is intentionally reserved/retired, state so explicitly at first use so the gap reads as deliberate rather than as an omission.

### Issue 2: Domain-discharge ordering states the same thing twice
**ASN-0126, The shape-gated emit**: "(0) and (i) jointly discharge the domain condition for (ii)... So arity-3 and registration must both hold before (ii) carries a truth value; a value of arity ≠ 3 fails (0) and is simply not a `→_sh`-step, and an unregistered K fails (i) before the conformance test is reached."
**Problem**: The second sentence ("arity-3 and registration must both hold before (ii)…") restates the first ("(0) and (i) jointly discharge the domain condition for (ii)") in different words. The intervening clause about `Sh-conf` reading two content slots is the only new content; it is surrounded by the duplicated framing. This is the anti-bloat "two sentences say the same thing" pattern around a precondition ordering.
**Required**: State the ordering once: (0) and (i) gate (ii)'s definedness; a value failing arity-3 or registration is simply not a `→_sh`-step. Drop the restatement.

### Issue 3: Span-count-vs-coverage distinction restated across four sections
**ASN-0126, Single-source / Three shapes / Shape-conformance**: the caveat "`|e|` is span count, **not** the number of tumblers in `coverage(e)`" appears in Single-source's `|e|` introduction, is repeated in Three shapes ("We measure G by its span count `|G|`"), and is then given a full standalone treatment in Shape-conformance ("The span-count and coverage measures diverge sharply… A single unit-depth span… is one span… yet its coverage is… generally infinite").
**Problem**: The Single-source parenthetical and the Shape-conformance paragraph carry the same load. The reader is told the same intrinsic-not-coverage fact three times before reaching the worked illustration, which demonstrates it a fourth. This is accreted redundancy, not a layered argument — each statement could stand alone.
**Required**: Keep the full treatment where it does work (Shape-conformance), and at the earlier sites use a bare cross-pointer rather than re-deriving the divergence.

### Issue 4: Open question 1 justifies an omission rather than posing the question
**ASN-0126, Open questions, item 1**: "A successor note is expected to add a reserved `idem` registry field…; **this note does not introduce it because no predicate, gate, or operation here would read it.**"
**Problem**: The bolded clause defends why `idem` is *absent* rather than advancing the open question itself. This is the flagged "prose explains why something is needed/not-here rather than what it says" pattern — meta-justification for a non-decision, in a section whose job is to state what is deferred.
**Required**: Drop the justification; the open question stands on its own. If a one-line rationale for deferral is wanted, "deferred — no operation here reads it" suffices without the defensive framing.

## OUT_OF_SCOPE

### Topic 1: Loss of single-tuple retraction scope under Binary gating
The note observes (Single-source) that Binary registration is strictly weaker than ASN-0086's UnitDepthRetractionDiscipline, so a non-unit contiguous-range retraction is a legal `→_sh`-step and R-Scope's `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}` holds only when the app routes through the unit-depth wrapper.
**Why out of scope**: This is a deliberate, acknowledged design choice (the worked "Born nullified" illustration exploits it intentionally), not a defect in this note. Whether the framework should *enforce* unit-depth at the gate, or continue to delegate discontiguous retraction to the front end, is a question for the operational-semantics successor note, not a revision here.

VERDICT: REVISE
