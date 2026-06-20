## Review: M6 — Content Retrieval & Query

I traced all seven operations against M1–M5 *as given* and against each owning note's postconditions, checking every upstream call typechecks and every contract is honored. The module is **buildable as written**: all seven ops compile against the supplied interfaces (I verified ~40 distinct upstream calls — no invented surface; the design even explicitly avoids non-existent `SpanSet::is_empty()` / `from_normalized_ordered`), and each op's algorithm matches its note's denotation. The four load-bearing decisions are sound and correctly attributed, so I want to be explicit they are **not** to be "fixed":

- **SHOWORIGIN_I de-scope** — `origins_I` needs an enumeration of `dom(C) ∩ ⟦σ⟧`, which M4 *deliberately* forbids (no range/prefix/ordered scan; `Ord` unused) and M3's registry is point-only. It is genuinely unbuildable within the seams; building it would force an M4-overreach defect. De-scoping with a recorded decomposition amendment, settled-by-construction (M6 exposes only `show_origin_v`), and confirming M10 promises no I-arity, is the correct response — not a silent hole.
- **R reverse-index in M5** — M5's *as-given* interface exposes `docs_containing`/`deletions`/`ever_placed` as M5 methods. Deferring to that (vs. the decomposition's "M6 owns the reverse-index hint" phrasing) co-locates the hint with R's authoritative state and keeps M6 stateless. Correct conflict resolution.
- **COMPARE V-reconstruction under D-CTG★** — `Run` carries no V-start, so the cursor must reconstruct V from `span.start()` + run widths; this is exact under content-density (an invariant M6 is entitled to lean on), and soundness (R1) checks out: per-block offsets put both feet at `lo+k`, the `lo<hi` guard makes every `ordinal_gap` a total same-chain subtraction, and the cross-product gives fan-out completeness (R2).
- **SHOWDELETIONS membership-test** — composing `arranged_content(d_B)` filtered by `deletions(d_A).denotes(·)` builds on M5/M1 as given (no SpanSet-intersection fault, no misplaced fold), and `denotes` is exact on the tested content addresses by prefix-freeness + merge-only-adjacent chain confinement.

No DEFECTs found. The items below are genuine but non-load-bearing.

### Revision list

1. **[SHARPENING]** In COMPARE's `resolve_blocks`, move the V-cursor alignment `debug_assert_eq!(m5.point(...).as_ref(), Some(&run.i_start), …)` **out of the `if first` guard** so it fires on every run. Under D-CTG★ the first-run check transitively covers later runs, but a per-run assert localizes a future density regression to the exact mis-aligning run instead of letting a mid-document V-gap pass the first-run check and silently mis-set a later block's `v_start`. (`vpos_of(&v)` stays depth-2-safe every iteration — a run exists only for a depth-2 span.)

2. **[SHARPENING]** Give `CompareError::NotContentSubspace` a `{ operand, index }` payload like its sibling `MalformedSpan`, so M10 can point the client at the offending spec rather than surfacing a locator-less rejection. The `Operand` is already in scope at the check site.

3. **[SHARPENING]** Rename/redocument the `dedup_docs` helper: in SHOWDELETIONS it dedups content I-addresses, not documents (it is really `dedup_addrs(impl Iterator<Item = Address>)`). The name misleads at that call site.

4. **[SHARPENING]** Add a guard in `run_addr` — `debug_assert!(i_start.element_field().map_or(false, |e| e.len() == 2))` — so the acknowledged "longer element field is silently truncated" hazard fails loudly if a non-2-component element address ever reaches M6. M3 only mints 2-component element fields, so this is a tripwire, not a path.

5. **[SHARPENING]** Tighten the I-arity de-scope corroboration: M10's enumerated reader sources omit ASN-0077 **and** ASN-0075 *entirely*, so they support "no SHOWORIGIN-over-I" only vacuously — the load-bearing argument is "M6's `Query` exposes only `show_origin_v`." Separately flag that M10's reader-marshaling list omitting 0077/0075 (both M6 readers M6 ships `show_origin_v`/`show_deletions` for) is an M10-side reconciliation item, not an M6 defect.

6. **[SHARPENING]** Unify the "document + span-set" request shape: COMPARE takes `&[Spec]` (one span each, multi-span via repetition) while FINDDOCSCONTAINING takes `Region { doc, spans: Vec<Span> }`. Both are faithful (COMPARE's `&[Spec]` is treated as the unordered set ASN-0122's `ρ` is), but a single idiom would cut reader friction.

VERDICT: CONVERGED
