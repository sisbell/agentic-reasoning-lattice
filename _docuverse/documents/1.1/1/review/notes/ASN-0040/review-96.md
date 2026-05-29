# Review of ASN-0040

## REVISE

### Issue 1: Meta-prose around B0 explaining why the axiom is needed rather than what it says
**ASN-0040, "The baptismal registry"**: "This ASN governs the write, so B0/B0★ are not a re-derivation of T8's permanence but the permanence law for the registry component specifically; whether the two components coincide (whether every allocator extension is matched by a baptismal write) is deferred to the open question `allocated(s) ⊆ s.B` below."
**Problem**: This is the flagged accretion pattern. The first half of the paragraph (distinguishing `allocated(s)` = realized domain / query phase from `s.B` = committed registry / write phase) legitimately situates the new state component. The quoted clause then (a) explains *why* B0 is needed ("not a re-derivation of T8") rather than what it asserts, and (b) defers to a downstream open question. The same `s.B`-vs-T8 relationship is touched a third time in the Properties table ("analogous to T8 for the registry component"). A reader following the B0 statement must skip past this to reach the actual law.
**Required**: Cut the "not a re-derivation … deferred to the open question below" clause. Keep only the operational query/write distinction that defines `s.B`; let B0/B0★ state the permanence law without the apologia, and let the open-questions section carry the `allocated(s) ⊆ s.B` deferral once.

### Issue 2: B4 adds little beyond the foundation Σ signature it restates
**ASN-0040, B4 / "Atomicity"**: "the foundation fixes every `op ∈ Σ` as a single partial function on 𝒮. Hence whatever registry update the operation performs is committed on one edge of `→`."
**Problem**: B4's content is exactly the foundation's Σ-signature property (each `op ∈ Σ` is one partial function = one transition edge) re-applied to `baptize`. The prose restates the signature rather than deriving anything baptism-specific. It is cited downstream (B8, B9) only as "single edge," which is the bare Σ property.
**Required**: Either fold the single-edge fact directly into the points of use (B8, B9) citing the foundation Σ signature, or, if B4 is retained as a named handle, reduce it to one sentence ("each `baptize(p,d) ∈ Σ` is one transition edge by the foundation Σ signature") without the surrounding restatement of the signature itself.

## OUT_OF_SCOPE

### Topic 1: B3 (Ghost Validity) constrains a content-storage predicate
**ASN-0040, B3**: introduces `Occupied : T × 𝒮 → {⊤,⊥}` and the requirement `Occupied(t,s) ⟹ t ∈ s.B`.
**Why out of scope**: "Content storage and retrieval" is on the explicit OUT OF SCOPE list. The ghost-element *concept* (baptized ≠ occupied) is intrinsic to baptism's meaning and worth naming, but the formal constraint dictating where content may live belongs to the future content-storage ASN that introduces `Occupied`. As written, B3 defines a claim over a content predicate; per the scope instruction such claims should be flagged. The Nelson grounding for ghost elements can stay as motivation without the `Occupied` requirement.

### Topic 2: allocated(s) ⊆ s.B activation discipline
**Why out of scope**: The relationship between allocator realized domains and the committed registry is correctly deferred to the open question; it requires an activation discipline not yet specified. Noted only to confirm the ASN's own deferral is appropriate, not an error here.

---

Note on rigor (no findings): I checked the substantive proofs. S(p,d) canonical form, S0, B5/B5a, B6 sufficiency *and* necessity (d≥3 adjacency; d=2 zero-budget), B7's full length-split / equal-length-parents / unequal-length-parents case analysis (including the T4 nonzero-last-component closer), B1 induction over target and non-target namespaces, B2, B8 same-namespace `m₂ ≥ m₁+1` and cross-namespace via B7, B9 constructive induction, and B10 are sound. The B0a → B_fin → next → Bop layering is non-circular: B_fin needs only singleton-union finiteness, not freshness. Boundary cases (empty registry/seed, hwm=0 first child, d=1 vs d=2) are all exercised by the trace. The B7 illustrations (equal-length parents, nesting prefixes) are concrete and correct, not bloat.

VERDICT: REVISE
