# Review of ASN-0118

This is a careful, unusually rigorous note. The composite decomposition is genuinely exhibited (not asserted), the three-branch provenance argument is airtight, the tiling is derived from ordinal arithmetic rather than hand-waved, and the I3-borrowing is scoped correctly (per-position facts only, with the global structure resting on the tiling + K.μ⁺ contract). The CP1-as-defining-frame thesis is sound. The findings below are precision defects and accreted prose, not structural failures.

## REVISE

### Issue 1: CP5 conflates the spec-set source with the content's actual allocator

**ASN-0118, CP5 / Claims table**: prose — "it equals the document that allocated `cᵢ` — a source, never `d` (unless `d` was itself that allocator)"; table — "OriginInvariance: `origin(cᵢ)` is unchanged by COPY and equals **the source document that allocated `cᵢ`, never `d`**".

**Problem**: `origin(cᵢ)` is the document that *allocated* `cᵢ`, which need not be the spec-set source `d_s`. COPY itself manufactures the counterexample: if `d_s` previously transcluded content allocated by a third document `d_C` (a chained transclusion, which CP2+CP1 produce), then resolving that content gives `cᵢ` with `origin(cᵢ) = d_C` — **neither the spec-set source `d_s` nor `d`**. The gloss "a source" / "the source document that allocated `cᵢ`" is wrong here: the true allocator may be a document the caller never named. This is the architecturally important case (transitive transclusion preserves the *original* allocator's attribution, not the intermediate source's), and CP5 understates it.

Separately, the table drops the prose's caveat and states "never `d`" baldly. This is false in the *copy-back* scenario: `d` allocates content `a` (so `origin(a) = d`), `d_s` transcludes `a`, then `d` does COPY from `d_s` resolving `a` — now `origin(cᵢ) = d`. The prose's "(unless `d` was itself that allocator)" handles this; the table contradicts it.

Note that CP11 is *correct* on the same scenario, because it uses `origin` (the true allocator) rather than the "source" gloss — so this is a CP5 wording defect, not a deeper flaw.

**Required**: State CP5 (and the table entry) as: `origin(cᵢ)` equals the document that *originally allocated* `cᵢ`, invariant under COPY (S7d); this allocator may be the spec-set source, a third document the source itself transcluded from, or `d` itself (copy-back / self-transclusion). Drop the unqualified "never `d`" from the table.

### Issue 2: CP11's formal object is a set, but the claim and example require a multiset

**ASN-0118, CP11**: "the multiset of origins carried by the placed material, `{ origin(cᵢ) : 0 ≤ i < W }`, is preserved verbatim"; worked example: "the placed multiset is `{d_A, d_A, d_B}`".

**Problem**: Set-builder notation `{ origin(cᵢ) : 0 ≤ i < W }` denotes a *set*, collapsing `{d_A, d_A, d_B}` to `{d_A, d_B}` and discarding multiplicity. But multiplicity is the content of the claim — the entire CP11/REPLICATE contrast turns on counting fragments (two fragments from `d_A` give two `d_A` entries; REPLICATE collapses to `{d, …, d}`). The label says "Multiset," the prose says "multiset," the example shows repeats, yet the formal statement denotes a set. As written, the formal claim is weaker than the one being argued.

**Required**: Use multiset notation or an indexed sequence (e.g., `⟨origin(cᵢ) : 0 ≤ i < W⟩`, or explicit multiset brackets) so the formal object carries multiplicity.

### Issue 3: CP0(a)'s bridge asserts run interval-disjointness without its reason

**ASN-0118, "What a spec-set names" (CP0(a))**: "The runs being a disjoint maximal partition of the totally-ordered `act(ρ, Σ)`, each run's positions ascend with `k` and **lie wholly below the next run's**, and C1b... lists the runs in strictly increasing V-start order, so concatenating the runs in C1b order reproduces the ascending enumeration of `act(ρ, Σ)` address-for-address."

**Problem**: "Lie wholly below the next run's" is the load-bearing step — without non-interleaving, concatenating runs in V-start order would *not* reproduce the ascending enumeration, and the whole `expand` = per-position-reading bridge collapses. Yet it is asserted from "disjoint partition of a totally-ordered set," which alone does not give it (a partition of a totally-ordered set into runs can interleave in general). The fact is true, but it needs the two premises the ASN already has on hand and does not invoke: shift fixes the prefix (so each run occupies one lexicographic prefix-line as a *consecutive* last-component interval) and S8-depth gives all of `act` a *common depth* (so no shorter/longer position can sit strictly inside a run's T1-interval). With both, V-start order = interval order.

**Required**: Add the one-clause justification — each run lies on a single lexicographic prefix-line as a consecutive interval (shift fixes the prefix), all at the common depth (S8-depth), so runs occupy non-interleaving T1-intervals and V-start order is interval order.

### Issue 4: Forward-reference signposts and defensive justification prose

This note carries the anti-bloat classifier; the following instances are meta-prose a reader must skip past, not reasoning that advances a claim.

- **CP0(b)/(c) downstream-consumer pointers**: "This is the seed of source isolation (CP6 below)." and "...as many distinct origins as the source content had homes (CP11 below)." These end sub-claims of a *definition* with pointers to downstream consumers rather than advancing the definition's meaning. Multiple sub-claims of one definition defer forward.

- **Resolution-basis paragraph, meta-narration + exclusion inventory**: "we fix here, once, the basis on which COPY's whole resolution and placement arithmetic stands" is document-structure narration; "...rests on S3★... and the run-decomposition... on the single-subspace premise so obtained — *not* on ASN-0058's C1 or C0a, whose stated preconditions are the full binding COPY drops, and *not* on the span's ordinal-level form, since `actionPoint(ℓ)` may fall anywhere" is a defensive use-site *exclusion* inventory (enumerating what the derivation does **not** depend on). The substantive core — content-residence gives single-subspace, S8-depth gives common depth, these two facts are all the arithmetic needs — stands on its own; the exclusion catalogue is the skippable accretion.

- **CP3c paragraph 1, defensive generality redundant with the concrete argument**: "COPY needs one wherever its other clauses fix individual bindings but leave the *extent* of some subspace's domain... underdetermined: absent an explicit closure, a model may admit spurious extra positions there, and `d`'s per-state invariants would be dischargeable only through the exhibited composite..." This general-principle/rationale paragraph says, abstractly, what the *following* paragraph then proves concretely (the S2 double-binding at `p`). The concrete paragraph is the one doing the work; the general one is the redundant defensive layer.

**Required**: Cut the forward "(CP6 below)/(CP11 below)" seeds and the "we fix here, once" / "not on C1 or C0a / not on ordinal-level form" exclusion inventory to their object-level content; fold CP3c's general-principle paragraph into one clause feeding the concrete S2 argument.

## OUT_OF_SCOPE

### The deferred open questions are correctly future territory
The C2-loss / partial-binding nominal-vs-resolved width question (OQ1), the placement-order invariant for repeated source addresses (OQ2), level-uniformity across differing source depths (OQ3), link-subspace transclusion (OQ6), and the link-undiscoverability-after-removal question (OQ4, DELETE territory) are genuinely new territory — they do not bear on any CP0–CP11 invariant as stated, and COPY's correctness does not depend on resolving them. Their deferral is appropriate; do not treat them as gaps in this ASN.

VERDICT: REVISE
