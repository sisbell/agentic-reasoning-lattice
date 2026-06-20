`Copy` on `VarId` and `RuleId` (both flow by value and as map keys throughout). For `signature`'s recursive memoization, specify a concurrent map or release the `DefMemo` lock before recursing — a `RwLock` held across the referent recursion would self-deadlock on the nested fill.

---

**Verdict rationale:** Every owned capability (PL type-check/eval/classify, defs-as-content with self-hosting expansion, the reactive rule engine with Q0–Q9 quiescence) is specified concretely enough to build; the upstream calls (`vstream.insert`, `link_store.emit`/`nullify`, `observe`/`members`/`targets_of`/BH-reads, `is_registered_document`, `value_at`, `snapshot`) are all real and correctly-typed; the source-note contracts are honored, with the few forced adaptations (pdef Multi→Unary, n=1 encoding, two-transaction register, single-deposit fires) each shown sound and tied to a concrete upstream constraint. The eight items above sharpen prose, concretize one elided type, and add Copy/locking trivia — none would stop or mislead a competent builder.

VERDICT: CONVERGED
