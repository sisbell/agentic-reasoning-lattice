# Review of ASN-0093

## REVISE

### Issue 1: Intro overstates the factoring as a single notational substitution
**ASN-0093, Intro**: "every operation and invariant here is identical to its counterpart in the fuller model except for one notational substitution — `E_doc` ... is replaced by `dom(M)`."
**Problem**: The ASN's own later text contradicts this. C1b states "ASN-0036 carries no content-side `#E(a) ≥ 2` invariant, so this is added here as a substrate-level commitment"; L0's C-clause is "added here"; C1c is a newly stated content-side analog. These are added commitments, not the `E_doc → dom(M)` rewrite. A reader takes the intro's "identical except for one substitution" as license to inherit ASN-0043/0036 proofs wholesale, which is false for the added C-side invariants.
**Required**: Qualify the framing to acknowledge the substrate adds content-side invariants (C1b, L0-C, C1c) beyond the `E_doc → dom(M)` substitution.

### Issue 2: ChainDiscipline "not an independent posit" stated four times
**ASN-0093, Scope bullet / "Sub-allocator chains are ASN-0040 sibling streams" / Lemma (ChainDiscipline) / Properties table**: the claim that the chains coincide with `S(b_·(d),1)` "forced by the K.α/K.λ emission rules ... not posited" appears in the Scope intro ("Derived chain identity"), in the sibling-streams paragraph, in the Lemma body ("This is not an independent posit"), and again in the Properties table row.
**Problem**: Two-plus paragraphs saying the same thing in different words. The defensive "not an independent posit" framing is itself a residue of a prior cycle's demotion (the SubAllocatorAxiom→lemma change); it explains *why the lemma is a lemma* rather than advancing the argument.
**Required**: State the coincidence once (the Lemma), drop the repeated "not a posit" assertions in the Scope bullet and table.

### Issue 3: L14 body carries forward-reference meta-prose
**ASN-0093, L14**: "StoreT4Validity is required to discharge T7's T4-validity precondition for the compared pair ...; it is a transition-indexed lemma derived later in this note (from ChainMembershipForOrigin + ChainElementT4Validity), and the simultaneous-induction discipline underwrites its availability at every reachable Σ where L14 is consumed."
**Problem**: This is forward-reference accretion — it narrates where StoreT4Validity is derived and why it's available, rather than stating L14. The derivation belongs in the discharge matrix (where it already appears).
**Required**: Reduce the invariant body to the L0+SC-NEQ+T7 statement; let the discharge matrix carry the StoreT4Validity dependency.

### Issue 4: SubspaceConventionAxiom enumerates downstream consumers
**ASN-0093, SubspaceConventionAxiom**: "SC-NEQ underwrites L14 (StoreDisjointness) and the L0 partition; the sibling relation underwrites the L1c chain exhibition's step `inc(b_C(d), 0) = b_L(d)`."
**Problem**: A definition/axiom introduction enumerating its use-sites — exactly the "this is consumed by X, Y, Z" pattern flagged for this note. It does not advance what the axiom *says* (`s_C = 1 ∧ s_L = 2`).
**Required**: Drop the use-site inventory; the consuming sites already cite SC-NEQ where they need it.

### Issue 5: ChainPrefixExtension "Quantifier scope" point duplicated
**ASN-0093, ChainPrefixExtension ("Quantifier scope") and Worked Example Step 8**: The note that S1 "ranges over the abstract stream ... independent of which elements are committed ... in particular the prefix relation holds at a freshly emitted stream element ... before it is committed" is restated in Step 8 ("conceptual-chain quantifier scope covers `ℓ_new` directly, since `ℓ_new ∈ A_L(d)` as a conceptual chain element regardless of whether `ℓ_new` is yet committed").
**Problem**: Same justification appearing twice. The worked example re-derives the lemma's own caveat inline.
**Required**: Keep the "Quantifier scope" clause at the lemma; in Step 8 cite ChainPrefixExtension without re-explaining its quantifier range.

### Issue 6: FirstEmissionFreshness opens with a proof-structure essay
**ASN-0093, FirstEmissionFreshness proof**: the first paragraph ("The content and link cases follow parallel structure with one substitution rule: ... The substitution rule carries this caveat across both cases.") describes how the two cases mirror each other before any case is proved.
**Problem**: Meta-prose about the shape of the proof rather than the proof. The circularity caveat (reading the new key's subspace from FirstEmission's structural form, not L0 at Σ') is load-bearing and should sit at the step that uses it, not in a preamble.
**Required**: Delete the substitution-rule preamble; fold the non-circularity caveat into the cross-subspace sub-proof where it is actually applied.

### Issue 7: Parameter-semantics tail drifts to implementation essay
**ASN-0093, Substrate primitive operations, "Parameter semantics"**: "A caller is expected to compute the address ... Implementations may treat the address as an output computed from `(d, Σ)` rather than as a free input; the substrate's semantics is unchanged in either reading because the pinning is total."
**Problem**: The substantive content — preconditions deterministically pin `a`/`ℓ` from `(d, Σ)` — is legitimate and belongs. The trailing sentences about caller expectations and implementation readings are implementation-mechanics prose that adds no spec-level guarantee.
**Required**: Keep the pinning statement; drop the caller/implementation commentary.

### Issue 8: Open-Questions link-withdrawal entry is an over-long out-of-scope essay
**ASN-0093, Open Questions, "Link withdrawal"**: three labeled paths (a/b/c) with udanax-green implementation detail ("`DELETEVSPAN` on the link's V-position ... the spanfilade entries persist ... discoverable via `find_links` and followable via `follow_link`").
**Problem**: Tombstoning is declared OUT OF SCOPE for this note, yet the entry develops a multi-paragraph implementation-grounded design analysis of three composition paths. This is essay content disproportionate to an open-question pointer and reaches into implementation mechanics the substrate explicitly defers.
**Required**: Compress to a one-to-two sentence pointer that withdrawal is deferred and that L12's value-equality clause is the load-bearing constraint a future ASN must revisit; move the path analysis to the future tombstoning ASN.

## OUT_OF_SCOPE

### Topic 1: Arrangement-mutation invariants (S2, S3, S8a, S8-depth, D-CTG, D-MIN)
**Why out of scope**: The substrate correctly holds these vacuous (`M(d) = ∅`) and defers the K.μ family; no error here.

### Topic 2: Document-address baptism discipline at K.σ
**Why out of scope**: K.σ's structural-only precondition admitting non-baptized `zeros = 2` tumblers is a deliberate substrate weakening, properly deferred to a higher-layer entity-hierarchy ASN.

META: The ASN defines abstract state, three allocation operations, and the invariants they preserve — it remains in specification territory; the findings are prose accretion, not drift.

VERDICT: REVISE
