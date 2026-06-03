# Review of ASN-0075

## REVISE

### Issue 1: wp formulas for Q1 and Q0 include a boundary conjunct that is not part of the weakest precondition

**ASN-0075, "The SHOWDELETIONS Operation" (wp analysis)**: For `q` the ASN explicitly strips the boundary conjunct —

> "the genuine weakest precondition for `q` carries no boundary conjunct: `wp(SHOWDELETIONS(d_A, d_B), q) = d_A ∈ E_doc ∧ d_B ∈ E_doc`"

— and argues at length that "That conjunct is not needed to compute `q`." But the very next derivations reintroduce it:

> "`wp(SHOWDELETIONS(d_A, d_B), Q1) = d_A ∈ E_doc ∧ d_B ∈ E_doc ∧ Σ is a composite-boundary state ∧ (E a ∈ dom(C) : ...)`"

and identically for `Q0`.

**Problem**: This is internally inconsistent. `Q1` (one half non-empty) and `Q0` (both halves empty) are state-level predicates over `M`, `R`, `dom(C)` — computable and well-defined at *any* reachable state, exactly as `q` is. Nothing about establishing `Q1` or `Q0` after execution requires `Σ` to be a composite boundary; the boundary conjunct is therefore not part of the weakest precondition for either, by precisely the reasoning the ASN used to strip it from `q`. The "general rule" the section invokes — "`wp(SHOWDELETIONS, P) = (precondition) ∧ P(Σ)`" — conflates the operation's *stated* precondition (which carries the boundary conjunct for semantic reasons) with the *weakest* precondition. Under either reading the treatment is incoherent: if `(precondition)` means the stated precondition, then `q`'s wp should also carry the boundary conjunct (it does not); if it means the well-definedness condition, then `Q1`/`Q0` should not carry it (they do).

**Required**: Make the wp treatment uniform. Either (a) strip the boundary conjunct from the `Q1` and `Q0` wp formulas so all three are genuine weakest preconditions `d_A ∈ E_doc ∧ d_B ∈ E_doc ∧ ...`, or (b) state clearly that these formulas are preconditions-relative-to-the-operation-contract (stated precondition conjoined with the postcondition) and apply that convention to `q` too. The "general rule" sentence must be corrected so it does not equate the stated precondition with wp.

### Issue 2: Roadmap scaffolding that does not advance the argument

**ASN-0075, "Why the Provenance Relation Is Load-Bearing"**: "The argument proceeds in two steps: a discrimination lemma (D-DISCR) exhibiting two states indistinguishable on `(C, L, E, M)` yet differently classified, and the necessity corollary (D-NEED) it yields."

**ASN-0075, "A Worked Example"**: "Having now stated the claims D-EXH, D-IDENT, D-ORIG, and D-SYM, we check each concretely against the resulting state."

**Problem**: Both sentences are pure structural announcements — they restate the section/lemma ordering that the labels and headings already convey, and a precise reader skips them to reach the actual reasoning. This is the meta-prose accretion the anti-bloat classifier targets: essay scaffolding sitting in slots where the claim itself should begin. (The worked example *itself* is valuable and required; only the framing sentence is noise.)

**Required**: Delete the two scaffolding sentences. The lemmas and the worked-example tables carry the structure without narration.

## OUT_OF_SCOPE

### Topic 1: Per-occurrence (Vstream-position-level) deletion detection
The granularity note correctly scopes out distinguishing which of several V-positions holding the same I-address was removed. This is genuinely a Vstream/arrangement concern for a future ASN, not a gap here.

**Why out of scope**: Detecting per-occurrence removal requires position-level (V-position) predicates, which belong to arrangement-operation ASNs, not to an I-address-set-granularity query.

### Topic 2: Three-document and n-document generalization, restoration operations
Raised correctly in Open Questions (third document witness, restoration consuming SHOWDELETIONS output, n-ary witness structure).

**Why out of scope**: These define new operations and new witness structures beyond the binary observational query specified here.

VERDICT: REVISE
