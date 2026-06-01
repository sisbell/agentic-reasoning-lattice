# Review of ASN-0086

## REVISE

### Issue 1: ChainMembershipForOrigin invoked at `↝`-reachable states, but the foundation lemma is scoped to `→`-reachability

**ASN-0086, R0a Case 2 / R0a-Cor1 / R7a discharge (4)(i)**: "By clause (b) of substrate-conformance (frontier emission), ASN-0093's ChainMembershipForOrigin lemma applies at Σ — whether Σ is `→*`-reachable or an `↝`-reachable conforming-layer post-state…"; "ChainMembershipForOrigin — the ASN-0093 theorem that frontier emission yields contiguous homed-sets — therefore holds at Σ' as a consequence of conformance."

**Problem**: ASN-0093's ChainMembershipForOrigin is stated "At every reachable state Σ," where reachability is via the K-operation transition system, and its truth rests on the K.α/K.λ contracts. The note re-reads its operative hypothesis as the abstract "frontier emission" clause (b) and then applies it to states reached by *arbitrary* higher-layer `↝`-steps. That re-reading is asserted, not derived. This matters because R7a (discharge (4)(iii)) consumes R0a-Cor1, and R0a-Cor1's contiguity conclusion at conforming `↝`-states rests on exactly this extension — so the gap is load-bearing, not cosmetic. There is also a whiff of circularity: R7a is the theorem that would establish an `↝`-conforming state's L-component is `→`-reconstructable, yet R7a's own proof presupposes the contiguity that reconstruction would justify.

**Required**: Derive the contiguity conclusion directly from conformance clause (b) — a one-line induction (if every fresh key is emitted at `inc(max homed, 0)` or as first-emission, the homed set is a contiguous chain prefix at every step) — rather than citing a foundation lemma whose stated scope is `→`-reachability. Alternatively, restrict R0a / R0a-Cor1 to `→*`-reachable states and show R7a needs nothing stronger.

### Issue 2: `#E = 2` design tradeoff stated in three places

**ASN-0086, R0a-Cor2 parenthetical, Properties table (R0a-Cor2 row), Open Question #7**: the L1b `#E ≥ 2` vs `#E = 2` tightening question, and the observation that R0a-Cor2 establishes `#E = 2` unconditionally, appear in all three locations in substantially the same words.

**Problem**: The anti-bloat classifier flags "two paragraphs… say the same thing in different words." R0a-Cor2's body already proves `#E = 2`; the parenthetical's editorializing about narrowing L1b, the table gloss, and Open Question #7's multi-sentence restatement are the same content thrice.

**Required**: Keep the proof in R0a-Cor2's body. Reduce Open Question #7 to the genuinely-open part (whether L1b *itself* should be tightened at the source) and drop the parenthetical's restatement.

### Issue 3: Justification-prose in structural slots (meta-prose accretion)

**ASN-0086, multiple sites**:
- Partition definition: "These are aliases for the two foundation stores, but they earn their keep by naming the two participating address classes of the relational view… Downstream predicates over the relation then read in relational vocabulary rather than store-domain vocabulary."
- R7a discharge (4)(i): "…therefore holds at Σ' as a consequence of conformance, **not as a separately imposed step-local invariant**."
- Opening paragraph parenthetical on K.σ/K.α "not reductions of `Emit_K`," repeated near the reduction Corollary.

**Problem**: These advance no reasoning. The "earn their keep" sentence justifies why an alias is worth introducing rather than stating what it denotes; the "not as a separately imposed invariant" clause defends the proof's structure rather than discharging an obligation; the K.σ/K.α non-reduction note is stated twice. Per the classifier, prose the reader must skip to reach the claim is a finding.

**Required**: Delete the "earn their keep" / "read in relational vocabulary" sentences (the alias definitions stand alone). Trim the defensive clause in (4)(i) to the bare claim. State the K.σ/K.α scope note once.

### Issue 4: Forward reference to R6 inside R3's Consequence

**ASN-0086, R3 Consequence**: "When we introduce the retraction type `R` (R6), `L_R` is one of the typed slices and R3 applies to it as well."

**Problem**: R3's consequence is parasitic on a construct (the retraction type) defined two sections later. The forward pointer adds nothing to R3 itself and only previews R6's payoff — exactly the deferral pattern the classifier names.

**Required**: Move this remark to the RetractionType definition (where `L_R` is introduced and R3's applicability to it is immediate), or drop it.

## OUT_OF_SCOPE

### Topic 1: Concurrency / atomicity of Emit vs Observe, and the consistency model for observing `A_K` transitions
**Why out of scope**: The note fixes SequentialAtomicTransitions from ASN-0093 and works in a single-authority serialized model. A concurrency/consistency model is genuinely new territory (correctly raised as an Open Question), not a defect of this ASN.

### Topic 2: Multi-arity typed relations `L_K^{(n)}` and binary projections of `|Σ.L(a)| > 3` links
**Why out of scope**: This ASN explicitly restricts to standard-triple links; higher-arity relational structure is a future construction, and the note is consistent about confining `L_K`, `A_K`, and Nullify's active-subset effect to arity 3.

### Topic 3: Cardinality bound of `nullified(Σ)` relative to `dom(Σ.L)`
**Why out of scope**: A structural ratio bound on retraction is a new invariant, not something the present append-only/audit construction needs to satisfy.

VERDICT: REVISE
