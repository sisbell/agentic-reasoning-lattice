# Review of ASN-0071

I checked the PC proof, the resolution/resolve-equivalence derivation, the worked scenario arithmetic (single, multi-block, and cross-depth queries), the content-vs-link exclusion, finiteness, and the currency semantics. The core mathematics is sound: the PC argument (componentwise fact → totality → full prefix agreement) closes, the worked traces compute correctly, M16 correctly forbids the cross-origin merges, and the subtree-capture / interior-action-point contrast is genuine. My findings are about accreted meta-prose and one untracked guarantee — consistent with the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Forward-reference use-site inventory in *The query*
**ASN-0071, The query**: "The two content-subspace preconditions `subspace(u) = s_C` and `actionPoint(ℓ) = #u ≥ 2` are what the *prefix confinement* argument below consumes; its position-1 instance is subspace confinement."
**Problem**: This sentence advances no reasoning — it inventories what a later argument "consumes" and points "below." It is the "definition's introduction enumerates downstream consumers" pattern. The reader learns the preconditions' role when PC actually uses them, two paragraphs later.
**Required**: Delete the sentence. The PC paragraph already states which preconditions it uses.

### Issue 2: Prefix confinement named twice, with the proof's own structure narrated
**ASN-0071, The query**: "The claim we need — call it *prefix confinement* — is that..." and later "We name this *prefix confinement* (PC)..."
**Problem**: The same lemma is christened twice in one paragraph. The proof also narrates its own scaffolding ("This fact discharges *totality*... With totality in hand the componentwise fact applies at every `1 ≤ j < #u`"), restating the plan it just executed. The logic is correct but the reader must skip past the meta-commentary to follow the chain.
**Required**: Name PC once. State the componentwise fact, then totality, then prefix agreement as a single forward chain without the "this discharges / with this in hand" connective prose.

### Issue 3: Currency parenthetical re-derives an already-established routing fact
**ASN-0071, Currency: state dependence**: "S3★ ∧ S3★-aux (SubspaceExhaustiveness, ASN-0047) supply the standing context that `ran(Σ.M(d)) ⊆ dom(Σ.C) ∪ dom(Σ.L)` — S3★ routes the two known subspaces and S3★-aux forecloses a third — but `find` does not consult the content store to evaluate it."
**Problem**: This re-states the exact S3★/S3★-aux routing argument already given in full in *The operation* ("Only content sharing can satisfy the predicate"). Here it is defensive padding — the point being made is simply "find reads only `E_doc` and `M`," which the surrounding sentence already says.
**Required**: Cut the parenthetical to the operative claim ("`find` reads only `Σ.E_doc` and `Σ.M`"); the routing derivation lives in *The operation*.

### Issue 4: find-vs-R / historical-containment distinction stated twice in the same section
**ASN-0071, Currency: state dependence**: the paragraph "A document whose arrangement once referenced `a` but has since been contracted... is not in `find(Q)`" and the later paragraph "Recovering the *historically*-containing set... `find` does not consult ASN-0047's provenance relation `R`..."
**Problem**: Both paragraphs make the identical point — present-tense containment ≠ ever-containment, contraction drops a document while `R` persists. The second paragraph restates the first in different words (the "two paragraphs say the same thing" pattern). The F-CUR worked-example bullet already instantiates it concretely.
**Required**: Merge into one paragraph: state the present-tense semantics, then the one-sentence `R`-comparison and its consequence for F-COMP.

### Issue 5: Content-vs-link exclusion is a derived guarantee absent from the Claims table
**ASN-0071, The operation**: "A document is returned because it shares *byte content*, never because it shares a *link* address. This is what justifies calling the operation content-transclusion discovery."
**Problem**: This is a genuine derived guarantee (`ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ⊆ dom(Σ.C)`), proven from S3★ ∧ S3★-aux ∧ L14. Every comparable guarantee — F-SHARE, F-PART, F-SOUND, F-CUR — carries a label and a Claims-table row. This one does not, so a substantive result reads as one-off exposition rather than a tracked claim.
**Required**: Promote to a labeled claim (e.g. F-CONTENT: matches occur only via shared `dom(C)` addresses) with a Claims-table row and Basis, or, if it is meant only as motivation for the operation's name, trim the derivation to a sentence.

## OUT_OF_SCOPE

### Topic 1: Visibility-filtered and replica-aware variants
**Why out of scope**: The ASN correctly defers access-control filtering and replica-divergent completeness to open questions and the *What we do not specify* section; these are new operations/layers, not gaps in this query's specification.

### Topic 2: Rejection vs. silent-filter policy for unresolvable positions
**Why out of scope**: F-FILT commits to charitable silent filtering and the ASN names the rejection-policy alternative as an open question. The choice belongs to a future policy ASN.

VERDICT: REVISE
