# Review: M5 — Arrangements & Editing (Vstream)

I checked this hard against the upstream interfaces (M1–M4), the Engine Composition Contract, and the ten source notes. The design is unusually disciplined: the implicit-position run-list makes D‑SEQ★/D‑CTG★/D‑MIN★ free, the effect-level `M5Rec` is correctly forced by M2's upstream-blind fold, the J‑couplings are enforced by co-locating M and R in one fold, and the mixed-length-iextent / level-class hazard (a real consequence of cross-origin transclusion under M1's level gate) is both *encapsulated* for M6 and *exposed-with-contract* for M7/M8.

I verified the load-bearing subtleties specifically:
- **VersionSnapshot replay determinism** — the `{source,new}` record's fold reads source at journal-order replay, which reconstructs source to its fork-point; correct, and the one place a fold reads sibling state. Sound.
- **ω(d_src) pre-read off a snapshot** — sound, because every document has an account-tier owner (accounts only arise via `delegate`, which co-registers a principal), so ω is genuinely stable and the lock choice can't race.
- **J1★ range-based coupling under unconditional R-append** — correct given R's set-union denotation (duplicate appends are P2 no-ops; P4★ guarantees in-range addresses already sit in R).
- **Eager I-adjacency coalesce** — complete and safe: shift preserves length, so cross-length (hence cross-origin, M16a) runs never merge, and shared-I-extent (M14a) is excluded.
- **`docs_containing` no-false-negatives** — a genuinely-contained address forces order-overlap, so `classify_spans ≠ Separated` is a sound superset even cross-length; narrowed correctly by `project`.
- **BadSpan = resolve's guard**, and ordinal-level depth-2 is the *effective* ASN‑0058 (C0a/C1a) precondition the resolution actually needs — no valid COPY is rejected.
- All upstream calls (`mint_*`+lock-key discipline, `stage_write`, `contains`, `transact`/`snapshot`, `shift` only on full element I-starts) are used exactly as the interfaces give them; no invented or contradicted API. Conflicts #2 (presence via `M4::contains`, not `M3::is_allocated`) and #6 (M5 owns R + any index; M6 owns only the query) are correctly identified decomposition imprecisions, soundly resolved.

I found **no defects**. The items below are genuine polish.

## Revision list

1. **[SHARPENING]** State the required `From` conversions the in-closure `?` operators depend on — `From<MintError> for InsertError`/`VersionError` and `From<ContentError> for InsertError`. The variants (`Mint(MintError)`, `Content(ContentError)`) imply them, but a builder shouldn't have to infer that the `mint_content(doc)?` / `stage_write(…)?` desugaring needs these.

2. **[SHARPENING]** Define `extend_run` / `extend_or_push_run` (used in INSERT/COPY) against §1's coalesce rule: widen the currently-open run when the new run I‑extends it (`shift(i_start, width) == next.i_start`), else push a new run. INSERT's "always one run" and COPY's origin-multiset preservation both rest on this helper.

3. **[SHARPENING]** Replace the fold shorthand `R'[k].push_back(r.iextent())` (and the VersionSnapshot equivalent) with the persistent form — `im::OrdMap` indexing returns `&V` and panics on an absent key, so the real code is `R' = R'.update(k, R'.get(k).cloned().unwrap_or_default().push_back(...))`.

4. **[SHARPENING]** Soften the "both standing invariants are type-enforced (not merely conventional)" claim for `Run`: derived `Deserialize` constructs `Run` directly, bypassing `Run::new`, so a deserialized Run's `width ≥ 1` / element-level guarantee rests on M2's checkpoint-integrity (the same trust posture as the rest of recovery), not on the type system. `iextent`'s `.expect` is then justified for all *minted-or-validly-recovered* Runs.

5. **[SHARPENING]** Add eager-vs-lazy coalesce to the Open build decisions list (it is argued in §1 but absent from the list, unlike every other realization choice); and have the `VersionSnapshot` fold skip `arrangements.update` when the source content is empty (`n = 0`) — the current path materializes a redundant empty entry that the lazy-absent convention otherwise leaves out (harmless, but it muddies the "absent ⇒ empty" equivalence).

6. **[SHARPENING]** Two cosmetic completeness fixes: in `stage_seat_link`, the CL‑OWN test compares `Option<Address>` with `Option<&Address>` — write `M1::document_of(link).as_ref() == Some(doc)`; and show `DocArrangement`'s `#[derive(Clone, Default, Serialize, Deserialize)]`, required transitively by `M5State`'s derives.

VERDICT: CONVERGED
