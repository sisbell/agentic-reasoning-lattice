# Review of ASN-0126

Checked and found sound before the findings below: the abutting-span witness in Shape-conformance (the TS3/TA-strict steps and the mutual-inclusion argument both verify), the T4-validity discharge and strict ascent of `chain_d`, FrontierUnification's two-branch split including the `J_d^Σ = −1` case, frontier-landing's endpoint argument from L-ContiguousPrefix, the three-move transfer behind `Nullify_Binary`'s single-tuple-scope postcondition (the `a_emit`-blind-to-F framing is correct), the four-configuration C2/C3 sweep, and every address computation in the worked illustration (`B = {3, 4, 5}`, `k = 3`, exit at `…2.7` all check). The remaining findings are narrow.

## REVISE

### Issue 1: `→_sh*`-reachability is quantified over everywhere and defined nowhere

**ASN-0126, Registry permanence (first use; pervasive thereafter)**: "P1 (RegistryInvariance). At every `→_sh*`-reachable state, `Σ.registry = Σ_init.registry`"

**Problem**: `→_sh` is defined (The shape-gated emit), but `→_sh*` and "`→_sh*`-reachable" never are. The rooting at `Σ_init` surfaces only inside P1's proof ("the base case `Σ = Σ_init` is immediate") and obliquely in ProjectionBridge's statement — a theorem's domain should not have to be reconstructed from a proof's base case. ASN-0086 defines its analog explicitly (Definition — Reachability: reflexive-transitive closure; Definition — LayerReachable: rooted at `Σ_init`); this note replaces the step relation, so it cannot inherit that definition, yet every major result — P1–P6, FrontierUnification, frontier-landing, Corollary RangeSterilization, the `Nullify_Binary` contract's "over `→_sh*`-reachable Σ" — quantifies over the undefined domain, and B3 and the Persistence clause additionally use the binary form ("at every `→_sh*`-successor Θ of Σ'").

**Required**: One definition, placed where `→_sh` is introduced, mirroring ASN-0086's: `Σ →_sh* Σ'` is the reflexive-transitive closure of `→_sh`; a state is `→_sh*`-reachable iff `Σ_init →_sh* Σ`, with `Σ_init` the registry-adjoined initial state of Registry permanence.

### Issue 2: the ghost-root witness misstates how single-tuple scope fails

**ASN-0126, Retraction as an attributed Binary**: "so `{t : a ≼ t} ∩ A_rel^{Σ'}` contains *every* link homed there (`1.1.0.1.0.1.0.2.1`, `1.1.0.1.0.1.0.2.2`, …), not just `{a}`"

**Problem**: "not just `{a}`" asserts the intersection contains `a`. It cannot: `a = d_retr.0.s_L` has `#E(a) = 1`, and L1b bars it from `dom(Σ.L)` at every reachable state — the same passage proves exactly this two sentences earlier ("so `a`, with `#E(a) = 1`, has `a ∉ dom(Σ.L)`"), and the argument applies verbatim at Σ'. The failure is two-sided: the intersection acquires every link homed at `d_retr` (the fresh emitter `b` included, since `a ≼ b`) *and omits `a` itself*. The operation contract's only-if clause states the omission direction correctly ("the intersection omits `a`"); this narrative witness contradicts it.

**Required**: Restate the conclusion: the intersection equals the full set of links homed at `d_retr` at Σ' — `b` included — and omits the ghost `a`, so it differs from `{a}` in both directions, failing single-tuple scope on both counts.

### Issue 3: reviewer-facing announcement clauses (anti-bloat)

**ASN-0126, Worked illustration / Range sterilization / Retraction as an attributed Binary**: "The registry is exhibited, not presumed:"; "C0 is checked, not assumed."; "Precondition (i) is likewise decided, not assumed; we walk one decision…"; "The ascent settles one more pinning, which the corollary's no-routing-around claim needs derived rather than asserted:"; "Collected as an operation contract, in the discipline of ASN-0086's operation blocks"

**Problem**: These clauses address the reviewer — assurances that an obligation is discharged, or explanations of why a derivation is present — while the discharges that follow are the actual content. The "X, not Y" announcement recurs three times in one section and reads as residue of prior rigor findings: the fix was the check itself, not the advertisement of the check.

**Required**: Delete the announcement clauses; keep the discharges. Where part of a sentence carries load — "we walk one decision, which the section's later registration checks abbreviate" licenses the later abbreviations — keep only that part.

## OUT_OF_SCOPE

### Topic 1: registry evolution
The note commits to construction-time registration as the only write ("the construction of `Σ_init` is the only act that writes the registry"), and P1–P4 are built on that immutability. What an app does when it later needs a new type — successor-registry migration, rebuild, the "successor registry" idem flags OQ1/OQ3 gesture at — is a successor note's machinery.
**Why out of scope**: the immutability is the design, and relaxing it is new territory, not an error in this note.

### Topic 2: concurrent emission
`a_emit` is a function of state and `→_sh` is a sequential step relation; two agents racing for the same home's frontier slot has no semantics here. The interleaved model is inherited from ASN-0086.
**Why out of scope**: atomicity and concurrency semantics are future territory for the substrate as a whole, not a gap this framework introduces.

VERDICT: REVISE
