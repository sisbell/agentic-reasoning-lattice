# Review of ASN-0134

This is a careful, deep note. The conflict theory (H0–H3), the confluence result (G1), the invariant partition (W0–W6), and the quiescence analysis (V0/V2/V1) are worked with genuine rigor — boundary cases are hit (H2's first-emission vs interior collision, W5's both branches of `P-tgt`, A5's `m=0`/`m=1`/`m≥2` taxonomy), the proofs do explicit case analysis rather than "by similarly," and the operation/step seam (§4's two order-dependence families, the literal-vs-operative reading of I1a) is drawn out rather than glossed. The worked scenarios (§7, §8) check the postconditions against concrete addresses. One classification error, with a real downstream consequence, and one completeness gap, both in A1's treatment of the behavioral reads.

## REVISE

### Issue 1: `age`/`stale` are misclassified as single-type / single-index "Observe_K-grade" reads

**ASN-0134, A1**: "A read confined to one type's active view — `Observe_K` itself, and `is_K`, `members(K, active)`, `targets_of(x, active)`, `succs`, `chain`, `tip`, `sources_to`, `target_of`, `age`, `stale`, the per-type `is_filtered` — is realized as one `Observe_K`-grade read touching one index, so its definitional single-state form and its realized single-index form coincide."

**Problem**: This directly contradicts the foundation it cites. ASN-0128 BH4 defines `age(a) = f_d^Σ − 1 − j` and states outright: *"The chain interleaves every type homed at `d`, so age counts the home's subsequent link traffic, **not K-events alone**."* The home frontier `f_d` aggregates the link emissions of *every* type homed at `d`; it is not a function of type `K`'s active view and is not an `Observe_K` read (which is per-type by ASN-0086). `stale(h) = {a ∈ A_K : age(a) > h}` inherits this — its output set is type-`K`, but each constituent `age(a)` reads `a`'s home's cross-type chain. So neither is "confined to one type's active view," and neither is "one `Observe_K`-grade read."

This is not merely loose phrasing, because A1's single-type/cross-type split is *load-bearing*: it is exactly what decides which reads get single-index atomicity for free (clause 4) versus which are §8 *multi-reads* requiring the global reader-side pin (clause 7, V2). The note never establishes that the home frontier `f_d` is deliverable at a single index over the surface it commits to (ASN-0086's per-type `Observe_K` plus ASN-0128's D1–D4/BH1–BH4 — none of which exposes a home-chain count). It simply asserts `age` is "one `Observe_K`-grade read." If `f_d` must instead be assembled by unioning per-type views to find the home's maximal chain index, then `age`/`stale` are precisely the cross-type multi-reads of §8 (drift-prone, sound only under clause 7) — yet A1 places them with the free single-index reads. A realistic quiescence predicate such as "type-`K` active and all events past horizon `h` retired" uses `stale`; under the current text its `stale` component is (mis)classified as discharging clause 7 for free, when the note has not shown the home-frontier read does not straddle a write.

**Required**: Either (a) justify `age`/`stale` as *home-relative single-snapshot* reads — name the read primitive that delivers `f_d` atomically at one index and correct the characterization (they touch one home's *cross-type* link chain, not "one type's active view," and are not `Observe_K` reads) — or (b) if the home frontier is recoverable only by assembling per-type views, reclassify `age`/`stale` (and any verdict built on them) as §8 multi-reads whose soundness requires MIC clause 7. The current "confined to one type's active view / one `Observe_K`-grade read" cannot stand alongside ASN-0128 BH4.

### Issue 2: A1's behavioral-read enumeration omits `is_in_chain`

**ASN-0134, A1**: "...a *read-only query* — an `Observe_K`, or any of ASN-0128's behavioral reads `members`, `is_K`, `targets_of`, `succs`, `chain`, `tip`, `sources_to`, `target_of`, `targets_keyed`, `age`, `stale`, `is_filtered` (D1–D4, BH1–BH4), each committing no `→_sh` step..."

**Problem**: ASN-0128 BH2 defines four reads — `succs`, `chain`, `tip`, **`is_in_chain`** ("`target ∈ chain(addr)`: ... an enumeration-derived test"). A1's explicit list, which is the form the prose claims rely on, enumerates eleven reads and drops `is_in_chain`. The category citation "(BH1–BH4)" arguably covers it, but an enumeration that claims to list "any of ASN-0128's behavioral reads" should be exhaustive. (No downstream classification is wrong — `is_in_chain` is a single-type BH2 walk-membership test, so it is zero-step and single-index like `chain` — but the list is incomplete.)

**Required**: Add `is_in_chain` to the enumeration, or replace the closed list with "the behavioral reads of D1–D4/BH1–BH4" so the category citation, not the partial list, carries the claim.

## OUT_OF_SCOPE

None to add. The note's own Open Questions and "What this note does not cover" correctly defer cross-server composition (OQ7/BEBE), batch read-atomicity (OQ5, the gap A5 leaves), durability-promotion (OQ6, V1's hypothesis), the realizing primitives for clauses 2/7/8 (OQ1–3, mechanism), and the static-partition weakening of clause 2 (OQ9) — each is genuinely future territory, not a hole in this note.

VERDICT: REVISE
