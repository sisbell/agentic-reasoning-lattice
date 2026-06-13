# Review of ASN-0130

The construction is strong, and I want to say so plainly before the findings: PR3a's substitution induction (with its capture/interference bookkeeping), the PR0/PR5a weakest-preconditions across the born-nullified boundary, PR2's event-wise acyclicity, and the lint's start-incomparability argument all hold up under adversarial reading, and the worked composition exercises them on concrete terms (the benign-coincidence vs. genuine-capture contrast and the frontier-ghost rejection are both correct). The issues below are one precision inconsistency and several instances of the forward-reference accretion this review mode targets.

## REVISE

### Issue 1: (iii)'s decidability attributed to (iv), in tension with PR1
**ASN-0130, PR0**: "the decoded term well-types, Γ_D ⊢ body : C_D, under WT + WT-ref — decidable because (iv) makes each referent's sig(r) defined (PR-SIG)"
**Problem**: This pins (iii)'s decidability to (iv), which requires each referent *actively* registered (`some (b,F,G) ∈ A_pdef^Σ`). But WT-ref's domain condition is only "sig(r) defined," and PR-SIG defines sig on the *ever-registered* addresses ("defined exactly on the ever-registered addresses ... fixed at first registration") — strictly weaker than active membership. PR1 draws exactly this line and depends on it: it classes "(iii) reads ... sig(r), fixed at r's first registration" as content/signature-intrinsic and therefore *permanent*, while "(iv) ... reads A_pdef^Σ (active membership)" is the lone non-permanent conjunct. PR1's permanence of (iii) only goes through *because* (iii) rests on ever-registration, not on (iv): a referent that is ever-registered but later de-registered still has sig defined, so (iii) types and stays valid while (iv) fails. Taken literally, PR0's "(iii) because (iv)" would make (iii) inherit (iv)'s impermanence and collapse PR1's conjunct-division — and would also contradict PR3's "a de-registered definition therefore still resolves, expands, and evaluates."
**Required**: In PR0, justify (iii)'s decidability via sig(r) being defined on *ever-registered* referents (a decidable audit check, computable down the acyclic DAG per PR2), and present (iv) as the separate *active*-registration requirement — matching PR1. The two checks catch different failures (never-registered referent ⇒ no typing judgment at (iii); de-registered referent ⇒ types but rejected at (iv)); the prose should not fold the first into the second.

### Issue 2: PR5 states the ST⁺ parameter reading twice
**ASN-0130, PR5 opening**: "...established by PD0's rules under the parameter reading fixed in the Parameters qualification below — every parameter read as a bound constant of its declared sort, PD0's aggregate-threshold side condition correspondingly extended from 'ℕ literal' to an ℕ literal or an environment-bound parameter."
**ASN-0130, PR5 Parameters qualification**: "the checker runs PD0's rules with each parameter treated as a bound constant of its declared sort ... The parameter reading extends that threshold position from 'ℕ literal' to an ℕ literal or an environment-bound parameter..."
**Problem**: The opening explicitly defers ("fixed in the Parameters qualification below") and then states the reading in full anyway; the qualification restates it. This is the forward-reference-then-restate pattern. Within the qualification, the soundness point is then made a third and fourth time ("An ℕ literal is fixed outright; an environment-bound parameter is exactly as fixed" / "Both admitted threshold forms are thus fixed across every step — the only property the soundness argument consumes").
**Required**: State the parameter reading once — name it in the opening and define it in the qualification (or vice versa), not both — and collapse the repeated "fixed" to a single sentence.

### Issue 3: PR5's View qualification restates PR-VIEW
**ASN-0130, PR-VIEW**: "A view-independent term's denotation is invariant in the view argument ..."; "An author who needs a read pinned to a slice regardless of caller pins it in the spelling..."
**ASN-0130, PR5 (View qualification)**: "such a term denotes identically at every view ..."; "the fixed-view respelling PR-VIEW describes remains available to an author who needs a pinned read."
**Problem**: The load-bearing new content of PR5's View qualification is *why* certification requires view-independence (PD0's classes are view-relative). The denotation-invariance fact and the respelling-availability remark are already established in PR-VIEW; restating them around the citation is padding.
**Required**: Cite PR-VIEW for denotation-invariance, drop the respelling-availability clause, and keep only the new rationale (PD0 view-relativity ⇒ certify only view-independent expansions).

### Issue 4: PS2 — meta-prose around the "entry-point seal below"
**ASN-0130, PS2**: "Emitted only by certify_pd_stable (PR5a), through the wrapped Emit_pd_stable(Σ, d, {a}, ∅) — a monopoly the entry-point seal below enforces rather than assumes; the assertion discipline is thereby the surface's mechanically, the tuple merely durable."
**Problem**: The enforcement claim is delivered by the *Entry points — the seal* paragraph ("This is what discharges the registration discipline ... for the shipped surfaces"). PS2 pre-announces it through a forward reference wrapped in meta-prose; the clause "the assertion discipline is thereby the surface's mechanically, the tuple merely durable" is compressed past readability and adds nothing the seal paragraph does not say.
**Required**: Reduce PS2 to "Emitted only by certify_pd_stable (PR5a)" and let the seal paragraph carry the enforcement claim once.

## OUT_OF_SCOPE

### Topic 1: Atomic allocation of a contiguous run
PR-ENC and PR0(i) require `A_def` to be one contiguous K.α-chain segment, and the worked example leans on "with no other K.α scoped to `d_b` interleaved." Producing such a run reliably — so a concurrent content append to the same document cannot split it — needs a transactional/atomic multi-address allocation primitive.
**Why out of scope**: `register_pred`'s contract is to *validate* a presented run, which PR0(i) does correctly; how a builder *obtains* a gap-free run under concurrency is an allocation-substrate concern, not a defect in this note's claims.

VERDICT: REVISE
