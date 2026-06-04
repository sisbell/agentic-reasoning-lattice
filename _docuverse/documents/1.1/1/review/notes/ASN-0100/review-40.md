# Review of ASN-0100

## REVISE

### Issue 1: Non-circularity defense is meta-prose restated in two locations

**ASN-0100, §Effect — Arrangement (INS.M-exhaustive)**: "To transfer it to every admissible decomposition we then invoke the uniqueness of Σ' (§Atomicity): because that uniqueness argument takes the canonical exhaustiveness as input (it is the ⊆ direction of the boundary V_{s_C}(d') equality there), the transfer cites the direct result plus uniqueness and so closes no circle"

**Problem**: This is prose whose only job is to argue that an argument is not circular — a flagged anti-bloat pattern ("prose justifies document ordering... non-circular by Y argument"). The same content reappears in §Atomicity ("the ⊆ direction (no fourth region) holds by the canonical decomposition's directly-established exhaustiveness — the step-tracking argument inside INS.M-exhaustive"). Two paragraphs in different sections carry the identical dependency-routing explanation. The underlying logic closes, but the defense of it is noise the reader must parse around.

**Required**: State the establishment once (canonical step-tracking establishes exhaustiveness of the unique Σ'; the post-state invariants depend on that Σ'). Delete the meta-commentary about which direction feeds which and why no circle forms. Remove the mirror restatement in §Atomicity.

### Issue 2: "established once and decomposition-independently" contradicts its own proof

**ASN-0100, §Effect — Arrangement and Claims table (INS.M-exhaustive)**: "The exhaustiveness clause is a property of the uniquely-determined post-state V_{s_C}(d'), established once and decomposition-independently." / Table: "decomposition-independent: the canonical K.μ⁻ + K.μ⁺ produce exactly those positions and uniqueness transfers it to all admissible decompositions"

**Problem**: The claim says "decomposition-independent" and in the same breath establishes it *via the canonical decomposition* then transfers by uniqueness. That is decomposition-dependent establishment plus a transfer step — the opposite of what "decomposition-independent" asserts. The phrasing is internally inconsistent.

**Required**: Pick one accurate description. Either "established for the canonical decomposition, then lifted to all admissible decompositions via uniqueness of Σ'" or drop the "decomposition-independent" label.

### Issue 3: I3-citation inventory is a use-site enumeration

**ASN-0100, §Effect Three (Scope of ASN-0082's I3)**: "This ASN cites I3's positive shift clause and the companion lemmas I3-L, I3-X, I3-D, I3-VD, I3-VP, I3-fin, I3-S2, I3-S3, which govern the regions ASN-0082's shift-only model covers; it does not cite I3-V, I3-CS, I3-CX, I3-C, or I3-S7..."

**Problem**: This paragraph enumerates which foundation lemmas are and are not cited, then announces a bookkeeping convention ("We state the partition once here and apply it throughout... The per-invariant subsections do not re-explain this partition"). This is a use-site inventory plus a meta-instruction to the reader — both flagged patterns. The actual content (INSERT adds an Insertion region the shift-only model omits, and reallocates content so I3-C fails) is one sentence; the rest is catalog.

**Required**: Reduce to the load-bearing fact: cite I3 for the shift clause; note that I3's whole-post-state characterizations (I3-C `Σ'.C = Σ.C`, etc.) do not hold because INSERT also allocates and inserts. Drop the lemma roster and the "we do not re-explain" instruction.

### Issue 4: wp-calculus applicability commentary is explanatory padding

**ASN-0100, §The Operation's... (Environmental Assumptions)**: "The distinction matters for backward reasoning: wp-style derivation of INSERT's preconditions applies to state preconditions, which are predicates on Σ. The composite-atomicity environmental assumption is not such a predicate — it constrains the substrate's execution model, not the state — and so it sits outside the wp calculus."

**Problem**: This explains why a particular assumption is not amenable to a technique applied three sections later. It advances no part of the operation's specification; it is rationale about methodology. The preceding sentences already state the assumption and its required scope precisely.

**Required**: Delete. The assumption's statement and its "establish by construction" closing sentence suffice.

### Issue 5: The S8-depth / K.μ⁻-empties point is stated three times

**ASN-0100**: appears in §The Operation's Inputs ("If a subsequent K.μ⁻ later empties V_{s_C}(d), S8-depth holds vacuously..."), in §Sequential text-subspace structure ("If a subsequent K.μ⁻ empties V_{s_C}(d), S8-depth becomes vacuous at that state, freeing a later first-insertion to choose a different m'"), and in the Claims table (INS.inv.depth row).

**Problem**: The same observation — that emptying the text subspace via an out-of-scope K.μ⁻ re-frees the depth parameter — is restated in three locations. Redundancy across sections is flagged anti-bloat.

**Required**: State once (the table row is the natural home), remove the two prose duplicates.

### Issue 6: Repeated forward deferrals to §Atomicity

**ASN-0100**: "(§Atomicity)" / "(see §Atomicity)" / "(established under §Atomicity)" recur in INS.M-exhaustive, in Substrate Decomposition step 3, and in the P7 provenance discharge.

**Problem**: Multiple paragraphs defer the same fact (uniqueness of Σ', forced K.α-before-K.ρ ordering) to the same downstream location — a flagged pattern. Each deferral asks the reader to hold an unresolved claim and jump forward.

**Required**: Where a deferred fact is used, state the one-line consequence inline (e.g., "K.α(a_k) precedes K.ρ(a_k,d), so a_k ∈ dom(C') when the pair is recorded") rather than pointing forward, or consolidate so the dependency is resolved before use.

## OUT_OF_SCOPE

### Topic 1: Minimum locking discipline for composite atomicity
**Why out of scope**: The first Open Question (what substrate machinery secures composite-level atomicity without global serialization, and failure-recovery to canonical order) is genuinely new territory — a substrate/concurrency concern, not a defect in INSERT's per-state contract.

### Topic 2: Link-subspace insertion semantics
**Why out of scope**: Insertion into the link subspace via K.μ⁺_L / K.λ is correctly bounded out; it is a structurally distinct operation for a future ASN.

META: (not applicable — the ASN remains squarely about state, the INSERT operation on it, and the invariants it must preserve; it is over-defended, not off-track)

VERDICT: REVISE
