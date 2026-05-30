# Review of ASN-0042

## REVISE

### Issue 1: Design-essay content in the O6 corollary slot
**ASN-0042, Structural Provenance, *Corollary (owner prefix containment)***: "An account-level principal may create sub-account positions as organizational namespaces, ghost elements, or internal partitions without introducing a new ownership principal — the owner decides what sub-numbering means."
**Problem**: The corollary's mathematical content is its first two sentences (`pfx(ω(a)) ≼ acct(a)`, instantiated from the O6 biconditional). The remainder is design elaboration sitting in a formal-corollary slot — it does not advance the containment claim. This is the essay-in-structural-slot pattern the anti-bloat pass targets. The Nelson LM 4/17 quote is already used verbatim under O1; repeating it here adds no derivation.
**Required**: Reduce the corollary to its claim plus the strict-vs-equality condition (the final sentence is concrete and may stay). Move or drop the namespace/ghost-element essay prose.

### Issue 2: The "delegate is the strict longest match" argument is reproduced verbatim across sections
**ASN-0042, O7(a) proof and NestingByDelegation inductive step**: both reprove the identical three-case covering-chain contradiction — given `pfx(π'') ≼ a` (or `≼ pfx(π')`), the cases `pfx(π') ≺ pfx(π'')` [excluded by delegation cond. (iv)], `pfx(π') = pfx(π'')` [excluded by (i)+(ii) length contradiction], and `pfx(π'') ≺ pfx(π')` [consistent, forces shorter prefix] are walked through in full each time. The same skeleton recurs in O10's final competition analysis and (in reduced form) in O3.
**Problem**: This is the "two paragraphs say the same thing in different words" pattern extended across four proof sites. Each reproduction is a maintenance liability and forces the reader to re-verify an argument already established.
**Required**: Factor the result into one named lemma — "a newly delegated `π'` satisfying conditions (i),(ii),(iv) is the unique strict longest-match coverer of any `a` it covers" — and cite it from O7(a), NestingByDelegation, O3, and O10.

### Issue 3: Self-referential scoping notes and section back-pointers in formal slots
**ASN-0042, O7(c) proof**: "The claim is asserted only at the entry state `Σ'` (postcondition (c))." **and O10 Formal Contract**: "...`Σ → Σ'` is a single baptism performed by `π` alone (the `allocated_by_{Σ'}(π, a')` conjunct, established in *Per-baptism authorization*)."
**Problem**: These are meta-prose pointing at the document's own structure rather than advancing the argument — a scope restatement and a proof-section back-pointer embedded in a Formal Contract. They match the forward-reference accretion patterns flagged for this note.
**Required**: Drop the scoping sentence (the postcondition already fixes the state); in the contract, state the `allocated_by` conjunct without the parenthetical pointer to the proof section.

## OUT_OF_SCOPE

None. Ownership transfer, overlap-enforcement, and federation are correctly deferred to Open Questions rather than asserted, so they are not errors in this ASN.

VERDICT: REVISE
