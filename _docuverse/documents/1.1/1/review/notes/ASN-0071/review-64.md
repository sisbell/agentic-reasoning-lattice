# Review of ASN-0071

## REVISE

### Issue 1: vspec/ContentReference conjunct ledger is an exhaustiveness inventory
**ASN-0071, *The query***: "relative to that definition's conjuncts it *keeps* one, *strengthens* one, *retains* one, and *drops* three. It **keeps** `Pos(ℓ)`... It **strengthens**... It **retains**... It **drops** three demands..."
**Problem**: The vspec is fully defined two paragraphs earlier (`subspace(u) = s_C, Pos(ℓ), actionPoint(ℓ) = #u, #ℓ = #u, actionPoint(ℓ) ≥ 2`). This paragraph is a conjunct-by-conjunct diff against ASN-0058's `ContentReference` whose only load-bearing content is one sentence — "search cannot guarantee... a query is posed against a source whose arrangement the requester does not control." The "keeps one / strengthens one / retains one / drops three" bookkeeping is decorative (note "keeps" `Pos` and "retains" `#ℓ=#u` are the same operation — preserving a conjunct — split into two labels for symmetry). A precise reader skips the ledger to reach the vspec semantics. This is exactly the use-site/exhaustiveness inventory the anti-bloat pass targets.
**Required**: Collapse to the substantive point — search relaxes `ContentReference` by dropping the source-controlled demands (`V_{u₁}(d_s) ≠ ∅`, `#u = m_C`, well-formed coverage) because the requester does not control the queried source. Drop the kept/strengthened/retained accounting.

### Issue 2: `iaddrs_one`/`resolve` coincidence paragraph is an ungrounded foundation aside
**ASN-0071, *Resolution***: "Where a vspec happens to be a well-formed `ContentReference`, the two coincide *as sets*: `resolve` decomposes `f = M(d_s)|⟦σ⟧` into maximally-merged runs (ASN-0058 C1a)... the set of run I-addresses is therefore exactly `{ M(d_s)(v) : ... } = iaddrs_one(d_s, σ)(Σ)`."
**Problem**: `iaddrs_one` is defined directly and self-containedly. No subsequent claim (F-COMP, F-SOUND, F-SELF, the worked scenario, finiteness) consumes the set-equality with `resolve`. The paragraph proves a relationship to the foundation that nothing downstream uses — accretion that does not advance the operation's reasoning. The preceding sentence ("the set-valued, deduplicating, coverage-tolerant counterpart of `resolve`") already conveys the intent; the coincidence proof is surplus.
**Required**: Remove the coincidence-as-sets derivation, or demote the relationship to a single descriptive clause. If the equality is meant to discharge a downstream obligation, name the consumer; otherwise cut it.

## OUT_OF_SCOPE

### Topic 1: Result/history (`R`) reconciliation, rejection-vs-filter policy, transition-straddling invariants
**Why out of scope**: These are the ASN's own Open Questions and concern future operations (currency-vs-provenance contract, contraction transitions). They are correctly deferred, not errors here.

VERDICT: REVISE
