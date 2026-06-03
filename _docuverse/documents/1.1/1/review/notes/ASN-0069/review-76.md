# Review of ASN-0069

## REVISE

### Issue 1: V8's transitive d_src ↔ d_new correspondence is misstated for subsequent forks

**ASN-0069, §"Structural Correspondence" (V8 prose)**: "The transitive `d_src ↔ d_new` correspondence for the subsequent-fork case (where `d_op = d_prev ≠ d_src`) follows by composing V8 at consecutive forks: V8 at the current fork (`d_prev ↔ d_new`) with V8 at `d_prev`'s own earlier fork (`d_src ↔ d_prev`), under the premise that `d_src` and `d_prev` are unedited across the intervening gap."

**Problem**: The cited "V8 at `d_prev`'s own earlier fork (`d_src ↔ d_prev`)" is only an instance of V8 when `d_prev` was the *first* fork of `d_src` (so `d_prev`'s own content operand `d_op = d_src`). When `d_new` is the third-or-later version, `d_prev` was itself a subsequent fork whose content operand was the version *before* `d_prev`, not `d_src` — so V8 applied at `d_prev`'s fork yields `(version-before-d_prev) ↔ d_prev`, never `d_src ↔ d_prev`. The two-step composition as written does not close; the general case requires induction along the entire version sequence of `A_v(d_src)` with every consecutive pair unedited. V11 supplies such an induction only for *first-fork chains* (each step `inc(·,1)`), which is a structurally different configuration from the sibling/subsequent-emission sequence at issue here. The transitive claim is therefore an unproven "follows by composing" for every version past the second.

**Required**: Either (a) provide the induction over `A_v(d_src)`'s emission sequence establishing `d_src ↔ d^(k)` for the subsequent-fork case (mirroring V11 but for the `k=0` sibling structure), or (b) restrict the V8 prose claim to the second-version case (`d_prev` = first fork) and mark the deeper case as not derived here.

### Issue 2: V2 re-derives a foundation result at length, then justifies the duplication in prose

**ASN-0069, §"Identity by Sub-Allocation" (V2) and §"Dependency Audit"**: "J4 (ASN-0047) supplies `d_src ≼ d_new` directly as a derived consequence in both sub-cases. We re-derive it by induction..." followed by a multi-paragraph nested induction; and "The one local re-derivation — `d_src ≼ d_new` ... — is retained to establish V2 as a named, self-contained structural claim ... rather than leaving it as a citation of J4's derived consequence."

**Problem**: J4 supplies `d_src ≼ d_new` directly. Naming the property locally as V2 is fine, but reproducing the full nested-induction proof of a result the foundation already discharges is duplication, and the Dependency Audit paragraph defending the duplication is meta-prose about document structure rather than content that advances the argument. Under the anti-bloat mandate this is exactly the accreted "justify why this is re-derived/placed here" pattern.

**Required**: State V2 as the named restatement of J4's `d_src ≼ d_new` consequence with a one-line citation; drop the nested re-derivation and the Dependency-Audit defense of retaining it.

### Issue 3: V11 carries defensive parentheticals that explain what is *not* needed rather than advancing the proof

**ASN-0069, §"Composability" (V11 inductive step and base case)**: e.g. "(The premise's universal '`V_{s_C}(d^{i-1}_new)` is the same set' entails the membership-transfer step ... directly; no set-equality chain back to `V_{s_C}(d_src)` through earlier chain members is needed, so the derivation rests on the formal premise as written without strengthening it.)" and "(V4b strengthens this to set equality ..., though only the inclusion is consumed by the inductive step.)"

**Problem**: These parentheticals argue why a stronger fact is unnecessary / what is or isn't consumed downstream — reviser-drift bookkeeping, not reasoning the reader needs to follow the step. They are residue of prior review cycles defending the proof against findings rather than proving anything.

**Required**: Delete the "no X is needed / only Y is consumed" asides; keep only the steps that establish the conclusion.

### Issue 4: Dependency Audit contains a downstream-consumption inventory

**ASN-0069, §"Dependency Audit"**: "Its nested length-induction by-product (`#d_new = #d_src + 1` for the subsequent-fork `k = 0` case) is local to that derivation and is *not* consumed elsewhere; in particular V11a re-derives its own length identity ... independently via TA5(d)."

**Problem**: This sentence tracks where a by-product is and isn't used downstream — a use-site inventory that conveys no specification content. It compounds the same accretion as Issues 2–3.

**Required**: Remove the consumption-tracking sentence; the Dependency Audit should state only which declared deps are used and that ASN-0040 is unused (the substantive content).

## OUT_OF_SCOPE

### Topic 1: Transitive correspondence across mixed first/subsequent fork trees
**Why out of scope**: A general correspondence theorem spanning arbitrary fork-tree paths (mixing `k=1` chain steps and `k=0` sibling steps) is new territory beyond V11's first-fork-chain result. Fixing Issue 1 only requires closing the specific subsequent-fork claim V8 already asserts; a full tree-wide theorem belongs to a later ASN.

VERDICT: REVISE
