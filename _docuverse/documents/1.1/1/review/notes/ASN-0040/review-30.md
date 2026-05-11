# Review of ASN-0040

## REVISE

### Issue 1: B0a's "Equivalently" formulation has ambiguous quantifier scope

**ASN-0040, B0a (Baptismal Closure)**: "Equivalently, `(A Σ, Σ' : Σ → Σ' : Σ'.B = Σ.B ∨ Σ'.B = Σ.B ∪ {next(Σ.B, p, d)} for some (p, d) satisfying B6)` — every transition either leaves the registry unchanged or extends it..."

**Problem**: The "for some (p, d) satisfying B6" appears at the end without parens, leaving the existential's scope ambiguous — does it bind only the second disjunct or the entire disjunction? The intended reading is clearly the second, but the formal notation should reflect this.

**Required**: Rewrite as `(A Σ, Σ' : Σ → Σ' : Σ'.B = Σ.B ∨ (E (p, d) : B6(p, d) : Σ'.B = Σ.B ∪ {next(Σ.B, p, d)}))` to scope the existential inside the disjunct.

### Issue 2: Type invariant Σ.B ⊆ T justified informally relative to other invariants

**ASN-0040, "The baptismal registry" section**: "*Justification.* Σ.B is introduced as a state definition... Thereafter, the only mechanism that enlarges Σ.B is baptism (by B0a, Baptismal Closure)... ∎"

**Problem**: This is a one-paragraph informal induction, whereas the structurally identical invariants B_fin, B10, and B1 are each given explicit inductive proofs with labeled base case, inductive step, and case analysis on the transition class. The asymmetric treatment of an invariant of equal logical status weakens the proof legibility.

**Required**: Promote the Σ.B ⊆ T claim to a labelled invariant (e.g., B_type) with a base case (B₀ conf. gives B₀ ⊆ T), an inductive step partitioning by B0a's two transition classes, and explicit citations of TA5(c)/TA5(d) for membership in T under baptismal transitions.

### Issue 3: wp analysis is incomplete relative to the invariants the ASN must preserve

**ASN-0040, wp section**: addresses wp(baptize(p, d), B1) and wp(baptize(p, d), a ∉ B), with state precondition, environmental, and lemma decomposition.

**Problem**: The ASN advertises wp analysis as targeting "the invariants themselves" but covers only two. B10's preservation and B7's per-transition compatibility are both load-bearing for B1's inductive step but are absorbed silently into the preservation proofs. The reader cannot see whether the dependency analysis for B10 has the same structure as the one for B1.

**Required**: Add at least wp(baptize(p, d), B10) — state precondition (B10 at Σ, B6 from PRE), environmental (B0a so non-baptismal ops cannot insert non-T4 elements), lemma (TA5a). This makes the symmetry between B1 and B10 explicit and exposes B0a's necessity at the same level of detail.

### Issue 4: B9 quantifier conflates registry and state

**ASN-0040, B9 statement**: "`(A p, d : B6(p, d) : (A M ∈ ℕ : (E B' : B' reachable from Σ.B by a finite sequence of baptisms : hwm(B', p, d) ≥ M)))`"

**Problem**: "B' reachable from Σ.B" is loose — reachability in the framework defined at *State Space and Transitions* is between states (`→*` is on 𝒮), not between registry sets. The proof itself uses states Bₖ as registries indirectly, but the formal quantifier should range over states.

**Required**: Rewrite as `(A p, d : B6(p, d) : (A M ∈ ℕ : (E Σ' : Σ →* Σ' via baptisms : hwm(Σ'.B, p, d) ≥ M)))`, matching the state-level reachability defined in the framework.

### Issue 5: Bridge1's witness uniqueness is silently assumed in downstream usage

**ASN-0040, Bridge1**: "(E (p, d) satisfying B6 : Σ' = baptize(p, d)(Σ) ∧ a = next(Σ.B, p, d))"

**Problem**: Bridge1 states existence of a witnessing (p, d) but not uniqueness. The commentary that follows ("the inclusion `allocated(Σ) ⊆ Σ.B` is preserved at every transition") and the alignment with Bop's `Σ' = baptize(p, d)(Σ)` implicitly require the witness to be unique — otherwise an allocator extension could correspond to multiple incompatible baptismal operations. Uniqueness is derivable (B7 forces (p, d) for a given `a` to be unique among B6-valid pairs) but is not stated.

**Required**: Add an explicit uniqueness clause to Bridge1 — "the witnessing (p, d) is unique" — and a one-line proof citing B7's namespace disjointness: any two B6-valid pairs with a common stream element coincide.

## OUT_OF_SCOPE

### Topic 1: Concrete content of B₀ beyond ASN-0034's mandated root
**Why out of scope**: B₀ conf. specifies structural conditions; the seed contents are deferred to the activation-discipline ASN through Bridge2, which is explicitly forward.

### Topic 2: Implementation of B4's atomicity (locking, transactions, single-threaded dispatch)
**Why out of scope**: B4 is a specification-level constraint on Op; the mechanism is a future ASN's concern.

### Topic 3: Convergence guarantees for distributed baptism
**Why out of scope**: Listed in Open Questions; the present ASN does not commit to a distributed model.

VERDICT: REVISE
