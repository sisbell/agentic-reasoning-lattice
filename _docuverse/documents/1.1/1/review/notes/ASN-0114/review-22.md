# Review of ASN-0114

The mathematics here is sound. I checked F1's satisfiability (the endset is its own witness — correct), the two collapses against ASN-0053's S2 (both biconditionals hold, each `⟹` is S2's contrapositive — correct), the F2 disconnectedness argument against S0 convexity (correct), the F5 derivation's use of L12+LP13 to cross the reflexive-transitive closure (correctly composed — they did not pretend L12 alone suffices), and the worked instance (the disconnection witness `a₃ < a₅ < a₇` with `a₅ ∉ coverage(e₁)`, the `δ(2,#a₃)` shift to `a₅`, and the `F`-restriction via LP-Fin all check out). The empty/invalid distinction (F7) is the genuinely load-bearing claim, and surfacing that the one real implementation collapses it (Q17) is exactly the kind of obligation an abstract spec exists to expose. No case is missing: `a ∉ dom(L)`, `i < 1`, `i > N`, empty slots 1/2/>3, and the non-empty type slot 3 are all handled.

The findings below are anti-bloat: accumulated meta-prose, with one clear forward-reference instance of the kind this review mode targets.

## REVISE

### Issue 1: A relation-reading convention forward-referenced into the collapses paragraph

**ASN-0114, "The substrate we build on"**: "The first collapse also fixes the reading of `R = ⟨⟩` when `R` stands for the coverage-relation rather than a single span-set: it abbreviates `coverage(R) = ∅`, which is well-defined on the relation."

**Problem**: This sentence sits in the substrate section, where the collapses are first stated — *before* F0, and before "`followlink` as a relation" has been introduced at all. It references "`R` stands for the coverage-relation," a framing that is not established until the later paragraph "Status of the result — a relation, determinate up to coverage" (which appears after F0, in the next section). So it is both premature (it explains how to read a notion the reader has not yet met) and a duplicate of that later paragraph, which fully develops the relation reading and the two single-value collapse cases. This is precisely the forward-reference accretion the review mode flags: the relation-reading convention has migrated upstream into the collapses paragraph instead of living once at its proper home.

**Required**: Cut the sentence from the collapses paragraph — that paragraph should state only the two biconditionals (`coverage(R) = ∅ ⟺ R = ⟨⟩` and `coverage(e) = ∅ ⟺ e = ∅`) and how each direction is discharged. Let the relation reading and its single-value collapse cases live solely in "Status of the result."

### Issue 2: F4's frame restates itself

**ASN-0114, F4 (PureRead)**: "…the content store `Σ.C`, the link store `Σ.L`, every arrangement `Σ.M(d)`, and **every other endset of the queried link are identical before and after.** In particular, requesting end `i` of link `a` changes neither `Σ.L(a)` itself, **nor any `Σ.L(a).eⱼ` for `j ≠ i`**, nor any document the selected end points into."

**Problem**: The first sentence already asserts `Σ.L` and "every other endset of the queried link" unchanged. The "In particular" sentence then re-asserts exactly that — `Σ.L(a)` and `Σ.L(a).eⱼ` for `j ≠ i` are both entailed by "`Σ.L` identical," and "any document the selected end points into" is entailed by "every arrangement `Σ.M(d)`" plus "`Σ.C`." The clause "nor any `Σ.L(a).eⱼ` for `j ≠ i`" is the same fact as "every other endset of the queried link are identical," one sentence apart. Two sentences saying the same thing.

**Required**: State the frame once. "The post-state equals `Σ`" plus the component list is sufficient; the "In particular" sentence adds no content (write-side confinement of the other ends already follows from `Σ.L` unchanged, and read-side confinement is F6's job). Drop it.

### Issue 3: The `coverage(R) := ⟦R⟧` bridge over-justifies a definitional synonym

**ASN-0114, "The substrate we build on"**: "extending `coverage` to a span-set `R` by the bridging definition `coverage(R) := ⟦R⟧`. The extension is faithful: `coverage(e)` unions the position sets over the spans of an endset (a set), `⟦R⟧` unions them over the spans of a span-set (a sequence), and both reduce to the *same* union over the *same* spans… An equality `coverage(R) = coverage(eᵢ)` is then well-typed…"

**Problem**: ASN-0053's `⟦R⟧` already denotes a span-set's position set, and `⟦R⟧ = coverage(eᵢ)` is *already* well-typed (a subset of `T` on each side) — the stated motivation ("then well-typed") does not require the synonym, since the un-bridged form was never ill-typed. The bridge buys only cosmetic `coverage`-on-both-sides symmetry, at the cost of a definition plus a faithfulness sentence. (I credit the F3-section rationale that coverage is "the semantically load-bearing projection," which is why this is Issue 3 and not Issue 1 — but the faithfulness justification is the avoidable surplus.)

**Required**: Either drop the synonym and write F1/F2/the first collapse with `⟦R⟧`, or keep the synonym as a bare one-line definition and delete the faithfulness justification (the equality of the two unions is immediate and need not be argued).

## OUT_OF_SCOPE

### Topic 1: Resolution shrinkage and the recorded-end vs. resolved-end boundary
**Why out of scope**: I checked whether F1's "exactness" must account for the implementation's V-position filtering (Q11, Q15, Q20), which can return *fewer* positions than the recorded end covers. The ASN correctly isolates this as *resolution* — a separable operation it scopes out — and F1's exactness is exactness to what the link *records*, invariant by F5. This boundary is handled correctly; the shrinkage belongs to the resolution ASN, and the Open Questions already point there. No defect.

META: not warranted — the ASN defines an operation by precondition (F0), postcondition (F1), frame (F4), and invariants (F5–F8), each stated abstractly enough to bind an alternative implementation; the implementation mechanics appear only as labeled corroboration, never as the contract.

VERDICT: REVISE
