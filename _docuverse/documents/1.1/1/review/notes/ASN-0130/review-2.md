# Review of ASN-0130

The note's architecture is sound — composing immutability, origin identity, and event ordering into a self-hosting definition store is the right design, and PR1/PR2 are genuinely well-argued. But five things need fixing: the discipline-enforcement story has a hole the note papers over with a false sentence, the view dimension of PL terms is never pinned down (which makes PR5's certificate ill-posed), and three smaller precision gaps.

## REVISE

### Issue 1: Discipline is claimed enforced but the shipped surface itself provides the undisciplined route
**ASN-0130, PR0 (Discipline and uniqueness)**: "The note's downstream claims (PR1, PR2, PR5's lint reading, PS1's dedup reading) are scoped to derivations that are registration-disciplined and surface-disciplined (SD, ASN-0128); a derivation driven entirely through the shipped surfaces is both."

**Problem**: The last clause is false. ASN-0128's I5/I6 expose `Emit_K` for *every* registered class, with exactly one class exclusion: `K ≁ R`. `pdef` and `pd_stable` are registered classes (PS1, PS2), `pdef ≁ R` and `pd_stable ≁ R` by the note's own non-collision stipulation, and `pdef`'s Multi gate admits any `(d, {a}, X_G)` — so a direct `Emit_pdef` call depositing an unvalidated classifier (no parse, no typing, no condition (iv)) is a call *through a shipped surface*, and the resulting derivation is not registration-disciplined. The note itself confirms `Emit_pdef` is the exposed emit ("the surface invokes the exposed emit (I5/I6, ASN-0128) at the `pdef` class"). ASN-0128 closed the analogous hole for [R] structurally: the uniform `K ≁ R` rejection makes `Nullify_Binary` "the one retraction entry point," which is what licenses SD's "a derivation driven through this surface alone is one." ASN-0130 copies the conclusion without the supporting exclusion. PS2's "Emitted only by the certification path of the registration surface" gestures at the right stipulation for `pd_stable` but names no mechanism; PR0 doesn't even gesture for `pdef`.

