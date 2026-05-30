# Review of ASN-0043

## REVISE

### Issue 1: Downstream-consumer enumeration in L1c

**ASN-0043, L1c (LinkAllocatorConformance)**: "The one fact not already recorded in the chain above is where the field separator lands: the first step seats the field-separating zero at position `#s + 1`, between the document prefix and the element field — the structure that CPP and the postcondition below consume."

**Problem**: The trailing clause "the structure that CPP and the postcondition below consume" is a use-site inventory naming downstream consumers rather than advancing the claim. It is exactly the forward-reference-accretion pattern flagged for this note. The locating fact (separator at `#s + 1`) is what matters; who later reads it does not.

**Required**: Drop the consumer enumeration. State where the separator lands and stop.

### Issue 2: Load-bearing meta-prose in the L9 witness

**ASN-0043, L9 (TypeGhostPermission), "Selection of `d'`"**: "Only `zeros(d') = 2` and T4-validity are load-bearing for the steps that follow; `d'`'s concrete value depends on which document of `Σ` is reused."

**Problem**: This sentence narrates which hypotheses the proof will lean on instead of doing proof work. The subsequent steps already invoke `zeros(d') = 2` and T4-validity where needed; the meta-commentary is noise the reader must skip past.

**Required**: Remove the sentence. If a step needs `zeros(d') = 2`, cite it at that step.

### Issue 3: Why-needed prose plus Open-Question deferral in L14a

**ASN-0043, L14a (NonTranscludability)**: "The `s_C`-residence hypothesis is load-bearing: without it, S3 alone places the image only in `dom(Σ.C)`, and subspace separation does not exclude a non-`s_C`-resident content address from `dom(Σ.L)`. The first Open Question records the ASN-0036 strengthening that would lift this hypothesis."

**Problem**: Two flagged patterns in one passage: (i) prose that explains *why the hypothesis is needed* rather than stating the invariant, and (ii) a deferral to a downstream location (the Open Question). The Open Questions section already carries the scope note; restating it here is duplication.

**Required**: Keep the discharge (S3 + L0 + L0a). Delete the counterfactual "without it…" sentence and the Open-Question pointer; the Open Question stands on its own.

### Issue 4: FSP mislabels a transition invariant; L11b's appeal to it is incoherent

**ASN-0043, FSP (FreshSiblingConformance) statement and L11b**: FSP claims `Σ'` "satisfies every state-local L-invariant (L0, L1, L1a, L1b, L1c, L3, L5, L6, L11a, **L12**, L14, L14a, L-fin)", and supplies an L12 bullet. L11b then states: "the non-state-local items enumerated at FSP, together with the transition corollary L12a (from L12), hold by their own proofs."

**Problem**: L12 (LinkImmutability) is a *transition* invariant — the worked example itself says "L12 constrains state transitions, not individual states … vacuously satisfied" for a single state. FSP therefore cannot consistently file L12 under "state-local invariants." Worse, L11b refers to "the non-state-local items enumerated at FSP," but FSP enumerates no non-state-local items — that reference is dangling. And "hold by their own proofs" is a checkmark-grade hand-wave: which proofs, for L12 / L12a / L12b across the specific `Σ → Σ'` transition?

**Required**: Decide explicitly what FSP covers. Either (a) FSP establishes the `Σ → Σ'` transition invariants L12/L12a (then say so and have L11b cite that directly, dropping the "non-state-local items" phrase), or (b) FSP is purely state-local and L12/L12a are discharged in each call site with a one-line "only `a`/`a'` is added, existing entries unchanged." Remove "hold by their own proofs."

### Issue 5: Duplicate statement of the arity-2 exclusion

**ASN-0043, "The Endset Structure" and L3**: The Endset Structure section already states "the conforming link store admits only `N ≥ 3` with a non-empty type endset, and we tighten L3 accordingly below." L3's body then repeats: "Arity-2 'untyped' links are not part of the design — where Gregory's implementation can store such links via empty-type-specset short-circuit, the resulting state lies outside this ASN's conforming link store."

**Problem**: Two paragraphs in different sections make the same claim (arity-2 excluded; Gregory's empty-type short-circuit lies outside the conforming store) in different words — a flagged duplication pattern.

**Required**: State the exclusion once, at L3 (where it is formalized). Reduce the Endset Structure mention to the design motivation without re-asserting the conformance verdict.

### Issue 6: L1b prose explains the rationale rather than the invariant

**ASN-0043, L1b (LinkElementFieldDepth)**: "Depth ≥ 2 keeps `subspace_I(a) = E(a)₁` stable under `inc(·, 0)`: with the subspace identifier in a non-terminal position, sibling allocation advances the rightmost ordinal and leaves the subspace component fixed."

**Problem**: This is "why the axiom is needed" prose attached to an INV. It justifies the depth bound by appeal to a later operational use (`inc(·,0)` stability) rather than stating what the invariant asserts. The stability fact is genuinely consumed only in L9/L11b, where it is re-argued anyway.

**Required**: Either delete the rationale sentence (the invariant `#E(a) ≥ 2` stands alone), or move the stability observation to the single site that uses it.

## OUT_OF_SCOPE

None. The ASN's scope boundaries (operations, resolution, indexing, deletion model) are correctly parked in the Scope section and Open Questions; no in-body claim strays into them.

VERDICT: REVISE
