# Review of ASN-0126

I checked the technical core carefully — the wp derivation, the projection bridge, RegisteredAdmissible, and the worked illustration — before turning to the anti-bloat pass.

The mathematics is sound. The guarded-command wp `wp(g_sh → S, R) ≡ g_sh ∧ wp(S, R)` is the correct IF-construct semantics (a failed guard aborts, `wp(abort,R)=false`); the absorption of L3 and `K ∈ T_admissible` into `g_sh` via RegisteredAdmissible checks out (`coverage(K)=coverage(K_j)≠∅ ⟹ K≠∅`); the projection bridge correctly transfers ASN-0086's C/M/L lemmas through `π`; and the born-nullified worked example is arithmetically correct (`a_R = …2.3 ∉ coverage(G_rng)=[…2.4,…2.7)`, then `a = inc(a_R,0) = …2.4 ∈ coverage(G_rng)`, so C3 fails at the next emit). Boundary cases — empty `F`, `|G|=0` under Multi, the empty registry, ghost targets — are all handled. The C2/C3 strict-strengthening witnesses are valid. No correctness defect found.

The findings below are the anti-bloat patterns the classifier flags.

## REVISE

### Issue 1: "Properties established" section is a use-site-inventory recap
**ASN-0126, Properties established**: "For a consuming app, the framework establishes six guarantees, each stated and proved in the body above — what each one buys:"
**Problem**: The section restates P1–P6 (each already fully stated and proved) and appends app-facing motivational gloss ("the type declarations an app fixes at `Σ_init` never drift out from under it", "an app may read the link store and assume conformance without re-validating"). The note's own framing — "each stated and proved in the body above" — concedes the redundancy. This is essay content / a use-site inventory in a structural slot; it advances no reasoning. The gloss also re-states the no-residence/ghost permission already given verbatim in *Shape-conformance*.
**Required**: Cut the section, or reduce it to a bare list of property labels with no per-bullet "what it buys" narrative.

### Issue 2: Defensive parenthetical in the projection bridge
**ASN-0126, The shape-gated emit**: "(PrefixSpanCoverage, used elsewhere in this note, needs no such bridge: it is an unconditional tumbler fact of ASN-0043 — "for any tumbler `x` with `#x ≥ 1`, …" — holding at every tumbler regardless of reachability or component count.)"
**Problem**: This pre-empts an objection the precise reader does not raise — that an unconditional lemma might need the reachability bridge. It is a defensive clarification of the bridge's scope, not a step in its use; the reader must skip it to stay on the argument.
**Required**: Delete the parenthetical.

### Issue 3: Meta-labeling sentence appended to the worked illustration
**ASN-0126, Worked illustration (State-independence)**: "This is the concrete content of both P4 and the no-residence-check decision."
**Problem**: The preceding three sentences — `Σ` with `c₂,c₃` ghost, `Σ'` with them stored, identical `Sh-conf` verdict because only span counts and registered shape are read — already *are* the demonstration. The closing sentence tells the reader what the example showed rather than letting it stand, and restates the no-residence point a third time.
**Required**: Delete the sentence; the worked steps carry it.

## OUT_OF_SCOPE

### Topic 1: Substrate-enforced unit-depth retraction discipline
**Why out of scope**: *Single-source* correctly observes that Binary registration is strictly weaker than ASN-0086's UnitDepthRetractionDiscipline — a single non-unit G-span clears the Binary gate, so R-Scope's single-tuple-scope holds only if the app routes through the unit-depth wrapper. The note deliberately makes this an app responsibility. Whether the substrate should offer a *registrable* unit-depth-disciplined retraction shape (recovering single-tuple scope as a gate guarantee rather than a convention) is a coherent future direction, not a defect here. It is not among the note's six open questions, which scope only arity/idempotency/behaviors.

VERDICT: REVISE
