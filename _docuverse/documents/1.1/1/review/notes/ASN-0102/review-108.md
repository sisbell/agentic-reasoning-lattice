# Review of ASN-0102

## REVISE

### Issue 1: X17's S8-fin justification states a false set identity

**ASN-0102, X17 (InvariantPreservation), S8-fin bullet**: "`dom(Σ'.M(d)) = dom(Σ.M(d)) ∪ {copied positions}` adds exactly `W = (+ j : 1 ≤ j ≤ k : n_j) < ∞` positions to the finite pre-state domain (S8-fin at `Σ`), hence remains finite."

**Problem**: The equation is wrong, and so is the cardinality claim derived from it. "Copied positions" is precisely `B_copy`'s region `[v, v+W)` (last components `[p, p+W)`). But the *displaced* positions `u + W` (for `u ∈ V_{s_C}(d), u ≥ v`) become new domain entries at last components `[p+W, n_S+W]` — these lie in `dom(Σ'.M(d))` but in neither `dom(Σ.M(d))` nor `{copied positions}`.

Concretely, in the ASN's own main worked example (`n_S = 5`, `p = 3`, `W = 4`): the displaced images sit at `[1,7],[1,8],[1,9]`, so post-state `V_{s_C}(d) = [1,1..9]`, yet `dom(Σ.M(d)) ∪ {copied}` = `[1,1..5] ∪ [1,3..6]` = `[1,1..6]`. The two sets differ, and the stated union adds only **1** position (`[1,6]`), not `W = 4`. The actual domain delta is `{[s_C,1,…,1,c] : n_S < c ≤ n_S + W}`, which X16's own tiling establishes.

**Required**: Replace the equation with the correct delta — `dom(Σ'.M(d)) ∖ dom(Σ.M(d)) = {[s_C,1,…,1,c] : n_S+1 ≤ c ≤ n_S+W}`, cardinality `W` — citing X16's tiling rather than `{copied positions}`. The finiteness conclusion survives; the derivation does not.

### Issue 2: Rhetorical emphasis injected into proof slots

**ASN-0102, "content immutability forces shared reference" section**: "Now the decisive step." … "The operation has no freedom here: having renounced content creation, the only addresses it can legally place are ones that already exist". Similarly the opening "this single fact dictates what the operation may and may not do" and X8's "An alternative implementation is free to store either."

**Problem**: These interjections sit inside the wp-computation and claim-derivation slots without advancing the reasoning — the wp argument is carried entirely by the partition into unmoved/displaced/copied classes and X1, not by the emphasis. Under the anti-bloat classifier these are essay content in structural slots; a reader must skip past them to reach the load-bearing membership obligation.

**Required**: Drop the rhetorical framing and let the wp partition stand on its own.

## OUT_OF_SCOPE

### Topic 1: Re-displacement of copied content by later operations
**Why out of scope**: The first Open Question (origin/discoverability under subsequent displacement) concerns INSERT/DELETE/REARRANGE interaction, which is future-ASN territory, not a gap in COPY's own contract.

VERDICT: REVISE
