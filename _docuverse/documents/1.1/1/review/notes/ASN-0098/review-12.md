# Review of ASN-0098

## REVISE

### Issue 1: C0 (ASN-0058) appeal in tightness achievability does not apply to endset spans

**ASN-0098, "Boundary and Width Behaviour" / *Same document, cross subspace***:
> "The image `s ⊕ ℓ` agrees with `s` at this position: by C0 (ASN-0058) the action point of `ℓ` is `k_ℓ = #s = #d_0 + 3`..."

The non-nesting and descendant cases make analogous C0 appeals:
> "by C0 (ASN-0058), `ℓ` has action point `k_ℓ = #s = #d_0 + 3 > j`..."

**Problem**: C0 (OrdinalDisplacementNecessity, ASN-0058) is stated for *well-formed content references* — a separate ASN-0058 datatype with C0's required preconditions on common depth and well-formed range. Endset spans per L4 (ASN-0043) are arbitrary T12-satisfying spans, where T12 requires only `Pos(ℓ)` and `actionPoint(ℓ) ≤ #s` — the action point may be anywhere in `{1, ..., #s}`, not necessarily at `#s`. If `k_ℓ < #d_0 + 2`, position `#d_0 + 2` falls in TumblerAdd's tail-copy or sum region, not prefix-copy, and the `(s ⊕ ℓ)_{#d_0 + 2} = s_{#d_0 + 2}` step fails. The same gap kills the non-nesting case at position `j` whenever `k_ℓ ≤ j`, the descendant base case at position `#d_0 + 1`, and the ancestor base case at position `#d' + 1`.

