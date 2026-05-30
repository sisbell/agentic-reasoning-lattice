# Review of ASN-0043

## REVISE

### Issue 1: "extending Σ" is used in two existential claims but never defined
**ASN-0043, L9 and L11b**: "there exists ... a conforming state `Σ'` extending `Σ`" / "(E Σ' extending Σ, a' ∈ dom(Σ'.L) ...)"
**Problem**: Both L9 and L11b quantify existentially over states `Σ'` that "extend" `Σ`, and the strength of each lemma depends entirely on what extension permits (e.g., may `Σ'.C` grow? must `Σ'.M = Σ.M`?). The proofs silently pin `Σ'.C = Σ.C` and `Σ'.M = Σ.M`, but the relation `Σ' extends Σ` is never defined. A self-contained ASN cannot leave the quantification domain of its load-bearing existentials implicit.
**Required**: Define the state-extension relation once (domains non-decreasing, agreement on the shared domain, etc.) and have L9/L11b cite it.

### Issue 2: The scope-lift caveat is deferred to from four sites and inventoried in Open Questions
**ASN-0043, L0a, L9, L14, L14a, Open Questions**: "Why this ASN's guarantee is scoped to the `s_C`-resident slice ... is recorded once in the Open Questions." ... "This is the single home for the forward-looking scope-lift caveat; L0a, L9, L14, and L14a state only the bare scoped fact and cite this question."
**Problem**: This is the flagged accretion pattern — multiple sections deferring to one downstream location, plus a use-site inventory in the target ("L0a, L9, L14, and L14a ... cite this question"). The pointer sentences in L0a ("recorded once in the Open Questions") and the parentheticals in L9/L14 advance no reasoning; the Open-Questions entry then lists its own citers, which rots as sections move.
**Required**: Keep the bare scoped fact at each site, drop the "recorded once / single home" pointer prose, and remove the citer inventory from the Open Questions entry.

### Issue 3: L1c enumerates its downstream consumers in the contract slot
**ASN-0043, L1c and Properties table**: "enables GlobalUniqueness and chain-prefix-preservation for link addresses"
**Problem**: A definition/axiom's statement should advance its own meaning, not list what later consumes it. "Enables GlobalUniqueness and chain-prefix-preservation" is a use-site inventory; L11a and the L9 proof already cite L1c where they need it.
**Required**: Delete the "enables ..." clause from L1c's body and from the table row.

### Issue 4: Defensive "what the axiom is NOT" prose around L1c and the L9 freshness arguments
**ASN-0043, L1c and L9**: "it is a structural producibility statement about each address presently in `dom(Σ.L)`, **not a log of past allocator firings**." ... "with **no appeal to first-class allocation events**." ... "The construction operates on the structural sibling stream alone, **so it is sound regardless of whether** `d'`'s link-subspace allocator's frontier is or is not retained in `Σ`."
**Problem**: These clauses defend the phrasing against an alternative formulation rather than state content. The reader does not need to be told what the axiom is not modeling to follow it.
**Required**: Remove the "not a log / no appeal to first-class events / regardless of frontier retention" defensive clauses.

### Issue 5: L9's Case-A/B discriminator reads as a relocated correction note
**ASN-0043, L9, L1c verification**: "The correct discriminator is per-`d'`: whether `d'` has any prior link allocations, not whether `dom(Σ.L)` is globally empty. (Links may exist under other documents while `d'` itself has none, in which case `d'`'s link-subspace allocator has not yet been set up.)"
**Problem**: "The correct discriminator is ... not whether ..." is the residue of a prior fix — it corrects an earlier (now absent) formulation rather than stating the present case split. The proof should simply present the two cases (d' has prior link allocations; d' does not); the meta-explanation of why the split is keyed on `d'` is reviser drift.
**Required**: State the two cases directly; drop the "the correct discriminator is ... not ..." framing and the explanatory parenthetical.

### Issue 6: L11a argues at length why a case split is unnecessary — a case the precondition already excludes
**ASN-0043, L11a, Derivation**: "Instantiating GlobalUniqueness at the link-address events therefore yields `a₁ ≠ a₂` for distinct events directly, **with no separate case split on `home(a₁)` versus `home(a₂)`** — GlobalUniqueness already covers both configurations." (and the parallel sentence in the table row)
**Problem**: GlobalUniqueness is cited as a foundation result whose precondition (T10a-conformance) is discharged by L1c. The single-sentence instantiation is the whole derivation. The added prose imagines a shared-home/distinct-home case split and then explains it is not needed — content that pertains to GlobalUniqueness's internal proof, not to this corollary.
**Required**: Reduce to the instantiation: L1c discharges T10a-conformance; GlobalUniqueness then gives `a₁ ≠ a₂`. Delete the "no separate case split / already covers both configurations" rationale here and in the table.

### Issue 7: The `.type` accessor introduces authorial-preference meta-prose
**ASN-0043, Named accessor**: "The two forms are interchangeable in all formal statements; **we prefer `.type` when the role is salient and `.e₃` when the position is the load-bearing fact**."
**Problem**: Stating that the two spellings are synonyms is sufficient. The sentence describing when the authors prefer each spelling guides nothing the reader can act on and is the kind of stylistic essay-content the anti-bloat pass targets.
**Required**: Keep "`Σ.L(a).type ≡ Σ.L(a).e₃`"; drop the preference sentence.

### Issue 8: L2's formal statement carries no formal content beyond the definition of `home`
**ASN-0043, L2**: "`(A a ∈ dom(Σ.L) :: home(a) depends only on a)`"
**Problem**: `home(a)` is *defined* as `N(a).0.U(a).0.D(a)` — a function of `a` alone. "Depends only on `a`" is therefore true by the definition, not an invariant the system could violate, and "depends only on" is prose, not a formal predicate. The genuine, non-trivial content (endsets do not enter the home computation) is real but is not captured by this restatement.
**Required**: Either drop the pseudo-formal line and keep L2 as a stated design consequence of the `home` definition, or formalize the substantive claim (e.g., for any two states agreeing on `a` but differing in `Σ.L(a)`'s endsets, `home(a)` is unchanged).

## OUT_OF_SCOPE

### Topic 1: Link–content consistency under transclusion of shared I-addresses
**Why out of scope**: Already correctly parked in Open Questions; it concerns cross-store invariants under editing/transclusion operations, which are operation-effect territory excluded by the Scope section. No action needed.

VERDICT: REVISE
