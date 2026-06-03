# Review of ASN-0075

## REVISE

### Issue 1: D-BOUND axiom prose restates D-EXH's rationale instead of stating the axiom
**ASN-0075, "Observational-discipline axiom (D-BOUND)"**: "This discharges D-EXH's composite-boundary hypothesis at every invocation — `P4★` (`Contains_C(Σ) ⊆ R`), a composite-boundary property of ASN-0047, holds at every such `Σ`, so the three-state classification is total."
**Problem**: The axiom's content is one sentence (SHOWDELETIONS is invoked at a composite boundary). The remainder is rationale about *why* the axiom matters, and it duplicates the load-bearing explanation already given verbatim-in-substance in the D-EXH paragraph ("The reachability hypothesis is load-bearing for the proof: it activates `P4★` ... At intermediate states inside a composite, `P4★` may fail, so the lemma's universal claim applies only to states observed at composite boundaries"). The same P4★-holds-at-boundaries argument now appears in two sections. This is the flagged pattern: prose around an axiom explaining why it is needed rather than what it says, plus two paragraphs saying the same thing.
**Required**: State D-BOUND as the bare invocation-discipline condition. Drop the P4★/D-EXH discharge explanation here; it already lives in the D-EXH paragraph.

### Issue 2: Post-D-DISCR paragraph re-states the lemma's own conclusion
**ASN-0075, "Why the Provenance Relation Is Load-Bearing"** (paragraph after the proof): "Any system supporting SHOWDELETIONS must therefore maintain state components `C*` *beyond* `(C, L, E, M)`... `R` as defined in ASN-0047 is one such `C*`; the necessity claim is that *some* `C*` adequate to discharge this disambiguation must be present, regardless of its specific representation."
**Problem**: This is a third utterance of a conclusion already carried by (a) the lemma statement D-DISCR and (b) the claims table entry for D-DISCR, both of which already say "any system supporting SHOWDELETIONS must maintain state components `C*` beyond the four foundation components." The paragraph advances no new reasoning past `∎`; it re-asserts the result in different words.
**Required**: Delete or compress to the single novel observation (the witnesses pin *every* component of `(C,L,E,M)`, so no projection suffices). Drop the `C*`-necessity restatement that the lemma and table already carry.

### Issue 3: D-IDENT link-survival bullet carries span-denotation essay content that does not advance the claim
**ASN-0075, D-IDENT, "Link survival" bullet**: "A span's denotation `⟦σ⟧` and the interior/boundary classification of its positions are fixed by ASN-0053 (σ.denotation, InteriorPoint); a link references the content address `a` whenever `a ∈ ⟦σ⟧` for some span `σ` in one of its endsets, and that membership condition holds uniformly whether `a` is the span's start or an interior point."
**Problem**: The point of the bullet is that links referencing `a` survive because `L` is immutable (P3/L12) and `a`'s identity persists. The interior-vs-boundary classification and uniform-membership elaboration add no force to that conclusion — identity preservation is what keeps every endset reference valid regardless of where `a` sits in a span. This is essay content in a justification slot.
**Required**: Reduce the bullet to: links in `dom(L)` reference content via endsets; `L` is preserved across arrangement transitions (P3/L12); therefore every link referencing `a` continues to reference the same `a`. Drop the span interior/boundary digression.

### Issue 4: Foundation Recap pre-asserts and forward-defers a result it proves later
**ASN-0075, Foundation Recap** (final sentence): "...so cross-document deletion comparison is structurally meaningful only for content (established as D-SUBSP)."
**Problem**: The Recap states the content-subspace restriction *and* forward-points to D-SUBSP, whose section then re-derives the same conclusion from the full L0/L14/S3★/CL-OWN chain. The Recap sentence is anticipatory deferral — it asserts the conclusion before the argument exists and signposts where the argument will appear.
**Required**: In the Recap, state only that the operation is confined to the content subspace (a scope declaration); move the "structurally meaningful only for content" justification entirely into the D-SUBSP section where it is proved.

## OUT_OF_SCOPE

None. The defined claims stay within the SHOWDELETIONS operation and do not stray into INSERT/DELETE/COPY/REARRANGE mechanics, link semantics, version-DAG structure, or replication.

VERDICT: REVISE
