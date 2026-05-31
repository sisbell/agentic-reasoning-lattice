# Review of ASN-0043

## REVISE

### Issue 1: FSE carries a defensive parenthetical that restates the preceding argument and contrasts an unused technique
**ASN-0043, FSE — FreshSiblingExistence (proof)**: "(We need no CPP invocation here: the terminal-only modification of `inc(·, 0)` already settles every position that determines `home`, including the separator zero at `#home(a) + 1` that agreement on `1..#home(a)` alone would not pin.)"
**Problem**: The three sentences immediately preceding the parenthetical already establish exactly this: that `inc(·, 0)` modifies only the terminal position, that the separator zero at `#home(a) + 1` is non-terminal and therefore untouched, and that positions `1..#home(a)` are likewise fixed. The parenthetical adds nothing to the chain of reasoning — it only contrasts with a tool (CPP) that the proof never invokes. This is precisely the reviser-drift pattern: defensive prose explaining why a technique is *not* used, restating an argument already made. A reader following the home-preservation argument must skip past it.
**Required**: Delete the parenthetical. The terminal-only argument stands on its own in the sentences above it.

### Issue 2: L9 opens the address-selection with an unused T0(a) infinitude argument that the explicit construction immediately supersedes
**ASN-0043, L9 — TypeGhostPermission, *Choice of `a`***: "By T0(a), element-field component values are unbounded, so infinitely many element-level tumblers with `subspace_I(·) = s_L` and `#E(·) ≥ 2` exist within `d`'s link subspace. We construct `a` explicitly by case analysis on `d`'s prior link-allocation state; the construction yields the freshness `a ∉ dom(Σ.L)` and the producibility chain."
**Problem**: The T0(a) infinitude sentence sets up an existence argument that the proof never uses. Freshness is delivered by the explicit case analysis: Case A constructs `a = d.0.s_L.1` and derives `a ∉ dom(Σ.L)` from the empty-set case hypothesis; Case B invokes FSE, whose own freshness rests on T10a.7 (sibling-enumeration injectivity) plus L-fin — not on T0(a). The opening sentence is decorative setup that is immediately discarded ("We construct `a` explicitly…"), so it does no work in the proof.
**Required**: Delete the T0(a) sentence; begin the subsection with the explicit case construction, which is what actually establishes freshness and producibility.

## OUT_OF_SCOPE

None. The substantive content (subspace residence, the FSP/FSE/CPP machinery, the type-by-coverage equivalence, and the six-step worked example) is sound: CPP's two invocations correctly pin both the document prefix and the separator zero; FSP's L1c bullet derives the strong `k₁ = 2` and `#tᵢ > #s` conjuncts from the seed-equals-home constraint; the worked example's coverage-equality check (`[g, g') ∪ [g', h) = [g, h)`) and discrimination check are correct. The remaining gaps are scoping questions the ASN already books as Open Questions.

VERDICT: REVISE
