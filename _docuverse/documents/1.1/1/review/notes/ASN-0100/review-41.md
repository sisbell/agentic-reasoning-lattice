# Review of ASN-0100

## REVISE

### Issue 1: The "I3-C does not hold" statement is repeated across four sites

**ASN-0100, §Effect Three (Shift) and §Verifying the Invariants — Post-state V-position well-formedness**: The fact that ASN-0082's I3-C (`Σ'.C = Σ.C`) is *not* preserved by INSERT is stated four times in different words:

1. Effect Three, "Scope of ASN-0082's I3…": *"I3's whole-post-state characterizations — in particular I3-C (Σ'.C = Σ.C) — do not hold of INSERT's M'(d)…"*
2. Effect Three, next paragraph: *"ASN-0082's I3-C (PostInsertionContentFrame), asserting exact equality Σ'.C = Σ.C for its shift-only model, is strictly stronger than INSERT's content frame and is not preserved here."*
3. §Post-state… section intro: *"ASN-0082's I3-S7 is not cited here — its own justification rests on I3-C (Σ'.C = Σ.C), which INSERT breaks…"*
4. §Post-state…, S7-invariants bullet: *"I3-S7 is not invoked: its ASN-0082 justification rests on I3-C (Σ'.C = Σ.C), which INSERT breaks."*

**Problem**: This is the anti-bloat "two paragraphs say the same thing in different words" pattern, compounded fourfold. The two Effect-Three paragraphs are adjacent near-duplicates; the two §Post-state mentions (section intro + S7 bullet) are also adjacent near-duplicates. The reader must re-parse the same disclaimer four times.

**Required**: State once — at the first cite of I3 — that INSERT cites I3 only for its positive shift clause (I3) and that the whole-post-state frames I3-C and I3-S7 do not transfer because INSERT extends `dom(C)`. Delete the other three restatements; downstream sections can cite that single note.

### Issue 2: Step-3 K.μ⁺ carries a defensive meta-paragraph that defers downstream

**ASN-0100, §The Operation: Formal Contract — Substrate Decomposition, step 3**: *"This 'adds exactly Insertion ∪ Shifted-right' is a feature of the canonical firing, not a constraint binding on every admissible decomposition: K.μ⁺'s vocabulary precondition (ASN-0047) is permissive… Exhaustiveness (INS.M-exhaustive) is a property of the post-state V_{s_C}(d'), not of the canonical K.μ⁺ firing; it is established for the canonical decomposition and lifted to all admissible decompositions in the §Effect — Arrangement clause below."*

**Problem**: This is meta-prose about what the step does/does-not constrain plus a forward pointer ("lifted … in the §Effect — Arrangement clause below"). The substantive content — exhaustiveness as a post-state property established by step-tracking — already lives in the Effect — Arrangement clause and is re-used in §Atomicity. The step-3 paragraph advances no reasoning the reader can act on at that point; it only forward-defers.

**Required**: Reduce step 3 to its factual content (K.μ⁺ adds the Insertion and Shifted-right V-positions, all in `s_C`). Drop the "feature of the canonical firing, not a constraint" defense and the forward reference; the admissible-decomposition latitude is already handled in §Atomicity's uniqueness argument.

### Issue 3: Defensive non-occurrence prose around K.σ and the labeled `*Identification.*` sub-paragraph

**ASN-0100, §The Operation: Formal Contract** (K.σ paragraph) and **§Verifying the Invariants — P6** (`*Identification.*` sub-paragraph):

- K.σ paragraph: *"The K.σ operation introduced in ASN-0093 is the document-registration primitive of that ASN's standalone substrate formulation — distinct from, and not composed with, ValidComposite★. INSERT itself is governed entirely by ValidComposite★ and admits no K.σ firing."*
- P6: a labeled `*Identification.*` sub-paragraph re-deriving `E_doc = dom(M)` at length before the one-line P6 step that uses it.

**Problem**: The K.σ paragraph explains *why an operation does not fire* — defensive justification of a non-occurrence. The frame condition `E' = E` (INS.frame.E) already says INSERT fires no entity-creation step; the K.σ disambiguation is rationale prose. The `*Identification.*` sub-label matches the flagged "sub-paragraphs labeled … that explain why rather than advance the step" pattern; `E_doc = dom(M)` under ValidComposite★ is a one-line substrate fact, not a multi-sentence excursion.

**Required**: Drop the K.σ paragraph or compress to a clause in the frame conditions ("no K.δ/K.σ fires"). Inline the `E_doc = dom(M)` identification into P6's proof step as a single cited clause rather than a labeled sub-paragraph.

## OUT_OF_SCOPE

None. The ASN bounds COPY/DELETE/REARRANGE/version-creation correctly: the INSERT-vs-COPY section contrasts COPY only to fix INSERT's identity character and explicitly declines to specify COPY mechanics, and the version-independence corollary states a property of INSERT (not of version creation). No out-of-scope claims are defined.

The substantive specification is sound: the three-region partition, the per-state/composite-boundary invariant split, the freshness-against-intermediate-state argument (Effect One), the D-CTG★ closed-interval discharge via D-CTG-depth, the empty/append/interior/`j=0` boundary cases, the INS.chain-shift derivation (inc/shift equivalence grounded in T4-validity rather than asserted), and the wp analyses (discoverability, provenance membership) all check out. The findings above are noise around a correct argument, not defects in it.

VERDICT: REVISE
