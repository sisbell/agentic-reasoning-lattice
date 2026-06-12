# Review of ASN-0129

The technical core of this note holds up under scrutiny: I verified the V-AUD lifts against D1–D3's bounds, V-IDX's vacuity argument against R-C1/S1–S3 (R's empty behavior set does make universal behavior-attachment unconstructible), PC6's converse at its one non-trivial leaf (the Observe_K normalization into a QD filter over V-TUP tests is correct, and the pattern conjunctions are finite query data), FP's footprints against the upstream definitions (including the home-wide BH4 footprint and `targets_keyed`'s cross-type read), PD0's ground against the step frames, and the full four-step trace — gate verdicts, dedup branches, C2/C3 landings (subtree(a₂) missing a₃ and a₄ by sibling non-nesting), the UV rewrite/preservation split at Σ₄, and all three value sequences from Σ₁ onward. All correct. The remaining issues are a coverage gap in PD0's classification rules, an unevaluated boundary state in the worked trace, anti-bloat patterns of the kind this note's classifier flags, and one inconsistency in the note's own conjecture bookkeeping.

## REVISE

### Issue 1: PD0's ST/SF rules omit sound atom forms and never state that the classification is spelling-level

**ASN-0129, PD0 (AuditMonotonicity)**: "The monotone classes, defined inductively with explicit polarity…" followed by the rule list (step-constants, residence, Boolean nodes, quantifiers, aggregates).

**Problem**: The audit-view membership atom `is_K(addr)` is ⊤-stable (its V-AUD definition is an existential over the grow-only `L_K` with a V-TUP body), and V-PRIM's membership test `t ∈ M_K` over the reflected audit member set is likewise ⊤-stable — but neither is classified by any PD0 rule. Their *spellings* are: `(∃ x ∈ L_K :: addr ∈ coverage_F(x))` lands in `ST` via the quantifier rule, while the extensionally equal atom does not. The same holds for the emptiness test `S = ∅` over a grow-only reflected domain (⊥-stable; classified only as `¬(∃ x ∈ S :: ⊤)`). So two extensionally equal terms receive different classifications, and PD0 nowhere says so. The dynamics intro promises "a classification of terms by their behavior along transitions," which reads as semantic; the rules are syntactic and spelling-sensitive. A protocol author who writes the natural atom form gets no verdict from the rules as stated, and nothing tells them the rewrite is the intended route.

**Required**: Either add the missing clauses (audit-view `is_K`; V-PRIM membership and emptiness over grow-only domains — each one line, each grounded by the same growth-plus-immutability argument already in PD0's proof) or state explicitly that ST/SF are spelling-level classes, with the existential spellings as the certified forms — and align the dynamics intro's "by their behavior" phrasing with whichever choice is made.

### Issue 2: The trace never evaluates Σ₀ — the empty-store boundary where the headline predicate is vacuously true

**ASN-0129, Worked composition**: "The value sequence of `quiescent(t)` at view `active` along the trace is ⊥, ⊤, ⊥, ⊥".

**Problem**: The trace has five states (Σ₀–Σ₄) but the sequences carry four values; Σ₀ is constructed (one document, empty link store) and then never evaluated. At Σ₀, `M_cmt = ∅`, so `OPEN(t) = ∅` and `quiescent(t) = ⊤` — vacuously. This is not a cosmetic omission: a fire-until-`quiescent(t)` loop observing Σ₀ terminates before any comment exists, which is precisely the trap the dynamics section exists to warn protocol authors about, and it is the one flip in the trace's reach (⊤ at Σ₀, ⊥ at Σ₁) that PD1's text does not exhibit. The standards make empty-structure boundaries mandatory; the note evaluates empty *domains* mid-trace (`M_res = ∅` at Σ₁) but skips the empty *store* for its own headline term.

**Required**: Evaluate `quiescent(t)` (and `ever_res`) at Σ₀, extend the stated sequences to five values (active: ⊤, ⊥, ⊤, ⊥, ⊥), and say in one sentence that quiescence-shaped predicates are vacuously true at the empty store — so a sound termination gate needs an activity witness alongside them.

### Issue 3: Anti-bloat — triple deferral to QD-audit, and a restated conclusion inside QD-audit

**ASN-0129, V-DOC / QD-audit / PC6 (base) / Structural reads only**: V-DOC: "Membership only: the atom consults the store domain at its argument and licenses no enumeration… Admission and restriction are both grounded at QD-audit." PC6: "a *membership* read of the arrangement-store domain — `is_doc`'s residence test, membership and nothing more, no base enumerating `dom(Σ.M)` (QD-audit…)". Structural reads only: "the arrangement domain by the residence test alone (`is_doc`, QD-audit: membership at the argument, never the binding, never the list)".

**Problem**: The membership-not-enumeration restriction on `is_doc` is stated in full at four sites, three of which also defer to QD-audit — the exact "multiple paragraphs defer to the same downstream location" accretion pattern. Separately, within QD-audit itself, the self-emit segment states its conclusion twice: "the vocabulary supplies no term spelling the test `a = a_emit(Σ, d)`: a grammar fact, read off V" is followed two sentences later by "The design conclusion needs only the grammar fact: a PL gate… has no spelling for where the surface's next emission *lands*" — the same division restated, with only the "the emitting surface performs it (S3)" clause new.

**Required**: State the restriction once in full (V-DOC is the definition site; QD-audit is the grounding) and reduce the PC6 and Structural-reads-only occurrences to bare citations of V-DOC. In QD-audit, collapse the design-conclusion sentence to the one new clause (the self-emit check belongs to the emitting surface, S3) and drop the restated half.

### Issue 4: The parity candidate is the third unproven separation claim, but the only one without a recorded proof obligation

**ASN-0129, PC6, "What the relativization costs"**: "the candidate witness that an unrestricted class strictly exceeds PL is the parity of `count(L_dom)`… so the candidate plausibly stands, unproven."

**Problem**: The note's own convention — established for C-reach and for the self-emit conjecture, both of which receive explicit conjecture status and a parked proof obligation at Open Question 6 — is not applied to the parity claim. Parity does argumentative work (it is the witness for "fold gaps are design exclusions," the vocabulary-axis half of the cost accounting, and C-reach's closing sentence leans on it standing independently of `reach`), yet it ends at "plausibly stands, unproven" with no open-question slot. Inconsistent bookkeeping for claims of the same epistemic kind.

**Required**: Record the parity non-expressibility claim as a proof obligation — either folded into Open Question 6 (it is an invariance question over the same ℕ-fragment vocabulary) or as its own entry — matching the treatment the other two conjectures received.

## OUT_OF_SCOPE

### Topic 1: Predicate dynamics in a system composed with the arrangement-layer transitions
**Why out of scope**: PD0–PD2 are proven against `→_sh` only. A deployment composing this substrate with ASN-0127's arrangement steps (K.μ⁺/K.μ⁻/K.μ~, K.δ) raises the question of whether the stability classes survive — they plausibly do, since PL's only arrangement read is `dom(Σ.M)`'s domain and no arrangement step removes a document key, but that is a composed-system result for the note that owns the layer boundary, not an error in this one.

### Topic 2: Certified gate idioms over the dynamics classes
**Why out of scope**: Patterns like conjoining an audit-class activity witness with an active-view quiescence condition (the shape Issue 2's boundary exposes) are protocol-construction machinery — the note correctly fences these in "What this note doesn't cover"; PD0–PD2 supply the typing they would be checked against.

VERDICT: REVISE
