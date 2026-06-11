# Review of ASN-0120

The mathematics of this ASN is sound — I checked the confinement argument (T5 prefix transfer), the recovery equation and its extensional form (LP-Fin Corollary, PrefixSpanCoverage, the S3/TS3 merge induction), the ML6 necessity/sufficiency discharge, both halves of ML9's Fact (a)/(b) composition, and the ValidComposite★ coupling vacuity; all hold up. The remaining issues are one representation-independence overstatement, one unresolved convention status, and anti-bloat accretion around the ρ=∅ boundary that the last several revise cycles deposited in three places without consolidating.

## REVISE

### Issue 1: The ρ=∅ / one-sided-link boundary is treated three times, with the same deferral issued twice
**ASN-0120, "What the endset arguments name" and "Three endsets" (ML5)**: The recovery-equation paragraph settles the boundary ("`e_j = ∅` is the unique admissible record... we return to this boundary below"); a later paragraph in the same section re-walks it in full ("`e_j = ∅` is the unique admissible record... legal link values... inert in ML9's discoverability test... Its definedness is settled here; what the empty non-type endset *means*... is deferred to the Open Questions"); the ML5 paragraph then restates the identical three facts ("`ρ(R_j, Σ) = ∅` forces `e_j = ∅`, the operation is defined on the input, the record is L3-legal, and the empty slot is inert in discovery. What the empty non-type slot *means*... we defer to the first Open Question").
**Problem**: Two paragraphs in different sections say the same thing in different words, and both defer the same question to the same Open Question — exactly the forward-reference accretion pattern this note's anti-bloat classifier flags. The commit trail (three consecutive ρ=∅ revisions touching ML5/ML6/ML9 prose) shows this is relocated content layering up across cycles rather than one settled treatment. The "we return to this boundary below" pointer in the recovery-equation paragraph is scaffolding for the duplication.
**Required**: One operational treatment of the boundary, in the resolution section (definedness, unique admissible record, K.λ legality, ML9 inertness, the `wf` non-requirements). ML5 keeps only its unique content — the Nelson LM 4/48 slot convention — citing the settled boundary without restating its three properties. One deferral to the Open Question, not two. Drop the forward pointer.

### Issue 2: ML2 overstates representation independence — the model does expose decomposition-sensitive observables
**ASN-0120, "What the endset arguments name" (ML2)**: "no observable *of this model's operations* is sensitive to it: the model exposes no span-positional accessor within an endset (ASN-0043, L5)..."; claims table: "no operation of the model distinguishes them."
**Problem**: The universal is false on the ASN's own citations. L5 itself grants span access "by membership `(s, ℓ) ∈ e` only" — and membership *is* decomposition-sensitive: for chain-adjacent resolved `a₁, a₂`, the query `(a₁, δ(2, #a₁)) ∈ e` distinguishes `{(a₁, δ(1,#a₁)), (a₂, δ(1,#a₂))}` from `{(a₁, δ(2,#a₁))}`. Likewise the foundation's `Observe_K` (ASN-0086) returns raw `(a, F, G)` triples, exposing the stored decomposition even though its *matching* is coverage-based. The enumerated trio (no positional accessor, LP21, L8) is correct; the universal quantification over "the model's operations" is not, and a downstream ASN citing ML2 as "decomposition is unobservable" would build on a falsehood the moment a read-back operation (the deferred READLINK shape) is specified.
**Required**: Scope the claim to what is actually proved: the observables this ASN's claims consult — projection (LP21), type matching (L8), discoverability (LP12) — are functions of coverage alone; decomposition remains observable via endset membership (L5) and value equality (L6), which is precisely why MAKELINK's postcondition deliberately pins coverage and leaves decomposition free. State it that way in both the prose and the ML2 table entry.

### Issue 3: The one-sided slot convention's normative status is unsettled
**ASN-0120, "Three endsets" (ML5)**: "The design does contemplate a degenerate *one-sided* link... and fixes its slot convention: the first endset is the populated one, designating the matter pointed at, and the second is left empty."
**Problem**: "Fixes" asserts a norm the operation does not enforce and no claim carries. The boundary paragraph explicitly admits *both* degenerate forms as legal — "`(∅, e₂, e₃)` and `(e₁, ∅, e₃)` are legal link values" — so a one-sided link with empty *first* slot and populated second is admitted by MAKELINK as specified, contradicting the stated convention. A formalizer extracting claims finds no carrier for the convention: ML5's table entry omits it entirely. As written, the convention is neither a precondition, nor an invariant, nor explicitly marked informative.
**Required**: Settle the status one way: either (a) the convention is normative — add it to MAKELINK's contract (e.g., a precondition that when exactly one of `ρ(R₁,Σ)`, `ρ(R₂,Σ)` is empty, it is the second) and record it in ML5's claim entry; or (b) it is informative Nelson commentary — say so explicitly ("recorded, not enforced; the operation admits both forms") so the admitted `(∅, e₂, e₃)` case and the quoted convention no longer sit in unacknowledged tension.

## OUT_OF_SCOPE

### Topic 1: Direct I-address endset arguments (ghost endsets, ghost types)
**Why out of scope**: The ASN correctly restricts itself to V-spec arguments and notes that reaching addresses outside `dom(Σ.C)` — the full generality of L4/L9 — requires a distinct argument shape. That is a different operation surface, properly a future ASN, and the restriction paragraph honestly records what MAKELINK-via-V-specs cannot create.

### Topic 2: Endset arguments referencing the link subspace (links to links)
**Why out of scope**: `wf` excludes link-subspace V-specs (`subspace(u_j) = s_C`), so the operation is simply undefined on them; what an extension must guarantee is new territory, and the ASN's Open Question already stakes it out.

### Topic 3: Semantics of the empty non-type endset
**Why out of scope**: The *definedness* of the boundary is settled in-model (correctly); what the degenerate link *asserts* is a semantic question the Open Question properly defers. (The duplication of that deferral is Issue 1; the deferral itself is sound.)

VERDICT: REVISE
