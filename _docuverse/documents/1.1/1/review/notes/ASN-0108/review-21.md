# Review of ASN-0108

## REVISE

### Issue 1: W5 declares tail-order preservation *necessary*, but W9d (and a clean counterexample) show it is not

**ASN-0108, W5 (OrderStability)**: "Resumption past a cursor `c` is well-defined across `Σ → Σ'` *only if* the ordering key preserves the cursor's *cut-point* and the relative `≺`-order *among the links in `After(c, ·)`* — the unseen tail the next window draws from."

**Problem**: This is a necessity claim — well-defined-resumption ⟹ (clause 1 ∧ clause 2). It is false under the no-skip reading the note's own walks use, and it directly contradicts W9d.

Take a cursor `c` with `After(c, Σ) = {r, s}`, `r ≺_Σ s`, both keys above `κ(c)`; let `N = 1`. A transition reorders the tail to `s ≺_{Σ'} r`, both still above `κ_{Σ'}(c)`. Then **clause 1 at `c` holds** (each of `r, s` keeps its classification above `c`), **clause 2 at `c` fails** (the `r, s` order inverted). Resume past `c`: window delivers `s` (the new `≺`-least), cursor `→ s`; next window delivers `r`. Both links delivered, no skip, no duplicate. A pure clause-2 violation produced no skip. For any skip, a tail link must drop *below a cursor* — which is a clause-1 event at that cursor, never a clause-2-only event.

The note itself concedes this twice. Its clause-2 walk admits the harm is really clause 1: "*Re-evaluated at the cursor `z` the reader actually held … the same event reads as a clause-1 crossing of `w` below `z`.*" And W9d states the general fact outright: "*a free permutation of the tail only reshuffles which order the surviving tail is delivered in, never whether the pass ends.*" If a free tail permutation delivers the whole surviving tail (no skip) and terminates, then clause 2 is not necessary for the no-skip/no-duplicate property the W5 walks demonstrate.

The only reading that rescues W5's "necessary" is *order-faithfulness to `≺_Σ`* — but that is incompatible with the stateless, recompute-each-call design (W3) and with completeness being "relative to each call's state" (W7, W4's caveat); there is no single `≺_Σ` to be faithful to across a mutating set. Under that reading the W5 walks (which exhibit *skips*) are the wrong demonstration.

**Required**: Reconcile W5 with W9d. Either (a) downgrade clause 2 from "necessary" to part of the *sufficient* discipline and state the genuinely necessary condition as clause 1 (cut-point) preserved at every cursor the pass visits — matching W9d's finding that clause-2 violations are harmless reshuffles; or (b) if order-faithfulness is the intended notion of "well-defined," define it precisely, replace the skip-walk with a reorder-walk that exhibits no skip, and explicitly separate order-faithfulness from no-skip/termination so W5 and W9d no longer collide.

### Issue 2: W9b's definition of "tail-inflow event" excludes its own kind (1), falsifying the "exhaustive basis" claim the termination proof rests on

**ASN-0108, W9b (CumulativeInflowSufficiency)**: "A **tail-inflow event** is any single transition that places a link into the reachable tail ahead of the then-current cursor — the exhaustive basis is this definition, not the catalogue that follows. The catalogued kinds are three: (1) the initial tail elements at the first call, (2) … (3) …"

**Problem**: Kind (1) — the initial tail at the first call — is *not* "a single transition that places a link into the reachable tail ahead of the then-current cursor." At the first call there is no prior cursor, and these links were not placed by any transition of the pass. So the catalogue's kind (1) is not an instance of the definition the note asserts is "the exhaustive basis." The multiplicity-bound proof then leans on this gap: it charges every delivery to "the inflow event that most recently placed that link into the reachable tail … as an initial element (kind 1), by creation (kind 2), or by becoming discoverable (kind 3)" — but an initially-present link has no placing *event* under the stated definition, so the charge function is undefined on exactly the base case. The bound "deliveries ≤ total tail inflow" is thus not established as written; it silently treats a non-event as an event.

**Required**: Either broaden the definition to admit "presence at the first call" as a base inflow contribution, or state the bound explicitly as `deliveries ≤ |initial tail| + |transition inflow events|` (with `|initial tail|` finite by M-fin). Drop or correct the "exhaustive basis is this definition" sentence, which the catalogue contradicts.

### Issue 3: anti-bloat — defensive/duplicated/forward-deferring prose to remove

This note carries the `review-mode.anti-bloat` classifier; the following do not advance the argument:

- **W9b**: "*the exhaustive basis is this definition, not the catalogue that follows.*" A defensive exhaustiveness claim that is, per Issue 2, false. Delete or repair.
- **M-mut (State/Matching-Set section) and W7** spell out the same orphaning mechanism in different words — both state "resident in `dom(Σ.L)` (LP13) … no longer discoverable (LP17)." W7 already says it is "the loss direction of (M-mut)," so it should cite M-mut for the mechanism and retain only its windowing-specific payload ("completeness is relative to a fixed state"), not re-derive orphaning.
- **W5 parenthetical**: "*… so it is genuinely stronger than clause 1 applied at the cursors — which is why W9d can later set clause 2 aside for termination.*" A forward-deferral to W9d embedded in the local argument; it is also entangled with the flawed necessity claim (Issue 1). Once Issue 1 is resolved, this defensive cross-pointer should go.

**Required**: Remove the three passages; fold any load-bearing content into the claim it serves.

## OUT_OF_SCOPE

### Topic 1: Multi-home-document ordering keys
The note correctly confines W6's append-at-tail to a single home document and defers the cross-document case to the Open Questions ("no single allocation-monotone key orders the whole result globally"). This is genuinely new territory, not a defect in this ASN; the deferral is appropriate. No action needed.

META: (none — the note defines a state-derived matching set, a windowed operation over it, and abstract guarantees on order/stability/termination/progress that any implementation's key must satisfy; it remains a system-guarantee specification, not implementation mechanics.)

VERDICT: REVISE
