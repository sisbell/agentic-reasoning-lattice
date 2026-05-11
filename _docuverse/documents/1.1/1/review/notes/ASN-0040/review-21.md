# Review of ASN-0040

## REVISE

### Issue 1: B₀ non-emptiness justification is inconsistent with the deferred parent prerequisite

**ASN-0040, B₀ conf. prose**: "Non-emptiness is required because with B₀ = ∅ the conformance conditions hold vacuously but no parent exists to anchor any baptism — the system cannot grow."

**Problem**: The argument presumes the parent prerequisite (p ∈ Σ.B required for baptism under p), which is explicitly deferred to the Open Questions. Under the current spec, Bop requires only B6(p, d) and B4 — neither asks p ∈ Σ.B. So a system starting from B₀ = ∅ can baptize any B6-valid (p, d) and grow normally. The "no parent to anchor" claim therefore does not hold in the spec as written.

**Required**: Either (a) justify non-emptiness on different grounds (e.g., "to anchor the field-hierarchy at a known root, even though formally permissible without"), (b) admit B₀ = ∅, or (c) tighten Bop's preconditions to require p ∈ Σ.B and remove the deferral.

### Issue 2: The unconditional inclusion allocated(Σ) ⊆ Σ.B is asserted but not derived

**ASN-0040, relationship-to-ASN-0034 paragraph**: "One inclusion holds unconditionally: allocated(Σ) ⊆ Σ.B — every address realized by an activated allocator is baptized at the moment of commitment, because Bop's postcondition adds exactly that address to Σ.B and B0a forbids any non-baptismal mechanism from enlarging Σ.B."

**Problem**: The supplied argument shows the converse direction (whatever enters Σ.B does so via Bop). It does not establish that every ASN-0034 allocator realization — a (T1) sibling increment or (T2) child spawn — produces a Bop transition. If ASN-0034's transition vocabulary Σ and ASN-0040's Op are independent, a (T1)/(T2) event could realize an address into `allocated(·)` without a corresponding Bop into Σ.B, breaking the inclusion. The argument needs the identification of (T1)/(T2) events with baptismal Bop transitions, which the ASN treats as implicit.

**Required**: Either make the identification explicit (a cross-ASN axiom asserting (T1)/(T2) ⊆ baptismal Op), or re-derive the inclusion under stated assumptions about the bridge between Op and Σ-transitions.

### Issue 3: The B0-from-T8 chain is incomplete as stated

**ASN-0040, paragraph preceding B0**: "T8 asserts allocated(Σ) ⊆ allocated(Σ') for every transition; under the conditional reverse inclusion Σ.B ⊆ allocated(Σ) this would yield Σ.B ⊆ Σ'.B."

**Problem**: To reach Σ.B ⊆ Σ'.B from Σ.B ⊆ allocated(Σ) and allocated(Σ) ⊆ allocated(Σ'), one additionally needs allocated(Σ') ⊆ Σ'.B — the *unconditional* inclusion at the successor state. The text names only the conditional reverse inclusion. A reader following the chain literally is stranded at allocated(Σ'), unable to land in Σ'.B without the unmentioned step.

**Required**: Spell the chain out: (1) Σ.B ⊆ allocated(Σ) [conditional, at Σ], (2) allocated(Σ) ⊆ allocated(Σ') [T8], (3) allocated(Σ') ⊆ Σ'.B [unconditional, at Σ'], ⇒ Σ.B ⊆ Σ'.B. Or drop the explanation, since B0 is taken as a standalone axiom regardless.

### Issue 4: B4 is miscast as a per-operation precondition in Bop's PRE

**ASN-0040, Bop**: "PRE: B6(p, d) — depth validity (defined below); B4 — serialized within namespace (p, d) (defined below)"

**Problem**: B4 is stated as a property of the transition vocabulary — each baptize(p, d) ∈ Op is a single atomic transition — not a fact a caller can establish or fail to establish on a per-call basis. Listing it alongside B6 (which the caller does choose) conflates two distinct categories of obligation: caller-side proof obligations and system-level structural assumptions.

**Required**: Separate the categories. Caller-side: B6(p, d). System-level structural assumption (or "frame"): B4 supplies single-edge semantics for each baptize(p, d). The phrasing "serialized within namespace (p, d)" is also misleading since B4 is unconditional and not namespace-scoped — namespace scoping enters only through B7's downstream consequence.

### Issue 5: B1's proof of preservation for non-target non-B6 namespaces does not present an exhaustive case structure

**ASN-0040, B1 preservation proof, "All other namespaces" branch**: The proof splits into three sub-cases: (B6-valid; non-B6 with stream entirely T4-invalid; non-B6 with T4-valid elements via stream identity).

**Problem**: The reader is not given an explicit enumeration of *which* non-B6 conditions land in which sub-case. The relevant taxonomy — d ∉ {1, 2}; zeros(p) + (d − 1) > 3; p violates T4 by interior defect; p violates T4 by trailing zero only with d = 2; p violates T4 by trailing zero only with d = 1 — is left for the reader to reconstruct. Without it, exhaustiveness is hard to verify, and the careful work in the "trailing zero, d = 1" branch reads as ad-hoc rather than as the unique residual case.

**Required**: Open the "other namespaces" branch with a one-paragraph enumeration of the four ways B6 can fail, mapping each to the sub-case that disposes of it. The current text contains all the ingredients; it just doesn't present them as a partition.

### Issue 6: B0a's "Equivalently" claim presumes every transition is op-associated, but this is established elsewhere

**ASN-0040, B0a closing**: "Equivalently, (A Σ, Σ' : Σ → Σ' : Σ'.B = Σ.B ∨ Σ'.B = Σ.B ∪ {next(Σ.B, p, d)} for some (p, d) satisfying B6) — every transition either leaves the registry unchanged or extends it by exactly the address that the corresponding baptismal operation would produce."

**Problem**: The equivalence between the partition formulation and the per-transition disjunction relies on "every transition is (Σ, op(Σ)) for some op ∈ Op" — supplied in the framework section, but not cited at the equivalence point. A skeptical reader who skipped the framework will not see the bridge.

**Required**: Add a parenthetical citation to the framework's transition definition at the "Equivalently" step, or restructure so the equivalence reads as a direct consequence of unfolding the framework's notion of →.

VERDICT: REVISE
