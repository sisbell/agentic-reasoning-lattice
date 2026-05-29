# Review of ASN-0036

## REVISE

### Issue 1: Cited foundation lemmas absent from the foundation

**ASN-0036, ShiftPreservation / subspace_I / S7c / D-CTG-depth (Depends and proofs)**: repeated citations to `NAT-sub` ("left-inverse identity `#a = δ + (#a − δ)`", "right-inverse identity"), `NAT-cancel` ("injectivity of `+ p`", "strict-to-strict lift"), and `NAT-zero` ("disjunction `0 < n ∨ 0 = n`").

**Problem**: The foundation vocabulary supplies exactly five ℕ axioms — `NAT-addcompat`, `NAT-closure`, `NAT-discrete`, `NAT-order`, `NAT-wellorder`. `NAT-sub`, `NAT-cancel`, and `NAT-zero` do not appear. The load-bearing position-arithmetic steps in ShiftPreservation conclusion (iv) (`#a − δ + 1 < #a`), subspace_I postcondition (c), and the injection in D-CTG-depth all rest on these three. A reviewer cannot verify them, so these proofs currently rest on unverified lemmas.

**Required**: Either confirm these are real ASN-0034 claims and add them to the foundation extract, or rederive the steps from the five available axioms (`NAT-discrete` + `NAT-addcompat` + `NAT-order` can likely cover the strict-successor and promotion steps; subtraction identities need explicit grounding).

### Issue 2: Use-site inventories around definition promotions

**ASN-0036, subspace_I block**: "We promote it here … so that downstream uses (S7c's own postcondition (a), ShiftPreservation's conclusion (iv) below, S8's run-corollary's subspace-preservation conclusion (i), the worked example's verification …, and the Properties table entry) can cite a single definitional source."
**ASN-0036, ShiftPreservation intro**: "This lemma decouples … so that downstream uses requiring T4b's projection on a shifted I-address — S7c's Consequence (b), `subspace_I`'s Postcondition (c), the worked example's …, and S8's run-corollary — cite a single source."
**ASN-0036, subspace block**: "We promote it to a Formal Contract here so that downstream uses can cite a single definitional source … used throughout S8a, S8-depth, the correspondence-run development of S8, the contiguity properties D-CTG/D-MIN/D-CTG-depth/D-SEQ, and the homomorphism lemmas …"

**Problem**: Each enumerates its downstream consumers rather than advancing the definition's meaning — exactly the use-site-inventory pattern. The reader skips past it to reach the contract.

**Required**: Delete the consumer enumerations. A definition stands on its statement; cross-references belong at the citing site, not the definition site.

### Issue 3: Prose justifying document ordering / non-circularity

**ASN-0036, subspace_I postcondition (c)**: the entire "*Note on non-circularity:* ShiftPreservation's proofs of conclusion (ii) … and conclusion (iv) … are derived from S7b, S7c, T10a.4, T4, and TumblerAdd's prefix rule alone — neither invokes `subspace_I`'s postcondition (c) or any output of S8."
**ASN-0036, S7a Depends**: "(Note on textual order: S7b is stated *after* S7a in this ASN for expository reasons … but the conditioning is now stated explicitly in S7a's Axiom, so S7a's well-formedness does not implicitly presuppose S7b …)"

**Problem**: Both paragraphs argue about ordering/circularity of the document rather than stating mathematical content. This is meta-prose defending the revision, not reasoning the reader needs.

**Required**: Remove. If non-circularity is genuinely at risk, the dependency graph in the Depends fields already encodes it; a defensive narrative is not needed.

### Issue 4: Depends fields duplicate proof-body arithmetic verbatim

**ASN-0036, ShiftPreservation Depends**: "NAT-addcompat … left and right order compatibility for the chain `1 + 1 ≤ a_{#a} + 1 ≤ a_{#a} + k`, strict successor clause `n < n + 1` instantiated at `n = 1` for `1 < 2`, and left order compatibility at `(#a − δ, δ, 1)` lifting `1 < δ` …"

**Problem**: This restates, step for step, the chain already carried out in conclusions (i) and (iv) of the proof body. The same is true of S7c Consequence (b)/(c) Depends and subspace_I Depends. Essay content in a structural slot, and two passages saying the same thing.

