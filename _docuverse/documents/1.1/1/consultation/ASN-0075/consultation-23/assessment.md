# Channel Assignment — ASN-0075 review-23

**Date:** 2026-05-25 19:27

## Issue 1: D-EXH's composite-boundary hypothesis isn't reflected in SHOWDELETIONS's precondition
Reason: The fix is a formal contract decision about whether observational operations are conceptually queries against stable/boundary states or invokable mid-transaction. Nelson's design intent on the relationship between queries and transaction boundaries informs which resolution path (precondition tightening vs. system-level discipline) honors the original design.
Nelson question: In Nelson's design, are observational operations like SHOWDELETIONS conceived as queries issued only at stable, transaction-boundary states, or are they expected to be runnable at any observable point in system state?

## Issue 2: D-ACT's structural observation about T1-consecutiveness in dom(C) is labeled "not needed for the bijection" yet spans a major case analysis
Reason: The fix is internal — it's a writing/structure decision about whether the observation has a downstream consumer within the ASN. The author can audit the ASN's own claims to determine if T1-consecutiveness is cited anywhere, and either promote it to a named lemma with explicit consumer or excise it with a forward reference.