**Required**: Either explicitly restrict the achievability argument to ordinal-displacement spans (and note that the canonical construction *chooses* such spans, so `k_ℓ = #s` is a consequence of the construction's specification, not of C0 applied to arbitrary endsets), or generalize each of the four cases to handle arbitrary action points. The simpler fix is the first: state up front that the canonical construction uses `ℓ = δ(n, #s)` and derive `k_ℓ = #s` from OrdinalDisplacement (ASN-0034) directly, rather than citing C0.

### Issue 2: Induction in descendant/ancestor cases is vestigial

**ASN-0098, *Descendant documents* / *Ancestor documents***:
> "*Inductive step (q → q + 1).* Suppose every depth-`q` descendant satisfies the structural form, and consider a depth-`(q+1)` descendant `d''`. By the structural argument applied directly to `d''` at the outset (which only uses M0 and Prefix)..."

**Problem**: The inductive step explicitly notes it applies the structural argument "directly to d'' at the outset", invoking M0 + Prefix + zero-count balance — the same machinery used in the base case. The induction hypothesis is never consumed. The proof at depth `q+1` does not depend on the proof at depth `q`; each depth's argument is independent. This is induction in form only.

**Required**: Drop the induction and prove directly: "For any descendant `d'` at any depth `q ≥ 1`, the structural form (i)–(iii) follows from M0 + Prefix + zero-count balance; the position-`#d_0 + 1` comparison then yields chain element above `s ⊕ ℓ`." Same treatment for the ancestor case. The induction adds verbosity without rigor.

### Issue 3: K.δ remark hand-waves subsumption by LP8

**ASN-0098, *Remark on K.δ***:
> "The K.δ-IsDocument case creates a new document `d_new` with `M'(d_new) = ∅`, which is the same scenario as LP8 above; in this ASN's reference frame K.σ (ASN-0093) is the document-registration operation, and K.δ-IsDocument is subsumed by the LP8 argument."

**Problem**: LP8 is formally stated for K.σ transitions specifically. K.δ-IsDocument is a distinct operation in ASN-0047's vocabulary. The remark says it "is subsumed" without indicating whether (a) K.δ-IsDocument is aliased to K.σ in this reference frame, (b) both coexist and the lemma must be restated for K.δ-IsDocument, or (c) the reference frame uses K.σ exclusively and K.δ-IsDocument is excluded. The "ASN-0047 transition-model frame layered over the ASN-0093 allocation substrate" framing leaves this ambiguous.

**Required**: Either generalize LP8's statement to cover both K.σ and K.δ-IsDocument explicitly, or clarify in the working reference frame which document-registration operation is canonical (and what happens to the other).

### Issue 4: Cross-chain achievability setup assumes specific span-endpoint chain

**ASN-0098, *Same document, cross subspace***:
> "The span is built on `A_C(d_0)`'s chain, so `s` carries `s_C` at position `#d_0 + 2` (by the structural form `s = [d_0, 0, s_C, k_s]`)."

**Problem**: The tightness condition's first conjunct only requires `s ∈ dom(Σ_e.C) ∪ dom(Σ_e.L)`. Every such `s` is indeed on some `A_C(d)` or `A_L(d)` chain by C1c/L1c, but the case enumeration silently fixes `s ∈ A_C(d_0)` and adds the symmetric `A_L(d_0)` case in a single inline sentence. The four-case structure (same-chain, same-doc cross-subspace, non-nesting, descendant, ancestor) is enumerated against *interfering* chains, parameterised by relation to a single `d_0`, but the *span endpoint's* chain choice is left implicit. Combined with Issue 1's ordinal-displacement assumption, the achievability argument's scope is more constrained than the prose admits.

**Required**: Make the case structure explicit: "Fix `s ∈ A_C(d_0)`'s chain (the canonical case); the symmetric case for `s ∈ A_L(d_0)` follows by exchanging `s_C ↔ s_L` throughout. Within the canonical case, interference splits by interfering chain as follows..." Then enumerate. Without this, the reader cannot tell whether the four cases exhaust interference or only a slice.

### Issue 5: Tightness predicate's universal quantifier over infinite F

**ASN-0098, *Boundary and Width Behaviour***:
> "`F` is countably infinite. ... Nonetheless, the quantifier is decidable by structural analysis... The proofs that follow consult `F` only through structural analysis of candidate forms, never via enumeration."

**Problem**: The tightness predicate `(A t ∈ F : s ≤ t < s ⊕ ℓ : t ∈ dom(Σ_e.C) ∪ dom(Σ_e.L))` is the second conjunct of the tightness definition. The ASN argues for decidability but does not establish that the *finitely-many candidates* claim ("only those `(d, s, k)` triples whose lex position falls within the interval need be examined") is a theorem. For each span `(s, ℓ)`, prove explicitly that `F ∩ [s, s ⊕ ℓ)` is finite — this requires showing that document tumblers with chain elements falling in the interval are bounded in length (since longer documents place chain elements at higher lengths, eventually exceeding `s ⊕ ℓ`) and bounded in component values (T1 case (i) bounds at the divergence position).

**Required**: Add a finitude lemma: `(A s, ℓ : (s, ℓ) satisfies T12 : |F ∩ [s, s ⊕ ℓ)| < ∞)`, with explicit argument. Without this the tightness predicate is well-defined but its decidability claim is not discharged.

### Issue 6: LP9 K.μ⁺_L freshness derivation duplicates ASN-0047 effect-clause work

**ASN-0098, LP9 proof, K.μ⁺_L sub-case**:
> "After K.μ⁺_L fires, K.μ⁺_L's effect clause (ASN-0047) directly states `dom(Σ'.M(d)) = dom(Σ.M(d)) ∪ {v_ℓ}` and `v_ℓ ∉ dom(Σ.M(d))` (the latter discharged within ASN-0047 by a per-subspace verification, summarised in the next sentence)..."

**Problem**: The proof says ASN-0047's effect clause "directly states" `v_ℓ ∉ dom(Σ.M(d))`. Checking ASN-0047's K.μ⁺_L Effect: it states `dom(M'(d)) = dom(M(d)) ∪ {v_ℓ} ⊃ dom(M(d))` — the strict containment `⊃` is the freshness commitment, but ASN-0047 does not prove it within the effect clause itself; the proof must come from somewhere. The ASN then proceeds to provide the proof via D-MIN★/D-CTG★/TS4/SC-NEQ. This is the right work to do, but the framing ("summarised in the next sentence") misleads — the next sentences are the proof, not a summary. Either ASN-0047 owns this proof and ASN-0098 cites it, or ASN-0098 owns it and frames it as its own derivation. The current phrasing splits responsibility ambiguously.

**Required**: Rewrite the LP9 K.μ⁺_L paragraph to either (a) cite a specific ASN-0047 lemma that discharges `v_ℓ ∉ dom(M(d))` and skip the in-line derivation, or (b) own the derivation explicitly: "K.μ⁺_L's effect clause asserts `dom(Σ'.M(d)) = dom(Σ.M(d)) ∪ {v_ℓ}`; we discharge the strict containment via..."

### Issue 7: Worked trace's e₂ construction not exhibited

**ASN-0098, *A Worked Trace***:
> "consider slot 2 of the link, with endset `e₂` chosen so that `coverage(e₂) ∩ ran(Σ_1.M(d₁)) = {i₁}` — only the I-address `i₁` from `d₁`'s current range lies in this slot's coverage (admissible by L4 of ASN-0043...)"

**Problem**: The worked trace's slot-2 illustration relies on an `e₂` whose construction is not exhibited. The reader must take on faith that such an `e₂` exists. For a worked trace whose purpose is to make displacement concrete, the endset should be displayed explicitly (e.g., `e₂ = {(i₁, [0, ..., 0, 1])}` of appropriate length).

**Required**: Exhibit a concrete span for `e₂` and verify the intersection claim, so the trace is self-contained against ASN-0058's PrefixSpanCoverage / T12.

### Issue 8: "F" definition uses notation that elides T4-validity check

**ASN-0098, *Boundary and Width Behaviour***:
> "`F = {a ∈ T : (E d ∈ T, s ∈ {s_C, s_L}, k ≥ 1 :: zeros(d) = 2 ∧ d satisfies T4 ∧ a = [d, 0, s, k])}`"

**Problem**: The definition does not include `a satisfies T4` as a witness condition. By inspection `a = [d, 0, s_C, k]` with `s_C = 1` and `k ≥ 1` is T4-valid when `d` is, but this is asserted without derivation. State the T4-validity of `a` as a postcondition of F's structural form, with the verification (zero count 3, no adjacent zeros given `d`'s field structure, first component nonzero from `d_1 ≠ 0`, last component `k ≥ 1`).