**Required**: Stipulate that the exposed `Emit_K` rejects `pdef`-class and `pd_stable`-class calls (extending I6's uniform preconditions, exactly the S3 pattern), making `register_pred` and the certification path the sole surface routes into those slices — then the quoted sentence becomes true. Alternatively, delete the sentence and present registration discipline as an unenforced assumption, accepting that the worked composition's guarantees then hold only by convention.

### Issue 2: The view dimension is unresolved — and PR5's certificate is ill-posed without it
**ASN-0130, PR-ENC / PR3 / PR5**: PR-ENC defines the signed term as "a pair of an ordered, sorted parameter context `Γ_D` … and a body" — no view recorded. PR3: "`evaluate(a, args, view, Σ)` is the ASN-0129 denotation of `expand(a)` at `(args, view, Σ)`" — view is a caller argument. PR5: the certificate asserts "membership in PD0's **ST** class" of the expansion.

**Problem**: PC3 (ASN-0129) makes every PL term carry one view, fixed at the top level, and PD0's stability classes are *view-relative*: `is_K(addr)` is in ST only "at view `audit`"; `M_K` is grow-only only "in an audit-view term"; PD1 shows the same spelling unstable at active/default views. Three consequences the note never confronts: (a) "expand(a) ∈ ST" has no truth value until a view is fixed, so the `pd_stable` certificate is ill-posed — and operationally hazardous: a consumer can evaluate a certified definition at `view = active`, where the certified stability guarantee does not hold. (b) Since `view` is supplied per `evaluate` call, expansion silently rebinds a referent's view-parameterized atoms (`members`, `targets_of`, `is_K`, `M_K`) to the caller's top-level view — a referent means different things at different call sites, a semantic choice (view-transparent references) that is nowhere stated as such. (c) The worked composition contradicts the view-as-argument design: step 1 describes the body as "an active-view emptiness test" and step 4 reasons "an active-view term can flip back (PD1)" — language that presupposes the body carries a view.

**Required**: Pin the view story and make PR-ENC, PR3, PR5, and the example agree. Either record a view in the signed term (extend `sig(a)` accordingly; then resolve cross-view referencing — e.g., normalize inlined referents through PC3's derivable fixed-view spellings — and drop or constrain `evaluate`'s view argument), or keep definitions view-polymorphic and make the certificate view-indexed (or restrict certification to spellings whose atoms are all fixed-view/step-constant, hence view-independent — checkable syntactically, and what the example's v2 happens to be).

### Issue 3: PR0's wp equivalence holds only on disciplined derivations, but is displayed unscoped
**ASN-0130, PR0 (Success, precisely)**: "`wp(register_pred(d, A_def), POST-ref) ≡ VALID(Σ, A_def) ∧ (hit(Σ, a) ∨ (d ∈ dom(Σ.M) ∧ C3(Σ, d)))`"

**Problem**: Both directions of this equivalence need registration discipline, yet the discipline-scoping sentence lists "PR1, PR2, PR5's lint reading, PS1's dedup reading" and omits the wp; only the C3-elimination step is explicitly scoped (to SD via DR). Two off-discipline counterexamples: (a) *Hit branch*: the derivation of POST-ref from a hit uses "under the discipline canonically shaped" — off-discipline, an I0-equal incumbent may have `F' = {(a, δ(1,#a)), (a.x, δ(1,#a+1))}` with `coverage(F') = subtree(a)` by subtree absorption but `addrs(F') = {a, a.x} ≠ {a}` (the I0a separating pair), so `VALID ∧ hit` holds while POST-ref fails. (b) *Born-nullified miss*: with `¬C3`, the formula says wp false; but a pre-existing raw tuple with `F'' = enc({a})` and an unrelated `G''` is not I0-equal (so `hit` is false and the deposit proceeds) yet satisfies POST-ref at Σ′ — formula false, postcondition true. The argument as written quietly invokes the discipline mid-derivation while presenting the formula as general.

**Required**: Scope both wp forms (the C3 form to registration-disciplined derivations; the reduced form to registration- plus surface-disciplined ones) — simplest is to add PR0's wp to the scoping list — or restate POST-ref/hit so the equivalence holds unscoped.

### Issue 4: Well-typedness of the expansion is asserted, never derived
**ASN-0130, PR3 (and PR2)**: "expansion terminates in a pure PL term whose free variables are the top level's own parameters `Γ_D`" and "the expanded result is a pure PL term (no references)."

**Problem**: Termination (PR2) and the free-variable accounting (PR-SIG) are derived; well-typedness is not. WT-ref types the reference node `a(e₁, …, e_k) : C_D`; expansion *replaces* that node by `expand(r)` with arguments substituted for parameters, and the claim that the result is still a PL term of the host's sort is a substitution lemma — types preserved when `Cᵢ`-typed argument terms replace `Cᵢ`-sorted parameters — used silently. It is load-bearing: without `expand(a)` well-typed at `C_D`, "the ASN-0129 denotation of `expand(a)`" in PR3's evaluation clause is not established to exist at the signature's result sort. The machinery is available (WT's PC2 plain-composition rule is literally `Γ ⊢ g[x := f] : C₂` from `Γ ⊢ f : C₁` and `Γ, x : C₁ ⊢ g : C₂`, and PL is closed under PC2), so the gap is one inductive sentence — but per the standards, "X follows from Y" must be shown, not implied.

**Required**: State and discharge the lemma: by induction down the reference DAG (well-founded by PR2), each replacement preserves typing via WT's PC2 substitution rule applied at WT-ref's premise sorts, so `Γ_D ⊢ expand(a) : C_D` with `expand(a) ∈ PL`.

### Issue 5: "Resident references" misdescribes condition (iv) in two places
**ASN-0130, What this note commits (PR0 bullet) and Worked composition step 5**: "the operation surface validates the encoded term — parse, well-type, *resident references only*" and "The residence check closes the frontier-ghost hazard for definitional references."

**Problem**: There is no residence check on references. Condition (iv) tests *registration* — an active `pdef` tuple denoting the referent — which is strictly stronger than residence (registration entails residence via the referent's own condition (i) plus C0 persistence, but not conversely: a resident, valid, unregistered run fails (iv)). The summary bullet and the example both name a weaker check than the one the spec defines, and a reader of either could conclude that referencing any resident run is admissible.

**Required**: Say "registered references only" in the bullet and "the registration check (iv)" in step 5, optionally noting that registration entails residence.

## OUT_OF_SCOPE

### Topic 1: Concrete encoding format
**Why out of scope**: PR-ENC deliberately fixes the discipline (injective, prefix-free, self-delimiting, decidable parse and typing) and parameterizes the bytes, parallel to the subspace-identifier convention; all proofs use only the discipline. The note states this boundary itself.

### Topic 2: Dangling-live-reference policy
**Why out of scope**: The status quo (validate (iv) at registration only; evaluation reads the audit slice and survives de-registration) is fully specified and internally consistent; whether `pdef` retraction should be blocked while live referents exist is a policy decision the note correctly defers (Open question 3).

### Topic 3: Authorization and naming
**Why out of scope**: Who may register, de-register, certify, or claim supersession — and human-facing naming (Open question 1) — are protocol/application-layer concerns; the substrate corpus has no authorization model anywhere, and the note correctly routes adjudication of competing supersessions to readers (PR4).

### Topic 4: Soundness of the ST checker
**Why out of scope**: PR5 commits the certificate's meaning and permanence, not the certification algorithm; soundness of the syntactic stability check is ASN-0129's Open Question 5, inherited and flagged as such.

VERDICT: REVISE
