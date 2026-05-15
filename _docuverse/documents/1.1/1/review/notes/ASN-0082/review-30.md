# Review of ASN-0082

## REVISE

### Issue 1: Missing span width preservation lemma for contraction
**ASN-0082, introduction and section structure**: "This ASN extends ASN-0053 (Span Algebra) with two complementary shift properties governing the arrangement transformations that underlie INSERT and DELETE."

**Problem**: The insertion side delivers I3-S, which connects I3's point-level shift to ASN-0053's span framework: "For a level-uniform span σ = (s, ℓ) with s ≥ p, subspace(s) = S, #s = #ℓ = m, and actionPoint(ℓ) = m, the shifted span σ' = (shift(s, n), ℓ) satisfies reach(σ') = shift(reach(σ), n) and width(σ') = ℓ." The contraction section has no parallel lemma — no statement establishing that level-uniform ordinal-level spans in the right region R preserve their width under σ. Given that the ASN's stated purpose is to provide "two complementary shift properties" and that the connection to span algebra is named as the reason both belong in this ASN, the asymmetric coverage is a gap. Downstream consumers reasoning about spans through deletion have no tool.

**Required**: Either (a) add a D-S lemma analogous to I3-S, proving that for a level-uniform ordinal-level span σ = (s, ℓ) with s ∈ R, the shifted-back span σ' = (σ(s), ℓ) satisfies reach(σ') = σ(reach(σ)) and width(σ') = ℓ — the proof should follow by direct computation at depth 2, using TumblerAdd/TumblerSub commutativity at single-component ordinals — or (b) explicitly defer this to a future ASN with a stated reason.

### Issue 2: wp analysis style inconsistency
**ASN-0082, post-insertion and post-contraction sections**: The insertion section provides detailed weakest-precondition derivations for I3-VP and I3-S2, surfacing TS2, TS4, S8a, and subspace preservation as discharged obligations through assignment statements. The contraction section's preservation lemmas (S8-depth-post, S8a-post, S2-post, S3-post, D-CTG-post, etc.) use straightforward forward proofs without comparable wp treatment.

**Problem**: The wp analysis is illustrative on the insertion side and reveals which foundation properties do load-bearing work for which postconditions. The contraction side's analogous properties — TA3-strict for D-BJ's order preservation, TA4 for D-SEP's algebraic identity, the subspace-1 / depth-2 scoping for the partial-inverse structure — would also benefit from this treatment. The omission either suggests the wp on insertion is decorative (in which case it should be cut) or that the contraction proofs are under-analyzed (in which case they should match).

**Required**: Either add wp analysis for at least one contraction preservation lemma (e.g., S8a-post or S2-post), or remove the wp sections from insertion and rely on the standard forward proofs throughout. Whichever direction, the rigor should be uniform across the two halves of the ASN.

### Issue 3: Depth = 2 restriction grounds mix levels
**ASN-0082, post-contraction shift scope discussion**: "The asymmetry with I3 (which is established at arbitrary m ≥ 2) is intentional, on three grounds. *Structural necessity from TA4...* *Design intent...* *Implementation reality...*"

**Problem**: Of the three grounds, only the structural one (TA4's zero-prefix requirement against S8a's componentwise positivity) is a mathematical necessity for the current proof. The design intent (Literary Machines design) and implementation reality (udanax-green hardcoding) are historical context. Presenting them as parallel "grounds" for a scope restriction conflates mathematical necessity with descriptive observation: the structural ground proves depth > 2 cannot work with this proof technique; the other two only observe that depth > 2 wasn't pursued historically.

**Required**: Restructure the discussion so the structural argument stands as the necessity claim, with the design-intent and implementation-reality material relocated as context (perhaps in a separate "Historical Notes" or "Open Question motivation" section). The current framing risks reading as appeal to authority for what is actually a precise mathematical constraint.

### Issue 4: I3-V exclusion clause readability
**ASN-0082, I3 contract**: "I3-V (vacating): `(A v : v ∈ dom(M(d)) ∧ subspace(v) = S ∧ v ≥ p ∧ v ∉ {shift(u, n) : u ∈ dom(M(d)) ∧ subspace(u) = S ∧ u ≥ p} : v ∉ dom(M'(d)))`"

**Problem**: The exclusion clause requires the reader to mentally construct the image set `{shift(u, n) : ...}` and then check non-membership. The wp analysis for I3-S2 case (7) makes the role of this clause clear, but the contract itself doesn't expose the underlying intent: "vacate original positions that are not the destination of any shift." The worked example explains this, but the formal contract is dense at first reading.

**Required**: Either rewrite I3-V using an equivalent but more direct formulation (e.g., "`v` is not of the form `shift(u, n)` for any `u ∈ dom(M(d)) ∩ subspace S ∩ {u ≥ p}`"), or add a one-line gloss after the formal statement explaining the role of the exclusion clause. Currently the reader must work through the worked example or the wp analysis to understand why the exclusion is needed.

### Issue 5: V_S(d) and V_1(d) used interchangeably
**ASN-0082, post-contraction shift section**: The contraction is scoped to S = 1 by axiom, yet the formal contracts and proofs alternate between `V_S(d)` (used in ThreeRegions, D-SHIFT, D-L, D-CS, D-DOM, D-CD, D-I) and `V_1(d)` (used in containment precondition, D-CTG-post, D-MIN-post, D-SEQ-post, D-SEP). Within a single proof (D-CTG-post), both notations appear.

**Problem**: While the two are equivalent under the subspace scoping axiom, mixing them is a clarity issue. A reader checking the chain of citations must verify each instance is interpreted under the axiom. The conventions in the foundation (ASN-0036) reserve `V_1(d)` for explicit text-subspace claims and `V_S(d)` for subspace-parametric statements; this ASN's mixed usage blurs that convention.

**Required**: Pick one notation and use it consistently. Given the subspace scoping axiom fixes S = 1, `V_1(d)` is the natural choice and aligns with how the foundation states D-CTG, D-MIN, D-SEQ.

## OUT_OF_SCOPE

### Topic 1: Generalized depth contraction (#p > 2)
**Why out of scope**: The author explicitly lists this as an open question, identifies TA4's zero-prefix condition as the structural obstacle, and notes that resolving it requires either strengthening TA4 or deriving the partial-inverse identity from first principles. Both routes are substantive new work outside this ASN's scope.

### Topic 2: Link-subspace mutations via tombstoning
**Why out of scope**: The contraction is scoped to text subspace because D-CTG, D-MIN, D-SEQ are text-only invariants and link-subspace mutation uses tombstoning instead of gap-closure. The tombstoning operation belongs in a separate ASN.

### Topic 3: Compositionality with full INSERT (content placement)
**Why out of scope**: The ASN explicitly scopes I3 to the shift sub-operation. Composing it with content allocation — including the n new I-addresses in dom(C) and the re-derivation of D-CTG, D-MIN, D-SEQ after gap-filling — is deferred to a future INSERT ASN. The note on weakening I3-C to S0 in the composing operation is appropriate forward-looking guidance.

### Topic 4: Spans straddling shift boundaries
**Why out of scope**: I3-S covers spans entirely within the shifted region (s ≥ p). Spans with s < p and reach(σ) > p (straddling the insertion point) are not addressed but represent a separate analytical concern about how spans split or extend under arrangement transformations.

### Topic 5: External state recording V-positions and update under shift
**Why out of scope**: Listed as an open question in the ASN. Belongs in a future ASN concerning the interface between arrangement transformations and external references (links, citations, etc.).

VERDICT: REVISE
