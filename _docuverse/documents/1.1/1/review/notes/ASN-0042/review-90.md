# Review of ASN-0042

## REVISE

### Issue 1: Conditions (v) and (vii) of the delegation predicate are redundant given (viii)
**ASN-0042, O15 / Definition (delegated)**: "the eight conditions form the complete admission gate" and the separate characterizations "Condition (v) ... `T4(pfx(π'))`", "Condition (vii) is the *freshness* gate".

**Problem**: Condition (viii) requires `(E p, d : B6(p, d) : pfx(π') = next(Σ.B, p, d))`. For the witnessing `(p, d)`:
- ASN-0040's B6 sufficiency gives `(A n ≥ 1 : cₙ ∈ S(p, d)` satisfies T4`)`, and `next(Σ.B, p, d) = c_{hwm+1} ∈ S(p, d)` (B2). Hence `T4(pfx(π'))` — condition **(v)** holds automatically.
- By B1/B2, `next(Σ.B, p, d) = c_{hwm+1} ∉ children = Σ.B ∩ S(p, d)`, and being in `S(p, d)` it is not in `Σ.B`. Hence `pfx(π') ∉ Σ.B` — condition **(vii)** holds automatically.

So (viii) entails both (v) and (vii). The prose presenting eight independent "gates" — and the `delegated` definition's claim that (vii) is a distinct freshness gate — overstates independence. (Note (iv) `zeros ≤ 1` is *not* implied: B6(iii) only bounds `zeros(p)+(d−1) ≤ 3`, so (iv) is genuinely needed — which makes the redundancy of (v)/(vii) the more conspicuous.)

**Required**: Either drop (v) and (vii) and derive them as consequences of (viii), or, if retained for readability, state explicitly that (v) and (vii) are entailed by (viii) (via B6 sufficiency and B1/B2) rather than presenting them as independent admission conditions. The downstream NamespacePrincipalExclusivity and DelegatorAllocatesPrefix derivations that cite (vii) should cite the underlying source.

### Issue 2: Defensive justification prose around condition (viii) (anti-bloat)
**ASN-0042, O15**: "Without (viii), O15 would admit a strict extension whose intervening stream positions were never baptized — a prefix that O18's material baptism ... cannot realize ... Gregory's allocation path confirms the restriction: `findpreviousisagr` followed by `tumblerincrement(…, 1)` ... Nelson grants owners discretion ... but every illustration he gives is dense, successive allocation ... so (viii) records sequential next-reachability as the admissible discipline."

**Problem**: This is the flagged pattern "new prose around an axiom explains *why* the axiom is needed rather than *what* it says." The counterfactual ("Without (viii)…"), the implementation appeal, and the Nelson rationale are justification, not content. A reader following the predicate must skip past all of it to reach the next condition.

**Required**: Reduce to a one-line statement of what (viii) asserts (delegate prefix must be the next stream address of some B6-valid namespace). Move motivation, if kept at all, to a single sentence; delete the counterfactual and the implementation/Nelson rationale.

### Issue 3: Cross-reference meta-prose in the `delegated` definition (anti-bloat)
**ASN-0042, Definition (delegated)**: "Condition (vii) asserts the pre-state freshness ...; its post-state counterpart ... is O18. Condition (viii) asserts pre-state next-reachability ...; it is what makes O18's material baptism realizable as a single `Bop(p, d)` step (O17b)."

**Problem**: This is document-plumbing prose ("X's counterpart is Y", "what makes Z realizable") rather than statement of the predicate. It matches the flagged pattern of a definition deferring to / inventorying downstream consumers (O18, O17b) instead of advancing its own meaning.

**Required**: State the conjunction of (i)–(viii) and stop. Drop the (vii)→O18 and (viii)→O17b mapping sentences.

### Issue 4: Duplicated invariant-induction statement
**ASN-0042, O6 proof, O9 proof, and Delegation section**: O6 and O9 each carry the parenthetical "O1a is a derived invariant established by induction over reachable states, not an axiom"; the Delegation section separately states "Each of O1a, T4, and O1b is a reachable-state invariant proved by the same induction ...".

**Problem**: Same fact asserted in three places ("two paragraphs in the same document say the same thing"). The consolidated induction in the Delegation section already discharges it once.

**Required**: Keep the consolidated statement in the Delegation section; reduce the O6/O9 parentheticals to a bare citation of it.

### Issue 5: FiniteRegistry is derived but unconsumed
**ASN-0042, FiniteRegistry**: "`(A Σ : Σ reachable from Σ₀ : |Π_Σ| < ∞)`".

**Problem**: O2's finiteness step bounds the covering set by `|C(a)| ≤ #a` (length-indexed prefixes + O1b), not by `|Π_Σ|`. The `next`/`hwm` preconditions in O10 need `Σ.B` finiteness (B_fin), not `Π` finiteness. I find no consumer of FiniteRegistry in O1–O10. A derived result with no downstream use is noise in an anti-bloat pass.

**Required**: Either cite the consumer that requires `|Π_Σ| < ∞`, or remove FiniteRegistry (and its row in the Properties table).

## OUT_OF_SCOPE

### Topic 1: Ownership transfer reconciling provenance (O6) with effective owner (O2)
**Why out of scope**: Already correctly deferred to the Open Questions; no transfer mechanism exists in the system as specified, so its invariants belong to a future ASN.

### Topic 2: Cross-node identity federation invariants consistent with O9
**Why out of scope**: O9 establishes node-locality; federation is new territory, properly listed under Open Questions rather than this ASN.

META:

VERDICT: REVISE
