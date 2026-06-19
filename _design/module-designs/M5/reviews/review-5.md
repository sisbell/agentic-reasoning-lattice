Reviewed against the M5 source notes (ASN‑0036/0058/0082/0084/0116/0117/0118/0119/0123/0047), the four upstream interfaces (M1–M4), the decomposition, and the Engine Composition Contract.

This is a strong, unusually careful design. I verified the load‑bearing pieces:

- **Every upstream call matches the given interface** (M1 `shift`/`validate`/`document_of`/`from_endpoints`/`classify_spans`/`denotes`/`intersect`/`union`/`normalize`/`difference_sets`; M2 `transact`/`snapshot`/`Staging`; M3 pure mints + lock keys + queries; M4 `stage_write`/`contains`). No invented or contradicted upstream API.
- **The folds realize the operation postconditions**: `splice_in`/`remove_range`/`reorder`‑tiling correctly implement I3/D‑SHIFT/Pivot‑Swap; the `iextent` lift is genuinely the only well‑formed Run→Span conversion and the malformed‑span trap is correctly avoided; J0/J1★/J‑LV fall out of one composite per op; VERSION's structural share copies the map (multiplicity), not the range (V2); R is co‑located so SHOWDELETIONS/FINDDOCSCONTAINING read one `(M,R)` snapshot (ASN‑0075).
- **The level‑class discipline is a real necessity** (transclusion across heterogeneous‑depth origins genuinely yields mixed‑length covers that fault M1's length‑gated ops), and the per‑class `difference_sets`/`intersect` + total `classify_spans`/`denotes` handling is sound.
- **ω(d_src) is provably stable** for an existing document (accounts are minted with their principal, no prefix changes, no longer‑prefix coverer possible), so VERSION's snapshot pre‑read of the branch/lock is correct.
- **Conflict resolutions are stated and sound** — the S3 gate is correctly `M4::contains` (presence), not `M3::is_allocated`; I‑adjacency coalesce is M14a/M16a‑safe; effect‑level journal is forced by M2's blind fold; the reverse‑prov index is correctly relocated to M5 (an index over M5's own R cannot be built from M6's pure surface).
- **No owned capability is missing and no neighbor material is designed.**

I found no material problem that would stop or mislead a builder. The items below are genuine but non‑load‑bearing.

## Revision list

1. **[SHARPENING] Reconcile §2's "rather than handing a raw mixed‑length cover across the seam" with `resolve_coverage`/`content_image`/`ever_placed`, which deliberately do.** State the asymmetry explicitly: M5 *encapsulates* the level‑class discipline behind the M6 **query** methods (`project`, `deletions`) so M6 never sees length‑gated algebra, but it *exposes* raw, un‑normalized, possibly‑mixed‑length covers to M7/M8 (`resolve_coverage`) and to FINDDOCSCONTAINING's filter (`content_image`) under the documented "consume under the level‑class discipline" contract. The method docs are correct; only the §2 blanket sentence over‑generalizes.

2. **[SHARPENING] Specify the CL‑UNIQ guard precisely in `stage_seat_link`.** `link ∈ m5.link_runs(doc)` is not well‑typed (an `Address` against `Vec<Run>`); the intended test is I‑extent membership over the link run‑list — "some link run's `iextent()` `.contains(link.tumbler())`" — which also catches a link already interior to a coalesced link run.

3. **[SHARPENING] Pin which primitive FINDDOCSCONTAINING's current‑containment filter uses.** The →M6 seam pairs `docs_containing` with `content_image`, but §9's algorithm filters by `project(d, region) ≠ ⟨⟩`. Note that current‑containment is computable either way and state that FINDDOCSCONTAINING uses `project` (which already applies the discipline internally), so `content_image`'s exposed role is the SHOWDELETIONS operand, not the filter.

4. **[SHARPENING] Resolve the `Run` public‑fields vs. "`stage_*`/op bodies are the only constructors" tension.** Public `i_start`/`width` permit a struct literal that bypasses `Run::new`'s `width ≥ 1` guard (a `width == 0` Run would panic `iextent`'s `.expect`). Either privatize the fields with read accessors, or restate the invariant as "every Run M5 *emits* has `width ≥ 1` by construction" and scope `Run::new` as the (v1‑unused) external‑producer guard.

5. **[SHARPENING] State that M5 has no `LockKey` space tag of its own.** All M5 mutations serialize on M3's `content`/`link`/`version`/`document` keys (arrangement + R co‑serialized within the document's allocation domain). Make this explicit so the engine assembler does not allocate an unused M5 `Space` tag and the serialization story is unambiguous.

6. **[SHARPENING] Note the `im` crate's `serde` feature as a build precondition** for `M5State`'s `Serialize`/`Deserialize` derive (it owns `im::OrdMap`/`im::Vector`), analogous to M4's `num-bigint` serde note — without it, no checkpoint serializes.

7. **[SHARPENING] Make VERSION's P‑tier scoping less indirect.** Rejecting the scoped‑out node‑tier cross‑owner case by letting `mint_document(&pfx)` return `Mint(NotAnAccount)` is correct but opaque; consider an explicit `zeros(pfx)==1` check yielding a clearer `VersionError` (or at least a one‑line P‑tier note at the branch), so M10 surfaces a self‑describing rejection.

VERDICT: CONVERGED
