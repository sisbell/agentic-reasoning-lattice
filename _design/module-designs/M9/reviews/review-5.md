## Review: M9 — Predicate & Coordination Layer

I came at this hard — the late-stage items most likely to hide a defect are the conflict resolutions and the self-hosting seam. The ones I checked held up:

- **The two-transaction `register_pred` weakening of PR1(iv)** is *sound*: validation at σ vs emit at σ′ can only regress conjunct (iv) (active endorsement); (0/i/ii/iii) are content/signature-intrinsic and monotone, and PR2's acyclicity needs only *ever*-registered-strictly-earlier (which survives), so nothing load-bearing breaks. Correctly argued.
- **`pdef` Multi (PS1) → Unary (M7)**: deferring to upstream is right, and the "G=∅ loses nothing under n=1" claim checks out — resolution/expansion read content from `start`, never the tuple's G.
- **UV default-view `K_queried` self-exclusion** is handled correctly, including the subtle trap that blindly delegating `members(retired, default)` to M7's aggregate-`is_filtered` would self-erase to ∅.
- **`Reflect` denotational-completeness**, **BH4 totalization via active-tuple-address identity (not `is_k` coverage)**, **`L_dom` via `⋃_K observe(…,Audit)` rather than M8's `type_slice`**, and the **`eval` ref-free / `evaluate_def` resolve-then-denote split** are all faithful and buildable.

No invented/contradicted upstream *semantics*, no dropped note contract, no owned capability missing, no overreach into M8/M10, internal model/interface/invariants agree. The items below are genuine but non-load-bearing.

### Revision list

1. **[SHARPENING] Resolve the `Vstream::new` / `LinkStore::new` handle-construction seam by engine-injection rather than depending on unpublished constructors.** M9 correctly and accurately flags that M5's `Vstream<'k,W>` and M7's `LinkStore<'k,W>` expose no public constructor, yet M9 must build both to drive `insert`/`emit`/`nullify`. The fix is non-semantic and obvious (each struct's fields are documented), but cleaner than asking two upstreams to publish constructors is to have `Coordinator::new` *receive* the handles (or factories) from the engine assembler — which also eliminates item 2's double-build. As written it's a trivial-but-real cross-module build dependency; secure it before claiming compile-readiness.

2. **[SHARPENING] Don't rebuild a second `Arc<TypeRegistry>` inside M9.** M9 builds its own `TypeRegistry` via `TypeRegistry::build(reserved, decls)` *and* its own `TypeCatalog`, while the engine separately builds a registry for `LinkState::genesis`. Two deterministic builds of the same data is sound but redundant and a divergence trap if inputs ever drift. Prefer a single engine-built `Arc<TypeRegistry>` injected into both the genesis path and M9's `LinkStore` handle; keep the `TypeKey→(CoverageClass,Registration)` catalog as M9's static-analysis projection of it.

3. **[SHARPENING] Re-file the "never `count = 0`" item from active-enforcement to certifier precision.** The type-checker neither rejects nor needs to reject `count(D) = 0` — it's well-typed. The actually-enforced invariant is *the certifier never over-certifies* (it lands `count = c` in `Neither`, soundly). State it that way; `¬∃` vs `count = 0` is an authoring-precision recommendation, not a well-formedness rule.

4. **[SHARPENING] Correct the `supersede` idempotency attribution.** `supersede` is a public `Coordinator` method consumed out-of-corpus and reaches M5/M7 directly — it does *not* traverse M10's lifecycle, so "idempotency is M10's, as for `create_new_document`" is imprecise. The substance (no idempotency key; caller must dedup; a lost-ack retry branches the lineage to `Indeterminate`) is right; just attribute the duty to the driving coordination caller and present `create_new_document` as the *pattern* analogue, not the same dispatcher.

5. **[SHARPENING] Make the `TypeKey`-by-verbatim-endset caller obligation prominent.** Catalog lookup is `Endset`-equality, but M7's type identity is by *coverage* (I0). A PL `TypeKey` built from a coverage-equal-but-byte-different endset will miss as `UnregisteredType`. M9 already provides canonical endsets (`reserved_type` + the caller's own decl keys); elevate "PL `TypeKey`s MUST be built from M9's canonical endsets" to an explicit contract (or canonicalize a `Concrete` key through the catalog's stored class before the probe).

6. **[SHARPENING] State that `signature(start)` on a miss recurses through referent signatures.** WT-ref needs `sig(r)` for each referent; the derivation is well-founded by PR2 (referents strictly-earlier-registered) and every referent is ever-registered whenever `start` is. One sentence makes the non-flat derivation buildable without inferring it.

7. **[SHARPENING] Note the `quiescent_scoped` single-body semantics and the dormant `Nat→u64` narrowing.** (a) Applying one `ScopeBody` and leaving sort-incompatible rules *unscoped* yields a *stronger, safe-direction* verdict than ASN-0133's per-rule-body model — never false-quiescence — but it isn't the exact per-rule scoping the note's `ρ_R` example implies; say so, and that exact scoping would need per-rule body declarations. (b) The `stale` horizon `Nat→u64` conversion should saturate (`≥ 2^64 ⇒ all non-stale`); dormant in v1 (no BH4 type catalogs) but worth pinning at the seam.

VERDICT: CONVERGED
