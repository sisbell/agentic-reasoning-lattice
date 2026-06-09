# Review of ASN-0126

## REVISE

### Issue 1: "Sh-conf consults no state" is stated four times

**ASN-0126, Shape-conformance / P5 / Worked illustration**: The claim that `Sh-conf` inspects only span counts and no state-indexed set appears at least four times:
- Shape-conformance: "`Sh-conf` does not test membership in `dom(Σ.C)`, `dom(Σ.L)`, or any state-indexed address set such as ASN-0086's `A_doc^Σ`, `A_rel^Σ`, `A^Σ`."
- Next paragraph: "No component of Σ is consulted — not `Σ.C`, not `Σ.L`, not `Σ.M` — and no other element of `dom(Σ.L)` is inspected."
- P5: "where defined, `Sh-conf` reads only the span counts... No state-indexed set is consulted."
- Worked illustration: "the predicate inspects only the span counts... never `dom(Σ.C)`, never `A_doc^Σ`."

**Problem**: The same structural fact is re-asserted in four locations with no added content. The reader who has parsed it once must re-parse three restatements to confirm nothing new is being said.

**Required**: State the no-residence-check fact once in Shape-conformance. Let P5 and the worked illustration *cite* it (P5 already could read "the predicate consults no state, per Shape-conformance"), not restate it.

### Issue 2: The C0+P1 two-premise argument is spelled out three times

**ASN-0126, Registration entries / C0 / P2**: The argument "coverage-class-key uniqueness (C0) makes `shape(·)` single-valued; registry invariance (P1) makes it state-independent; neither alone suffices" is given in full in Registration entries ("it is coverage-class-key uniqueness that makes `shape(K)`... single-valued"), again in the C0 paragraph ("under C0, `shape(·)` and `idem(·)` are single-valued functions... together with P1's invariance"), and a third time in P2 with the explicit "Neither premise alone suffices" breakdown.

**Problem**: Three full statements of one argument. (P3's "by the same two-premise argument as P2" is the correct compression — do that everywhere.)

**Required**: Give the two-premise argument once, in P2. Reduce Registration entries and C0 to stating the well-formedness condition itself, without re-deriving its single-valuedness consequence.

### Issue 3: "Registration is construction-time, not runtime" repeated four times

**ASN-0126, Registry permanence / Registration entries / C0 / Open question 4**: 
- Registry permanence: "Every registration is therefore an entry present in `Σ_init.registry` — a construction-time act — and no entry is added at runtime."
- Registration entries: "the registry is fixed at the moment Σ_init is defined."
- C0: "It is a precondition on substrate construction."
- Open question 4: "registration being a construction-time act either way."

**Problem**: A consequence of P1 restated in four sections.

**Required**: Keep it where P1 is derived (Registry permanence); drop the restatements.

### Issue 4: Forward-pointers and "not a hole / not a revision" meta-prose in Single-source

**ASN-0126, Single-source**: 
- "and the closing paragraph of this section records that escape hatch" — a forward pointer to the same section.
- "An app needing multi-source relations therefore does not *bypass* the gate here; it drops to a *different* substrate... which is a separate layer, not a hole in this one. The framework does not provide machinery for the multi-source case. Adding it later means a supplemental note, not a revision here."

**Problem**: The forward pointer adds nothing the reader needs before reaching the paragraph. "not a hole in this one" / "not a revision here" are defensive justifications of scope, not reasoning. The substantive content — "multi-source drops to ASN-0086's ungated `→`" — survives without them.

**Required**: Delete the forward pointer and the defensive scope clauses. Keep the one sentence stating where multi-source lives.

### Issue 5: Near-duplicate sentences on "one F span may cover a range"

**ASN-0126, Single-source (para 1)**: "Note that the one F span may itself cover a contiguous range or a whole subtree, not merely one address" followed two clauses later by "The substrate narrows away only the multi-span, discontiguous from-set... it does not narrow what one span may reach."

**Problem**: Two sentences asserting the same thing (a single span may reach a range/subtree).

**Required**: Collapse to one.

### Issue 6: Defensive "not a theorem" hedge

**ASN-0126, Three shapes**: "Exhaustiveness of the three shapes is a design judgment over observed lattice usage, not a theorem."

**Problem**: This hedge defends against a challenge the note doesn't otherwise invite — it advances no part of the shape definition. The shapes are what they are by registration; their adequacy is self-evidently a design choice.

**Required**: Remove, or fold into a single clause if exhaustiveness genuinely needs disclaiming.

### Issue 7: `[r]` in the re-expressed Nullify is undefined

**ASN-0126, Single-source**: "The framework re-expresses retraction in the attributed form `Emit_R(Σ, d_retr, [r], {(a, δ(1, #a))})`: a single attributing source span (`|F| = 1`)..."

**Problem**: `r` is introduced here and never defined — what address does the attribution span denote (the home document? the proposer?). The `[x]` unit-depth-singleton convention isn't even introduced until the Worked illustration. For the shape claim only `|F| = 1` matters, but presenting this as a concrete *re-expression of an ASN-0086 operation* with an undefined component leaves the operation under-specified at exactly the point the note claims to make it concrete. (The worked example silently picks `[c₁]` as the attribution, confirming `r` is a free parameter.)

**Required**: Either define what `r` denotes, or state explicitly that the attribution content is an operational free parameter (deferred to the successor note) and that only `|F| = 1` is the shape commitment here.

## OUT_OF_SCOPE

### Topic 1: Idem semantics and what counts as "the same" tuple
The registry carries an `idem` flag, but its operational meaning at emit (Open question 1) is correctly deferred. P3 establishing only its state-independence is the right level of commitment for this note.

### Topic 2: R-Scope weakening under non-unit Binary retraction
The note correctly observes that `→_sh` gates R by Binary, not unit-depth, so a general `→_sh`-reachable state can carry a non-unit-range `L_R` tuple, and the worked example exploits this. ASN-0086's R-Scope single-tuple-scope property therefore does not hold at general `→_sh` states; the note relocates unit-depth to operational construction. This is a deliberate, honestly-flagged design consequence, not an error — the operational discipline that restores R-Scope belongs to the successor note.

VERDICT: REVISE
