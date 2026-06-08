# Review of ASN-0111

This note specifies a pure read of a link by its own address — `readlink(a, Σ) ≡ Σ.L(a)`. The core specification (state component, operation definition, definedness, completeness, role/structure preservation, the recorded-vs-resolved distinction) is abstract, correct, and well-supported. The worked example checks out arithmetically (zeros, element-field projection, `inc(a,0)`, `δ` displacements, the LP-Fin Corollary application all verify). The problems are bloat, concentrated in RL2 and RL5, consistent with the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: RL2 carries a multi-paragraph essay justifying why no arity-4 example is shown
**ASN-0111, RL2 (Role preservation), worked-read RL2 check**: "We deliberately do not exhibit such an instance, but the reason is presentational, not a matter of reachability. An `N = 4` link *is* `→*`-reachable... What caps arity at three is not the abstract model but udanax-green — creation (`docreatelink` passes three specsets), the spanfilade index (`LINKFROMSPAN`/`LINKTOSPAN`/`LINKTHREESPAN`), the V-subspace assignment (`setlinkvsas`), and retrieval (the three-slot `RETRIEVEENDSETS`, the `whichend ∈ {1,2,3}` guard)... So the two senses of 'reachable' diverge here..."
**Problem**: This is defensive meta-prose explaining a presentational choice, padded with an enumeration of udanax-green implementation mechanics. The substantive claim — the per-slot copy is identical at every index, so arity-3 verification establishes arbitrary arity — is one sentence. The reader must skip past the rest to follow the argument. The implementation enumeration is system-mechanics that the abstract guarantee does not depend on.
**Required**: Reduce to the load-bearing sentence: the read copies `Σ.L(a).eᵢ` into slot `i` by a per-index rule that names no other slot, so verifying slots 1–3 establishes every `N ≥ 3`. Drop the "two senses of reachable" essay and the udanax-green call-site inventory.

### Issue 2: RL5 is dominated by hedging paragraphs that do not advance the claim
**ASN-0111, RL5 (Type-by-address)**: "We must be careful not to overstate this into an asymmetry that does not hold..." and "We do not claim these exhaust every structural distinction between the slots: the directional significance of the from/to pair (L7) has no type-slot analogue, and the implementation segregates the type endset into its own V-subspace and search dimension. But those distinctions either lie outside the link value the read returns... or are implementation detail..."
**Problem**: Two of RL5's paragraphs are defensive justification — guarding against an overstatement and disclaiming exhaustiveness — rather than stating what the read surfaces about the type. The "V-subspace and search dimension" reference is implementation detail the claim then immediately sets aside. The actual content of RL5 (type interpreted by `coverage(e₃)` without dereference; type slot mandatorily non-empty; ghost types read completely) is buried under the hedges.
**Required**: State the two type-slot facts the read surfaces (non-empty by L3, coverage-identity by L8) and that ghost types read completely. Remove the "must not overstate" and "do not claim these exhaust" paragraphs and the V-subspace/search-dimension aside.

### Issue 3: The standing-precondition paragraph justifies the precondition at length rather than stating it
**ASN-0111, Deriving the read**: "This is not a convenience: the substrate facts we lean on — L0, L1, L1b, L0b, L3, L8, L12 — are *theorems about reachable states*, not properties of every conceivable store. A hand-built `Σ` carrying an arity-2 link... would satisfy none of them, and the guarantees... would have no ground to stand on. Every such guarantee is therefore claimed *only* under this standing precondition..."
**Problem**: Matches the "new prose around a precondition explains why it is needed rather than what it says" pattern. The precondition itself — `Σ` is `→*`-reachable / invariant-satisfying — is one clause; the rest is rationale for why it matters, including an imagined hand-built counterexample the carrier already excludes.
**Required**: State the precondition (`readlink` is specified over `→*`-reachable, invariant-satisfying `Σ`; "for a state `Σ`" means this) in one or two sentences. Drop the counterexample and the list of which theorems would otherwise fail.

### Issue 4: The "unwitnessed vs gone" distinction is stated three times
**ASN-0111, "Recorded relationship versus resolved position" / RL8 paragraph / worked orphaned instance**: the prose section, the post-RL8 paragraph ("The read distinguishes *the relationship is gone* from *the relationship is unwitnessed*"), and the worked example ("The read thus distinguishes *the relationship is unwitnessed* (true here) from *the relationship is gone* (false...)") each make the same follow/search-reports-emptiness point.
**Problem**: The example reinforcing the claim is legitimate, but the prose section and the RL8 paragraph restate the same contrast in different words before the example does it a third time. Two of the three are the same statement reworded.
**Required**: Make the distinction once in prose (RL8 paragraph), then let the worked instance demonstrate it. Trim the duplicate in "Recorded relationship versus resolved position."

## OUT_OF_SCOPE

None. The note correctly confines itself to the direct read and defers following, searching, counting, creation, and editing to their own ASNs.

VERDICT: REVISE
