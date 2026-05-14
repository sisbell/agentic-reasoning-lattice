# Review of ASN-0042

## REVISE

### Issue 1: FirstDelegatorIsπ unnecessarily invokes AccountLevelPermanence with insufficient preconditions

**ASN-0042, Sub-lemma (FirstDelegatorIsπ), base case proof**: "Apply the single-transition AccountLevelPermanence (whose reachability and `π ∈ Π_{Σ̃}` premises hold by hypothesis and iterated O12) to any `a ∈ dom(π'') ⊆ dom(π)` whose effective owner changed in this transition: it yields `pfx(π) ≼ pfx(π_d)`."

**Problem**: AccountLevelPermanence (single-step) requires `a ∈ dom(π) ∩ Σ.B` with `ω_{Σ'}(a) ≠ ω_Σ(a)`. The proof selects `a ∈ dom(π'') ⊆ dom(π) ∩ Σ̃.B` with changed effective owner. But when the newly delegated principal `π''` has an empty allocated-address domain — `dom(π'') ∩ Σ̃.B = ∅` — no such `a` exists. This case arises whenever `π` delegates a prefix into a sub-region where no addresses have been allocated yet, which is a legitimate scenario in the model: delegation creates a namespace for future allocation. The worked example exhibits exactly this — when π_N delegates `[1, 0, 2]` to π_A, the sub-domain may be allocation-empty at the moment of delegation. Without an allocated address in `dom(π'')`, no `ω` changes in the introducing transition, and AccountLevelPermanence's precondition is unsatisfiable. The same gap appears in the inductive step ("from condition (ii) and the AccountLevelPermanence step as in the base case").

**Required**: Derive `pfx(π) ≼ pfx(π_d)` directly from delegation condition (ii) without invoking AccountLevelPermanence:
- By (ii), `π_d` is the most-specific covering principal of `pfx(π'')` in `Π_{Σ̃}`, so `pfx(π_d) ≼ pfx(π'')`.
- By the sub-lemma's hypothesis `pfx(π) ≺ pfx(π'')`, `π ∈ Π_{Σ̃}` covers `pfx(π'')`.
- By (ii)'s most-specific clause, `#pfx(π) ≤ #pfx(π_d)`.
- Both `pfx(π)` and `pfx(π_d)` are prefixes of `pfx(π'')`; by the covering-chain lemma (cited from O2's proof), they are `≼`-comparable.
- With `#pfx(π) ≤ #pfx(π_d)`, the comparison gives `pfx(π) ≼ pfx(π_d)`.

The remainder of the base case (concluding `pfx(π_d) = pfx(π)` via empty `S_π`) and inductive step (concluding `pfx(π) ≺ pfx(π_d)` via `π_d ≠ π` and O1b) carries through using this direct argument.

### Issue 2: O10 Form B coverage analysis overstates necessity as sufficient

**ASN-0042, O10 proof, `zeros(pfx(π)) = 0` case, Form B analysis**: "The prefix relation `pfx(π_i) ≼ a'` forces `u = U^{(i)}_1`. Hence Form B sub-delegate `π_i` covers `a'` iff `u = U^{(i)}_1`."

**Problem**: The "iff" is wrong for Form B sub-delegates with `#pfx(π_i) > #pfx(π) + 2`. Such a sub-delegate has `pfx(π_i) = pfx(π).0.U^{(i)}_1.U^{(i)}_2....` with `U^{(i)}_2 > 0` (positivity from T4). Coverage of `a' = pfx(π).0.u.0.1.0.1` requires `pfx(π_i)`'s component at position `#pfx(π) + 3` to match `a'._{#pfx(π) + 3} = 0`, but `U^{(i)}_2 > 0`. Coverage fails regardless of `u`. The precise condition is: a Form B sub-delegate of length exactly `#pfx(π) + 2` with `U^{(i)}_1 = u` covers `a'`; longer Form B sub-delegates never cover `a'`. The construction's conclusion (choose `u ∉ S`) remains correct because `S` conservatively includes `U^{(i)}_1` from all Form B sub-delegates, but the "iff" intermediate claim misleads readers about the actual coverage conditions.

**Required**: Replace the "iff" with the precise characterization: "A Form B sub-delegate of length exactly `#pfx(π) + 2` covers `a'` iff `u = U^{(i)}_1`; longer Form B sub-delegates fail at position `#pfx(π) + 3` (positive `U^{(i)}_2` against `a'`'s zero) and cannot cover `a'` regardless of `u`. Choosing `u ∉ S` thus excludes all Form B coverage."

### Issue 3: O15 axiomatized before `delegated` relation is defined

**ASN-0042, State Axioms section (O15)**: "Principals enter Π exclusively through bootstrap (in Π₀) or delegation (satisfying the `delegated` relation defined below)... `(A π' ∈ Π_{Σ'} ∖ Π_Σ : (E π ∈ Π_Σ : delegated_Σ(π, π')))`"

**Problem**: O15's formal content quantifies over `delegated_Σ`, which is not defined until the "Delegation" section many pages later. Proofs of O3, AccountLevelPermanence, FirstDelegatorIsπ, O4, and others also reference conditions (i)–(vi) of `delegated` before the relation is formally introduced. The acknowledgment "defined below" signposts the issue but does not resolve it — readers cannot interpret the axiom's quantification, or verify the proofs that depend on it, without skipping ahead. Bootstrap-exclusion arguments (recurring in O3, O8, AccountLevelPermanence, FirstDelegatorIsπ) depend on the very structure being forward-referenced.

**Required**: Either (a) move the `delegated` definition before the State Axioms section so its conditions can be cited within their definitional context, or (b) state O15's content using the explicit six conditions inline (so it is self-contained even if the named relation is introduced later). The current structure obscures the dependency graph among foundational claims.

## OUT_OF_SCOPE

None — the open questions section appropriately defers ownership transfer, enforcement against overlapping claims, content accessibility upon principal death, domain density, cross-node federation, provenance-versus-ownership divergence under transfer, and delegation event recording. The scope section appropriately excludes modification rights, publication contracts, content storage, operation-specific effects, links and endsets, baptism mechanism, replication, and authentication mechanisms.

VERDICT: REVISE
