# Regional Review — ASN-0034/T4a (cycle 3)

*2026-04-22 01:20*

### T4's prose description of T4a's proof method doesn't match T4a's actual proof
**Foundation**: structural — proof descriptions should accurately characterize the proof they reference
**ASN**: T4 main text: "**T4a (SyntacticEquivalence)** proves that the field-segment constraint is equivalent to the condition that every field segment of `t` is non-empty. Proved in `T4a.md` by case analysis on `k = zeros(t) ∈ {0, 1, 2, 3}`."
**Issue**: Two problems. (1) T4a's proof is inlined in this ASN, not located in an external `T4a.md` — the file reference is stale or fictitious. (2) T4a's actual proof structure is Forward / Reverse, each subdivided into *first segment*, *last segment*, *interior segments* — not a case analysis on `k`. The reader told to expect case analysis on `k ∈ {0,1,2,3}` finds a structurally different proof.
**What needs resolving**: Either rewrite the description to match T4a's actual proof structure (Forward/Reverse on positional conditions vs. segment non-emptiness), or drop the external-file reference, or reorganize T4a's proof to match the described structure.

### Pairwise distinctness of `0, 1, 2, 3` not established by the axioms in scope
**Foundation**: NAT-zero (0 ∈ ℕ, 0 ≤ n), NAT-discrete (m < n → m+1 ≤ n), NAT-order (strict total order with `≤` derived)
**ASN**: T4c Injectivity: "The values `0, 1, 2, 3` are pairwise distinct in ℕ (NAT-order trichotomy)…". T4c Exhaustion: "so `zeros(t) ∈ {0, 1, 2, 3}`".
**Issue**: Trichotomy says that for any `m, n ∈ ℕ` exactly one of `m < n`, `m = n`, `n < m` holds — it does not determine *which one* holds for the specific numerals `0, 1, 2, 3`. Nothing in NAT-zero, NAT-discrete, or NAT-order rules out a model in which `0 = 1` (e.g. ℕ = {0} interpreting `n + 1 = 0`). To get `0 < 1 < 2 < 3` (hence four distinct elements), one needs at minimum an axiom like `n < n + 1` or `n ≠ n + 1`. Absent such an axiom, Exhaustion's four-element set and Injectivity's pairwise-distinctness both lack foundation.
**What needs resolving**: Either add an axiom providing successor-distinctness (`n < n + 1`, or equivalently `n ≠ n + 1` on ℕ), or recast T4c so it does not depend on the numerals `0, 1, 2, 3` being four distinct ℕ elements (e.g., treat the label-assignment without a finite-set enumeration).

### T4b over-cites T4c: the level→field-set mapping is introduced in T4b, not supplied by T4c
**Foundation**: T4c's stated postcondition — label assignment `(zeros(t) = k ↔ t is a {node,user,document,element} address)`
**ASN**: T4b prose: "T4c labels a T4-valid `t` *node*, *user*, *document*, or *element* according as `zeros(t) = 0, 1, 2, 3`; the field set at each level is `{N}`, `{N, U}`, `{N, U, D}`, `{N, U, D, E}` respectively; and field `X ∈ {N, U, D, E}` is *absent in `t`* iff `X` is not in the field set of `t`'s level." T4b Depends: "T4c (LevelDetermination) — supplies the hierarchical level assignment from which field absence is defined."
**Issue**: T4c supplies only the label-from-zero-count biconditionals. The level→field-set mapping (`node → {N}`, `user → {N,U}`, etc.) is introduced inside T4b itself, with no basis in T4c. Once that mapping is in hand, "absence" collapses to "`zeros(t) < position of X in (N,U,D,E)`" — a statement about `zeros(t)` directly, with T4c's labels playing no load-bearing role. The dependency claim misstates what T4c contributes; the field-set mapping is either T4b's own definition (in which case T4c need not be a dependency) or it belongs in T4c's statement (in which case T4c's current statement is incomplete).
**What needs resolving**: Either move the level→field-set mapping into T4c's statement (making T4c a genuine supplier of what T4b uses), or define absence in T4b directly in terms of `zeros(t)` without the T4c detour and remove T4c from T4b's Depends.

### "Field separator" defined inconsistently as component vs. position
**Foundation**: T4's own stipulations
**ASN**: T4 prose (hierarchical structure section): "Define a *field separator* as a component with value zero." T4 Axiom: "T4 stipulates that a position `i` of `t` is a *field separator* iff `tᵢ = 0`." T4 final paragraph: "zero components are field separators and non-zero components are field components."
**Issue**: The prose identifies the *component* (the zero value at some index) as the field separator; the Axiom identifies the *position* (the index `i` where `tᵢ = 0`) as the field separator. These are different objects — a component is a value in ℕ, a position is an index in `{1, …, #t}`. Downstream text shifts between "separator position" (T4b's "separator positions are exactly recoverable") and "zero component" (T4 final paragraph) without a bridge.
**What needs resolving**: Pick one of "component with value zero" or "position with zero-valued component" as the definition of *field separator* and conform all uses to it (or introduce two distinct terms — e.g., *separator component* vs. *separator position*).

### T4 frames T4a, T4b, T4c as parallel postconditions but they are mutually dependent
**Foundation**: structural — postconditions of a claim should be consequences of that claim, not of each other
**ASN**: T4 Formal Contract Postconditions: "T4a (SyntacticEquivalence): … T4b (UniqueParse): … T4c (LevelDetermination): …". T4b Depends: lists both T4a and T4c. T4c Depends: lists T4 only.
**Issue**: T4 presents T4a, T4b, T4c as a triple of postconditions on equal footing. But the dependency structure is not parallel: T4b depends on both T4a *and* T4c, and T4c in turn is cited by T4b for its absence definition. Readers navigating T4's postcondition slot find three named consequences with no indication that one (T4b) is built on top of the other two.
**What needs resolving**: Either reorganize T4's postconditions to reflect the actual dependency order (e.g., T4a and T4c as direct consequences of T4, with T4b marked as a downstream theorem combining them), or promote T4b to a separate claim that is not in T4's postcondition slot.

### T4 Axiom's canonical form contradicts itself for low zero counts
**Foundation**: T4's own Axiom
**ASN**: T4 Axiom: "A T4-valid address tumbler has the canonical written form `t = N₁. ... .Nₐ . 0 . U₁. ... .Uᵦ . 0 . D₁. ... .Dᵧ . 0 . E₁. ... .Eδ` where `0 < Nᵢ, 0 < Uⱼ, 0 < Dₖ, 0 < Eₗ` at every position, with only the first `zeros(t) + 1` field segments present."
**Issue**: The written form displays three literal `.0.` separators and four field segments. The trailing qualifier "with only the first `zeros(t) + 1` field segments present" contradicts what the form shows: if `zeros(t) = 0`, the canonical form has zero separators and one segment, which cannot be read off the displayed template without discarding both the `.0.` separators and the trailing fields. A precise reader cannot determine whether the display is (a) a single canonical form with optional tail truncation, or (b) a family of four distinct canonical forms, one per zero count. The relationship between the displayed form and the `zeros(t) + 1` qualifier is not specified.
**What needs resolving**: Either restate the canonical form as four explicit cases keyed to `zeros(t) ∈ {0, 1, 2, 3}`, or state the truncation rule formally (e.g., "when `zeros(t) = k`, the canonical form ends at the `k+1`-th field segment, omitting the remaining separators and fields").
