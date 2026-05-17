# Review of ASN-0047

## REVISE

### Issue 1: Cross-document disjointness lemma Case B mixes load-bearing structural lifting with T10a-allocator case enumeration

**ASN-0047, Allocator hierarchy under documents (Cross-document disjointness chain lemma)**: The Case B proof has two layers — a structural lifting from document-level prefix-incomparability to anchor-level prefix-incomparability, and an enumeration of configurations (i)/(ii)/(iii) under T10a-allocator trichotomy. The Coverage paragraph asserts "every prefix-incomparable pair falls into at least one of (i)–(iii)" by appeal to S7d.

**Problem**: This ASN's K.δ k = 1 ghost-base relaxation admits documents whose producing event isn't T10a-allocator-tracked (the operand `t` need not be in E_doc, A_v(t) isn't activated). Such documents may produce pairs that fall outside the (i)/(ii)/(iii) enumeration as stated, which appeals to S7d's "T10a-conforming allocation event" — a foundation invariant that the ghost-base extension explicitly stretches. The lemma's *conclusion* may still hold via the structural lifting alone (the Case B hypothesis `d₁ ⋠ d₂ ∧ d₂ ⋠ d₁` suffices for the suffix-extension argument), but the proof's presentation makes the enumeration appear load-bearing.

**Required**: Either explicitly mark the enumeration as motivational and rely on the structural lifting alone for the proof, or extend the enumeration to cover ghost-base × live and ghost-base × ghost-base configurations.

### Issue 2: S8 unqualified in ExtendedReachableStateInvariants but qualified in the discharge lemma

**ASN-0047, Extended reachable-state invariants**: The per-state theorem lists `... S8a ∧ S8-fin ∧ S8-depth ∧ S8 ∧ D-CTG★ ...` without qualification on S8.

**Problem**: The S8 discharge lemma in the proof body explicitly argues that ASN-0036's S8 cannot be applied to the unprojected `dom(M(d))` once link-subspace V-positions exist (they target dom(L), violating unprojected S3). The lemma decomposes S8 at Σ' per-subspace: content-subspace via ASN-0036's S8 over the projection `M(d')|_{V_{s_C}(d')}`, link-subspace via D-SEQ★(s_L). The bare "S8" in the invariant list therefore overstates what holds at the post-state.

**Required**: Replace bare "S8" with "S8 (over the content-subspace projection)" or equivalent, or fold the per-subspace decomposition into the invariant's statement.

### Issue 3: Broken forward reference to "Other admissible decompositions"

**ASN-0047, Decomposition of K.μ~ (Case 2)**: "Other admissible decompositions may exist for particular π shapes (see *Other admissible decompositions* below)".

**Problem**: No section header by that name exists in the ASN.

**Required**: Either add the referenced section or remove the parenthetical.

### Issue 4: K.δ ghost-base freshness — cross-allocator distinctness handled implicitly

**ASN-0047, K.δ table k = 1 ghost-base row**: Discharge path "Path 2 (K.δ precondition + TA5 determinism at the tumbler layer)".

**Problem**: TA5 determinism fixes the candidate as `inc(t, 1) = t.1`. K.δ's `e ∉ E` precondition checks this candidate against E. But the worked example's prose says freshness is "verified by inspection of E₇" — this is operationally how the check fires, but the ASN doesn't explicitly state why this inspection-based check is sufficient *without* T10a's allocator-level uniqueness. Specifically, what guarantees that some other (non-T10a-tracked) entity allocator hasn't independently emitted t.1 into E in the meantime? Sequential single-event model is implicit; concurrent or multi-protocol scenarios aren't addressed.

**Required**: Add one sentence noting that single-event sequential semantics underwrites the inspection-based discharge, or defer concurrent-allocation handling explicitly to an open question.

### Issue 5: Definition introductions enumerate downstream consumers (meta-prose accretion)

**ASN-0047, D-SEQ★ derivation**: "D-SEQ★ is the per-state invariant referenced by K.μ⁻'s precondition clause (A) ... and re-established in full detail here ... Downstream sections (K.μ⁻ admissibility, the K.μ~-FIX domain-fixity argument, the link-subspace fixity proof, and the ExtendedReachableStateInvariants induction) appeal to D-SEQ★ by name at each state where its premises hold."

**Problem**: This enumerates four downstream consumers rather than advancing D-SEQ★'s meaning. The pattern of inventorying use-sites at definition time recurs at SubAllocatorAxiom ("downstream of each sub-allocator's first emission..."), at CL-UNIQ ("CL-UNIQ is what lets K.μ~'s link-subspace identity property be derived..."), and elsewhere.

**Required**: Remove the use-site inventories. Downstream sections cite back when they appeal to the definition; the forward direction inflates the definition without adding content.

### Issue 6: Document-ordering justification prose

**ASN-0047, Elementary transitions (K.μ~ deferral)**: "The decomposition account ... is deferred to the dedicated *Decomposition of K.μ~* section below, placed after the per-state invariants S3★-aux ... CL-UNIQ ... on which it depends. This presentation order avoids forward references."

**Problem**: The reader can see the deferral by reading the section pointer; commentary about *why* the placement order works is meta-prose that doesn't advance the argument.

**Required**: Trim to "The decomposition account is in §Decomposition of K.μ~ below."

### Issue 7: SubAllocatorAxiom — axiom prose explains why rather than what

**ASN-0047, Allocator hierarchy under documents (SubAllocatorAxiom + Reconciliation)**: The axiom itself is three labeled clauses (Exists, Disjoint, Namespace), each concise. But the surrounding prose ("Reconciliation with ASN-0043's L1c", "What the inc derivations do *not* supply", the dispatch table) spends ~30 lines justifying why the axiom is *needed* (T10a's at-most-once constraint, L1c's structural-existential gap, etc.) before stating the operational claim.

**Problem**: The "why is the axiom needed" rationale belongs in a design note, not in the spec itself. The axiom's content is clear; the surrounding apparatus inflates it.

**Required**: Compress the rationale to one sentence (e.g., "T10a's at-most-once spawning constraint prevents deriving sub-allocator existence operationally, so we admit it as an axiom") and remove the multi-paragraph reconciliation walk-through.

### Issue 8: Worked example notation switching adds reading overhead

**ASN-0047, Worked example: fork with subsequent insertion**: Each verification line uses the starred form (P5★, J1★) and then immediately annotates "(Reduces to P5 at this state since L is empty)" or similar.

**Problem**: Stating the starred form and parenthetically reducing it twenty times across the example doesn't add information after the first occurrence; the example would read more cleanly if the section preamble made the reduction once.

**Required**: State the four-component reduction once in the example preamble (already partly done) and drop the per-line reduction annotations.

## OUT_OF_SCOPE

### Topic 1: Concurrent-event semantics

The ASN's transition model is implicitly sequential (one composite at a time, sequential composition). The discharge of K.δ freshness via "inspection of E" assumes single-event semantics. Concurrent allocation is correctly deferred to an open question.

**Why out of scope**: This ASN classifies elementary state transitions; concurrent semantics belongs in a separate ASN.

### Topic 2: Tombstone-style link withdrawal mechanism

The named gap under *Structural sufficiency and known gaps* — Nelson's "not currently addressable" link status (LM 4/9) — is correctly flagged as requiring a state-model extension beyond the present five-component state.

**Why out of scope**: The mechanism (status flag, tombstone marker, retraction-link convention) would be a state-model extension; this ASN admits the gap.

### Topic 3: Cross-version content correspondence

The ghost-base versioning example produces e₁ as a version of t, but the ASN explicitly defers "the richer version contract (arrangement invariants between successive versions, content-allocator linkage, provenance flow, lineage acyclicity)" to a subsequent version-management ASN.

**Why out of scope**: Version-lineage semantics is its own topic.

META: The ASN defines state, operations on state, and invariants of state at the appropriate abstraction; it has not drifted into implementation territory.

VERDICT: REVISE
