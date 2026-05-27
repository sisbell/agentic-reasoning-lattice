# Review of ASN-0099

## REVISE

### Issue 1: 𝒮 terminology conflates allocator state with full system state
**ASN-0099, "Completeness" section**: "We let `result : 𝒫(T) × 𝒮 → 𝒫(T)` denote a conforming implementation's actual output function, where 𝒮 is the system state space introduced by ASN-0034's AllocatedSet and exercised throughout the substrate."

**Problem**: ASN-0034's AllocatedSet defines 𝒮 specifically as "a configuration of the allocator tree" — the allocation system's state space. The current ASN uses 𝒮 for the full Xanadu system state with components (C, L, M, E, R). These are different abstractions. The citation "introduced by ASN-0034's AllocatedSet" is misleading.

**Required**: Define 𝒮 locally as the full Xanadu system state space, or write Σ = (C, L, M, E, R, ...) without citing ASN-0034's narrower 𝒮 as the source. The same imprecision is repeated for `result_filtered` and `result_scoped` signatures.

### Issue 2: "Verifying F17" attributes Σ.L preservation to wrong claim
**ASN-0099, worked example "Verifying F17 across Query 4's K.μ⁻"**: "by F9-cor (with K.μ⁻ inheriting Σ.L = Σ'.L from A1), Σ'.L = Σ.L."

**Problem**: F9-cor's conclusion is `findlinks(I, Σ) = findlinks(I, Σ')` (findlinks invariance), not `Σ'.L = Σ.L`. The preservation `Σ'.L = Σ.L` is supplied directly by A1; F9-cor uses this as a premise, not as a conclusion. Citing F9-cor for the link-store equality is backwards.

**Required**: Restate as "by A1, Σ'.L = Σ.L; F17 then predicts..." or similar. The downstream chain via F17 is correct; only the citation handle is off.

### Issue 3: F4's "weakening" branch frames F1 simultaneously as definition and consequence
**ASN-0099, F4 derivation**: "(Weakening direction.) The dual direction is discharged by F3 (Soundness): an implementation conforming to a weakening P_w of F1 ... would return links satisfying P_w but not F1, violating F3 which requires a ∈ result(I, Σ) ⟹ matches(a, I, Σ) with matches read as F1."

**Problem**: The argument fixes F1 as the abstract spec and shows that adopting any weaker `matches_w` produces implementations whose returns violate F3-as-stated-against-F1. But F3 itself is parameterised by the chosen `matches`. The argument is sound under the meta-assumption "F1 is the reader's intended match condition", but the proof doesn't surface this meta-assumption. Reader can be left wondering whether F4 establishes uniqueness or merely consistency with F1's own framing.

**Required**: One-sentence clarification that F4's uniqueness is *relative to the reader's promise* — F1 is the unique match predicate compatible with the reader's promise of "every link touching the queried region appears" — and that "violates F3" is read with F1 as the reference predicate. The argument is already correct; the framing needs to acknowledge the meta-level fixity of F1.

### Issue 4: F2-sco's "dom(Σ.L) ∩ S" implicitly extends matches predicate domain to S
**ASN-0099, F2-sco**: "For every a ∈ dom(Σ.L) ∩ S: matches(a, I, Σ) ⟹ a ∈ result_scoped(I, S, Σ)."

**Problem**: `matches(a, I, Σ)` is defined only for `a ∈ dom(Σ.L)` (it consults `|Σ.L(a)|`). Quantifying over `a ∈ dom(Σ.L) ∩ S` keeps `matches` in its domain — but the ASN doesn't state explicitly what happens for `a ∈ S ∖ dom(Σ.L)`. Soundness F3-sco resolves this (such a's cannot be in the result because the result is bounded by `dom(Σ.L) ∩ S`), but the well-definedness of `matches` at the predicate level deserves a one-line note.

**Required**: A brief note that `matches(a, I, Σ)` is undefined for `a ∉ dom(Σ.L)`, and that scope-filter intersection `dom(Σ.L) ∩ S` keeps every quantification within the predicate's domain.

## OUT_OF_SCOPE

### Topic 1: Procedural specification of FINDLINKS implementation
**Why out of scope**: The ASN explicitly disclaims procedural specification ("We have not specified the procedure by which the operation is computed"). Index maintenance, query optimisation, and storage layout are downstream implementation concerns.

### Topic 2: Cross-server replication and partition tolerance
**Why out of scope**: The ASN's Open Questions section lists this explicitly ("multiple physical instances of the link store, where partition tolerance and consistency models become relevant"). Distributed semantics belong to a downstream BEBE-layer ASN.

### Topic 3: FOLLOWLINK / I→V resolution (inverse direction)
**Why out of scope**: The ASN explicitly defers this: "We have not specified the inverse direction... That is the I→V resolution belonging to FOLLOWLINK/RETRIEVEENDSETS, and it has its own specification with its own subtleties."

### Topic 4: Behaviour for query I-sets including unallocated addresses
**Why out of scope**: The ASN explicitly flags this: "We have not specified what FINDLINKS returns when the query I-set includes addresses outside `dom(Σ.C) ∪ dom(Σ.L)`. The match predicate still works mechanically... but the operational meaning... is left unsettled." A future ASN can pin down ghost-address semantics.

### Topic 5: Access-control composition with discovery
**Why out of scope**: The ASN notes access control as "a separate concern that composes with discovery rather than altering its semantics" and explicitly declines to formalize it. Access-control mechanics belong to a security-layer ASN.

### Topic 6: Combined findlinks_filtered_scoped operation
**Why out of scope**: The ASN explicitly notes "the combined operation adds no new structural content over the two separate operations and so is left implicit here". Downstream specs needing the composed form can restate the trivial intersection.

VERDICT: REVISE
