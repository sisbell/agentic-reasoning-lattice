# Review of ASN-0036

## REVISE

### Issue 1: The "k = 0 trivial / k ≥ 1 only load-bearing for nⱼ ≥ 2" message is restated six times across S8

**ASN-0036, Span decomposition (S8 existence proof, corollary, non-canonicality remark, and all three Formal Contract slots)**: the same observation — that the singleton witness exercises `shift` only at `k = 0` (identity), so S7b/S7c/ShiftPreservation become load-bearing only for coarser decompositions — appears in:
1. the existence argument ("No structural facts about `a` beyond its existence are invoked…");
2. the corollary preamble ("This is not part of the existence argument…");
3. the *Non-canonicality* remark;
4. the Formal Contract *Preconditions* ("Neither S7b nor S7c is a precondition of the existence claim…");
5. the *Postconditions* (restated again);
6. the *Depends* block (restated a third time).

**Problem**: This is reviser-drift accretion — one true claim padded across six slots. A reader tracking S8 must repeatedly skip identical hedging to follow the actual decomposition argument.
**Required**: State the singleton/coarser distinction once (in the proof body), and let the contract slots cite dependencies without re-litigating which `k` exercises them.

### Issue 2: Verbatim "S0 discharges the persistence step" sentence repeated in five Depends blocks

**ASN-0036, S7a / S7b / S7c / subspace_I / ShiftPreservation (*Depends*)**: the clause "S0 (content immutability) — discharges the persistence step that connects `a ∈ dom(Σ.C)` in the current state to the T10a allocation event under which T10a.4 originally established T4-validity (the tumbler is identity-fixed thereafter)" is reproduced near-verbatim five times.
**Problem**: Two-plus paragraphs saying the same thing in the same words. The persistence-bridging argument is identical in every case; restating the full multi-clause sentence is noise.
**Required**: Establish the S0-persistence bridge once (it is a generic fact about every `a ∈ dom(Σ.C)`), then cite it by name.

### Issue 3: Text-subspace-only / link-subspace-deferred caveat repeated across the contiguity section

**ASN-0036, Arrangement contiguity (section intro, S8a Remark, D-CTG Frame, D-MIN Frame)**: "this is the text subspace `S = 1`; the link subspace `S = 2` is sparse, append-only with tombstones, deferred to a future ASN" appears at least four times, and the subspace-alignment *Remark* after S8a is a further deferral essay whose content is also posed as an Open Question.
**Problem**: Multiple paragraphs defer to the same downstream location — the flagged "see X below / deferred to Y" accretion pattern. The link-subspace exemption needs to be stated once for the whole section.
**Required**: Bind the text-subspace restriction once at the section head; drop the per-property restatements and collapse the alignment Remark into the single Open Question that already covers it.

### Issue 4: S7c forward-reference essay explains its placement rather than advancing S7

**ASN-0036, paragraph preceding S7**: "(S7c, stated here for architectural completeness, is load-bearing for S8's correspondence run definition in the non-singleton case (nⱼ ≥ 2)… S7c is not load-bearing for S7 itself.)"
**Problem**: This is a use-site inventory — meta-prose justifying why S7c sits where it does and enumerating its downstream consumers. It advances neither S7c's meaning nor S7's proof.
**Required**: Remove the placement justification; S7c's role in S8 belongs in S8's Depends (where it already is).

### Issue 5: S8a is labeled "axiom" but carries a multi-conjunct derivation — which conjuncts are axiomatic is ambiguous

**ASN-0036, S8a**: the *Axiom* line states only "V-positions are element-field tumblers of depth at least 2," yet the Postconditions assert the full predicate `zeros(v) = 0 ∧ #v ≥ 2 ∧ (A i : vᵢ > 0)`, and a *Proof* then derives `zeros(v) = 0` and positivity from the structural premise. The positivity conjunct is further annotated as "explicitly stated… structurally it is entailed."
**Problem**: A reader cannot tell whether `zeros(v) = 0` is posited or proved, and the "stated-but-entailed" note is prose explaining a design choice rather than establishing a property. An axiom should not need a proof body.
**Required**: Either present S8a as a definition (V-positions are element fields) with `zeros = 0`/positivity as derived postconditions, or as an axiom with the conjuncts posited — not both. Drop the redundancy justification for the positivity conjunct.

## OUT_OF_SCOPE

### Topic 1: Link-subspace (S = 2) contiguity and tombstone semantics
**Why out of scope**: The note correctly defers sparse/append-only link-position structure to a future ASN; this is new territory, not a defect here. (Flag the *repetition* of the deferral per Issue 3, not the deferral itself.)

### Topic 2: Operation-level preservation of D-CTG/D-MIN/S2 and subspace alignment
**Why out of scope**: Whether INSERT/DELETE/COPY/REARRANGE preserve the contiguity invariants and `subspace(v) = subspace_I(M(d)(v))` is explicitly an operations-layer obligation; the strand model bounds the two sides independently, which is the correct division.

VERDICT: REVISE
