# Review of ASN-0131

This note is mathematically sound. I checked the core claims and they hold: RE-DEF's biconditional makes RE-SND/RE-CMP immediate; the `touch_W` pull-out of the existential makes `RE(W,d,Σ) = {(i,e) ∈ Avail(Σ) : touch_W(e)}`, which carries RE-UDIST and the one-sided RE-UDIST-∩ cleanly; the non-injectivity counterexample to `⊇` is genuine; RE-ADDR's antichain argument is correct; the RE-CWP weakest-precondition derivation and its `R = ∅` boundary check out; the retraction-stability forward/backward halves (R6a + R-Scope) are valid under the stated `coverage(Θ) ∩ dom(Σ.C) = ∅` hypothesis; and the worked instance's field-agreement argument for `coverage(e₃) ∩ dom(Σ.C) = ∅` is rigorous. Boundary cases (RE-BND), a concrete example, and a non-trivial wp are all present. No hand-waves, no notation reinvention, no improper cross-ASN references — every cited ASN is a foundation.

The findings below are the accretion the `anti-bloat` classifier flags, plus one cross-reference defect.

## REVISE

### Issue 1: Counterfactual about a delete primitive the foundation does not supply

**ASN-0131, "Stability ... under editing of the queried document"**: "So delete-stability is scoped to text depth `#p = 2` and insert-stability to every `#p ≥ 2` — an asymmetry in the displacement's *existence*, not in the stability argument, which would cover a higher-depth delete were the foundation to supply one."

**Problem**: The clause "which would cover a higher-depth delete were the foundation to supply one" reasons about a primitive that ASN-0082 does not provide — the imagines-an-excluded-case pattern. Worse, the conclusion it previews (the argument is depth-general) is established two sentences later, in its own right: "the unique lift to the full state writes `Σ.M(d)` ... at any content depth." So the clause is a forward preview of a conclusion the M-only lift delivers anyway — two passages asserting the same depth-generality in different words.

**Required**: State the scope without the counterfactual: the stability argument needs only that the edit is M-only and is therefore depth-general; the `#p = 2` delete scope reflects which displacement primitives ASN-0082 supplies. Let the M-only lift carry the depth-generality once.

### Issue 2: Elaborate defense of a non-reachable intermediate state

**ASN-0131, same section**: "The vacated positions `[p, shift(p, n))` the shift primitive does *not* backfill (I3-V), so the bare shift leaves an interior gap in `V_{s_C}(d)` that violates the standing contiguity invariants D-CTG★/D-SEQ★ (ASN-0047) — and indeed ASN-0082 supplies no D-CTG-preservation lemma for the insertion shift (only for the gap-closing delete, D-CTG-post). That gap configuration is therefore not a reachable state; by the atomicity of transitions (SequentialTransitionAxiom, ASN-0047) it is a non-queryable intermediate of the *non-atomic* full insert, not a state at which `RE` is evaluated."

**Problem**: RE is a query over a state; it is never asked at a non-reachable state, so the gap configuration cannot affect RE's stability. The passage builds a whole detour (I3-V, the D-CTG★/D-SEQ★ violation, "ASN-0082 supplies no D-CTG-preservation lemma," atomicity) to dismiss a worry the claim's carrier — reachable states — already excludes. The reader must skip past it to reach the actual conclusion in the next sentence ("At each reachable post-edit state, then, `RE` tracks the image's motion by membership").

**Required**: Reduce to the load-bearing statement: RE is evaluated only at reachable (D-CTG★-satisfying) states, where the net effect of insert/delete is an M-only, gap-free arrangement edit. The intermediate-gap excursion does not advance the claim and should be cut or compressed to a clause.

### Issue 3: Open Questions referenced by number against an unnumbered list

**ASN-0131, body and Claims table vs. "## Open Questions"**: The body and table cite "Open Question 1" (RE-WHOLE), "Open Question 3," "Open Question 4," and "Open Question 6," but the Open Questions section is seven unlabeled paragraphs with no numbers.

**Problem**: A reader cannot resolve "Open Question 4" without counting paragraphs. The numbering happens to match paragraph order, but the references are not directly followable — a precision defect in a document that is otherwise careful with its cross-references (every claim and foundation citation is labeled).

**Required**: Number the Open Questions paragraphs (1–7) to match the in-text references, or replace the numeric references with the question's subject.

## OUT_OF_SCOPE

No out-of-scope **claims** appear. The ASN correctly confines its out-of-scope material to the Open Questions (link-subspace regions, non-co-resident link stores, rendered V-position answers, type-slot/content matches, multiplicity) rather than smuggling them in as theorems, and mentions sibling operations (FINDLINKSFROMTOTHREE) only as one-line contrasts, not as load-bearing citations. The decidability/computability paragraph and the worked instance, though long, are protected content — statements of what the operation does and a required concrete example — not bloat.

VERDICT: REVISE
