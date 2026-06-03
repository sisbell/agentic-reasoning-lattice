# Review of ASN-0068

## REVISE

### Issue 1: Mixed-subspace paragraph reasons about an input CV-IN already excludes
**ASN-0068, The Input (after CV-IN-N)**: "Were `R_a` to range over content positions (subspace `s_C`) while `R_b` ranged over link positions (subspace `s_L`), the I-addresses on the two sides would inhabit disjoint storage subspaces — `dom(C)` and `dom(L)` respectively, by L14 (ASN-0047) — and no I-address could coincide. The relation would be empty: comparison is a per-subspace operation."
**Problem**: CV-IN already stipulates "A common subspace identifier `S ∈ {s_C, s_L}` governs both restrictions." A mixed `(s_C, s_L)` input is therefore inadmissible — the precondition's carrier excludes it. This paragraph computes the result of an input the precondition forbids, which is the reviser-drift pattern of imagining a case the precondition already rules out, dressed as post-hoc justification for why the common-subspace requirement exists. It does not advance the operation's definition.
**Required**: Delete the paragraph. If a motivating remark for the common-subspace clause is wanted, fold a single clause into CV-IN itself ("a common `S` because cross-subspace I-addresses are disjoint by L14") rather than narrating an excluded scenario.

### Issue 2: Duplicated "restriction is not a filter" prose across two sections
**ASN-0068, The Input**: "Restriction is therefore not a separate filtering stage — it is part of what defines the operation, the lens through which it is asked to look."
**ASN-0068, Example 5**: "the restriction is not a post-hoc filter on a depth-independent diff but a constituent of what the maximal runs *are*."
**Problem**: Two paragraphs in different sections assert the same proposition in different words. Example 5 already *demonstrates* the point concretely (the gap at `[1,2]` fragments a width-4 run), which is the load-bearing content; the input-section sentence is an untethered essay restatement of the same claim.
**Required**: Keep the demonstration in Example 5; drop the abstract restatement in the input section (or the trailing editorial clause of Example 5). One statement of the principle, anchored to the example, suffices.

### Issue 3: Worked-Examples inventory sentence is navigational meta-prose
**ASN-0068, Worked Examples**: "We verify the definitions and CV-MAX against concrete configurations: a cross-document contiguous-transclusion case (Example 1), a cross-document self-transclusion case where merging is blocked (Example 2), a self-comparison case... (Example 3), a differing-depths case (Example 4, after CV-SPAN-VIEW), and a proper-restriction case... (Example 5)."
**Problem**: This is a use-site inventory in a structural slot — a table-of-contents for the examples that follow, including a forward-reference deferral ("Example 4, after CV-SPAN-VIEW"). Each example already states its own purpose in its opening line, so the list adds no reasoning.
**Required**: Remove the inventory sentence; let each example introduce itself. If section ordering must be explained, the placement of Example 4 after CV-SPAN-VIEW is self-evident from the projection it exercises and needs no announcement.

## OUT_OF_SCOPE

### Topic 1: Concurrent mid-comparison arrangement modification
The Open Questions raise invariants under concurrent modification. This belongs to a future concurrency/transaction ASN, not here; CV-RO and CV-DETERM correctly scope the present note to snapshot semantics.

### Topic 2: Cross-replica result agreement (BEBE)
Replication-equivalence of `compareversions` results is correctly deferred — replication protocol is out of scope per the stated scope list.

VERDICT: REVISE
