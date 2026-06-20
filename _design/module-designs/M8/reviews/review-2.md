# Review: M8 — Link Query & Discovery

I went through every method against the upstream interfaces and the source-note statements, traced each algorithm for faithfulness, and stress-tested the load-bearing claims (the arity-3 invariant, `classify_spans` on cross-subspace spans, the last-witness set identity, the address-key cursor). The design is unusually disciplined: every upstream call type-checks against M1/M2/M3/M5/M7 as given, no API is invented, every owned capability is present, the boundary against M6/M7/M9 holds, and the eight conflicts are resolved soundly and documented. The two most consequential "deviations" — the **flipped supersession slot convention** and **content-only `project`** — are not liberties but *interface fidelity* (M7 actually stores `FROM=old`, M5's `project` actually is content-only), and both are correctly noted.

I verified in particular:
- **`delete_orphans`** = `findlinks(A_del) \ findlinks(retained)` is provably the ASN-0117 last-witness orphan set (since `ran(M(d)) = A_del ∪ retained`), with bounds that mirror DELETE's preconditions so the preview isn't of a coerced delete. Correct.
- **`retrieve_endsets`** `touches()` via `classify_spans` is exact: a span's coverage *is* its half-open tumbler interval, so `classify_spans` is the point-set relation, and content vs. link/cross-doc spans are order-`Separated`, never falsely surfaced. Correct.
- **windowing** via `OrdSet<Tumbler>` range-cut realizes ASN-0108's permanent address key (W4/W5/W6/W8) with cursor-survives-orphaning for free. Correct.
- **arity-3 invariant** holds across every v1 M7 creation path, making the `{FROM,TO,TYPE}` union the *exact* ASN-0127 disjunction, with the arity-≥4 risk honestly pinned.

I found no unbuildable component, no contradicted upstream call, no dropped contract, no internal inconsistency. The items below are all genuine-but-non-load-bearing.

## Revision list

1. **[SHARPENING]** State the `SlotSpec::Spans` non-empty invariant. `match_core` pushes `(slot, e)` for any `Spans(e)`; if a caller routes an *empty* `Endset` through `Spans` instead of `Empty`, M8 hands an empty `Endset` to M7's `match_links`, which M7 documents as "never an empty Endset." The result is still FL-EMP-correct (∅, since it empties the AND), so this is tidiness, not a correctness bug — but make it a stated caller obligation that `Spans` carries a non-empty `Endset`, or have `match_core` normalize an empty-coverage `Spans` onto the `Empty`/zero path so M7's guidance is respected by construction.

2. **[SHARPENING]** Sharpen the contract of the uniform `View::Active` filtering. Conflict #8 already documents that `findlinks_v`/`count_v`/`window_v`/`discoverable_from` are `foundation ∩ addressable`, diverging from ASN-0127/0098/0108's *unfiltered* `findlinks_V`/`discoverable_from`/`Match`. In each method's contract say so explicitly, and especially flag that **`discoverable_from` is the compound "arrangement-reachable AND active," not pure LP12** — a nullified-but-reachable link returns `Ok(false)` here, whereas LP12 (which predates retraction) would call it discoverable. A caller wanting raw LP12 then knows to compose `followlink` + M5 `project` itself.

3. **[SHARPENING]** Guard the empty-image case in `discoverable_from_on`. For a registered-but-empty `d`, `content_runs ∪ link_runs = []`, so `img` is an empty `Endset` fed to `stab_union`; correctness then relies on `stab(empty) = ∅` (M7 doesn't prohibit an empty *stab* query, unlike `match_links`, but doesn't promise it either). Add `if full.is_empty() { return Ok(false) }` — mirroring `findlinks_v`'s `img.is_empty()` short-circuit — for safety and to keep the empty-query reliance off the M7 surface.

4. **[SHARPENING]** Disambiguate `project`'s error and scope in its contract. `followlink(a, slot).map_err(|_| NotALink)` maps *both* "`a ∉ dom(L)`" and "slot index out of range" to `NotALink`; either add a `BadSlot` variant or document that `NotALink` subsumes an out-of-range slot. Separately, put the content-subspace-only restriction (strictly weaker than ASN-0098's subspace-agnostic `project`; link-side reverse discovery is M7's BH3) into the public method doc-comment, not only §5, so a builder doesn't expect link-subspace V-positions back.

5. **[SHARPENING]** `image` is public and returns `Vec<Run>` with possible duplicates under overlapping input spans. The internal harmlessness is argued, but since it's a public method whose source (ASN-0127 `image`) is a *set*, either dedup at the boundary or state the dedup obligation in the method contract so an external caller isn't surprised.

6. **[SHARPENING]** Note in `in_claims`/`out_claims` that `y`/`x` are expected to be resident link addresses. Exactness of `match_links(slot, enc([y])) ∩ type_slice(Supersedes)` ⟺ `old(e)=y` relies on the `dom(L)` prefix-antichain (EL4 + R0a); for an arbitrary non-link `y` the overlap test can over-match a prefix-comparable claim. Document the `y,x ∈ dom(L)` precondition (or gate and return `[]` otherwise).

7. **[SHARPENING]** Tighten the pseudo-code so it compiles cleanly: the `.filter(|t| keep(t))` / `.filter(|t| home_ok(q, t))` closures receive `&&Tumbler` (need `*t`); private helpers `stab_union`/`addrs` omit their `W: HasLinks` bound; and `vspan` elides the `Span::new(..)` unwrap. All trivial, but worth fixing in the reference bodies a builder will copy.

VERDICT: CONVERGED
