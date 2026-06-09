# Review of ASN-0121

## REVISE

### Issue 1: FL-WILD table overclaims "consulting no endset" for the all-wildcard operation
**ASN-0121, Claims Introduced table, FL-WILD row**: "all-wildcard returns all addressable links of every arity `N ≥ 3`, consulting *no* endset (every `lift` is `true` independent of endset content, so no endset enters `sat`)"

**Problem**: The parenthetical justification establishes only that `sat` reads no endset. But the *operation* for the all-wildcard request is `findlinks((∗,∗,∗,∗), Σ) = addressable(Σ) = dom(Σ.L) \ nullified(Σ)`, and computing `nullified(Σ)` requires identifying the retraction relation `L_R^Σ` — which reads every link's slot-3 endset (to test membership in `[coverage(R)]`) and each retraction tuple's to-coverage. So the operation *does* consult endsets even when every `lift` is `true`. "sat consults no endset" does not license "the operation consults no endset," because addressability determination reads retraction endsets. The body text ("`findlinks((∗,∗,∗,∗), Σ) = addressable(Σ)` — all currently addressable links") is accurate; only the table's added "consulting no endset" clause overstates. This is the same kind of read-set precision the ASN is otherwise careful about (FL-DEF's frame, "reads only the link-store projection `Σ.L`").

**Required**: Scope the clause to `sat` (e.g., "no endset enters the matching predicate `sat`; addressability is still determined by reading retraction-link endsets to compute `nullified`"), or drop "consulting no endset" from the table row, leaving the accurate "returns all addressable links of every arity `N ≥ 3`."

## OUT_OF_SCOPE

None beyond the topics already correctly deferred to the Open Questions (version/time-qualified inquiry, the V-spec ↔ I-address invariant, single-subtree residence reduction, exact subtype-by-containment conditions, and cross-federation completeness). These are properly stated as open questions rather than claimed.

VERDICT: REVISE
