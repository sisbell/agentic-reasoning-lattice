# Review of ASN-0100

This is a careful, largely sound specification. The forward verification, the worked examples, the wp analysis, and the per-state/boundary atomicity split are all substantive. My findings are mostly accretion the anti-bloat classifier flags, plus one precondition-discharge that is asserted rather than shown.

## REVISE

### Issue 1: K.μ⁻ strict-contraction precondition is asserted, not discharged
**ASN-0100, §Atomicity**: "The decomposition is admissible under ValidComposite★ because (i) every elementary transition's per-step precondition is met at its intermediate state."
**Problem**: K.μ⁻'s elementary precondition (PerSubspaceContractionScope, ASN-0047) requires *at least one S with strict contraction* `n'_S < n_S`. The decomposition fixes `n'_{s_C} = p_m − 1`, `n'_{s_L} = n_{s_L}`. The strict-contraction obligation reduces to `p_m − 1 < N`, i.e. `p_m ≤ N` — which is exactly `Right ≠ ∅` from (INS.μ⁻-fires), the firing condition. The blanket "(i)" sentence never makes this one-step connection, even though the ASN spells out far smaller steps elsewhere. The hardest-to-check precondition of the contraction step is the one left implicit.
**Required**: Add an explicit line: K.μ⁻ fires only when `Right ≠ ∅` (INS.μ⁻-fires), which gives `p_m ≤ N = n_{s_C}`, hence `n'_{s_C} = p_m − 1 < n_{s_C}`, discharging the strict-contraction precondition; `n'_{s_L} = n_{s_L}` contracts nothing and needs no discharge.

### Issue 2: Repeated forward deferral to the same downstream section
**ASN-0100, §Effect Two**: "is verified once in §Post-state V-position well-formedness below."
**ASN-0100, §Sequential text-subspace structure (empty case)**: "S8a: each Insertion position satisfies S8a, verified once in §Post-state V-position well-formedness."
**Problem**: Two paragraphs in different sections defer the S8a/depth check on `shift(p,k)` to the same downstream location — the "multiple paragraphs defer to the same place" accretion pattern. The reader must hold an open obligation across several sections. The first deferral also carries the defensive phrasing "is verified once" — meta-prose about the proof's own bookkeeping rather than content.
**Required**: Prove S8a/depth for `shift(p,k)` at first need (it is a two-line OrdAddHom + result-length argument) and have later sections cite the established claim, or move the single proof earlier and remove the duplicate forward pointers.

### Issue 3: Anticipatory block-algebra bridge misplaced in Effect One
**ASN-0100, §Effect One (after the INS.chain-shift induction)**: "Consequently the Insertion region {(shift(p, k), a_k) …} coincides with {(shift(p, k), shift(a_0, k)) …}, which is exactly the denotation ⟦(p, a_0, n)⟧ of the mapping block (p, a_0, n) under OrdinalShiftBase (ASN-0058) — there the run's I-address a_0 + k reads as shift(a_0, k)."
**Problem**: This is S8★ content — the single-run merge of the Insertion block — surfaced inside the *allocation* sub-section. The actual merge (M7 V-/I-adjacency) is performed later in §Per-subspace span decomposition. Placing the denotational bridge here makes Effect One do double duty as a preview of the block-algebra section, the forward-reference accretion the classifier names.
**Required**: Keep INS.chain-shift's algebraic conclusion (`a_k = shift(a_0, k)`) in Effect One; relocate the "coincides with ⟦(p, a_0, n)⟧" sentence to §Per-subspace span decomposition where the merge is established.

### Issue 4: Redundant restatement in the re-insertion example
**ASN-0100, §Empty-document re-insertion after full clearance**: closing sentence "That I-side distinction is the sub-case's entire content: K.α keys on dom(C), so the non-empty residual {a_prev} routes it into the subsequent-emission branch, continuing A_C(d) past the persisted frontier rather than restarting at a first emission."
**Problem**: This restates step 1 of the same example ("K.α keys its branch on dom(C) … fires the subsequent-emission branch … continuing A_C(d)'s inc(·,0) chain past the persisted frontier") in different words — the "two paragraphs say the same thing" pattern, here within one example.
**Required**: Delete the closing restatement; step 1 already carries the distinction.

## OUT_OF_SCOPE

### Topic 1: Link-subspace insertion, COPY, DELETE/REARRANGE, version derivation, replication
**Why out of scope**: The ASN bounds these explicitly in §Bounding the Scope and the Open Questions, consistent with the declared scope. No action needed; the boundary is drawn correctly.

### Topic 2: Self-composition closure and concurrent same-position INSERTs
**Why out of scope**: Raised as Open Questions; these concern an algebra of operations and a concurrency model that postdate the single-operation per-state contract this ASN fixes.

VERDICT: REVISE
