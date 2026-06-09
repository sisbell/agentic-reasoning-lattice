# Review of ASN-0126

## REVISE

### Issue 1: Inconsistent count of K.λ_sh's added preconditions
**ASN-0126, "The shape-gated emit" vs "Registry permanence"/wp projection**: "The shape-gated emit" defines `K.λ_sh` as "`K.λ` with **three** added preconditions: (0) ... (i) ... and (ii)", and P4 relies on (0) being load-bearing ("a non-triple value fails (0) and is not a `→_sh`-step at all"). But the projection paragraph states "a `K.λ_sh`-step as a `K.λ` step — its **two** added preconditions only restrict when it fires", and the wp paragraph says "`K.λ_sh` differs from `K.λ` only by conjoining **two** guards — (i) K registered, (ii) `Sh-conf`".
**Problem**: The arity guard (0) `|value| = 3` is genuinely an added precondition — it narrows `K.λ`'s inherited `N ≥ 3` (L3) down to `= 3`, and it also restricts when the step fires (it rejects higher-arity emits). The projection claim that "two added preconditions only restrict when it fires" undercounts: three do. The wp's choice to *omit* (0) from `g_sh` is justified separately (the postcondition forces arity-3), but that is a wp-specific move, not a statement about how many preconditions `K.λ_sh` carries.
**Required**: State consistently that `K.λ_sh` has three added preconditions (0),(i),(ii); in the projection paragraph say all three restrict firing; keep the wp's omission of (0) explicitly scoped to the wp derivation only.

### Issue 2: Scope of the "at every emit" guarantee vs the direct-link-store escape hatch
**ASN-0126, Single-source (closing) and intro**: Intro promises "a static shape-conformance check the substrate can apply at **every emit**." P4 proves only that "No **`→_sh`-step** extends `dom(Σ.L)` with a tuple ... whose K is unregistered, nor with one for which `Sh-conf` fails." Single-source then says "an app needing multi-source relations can interact with the link store directly. The substrate does not provide machinery for that case."
**Problem**: P4's guarantee is local to `→_sh`-steps; it does not establish that `dom(Σ.L)` contains only conforming tuples. If a single substrate instance also exposes ASN-0086's ungated `K.λ` (the "interact with the link store directly" path), then non-conforming tuples can enter `dom(Σ.L)` off-gate, and the intro's "at every emit" overclaims. Conversely, if `→_sh` is the *sole* transition relation of a framework-governed substrate (as "All reachability in this note is with respect to `→_sh`" suggests), then "interact with the link store directly" cannot mean a bypass *within this substrate* and should be reframed. The note never pins down which.
**Required**: One explicit sentence settling the relationship: either declare `→_sh` the complete transition relation of a framework substrate (so multi-source means dropping to a *different* layer/substrate, not bypassing the gate), or weaken the central guarantee to "every framework-mediated (`→_sh`) emit" and acknowledge `dom(Σ.L)` may carry off-gate tuples.

### Issue 3: P4 "falls out of the wp derivation" conflates enablement with landing
**ASN-0126, Properties — P4**: "P4 ... falls out of the weakest-precondition derivation ...: the wp of the gated emit against `(a,F,G) ∈ A_K^{Σ'}` carries `K registered ∧ Sh-conf` as its leading conjuncts, so no firing emit escapes the gate."
**Problem**: The wp targets *active-subset* membership, a strictly stronger postcondition that a conforming tuple can fail (the "born nullified" witness). A non-conforming tuple failing the wp's `Sh-conf` conjunct only shows it fails to land active — not that it never enters `dom(Σ.L)`. P4's actual claim (non-conforming tuples never enter the audit slice at all) is established by `K.λ_sh`'s **enablement** preconditions, not by the wp. The note itself draws this enablement-vs-landing distinction carefully in "The shape-gated emit," so the P4 property statement is in tension with its own analysis.
**Required**: Derive P4 from `K.λ_sh`'s enablement preconditions directly (the direct argument is already present in the same entry); drop or restate the "falls out of the wp" remark so it does not present the active-subset wp as the source of an enablement guarantee.

## OUT_OF_SCOPE

### Topic 1: Idem semantics, standard registrations, predicate composition
**Why out of scope**: The note commits only to the idem flag's structural presence and state-independence (P3); the operational meaning, standard pre-registrations (including whether R ships registered), and predicate composition are explicitly enumerated as successor-note work (Open questions #1–#6). These are correctly deferred, not gaps in this ASN.

### Topic 2: Per-type lower bound on `|G|` (e.g. "citation must have ≥1 target")
**Why out of scope**: The catalog deliberately bounds `|G|` only from above and houses any `1 ≤ |G|` floor as a type-semantic rule one layer up. The note grounds this in both Nelson (one-sided links sanctioned) and Gregory (empty to-set stored silently). This is a defensible scoping decision, not an omission.

VERDICT: REVISE