**Required**: Depends fields should name the cited claim and its role in one clause each ("NAT-addcompat — order-compatibility for the length chain"), not re-execute the derivation.

### Issue 5: Multiple paragraphs deferring to the same downstream location

**ASN-0036**: S7c Consequence (b) ("established in full by **ShiftPreservation** conclusion (iv) below"), subspace_I postcondition (c) ("This is **ShiftPreservation** conclusion (iv) below"), and S8's run-corollary ("apply ShiftPreservation … pointwise") all defer the identical subspace-preservation fact to ShiftPreservation, each with its own framing paragraph.

**Problem**: Three sections point at one downstream lemma for the same fact — the compounding deferral pattern. The reader bounces between four locations to assemble one argument.

**Required**: State the fact once at ShiftPreservation; at the three citing sites use a bare one-line citation with no re-explanation of why ShiftPreservation is "the single canonical source."

### Issue 6: Reindexing bookkeeping in the S8 corollary

**ASN-0036, S8 corollary proof**: "(The reindexing from ShiftPreservation's (i, ii, iii, iv) to this corollary's (ii, T4-validity intermediate, iii, i) reflects this corollary's traditional S8 ordering — subspace identifier first.) Conclusion (ii) of this corollary corresponds to ShiftPreservation's (i); conclusion (iii) to ShiftPreservation's (iii); conclusion (i) to ShiftPreservation's (iv)."

**Problem**: Pure index-correspondence bookkeeping that advances no reasoning. If the conclusions are renumbered, just state them in the chosen order and cite.

**Required**: Delete; renumber inline.

### Issue 7: S5 Frame is a defensive scope essay

**ASN-0036, S5 Frame**: "… the I-address `a` is treated abstractly (no tumbler structure assigned to it), so S7b (`zeros(a) = 3`) and S7c (`#E(a) ≥ 2`) are not established for `a` … The V-position patterns … incidentally satisfy S8a, D-MIN, D-CTG, and D-SEQ — these are unforced strengthenings noted in the body — but the witnesses are not claimed to be full strand-model states."

**Problem**: A long paragraph cataloguing what the proof does *not* establish and which incidental properties the witnesses happen to satisfy. This is defensive justification, not part of the existence argument.

**Required**: Reduce to a single sentence: "S5 ranges over S0–S3 only; the witnesses are not claimed to satisfy later invariants."

### Issue 8: Duplicated caveat text in S8 Depends

**ASN-0036, S8 Depends (S7b and S7c entries)**: both read "required only by ShiftPreservation, which the run-corollary cites pointwise at `k ≥ 1`; vacuous on the singleton witness exhibited in the existence proof (where only `k = 0` arises and the shift is the identity)" — near-verbatim twice.

**Problem**: Two paragraphs saying the same thing in different (here, identical) words.

**Required**: Collapse to one entry covering S7b and S7c jointly.

### Issue 9: Self-referential consultation citation

**ASN-0036, S3 Axiom**: "Nelson confirms (consultation answer ASN-0036): 'Every V-reference should resolve …'"

**Problem**: An ASN citing a consultation tagged with its own number reads as a cross-reference and is not a foundation citation. At minimum it is unclear whether this is quotable architectural intent or a procedural artifact.

**Required**: Quote Nelson's source directly (LM reference) without the "consultation answer ASN-0036" tag, or drop the parenthetical.

## OUT_OF_SCOPE

### Topic 1: Operation preservation of D-CTG / D-MIN / S2 / subspace alignment
**Why out of scope**: Whether DELETE/INSERT/COPY/REARRANGE preserve contiguity and subspace alignment is correctly deferred to each operation's ASN and listed in Open Questions. The strand model states the invariants and the base case (empty arrangement); operation frame conditions are new territory.

### Topic 2: Subtraction homomorphism and round-trip for ordinals
**Why out of scope**: `ord(v ⊖ w) = ord(v) ⊖ w_ord` and the round-trip conditions are flagged in Open Questions; they require TA7a's conditional subtraction results and belong in a follow-on note, not this one.

VERDICT: REVISE
