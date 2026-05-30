# Review of ASN-0042

The mathematics here is, on the whole, correct and unusually thorough — the invariant-preservation inductions (O1a, O1b, O4, O6, PrefixBaptismCoupling, NestingByDelegation) discharge their base cases and steps explicitly, and the longest-match well-definedness in O2 is sound. My findings are concentrated where this note's `review-mode.anti-bloat` classifier directs: duplicated derivation, near-verbatim repeated prose, and forward-pointer accretion. One redundant re-derivation (O6 corollary) is a correctness-adjacent waste, not an error.

## REVISE

### Issue 1: Near-verbatim duplicate deferral within the same section
**ASN-0042, Structural Provenance**: two paragraphs carry the same sentence —
> "whether a transfer regime that makes them diverge can preserve the model's invariants is deferred to the Open Questions."

appears once mid-section (AccountPrefix discussion) and again in the closing paragraph ("Under the system as specified, these coincide; whether a transfer regime that makes them diverge can preserve the model's invariants is deferred to the Open Questions."). A third instance appears in the Permanence section ("transfer is deferred to the Open Questions").
**Problem**: This is the "multiple paragraphs defer to the same downstream location" / "same thing in different words" pattern — here it is the *same* words twice in one section. The deferral adds nothing the Open Questions list does not already carry.
**Required**: State the transfer-deferral once (at most), or drop it entirely since the Open Questions already record it.

### Issue 2: O6 corollary re-derives what the main biconditional already gives
**ASN-0042, O6, Corollary (owner prefix containment)**: "We derive this in four steps. (1) By O1a... (3) Two cases arise from the zero count. When `zeros(pfx(ω(a))) = 0`... When `zeros(pfx(ω(a))) = 1`..."
**Problem**: The body of O6 already proves the biconditional `pfx(π) ≼ a ≡ pfx(π) ≼ acct(a)` for an *arbitrary* principal with `zeros(pfx(π)) ≤ 1`. Since `ω(a)` is such a principal and `pfx(ω(a)) ≼ a` by definition, the corollary is the one-line instantiation `pfx(ω(a)) ≼ acct(a)`. The four-step re-run of the `zeros = 0 / zeros = 1` case analysis duplicates the main proof verbatim in structure.
**Required**: Replace steps (1)–(4) with a single instantiation of the O6 biconditional at `π = ω(a)`; keep only the strict-vs-equality remark.

### Issue 3: Forward-pointer use-site inventory in BootstrapContainment
**ASN-0042, State Axioms**: "**BootstrapContainment (derived).** ... Proofs below cite this fact to exclude the bootstrap origin of a newly observed principal `π' ∉ Π_Σ`."
**Problem**: The final sentence is a use-site inventory — it inventories where the lemma will later be invoked rather than advancing the lemma. The fact and its one-line proof are self-contained; the consumers (O3, O8, OwnershipDomainPermanence) cite it where needed.
**Required**: Delete "Proofs below cite this fact to exclude the bootstrap origin..." — the lemma stands without naming its future call sites.

### Issue 4: O10 branch analysis fully duplicated between proof and worked example
**ASN-0042, O10 proof (Construction) and Worked Example (Fork)**: the field-opening (`hwm_0 = 0`, `inc(pfx(π), 2)`) versus sibling-advance (`hwm_0 ≥ 1`, `inc(...,0)`) case split is worked once in the O10 *Construction* paragraph and then again, in full, in the worked example (π_A's sibling-advance fork and π_B's field-opening fork, each with its own O5/B6/O10(a)/O10(b) re-verification).
**Problem**: A concrete example is required and welcome, but here it re-derives the same two `next`-branches the proof already discharged, with parallel O5/B6 checks. The example should *witness* the proof on specific tumblers, not re-prove the branch lemma.
**Required**: In the worked example, exhibit one branch on concrete addresses and cite the O10 Construction for the branch already proven there; drop the re-verification of O5/B6 that merely restates the proof's general argument.

### Issue 5: DelegatorAllocatesPrefix closes with a restatement of its own conclusion
**ASN-0042, Delegation**: after the proof ends with "∎", the following paragraph reads "The derived property states a coupling: when a delegation transition fires, the delegator is the unique principal whose O5 authority underwrites the baptism of the new prefix."
**Problem**: This restates the just-proven postcondition (`allocated_by_{Σ'}(π_d, pfx(π'))`) in prose. The Gregory sentence that follows is concrete evidence and may stay; the restatement is noise.
**Required**: Drop the restatement sentence; keep the implementation-evidence sentence.

## OUT_OF_SCOPE

The Open Questions (transfer regime, overlap enforcement, custodial continuity, density, cross-node federation, delegation-event recording) are correctly deferred and correctly scoped as future ASNs — no action needed. The fork producing only a namespace/document slot rather than an element-level content address is appropriate: content placement is out of scope, and the ASN states this honestly.

VERDICT: REVISE
