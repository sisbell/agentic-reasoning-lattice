# Cone Review — ASN-0036/S5 (cycle 3)

*2026-04-13 15:42*

I'll read through the ASN systematically, tracking definitions, quantifier scopes, and cross-property dependencies.

<tool_call>
<tool_name>Read</tool_name>
<parameters>
<file_path>/Users/shane/Documents/github/claude/xanadu-spec/vault/project-model/ASN-0036/formal-statements.md</file_path>
</parameters>
</tool_call>

<tool_call>
<tool_name>Glob</tool_name>
<parameters>
<pattern>vault/project-model/ASN-0036/**/*</pattern>
</parameters>
</tool_call>

<tool_call>
<tool_name>Glob</tool_name>
<parameters>
<pattern>vault/project-model/ASN-0034/**/*</pattern>
</parameters>
</tool_call>

---

### S3 weakest-precondition formula shifts from pre-state to post-state between narrative and proof
**Foundation**: (internal — foundation ASN)
**ASN**: S3 narrative: "The weakest precondition for S3 under an operation that adds a V-mapping M(d)(v) = a is: wp(add-mapping, S3) ⟹ a ∈ dom(Σ.C)" — S3 proof Case 2: "This is precisely the weakest precondition identified above: wp(add-mapping, S3) ⟹ a ∈ dom(Σ'.C)"
**Issue**: The narrative derives `a ∈ dom(Σ.C)` — a pre-state condition, which is what a weakest precondition should be. It then carefully distinguishes the atomic case: "An operation that atomically creates content at a and adds the mapping… satisfies S3 in the post-state without sequential precedence — a ∈ dom(Σ'.C)." The proof's Case 2 then collapses both cases, writing `a ∈ dom(Σ'.C)` (post-state) and claiming "this is precisely the weakest precondition identified above." It is not the same formula: `Σ.C` ≠ `Σ'.C`. For mapping-only operations (where `C' = C`), the two coincide; for operations that atomically create content, `a ∈ dom(Σ'.C)` can hold when `a ∉ dom(Σ.C)` — the post-state formula is strictly weaker. The proof also misapplies wp terminology: the condition `a ∈ dom(Σ'.C)` is a post-state verification obligation, not a weakest precondition (which by definition is a pre-state predicate). The formal contract correctly states the general post-state obligation ("ensures a ∈ dom(Σ'.C) in the post-state"), so the contract is right and the proof's cross-reference to the narrative's wp is wrong.
**What needs resolving**: The proof's Case 2 should cite the formal contract's per-operation post-state obligation rather than the narrative's wp formula. The claim "this is precisely the weakest precondition identified above" must be removed or corrected — it equates formulas over different state scopes (`Σ.C` vs `Σ'.C`) and misapplies the term "weakest precondition" to a post-state condition.

---

### AX-1 is a system-level axiom embedded inside S3's formal contract
**Foundation**: (internal — foundation ASN)
**ASN**: S3 formal contract: "AX-1 (initial empty state — dom(Σ₀.C) = ∅, dom(Σ₀.M(d)) = ∅ for all d)." S5 formal contract: "AX-1 (initial empty state) provides the starting state Σ₀." S5 proof: "By AX-1, dom(Σ₀.M(d)) = ∅ for all documents d, and dom(Σ₀.C) = ∅."
**Issue**: AX-1 defines the initial state of the entire system — both content store and arrangement components. It is used by S3 (induction base case) and S5 (construction starting point). Yet its authoritative definition appears only inside S3's formal contract as a precondition. S5 references AX-1 by name but abbreviates it to "initial empty state" without restating both conjuncts (`dom(Σ₀.C) = ∅` and `dom(Σ₀.M(d)) = ∅`). This creates two problems: (1) S5 is implicitly coupled to S3's contract structure — if S3's contract is refactored, AX-1's definition moves or disappears, breaking S5's foundation; (2) a reader examining only S5's formal contract sees "AX-1 (initial empty state)" with no indication that it specifies content-store emptiness, not just arrangement emptiness. The initial-state specification is a system-wide commitment that both properties depend on independently.
**What needs resolving**: AX-1 should be a standalone axiom — defined once at the ASN level (not inside any property's contract), with its full content (`dom(Σ₀.C) = ∅` and `dom(Σ₀.M(d)) = ∅` for all `d`) stated in the definition. S3 and S5 should both cite it by reference, not one defining and the other abbreviating.

---

### S5 sketch misstates the number of states in the constructed trace
**Foundation**: (internal — foundation ASN)
**ASN**: S5 motivational sketch: "We construct an execution trace of N + 2 states beginning at Σ₀: first a content-creation transition that introduces an I-address a, then N + 1 arrangement-extension transitions." S5 formal proof: "We construct an execution trace σ_N = ⟨Σ₀, Σ₁, Σ₂, …, Σ_{N+2}⟩ comprising N + 2 transitions."
**Issue**: The sketch says "N + 2 states." The construction has 1 content-creation transition + (N + 1) arrangement-extension transitions = N + 2 transitions, requiring states Σ₀ through Σ_{N+2} — that is, N + 3 states. The formal proof correctly counts "N + 2 transitions"; the sketch's "N + 2 states" is off by one. The error is confined to the motivational paragraph; the formal proof, constructions, and verifications all use the correct count.
**What needs resolving**: The sketch should say "N + 3 states" or (more naturally) "N + 2 transitions."

## Result

Cone not converged after 3 cycles.

*Elapsed: 3212s*