**Required**: Either add `a satisfies T4` as a derived postcondition with its proof, or cite ASN-0093's StoreT4Validity / chain-element-T4-validity lemma as the source.

### Issue 9: LP4 hypothesis `Σ'.M(d) = Σ.M(d)` requires both `d ∈ dom(Σ.M)` and `d ∈ dom(Σ'.M)`

**ASN-0098, LP4**:
> "for every endset `e`, and every document `d ∈ dom(Σ.M)`: `Σ'.M(d) = Σ.M(d) ⟹ project(e, d, Σ') = project(e, d, Σ)`"
> "The hypothesis `Σ'.M(d) = Σ.M(d)` requires `d ∈ dom(Σ'.M)` for the equation to be parseable; this is automatically satisfied because `d ∈ dom(Σ.M)` together with M1 (ASN-0093) gives `d ∈ dom(Σ'.M)`..."

**Problem**: The note correctly identifies that `d ∈ dom(Σ'.M)` is needed to parse the hypothesis, but cites M1 of ASN-0093 (`dom(M) ⊆ dom(M')` across transitions). LP4 quantifies over arbitrary transitions including K.μ⁻, K.μ~, etc. — none of these remove documents from `dom(M)`, so the citation is correct. But the reasoning would fail if a future operation removed documents. State this as a frame condition assumption explicitly: "LP4 assumes the reference frame's transitions all satisfy `dom(M) ⊆ dom(M')`," so the lemma's robustness is auditable when the frame changes.

**Required**: Either restate LP4 with an explicit `d ∈ dom(Σ.M) ∩ dom(Σ'.M)` precondition (cleaner, no frame assumption), or document the M1 dependency as load-bearing on the reference frame's monotonicity.

### Issue 10: Range of `subspace(v)` in LP20 corollary not fully bounded

**ASN-0098, LP20**:
> "Split by V-position subspace, the corollary refines to: `{Σ.M(d)(v) : v ∈ project(e, d, Σ) ∧ subspace(v) = s_C} ⊆ coverage(e) ∩ dom(Σ.C)` ... `{Σ.M(d)(v) : v ∈ project(e, d, Σ) ∧ subspace(v) = s_L} ⊆ coverage(e) ∩ dom(Σ.L)`"

**Problem**: The split assumes the two subspaces partition `project(e, d, Σ)`. This rests on S3★-aux (SubspaceExhaustiveness) — every `v ∈ dom(Σ.M(d))` has `subspace(v) ∈ {s_C, s_L}`. The proof cites S3★-aux but does not explicitly state that together with S3★ and the exhaustiveness, the union of the two subset equations covers the entire projection (i.e., the corollary is partition-complete, not just per-subspace). Without this, the corollary is informative but doesn't fully describe the projection's range.

**Required**: Add a clause stating the partition-completeness: `{Σ.M(d)(v) : v ∈ project(e, d, Σ)} = {... ∧ subspace(v) = s_C} ∪ {... ∧ subspace(v) = s_L}`, with brief derivation from S3★-aux.

## OUT_OF_SCOPE

### Topic 1: Decidability and finite-representation algorithms for `project`

The ASN defines `project` as a set comprehension consulting `Σ.M(d)`. Whether `project` is computable in finite time (it is, when `dom(Σ.M(d))` is finite by S8-fin), how to enumerate it efficiently, and what representation a runtime should use are implementation concerns. The ASN appropriately leaves these out.

### Topic 2: Inverse-projection / discovery query semantics

The first open question — "What invariants must a reverse-discovery primitive preserve when, given a V-position in some document, it returns the set of links whose projections contain that V-position?" — is explicitly out of scope and belongs in a future ASN on link indexing or discovery.

### Topic 3: V-order preservation under K.μ~

The third open question — whether V-order of projected positions reflects I-order under arrangement-shape conditions — is a refinement of LP11's bijection-based displacement claim and belongs in a future ASN on arrangement geometry.

### Topic 4: Type-endset semantics

The introductory note explicitly excludes link type semantics. The ASN's slot-3 mention (LP3, L3 reference) is purely structural; semantic interpretation of types is correctly deferred.

VERDICT: REVISE
