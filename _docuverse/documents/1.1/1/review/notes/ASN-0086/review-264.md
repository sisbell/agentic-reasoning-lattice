# Review of ASN-0086

I read the note in full and checked each property's proof against its preconditions, the operation contracts (Emit_K, Observe_K, Nullify), the boundary cases (first vs. subsequent emission, self-emit target, empty link store, higher-arity links), and the two weakest-precondition derivations. I also verified every cross-ASN citation resolves to a foundation (0034, 0036, 0040, 0043, 0093) and checked the worked sketch's arithmetic.

## REVISE

No REVISE items. Detail on the checks that could have produced them:

- **R0a (FlatLinkDomain)** — both cases sound. Cross-home: `zeros(a') = zeros(a) + zeros(w)` with `zeros(w) = 0` (L1) forces the three zeros of `a'` to coincide positionally with `a`'s, giving `home(a') = home(a)`, contradicting `d' ≠ d`. Same-home: (UL) + T3 close it. No circularity (R0a → L-ContiguousPrefix → ChainMembershipForOrigin; R-Scope/wp → R0a).
- **R-Scope (SingleTupleScope)** — P1 branch uses R0a at Σ; self-emit branch correctly switches to R0a at Σ' (since `a ∉ dom(Σ.L)`). Arity-independence justified (consults only the prefix + antichain). Case split exhaustive.
- **wp Case 1 and Case 2** — both derivations establish necessity and sufficiency. Case 2's third conjunct is genuinely a Σ-state predicate (finitely checkable over `L_R^Σ`), and the `a_emit ∉ coverage(G)` escape branch is shown non-redundant and instantiated concretely in Step 4. The reduction `postcondition ⟺ a ∈ A_rel^{Σ'}` (Case 1) and `⟺ a ∉ nullified(Σ')` (Case 2) are correct.
- **Discipline-discharge induction (Three Operations)** — case split over `→`-steps (K.σ/K.α, Emit_K at K≁R, higher-arity K~R, arity-3 K~R) is exhaustive; the only `L_R`-growing kind is routed to Nullify by the layer's discipline commitment without circularity.
- **CoverageEqualityDecidable** — the empty-gap-skip / nonempty-cell-representative argument is complete; the `c_k.0` immediate-successor step is grounded in the foundation (T1 case (ii)).
- **Worked sketch** — `a₁ = 1.0.1.0.1.0.2.1` parses to `home = d`, `E₁ = s_L`, chain elements `a₁,b₁,a₂,b₂,a₃` are consistent with the `inc(·,0)` recurrence and T1 ordering; the active/audit divergence at Σ₁ and the self-nullification at Σ₄ check out.

Anti-bloat sweep: no meta-prose obstructed reading. Justifications (e.g., RetractionType's L9 clause, RetractionDirectionality's L7 clause) advance the meaning of the construct rather than re-explaining why an axiom is needed; forward pointers are not duplicated deferrals; no use-site inventories or document-ordering apologetics remain. Prior accretion appears already trimmed.

## OUT_OF_SCOPE

### Topic 1: Multi-arity typed relations and cross-layer retraction survival
The Open Questions (binary projections of `|Σ.L(a)| > 3` links, `Nullify(b)` for `b ∈ L_R`, cross-layer discipline for R6a/R6c) are correctly deferred — they introduce machinery beyond this note's standard-triple `L_K` and single substrate layer.

### Topic 2: Concurrency/atomicity model for Observe vs. Emit
Whether `A_K` transitions are observed atomically is a consistency-model question for a future ASN, not a gap here (this note's `→` is the sequential ASN-0093 transition relation).

VERDICT: CONVERGED
