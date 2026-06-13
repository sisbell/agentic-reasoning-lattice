# Review of ASN-0123

This is a strong, carefully argued note. The core lemmas I checked closely — SA, VN-B1, V8, the V9(a) severance argument, V10 — are rigorous, the boundary cases (empty source `n = 0`, sharing in `A`, first-vs-subsequent version via k=1/k=0) are handled, and the implementation deviations are honestly flagged. Two issues remain.

## REVISE

### Issue 1: Node-tier cross-owner fork — V9(b) ownership is asserted, not established

**ASN-0123, Identity clause (cross-owner branch) / V-WF / V9**:
- Operation: "*v := a fresh document identity that π allocates in its own document-creation namespace: `allocated_by(π, v)`.*"
- V9: "*let v be the identity π allocates — `allocated_by(π, v)` … so O5 gives both `pfx(π) ≼ v` (O5(i)) and the maximality … Then: (b) Ownership — `ω'(v) = π`.*"
- V-WF: "*a node-tier forker (`zeros(pfx(π)) = 0`, which O1a admits into Π) … reaches a fresh document only through an out-of-scope, possibly multi-step document-creation composite — baptizing an intermediate account before the document. That sub-composite's sole consumed contract is `Document(v) ∧ v ∉ E ∧ O5` …*"

**Problem**: P-prin admits any `π ∈ Π`, and O1a explicitly admits node-tier principals (`zeros(pfx(π)) = 0`). For such a forker, V-WF concedes `v` can be reached only by first baptizing an intermediate account, after which the document `v = [N,0,U,0,D]` sits beneath that account's prefix `[N,0,U]`. Both readings of "baptizing an intermediate account" break the V9 derivation, and the ASN resolves neither:

- *If the account is delegated as a principal `π_acct`* (the standard O15 path), then `pfx(π) ≺ pfx(π_acct) ≼ v`; the effective owner is the most-specific coverer (O2), so `ω'(v) = π_acct ≠ π` and **V9(b) is false**. Worse, `allocated_by(π, v)` is then false (`v` is `allocated_by π_acct`), so O5 at `v`'s allocating transition yields maximality *w.r.t. `π_acct`*, not `π` — and V9(a)'s step "*O5's maximality … forces `#pfx(π_o) ≤ #pfx(π)`*" loses its premise.
- *If the account is left a bare entity (no principal)*, then `allocated_by(π, v)` and `ω'(v) = π` can hold, but the ASN never says this, and a document effectively owned by a node-tier principal through an undelegated account is an unusual configuration not justified against the account-tier ownership reasoning the rest of the note relies on (e.g., the `zeros ≤ 1` appeals in V8 and V9 themselves).

V-WF's claim that the sub-composite "*provides … O5*" never pins *which principal* O5 is with respect to — and V9(a)/(b) require it to be `π`.

**Required**: restrict the cross-owner clause and V9 to account-tier forkers (`zeros(pfx(π)) = 1`); or specify explicitly that node-tier forking creates an *undelegated* intermediate account entity (so `allocated_by(π, v)` and `ω'(v) = π` hold) and justify that ownership configuration; or restate V9(b) as "`ω'(v)` is the unique maximal-length principal covering `v`" and route the severance argument through that principal.

### Issue 2: V9w's first conjunct cites a composite-boundary property at an unconstrained start state

**ASN-0123, V9w**: "*`(a, d_src) ∈ R'` … The first conjunct holds at Σ already: `d_src` contains `a` in its content subspace, and containment is provenance-bounded at composite boundaries (P4★).*"

**Problem**: P4★ is a *composite-boundary* property — the foundation's `ExtendedReachableStateInvariants` lists `P4★ ∧ P4a ∧ P7a` only among the properties that hold "*at a composite boundary*," explicitly excluding them from the per-state invariants. But the operation is specified to run at "*every reachable Σ with `d_src ∈ E_doc`*," and the note's own atomicity remark concedes that composites may begin at interior states ("*nothing in the foundation forbids another composite from beginning there*"). At such an interior `Σ`, P4★ need not hold, so the cited justification does not establish `(a, d_src) ∈ R`. The conclusion is salvageable by a different route — `a` entered `d_src`'s content-subspace range at some prior transition whose boundary recorded `(a, d_src)` via J1★, and P2 preserves it — but that is not the argument given, and the note surfaces the exact tension itself in the atomicity remark.

**Required**: constrain the operation's start state `Σ` to a composite boundary, or replace the P4★ citation with the persistence argument (J1★ at the recording boundary + P2).

## OUT_OF_SCOPE

### Topic 1: the document-creation composite invoked by the node-tier cross-owner path
The internal step structure of minting a fresh document under a principal's domain (intermediate account baptism, document sub-allocator mechanics) is correctly deferred to the out-of-scope document-creation operation. Issue 1 does **not** ask this ASN to specify that mechanism — only that the in-scope ownership conclusion V9(b) be made honest about what the deferred mechanism actually delivers (and about which principal `ω'(v)` names).

### Topic 2: serialization of concurrent same-source forks
The freshness/uniqueness of `v` (V0) leans on B-Seq's single-authority serialization, and the ASN flags concurrent forking as an open question. This is genuinely future territory (a concurrency-model ASN), not a defect here.

VERDICT: REVISE
