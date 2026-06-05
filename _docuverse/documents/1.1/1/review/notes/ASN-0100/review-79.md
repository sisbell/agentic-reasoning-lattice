# Review of ASN-0100

## REVISE

### Issue 1: Empty worked example conflates empty arrangement with empty allocation history
**ASN-0100, §A Worked Example, "Empty-document first insertion"**: "a_{new0} = [d.0.s_C.1] (first-emission predicate fires since {a' ∈ dom(Σ.C) : origin(a') = d} = ∅)."
**Problem**: The stated setup stipulates only `V_{s_C}(d) = ∅` and `V_{s_L}(d) = ∅` — an empty *arrangement*. But K.α's first-emission predicate (ASN-0093) is gated on `{a' ∈ dom(C) : origin(a') = d} = ∅` — empty *allocation history*. These are independent: by S0/P0 content persists in `dom(C)` even after it is removed from the arrangement, so a document with an empty content arrangement may still carry prior d-origin addresses in `dom(C)`, in which case the **subsequent**-emission branch fires and `a_{new0} = inc(a_prev, 0) ≠ [d.0.s_C.1]`. The parenthetical "since {a' ∈ dom(Σ.C) : origin(a') = d} = ∅" is asserted as if it followed from the empty-arrangement setup; it does not. (The non-empty example is careful here — it explicitly stipulates `a₁,…,a₅` are "the first five" emissions — making the omission in the empty case conspicuous.)
**Required**: Either add an explicit stipulation that no content was ever allocated under `d` (`{a' ∈ dom(Σ.C) : origin(a') = d} = ∅`), or note that the first-emission address values depend on allocation history, not arrangement emptiness, and that the post-state invariants hold for whatever fresh `a_k` the branch produces.

### Issue 2: L0 content-clause argument duplicated verbatim across two sections
**ASN-0100, §Link store unchanged** and **§Atomicity and Canonical Order, Link-store bullet**: Both paragraphs discharge L0's second conjunct (`a ∈ dom(C) ⟹ subspace_I(a) = s_C`) by the identical move — "for each freshly allocated/emitted `a_k`, `subspace_I(a_k) = s_C` by DisjointSubAllocatorChains (ASN-0093); pre-existing entries inherit from the pre-state."
**Problem**: Two paragraphs in different sections state the same argument. The reader checking L0 encounters it twice with no added content the second time.
**Required**: State the L0-content discharge once and have the other site cite it.

### Issue 3: Hub-and-spoke deferral to §Atomicity for the fresh-address discharge
**ASN-0100, §Post-state V-position well-formedness (S7 invariants), §P6, and §Atomicity**: Multiple sections defer the same obligation downstream — "discharge S7a, S7b, C1b, and C1c once in §Atomicity"; "discharge P6 once in §Atomicity"; with §Atomicity then announcing "this is the single discharge of each (the other invariant sections cite it rather than re-prove it)."
**Problem**: This is meta-coordination prose about *where* a discharge lives, distributed across three sites, that the precise reader must thread together. The repeated "discharge … once in §Atomicity" markers advance no reasoning; they manage document layout.
**Required**: Discharge the fresh-`a_k` per-address invariants in one place and let each invariant section's normal flow reach it without the bookkeeping refrain.

### Issue 4: C1a precondition discharge repeated near-verbatim
**ASN-0100, §Per-subspace span decomposition (S8★)** and **§Atomicity, post-K.μ⁻ bullet**: The three C1a (RestrictionDecomposition) preconditions are discharged twice with the same phrasing — "functionality from S2, finiteness from S8-fin, single-subspace induced domain of common depth `m_C` from S8-depth."
**Problem**: While the two states differ (final vs. intermediate), the precondition-discharge text is duplicated rather than parameterized, adding length without distinguishing content.
**Required**: Factor the C1a-precondition discharge into one statement applicable to any single-subspace restriction satisfying S2/S8-fin/S8-depth, and instantiate it at each site by reference.

## OUT_OF_SCOPE

### Topic 1: First/subsequent emission semantics under prior deletion
**Why out of scope**: The precise interaction of INSERT's allocation branch with a document whose content was previously DELETEd is a consequence of DELETE's semantics (out of scope per the scope list). Issue 1 only requires the *example* be made accurate; the general allocation-after-deletion behavior belongs to a DELETE/composition ASN.

META: Not applicable — the ASN defines an operation's abstract state effect, allocation footprint, and invariant preservation, which is squarely specification territory; the implementation references (the "knife") are brief and tied to abstract properties.

VERDICT: REVISE
