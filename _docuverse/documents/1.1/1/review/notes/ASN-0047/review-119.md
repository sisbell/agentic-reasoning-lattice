# Review of ASN-0047

## REVISE

### Issue 1: K.δ case (ii) k = 2 sub-case A "induction" framing is incoherent

**ASN-0047, K.δ case (ii) discharge, sub-case A**: "Induction on K.δ case (ii) k = 2 events activating account sub-allocators. Base case: the first K.δ case (ii) k = 2 event whose operand `t` is a node — either sub-case B (t a non-bootstrap node) or sub-case C (t = n₀)... Inductive step: every K.δ case (ii) k = 2 event with operand `t = account` (the present sub-case A)..."

**Problem**: The base case is over events spawning *account sub-allocators* (sub-cases B/C, operand = node), while the "inductive step" is over events spawning *document sub-allocators* (sub-case A, operand = account). These are categorically different events on different allocators. The "step" never inducts over a chain of sub-case A events — it just appeals once to a prior sub-case B/C event, with P1 preservation. This is not an induction; it is a direct preservation argument with a single prerequisite event.

**Required**: Either reframe as direct preservation ("the K.δ event that minted t placed t into `dom(A_account(parent(t)))`; P1 preserves the membership") or make the well-founded order explicit (e.g., induction on entity-tree depth, with sub-case C at depth 1, sub-case B at depth 1, sub-case A at depth 2).

### Issue 2: K.μ⁻ derived precondition `dom(M(d)) ≠ ∅` is not stated explicitly

**ASN-0047, K.μ⁻ amendment (Empty-arrangement boundary)**: "The effect clause `dom(M'(d)) ⊂ dom(M(d))` is itself unsatisfiable when `dom(M(d)) = ∅`... so the effect clause forces `dom(M(d)) ≠ ∅` as a derived precondition."

**Problem**: A precondition derived from effect-clause unsatisfiability is implicit. A specification reader checking "can K.μ⁻ fire here?" must reason about set-theoretic satisfiability of the effect clause rather than reading off a precondition list. This is the kind of operational reasoning the ASN avoids elsewhere.

**Required**: Add `dom(M(d)) ≠ ∅` as an explicit precondition of K.μ⁻ in the elementary transition definition, noting it follows from the effect clause's satisfiability.

### Issue 3: K.μ~ dependency chain misroutes S3★(Σ') through admissibility (ii)

**ASN-0047, Decomposition of K.μ~ (Dependency chain at a glance)**: "S3★(Σ') from K.μ~ admissibility clause (ii) → subspace preservation derived → link-subspace fixity Steps 1–3 → Step 4..."

But the verification matrix entry for S3★ under K.μ~ reads: "both clauses preserved via K.μ⁻ restriction + K.μ⁺ amendment alone (link-subspace fixity is downstream, not prerequisite)."

**Problem**: Admissibility clause (ii) is a *guard* the operation must satisfy — it cannot itself be the *source* of S3★(Σ'). The actual derivation routes through K.μ⁻ + K.μ⁺ decomposition (the "independent route" mentioned later). The chain header invites a circular reading where admissibility (ii) supplies what it's checking. The body text acknowledges the issue but does not fix the chain header.

**Required**: Reword the chain head to "S3★(Σ') established via K.μ⁻ + K.μ⁺ decomposition (independent route); admissibility clause (ii) is a redundant safety check satisfied by the same decomposition". Make the routing through admissibility (ii) a verification obligation, not a derivation source.

### Issue 4: Inconsistent P4 vs P4★ in worked examples

**ASN-0047, Worked example: interior content replacement**: "*P4 (Contains ⊆ R).* `Contains(Σ') ⊇ {(a₁, d), (a₂', d), (a₃, d), (a₄, d)}`; each pair is in R'..."

**Problem**: P4 is explicitly superseded by P4★ in the extended state (`Amendments to existing transitions` and elsewhere). The "fork with subsequent insertion" worked example correctly uses P4★/Contains_C. The interior content replacement example uses the superseded P4/Contains naming. Inconsistency confuses readers tracking which invariant is being checked.

**Required**: Replace "P4 (Contains ⊆ R)" with "P4★ (Contains_C ⊆ R)" and "Contains(Σ')" with "Contains_C(Σ')" throughout the interior content replacement example.

### Issue 5: Worked example fork verification omits S3★ link clause and L-invariants

**ASN-0047, Worked example: fork with subsequent insertion**: The Σ₂ verification lists J0, J1★, J1'★, J4, P4★, P7a, P8 — but omits explicit checks of S3★, L0, L1, L1a, L1b, L1c, L3, L14, L-fin, CL-OWN, CL-UNIQ.

**Problem**: While these invariants are vacuously satisfied at Σ₂ (since `dom(L₂) = ∅` makes link-related invariants vacuous, and only content-subspace V-positions exist), the verification should explicitly acknowledge this. A reader checking the example as a model for verification practice will not see how to handle these invariants in non-vacuous cases without referencing the third worked example (link allocation). At minimum, "L invariants vacuously satisfied since `dom(L₂) = ∅`" should appear.

**Required**: Add a brief catch-all verification line at the end of each post-state check noting which invariants are vacuously satisfied and which are inherited unchanged from frame conditions.

VERDICT: REVISE
