# Review of ASN-0086

## REVISE

### Issue 1: R6b carries an inert hypothesis its own proof disowns
**ASN-0086, R6b (SingleDepthRetraction)**: the formal statement quantifies over `… ∧ b ∈ nullified(Σ) : a ∈ nullified(Σ)`, and the proof then states "(The conclusion holds equally without the fourth hypothesis…)".

**Problem**: A lemma should assert exactly what it proves. The fourth hypothesis `b ∈ nullified(Σ)` is load-bearing in appearance but inert in fact — the proof discharges the conclusion from the first three hypotheses alone and explicitly says so. A reader cannot tell from the statement whether the non-fixpoint conclusion is *conditional* on the retractor being nullified (it is not). The accompanying justification ("stating it with `b ∈ nullified(Σ)` is what makes the lemma express the non-fixpoint property") is rationale-prose substituting for a precise statement.

**Required**: State R6b as the unconditional fact `a ∈ A_rel^Σ ∧ (b,F',G') ∈ L_R^Σ ∧ a ∈ coverage(G') ⟹ a ∈ nullified(Σ)`, and express the non-fixpoint *interpretation* in a one-line remark ("in particular this holds when `b` is itself nullified") rather than smuggling it into the hypotheses.

### Issue 2: R0a-Cor1 is named a corollary of R0a but is proved from L-ContiguousPrefix
**ASN-0086, R0a-Cor1 (DepthTwoLinkAddresses)**: the label and placement assert derivation from R0a (FlatLinkDomain), but the proof opens "By L-ContiguousPrefix, every `a ∈ dom(Σ.L)` lies on the form…" and never invokes R0a's antichain. The properties table even records "R0a-Cor1 … (= L-ContiguousPrefix)".

**Problem**: The dependency name contradicts the actual proof. A reader tracing what R0a-Cor1 rests on is misdirected.

**Required**: Rename it (e.g., L-ContiguousPrefix-Cor1) or restate its dependency line as deriving from L-ContiguousPrefix, consistent with the table and the proof.

### Issue 3: Forward-reference / meta-prose accretion (anti-bloat classifier)
The note carries `review-mode.anti-bloat`; the following passages are noise to skip past, not reasoning that advances a claim:

- **Redundant second proofs of one step.** R0a Case 2 closes with "(Equivalently, by T10a.2 applied to the distinct siblings `a`, `a'` of `A_L(d)`)" after already concluding `a = a'` via `#a = #a'` + T3. Two justifications for the identical step.
- **Definition enumerating its downstream consumer.** Definition — RetractionType ends "Since `L_R^Σ` is one of the typed slices, R3 (TypedSliceMonotonicity) applies to it: every nullification leaves an entry in `L_R` that persists…" — this advances R3's reach, not RetractionType's meaning.
- **Rationale-prose explaining why clauses are shaped as they are.** "Clauses (b) and (c) together are the ASN-0093 chain discipline: (b) makes 'the fresh key at `d`' singular, so (c)'s … is unambiguous rather than open between several keys seeing the same pre-step frontier `J`." This argues for the structuring choice rather than stating the clauses.
- **Self-justifying design notes inside the WP.** WP Case 1: "We retain PC in the stated precondition because it is the condition the relational layer establishes." This justifies a non-weakest choice the surrounding text already proves is non-weakest.

**Required**: Delete the redundant alternative justifications and the consumer/rationale sentences. Keep the object-level content (the chosen proof, the definition, the clause statements) and drop the prose that explains the authoring choices.

### Issue 4: Single-tuple scope is derived twice in different words
**ASN-0086, Definition — Nullify (paragraph "Single-tuple scope under R0a")** and **WP Case 1 ("Sufficiency")** both reconstruct `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}` from R0a at Σ and Σ'.

**Problem**: Two paragraphs in different sections establish the same result by the same argument — the anti-bloat "two paragraphs say the same thing in different words" pattern. The WP section even re-invokes the Nullify-definition derivation it duplicates.

**Required**: Prove single-tuple scope once (in the Nullify definition), and have WP Case 1 cite it rather than re-derive it.

## OUT_OF_SCOPE

### Topic 1: Higher-arity typed relations `L_K^{(n)}`
The note restricts `L_K` to standard-triple links and defers `|Σ.L(a)| > 3` to an open question. Defining typed relations over higher arities is genuinely new territory, correctly deferred.

### Topic 2: Concurrency / atomicity of Emit vs Observe
The active/audit consistency model under concurrent operations is raised in Open Questions and belongs in a future ASN; the present note's single-authority, sequential-transition framing is a legitimate scope boundary.

### Topic 3: Cardinality bounds on `nullified(Σ)`
Whether unbounded retraction is permitted or a structural ratio must hold is a substrate-policy question outside the relational-vocabulary contribution of this ASN.

VERDICT: REVISE
