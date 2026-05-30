# Review of ASN-0082

## REVISE

### Issue 1: Forward-reference / dual-inventory prose in I3-S
**ASN-0082, Span Width Preservation (after I3-S derivation)**: "This connects the point-level shift to ASN-0053's span framework: **the displacement arithmetic underlying span endpoints (SpanReach) commutes with uniform ordinal translation.** The dual lemma D-S below establishes the same commutativity for the inverse (contraction) shift; together (I3-S, D-S) constitute the span-algebra closure for both arrangement transformations specified by this ASN."
**Problem**: The bolded sentence restates the lemma's content as a slogan, and the following sentence is a forward pointer plus a use-site inventory ("together (I3-S, D-S) constitute…"). Neither advances I3-S's reasoning — the lemma is complete at the ∎. This is exactly the "definition/lemma prose enumerating downstream relationships + deferral to a downstream location" pattern flagged for this note.
**Required**: Cut to at most the single motivating sentence ("both endpoints shift by the same displacement; the width between them is invariant"). Drop the bolded restatement and the D-S forward inventory.

### Issue 2: Statement Registry carries analysis verdicts, not statements
**ASN-0082, Statement Registry**: D-CTG / D-MIN / D-SEQ rows read "…— NOT preserved by shift alone", "…— NOT preserved by shift when p = min(V_1(d))".
**Problem**: The registry is an index of statements and their provenance. The "NOT preserved by shift" verdicts duplicate the dedicated prose section *Arrangement invariants not preserved* (which already establishes, with the worked gap example, that D-CTG/D-MIN/D-SEQ fail post-shift). The same conclusion stated in two places is the "two paragraphs say the same thing" pattern; the registry copy will rot independently of the prose.
**Required**: Strip the "NOT preserved…" annotations from the registry rows, leaving the citation status (cited, ASN-0036). Keep the analysis in the prose section only.

### Issue 3: Defensive exhaustiveness in the Consistency paragraph
**ASN-0082, Post-Insertion Shift, "Consistency"**: the seven-way pairwise inventory ("*Shifted vs left… Shifted vs shifted… Shifted vs cross-subspace… Left vs cross-subspace… Cross-document… Vacated vs assignment regions… Closure consistency*").
**Problem**: Only two checks are load-bearing for well-definedness of M'(d): shifted-vs-shifted (TS2 injectivity) and shifted-vs-left (TS4 ordering). The remainder are disjoint "by definition" (left vs cross-subspace), "by document identity" (cross-document), or restate the closure clauses verbatim. The reader must work past five trivial cases to reach the two that matter — a use-site/exhaustiveness inventory, not an argument.
**Required**: State the two non-trivial disjointness facts (injectivity, strict advance past p) and assert the rest hold by subspace/document partition in one clause. I3-S2 can then cite the trimmed result unchanged.

### Issue 4: Provenance meta-prose opening Ordinal Extraction
**ASN-0082, Ordinal Extraction (opening)**: "These extraction, reconstruction, and projection functions are not foundation primitives; we define them here as local index operations on tumblers and establish their properties directly from T0's component projection and the tumbler arithmetic of ASN-0034."
**Problem**: This explains *why the definitions are local* and *what they will be derived from* rather than advancing any definition's meaning — the "new prose explains why X is needed rather than what it says" pattern. The "introduced (local)" tags on each definition already carry the provenance.
**Required**: Delete the sentence; begin with the OrdinalExtraction definition. The local-vs-foundation status is already recorded per-definition and in the registry.

## OUT_OF_SCOPE

### Topic 1: Depth > 1 generalization of the gap-closure round-trip
The supporting lemmas (ord/vpos/w_ord, OrdinalOrderEquivalence, OrdAddHom) are proven at general depth m ≥ 2, while the contraction is correctly fixed at #p = 2 because D-SEP's round-trip relies on TA4's zero-prefix precondition, which is incompatible with S8a componentwise-positivity at intermediate depths. The note already records this tension in the wp conjunct-3 discussion and defers the general-depth round-trip to Open Questions. No action — the depth-2 restriction is sound and the deferral is the right call.

META: not applicable — the ASN specifies arrangement-layer state transformations (shift/contraction over M(d)) and their invariant-preservation guarantees abstractly; it has not drifted into implementation mechanics.

VERDICT: REVISE
