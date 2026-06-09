# Review of ASN-0117

## REVISE

### Issue 1: Redundant dual proofs in the entity and provenance frames
**ASN-0117, Effect / Frame (DEL-FENT, DEL-FPROV)**: "Two independent arguments converge. *Directly:* DELETE baptizes no fresh node, account, or document and removes none... *By composition:* both component steps carry an entity frame `E' = E`..." (and the parallel "*Directly:* ... *By composition:*" in DEL-FPROV).
**Problem**: Each frame clause proves the same conclusion (`E' = E`, resp. `R' = R`) twice by two distinct routes. One suffices. The duplication is meta-prose accretion — the note is hedging which justification to keep rather than choosing one. This is the anti-bloat pattern "two paragraphs say the same thing in different words."
**Required**: Keep a single derivation per frame (the "by composition" route is consistent with the rest of the note's framing; the permanence-based route is the alternative). Delete the other.

### Issue 2: Defensive parenthetical disclaiming an unused lemma
**ASN-0117, "Link survival" section**: "(We do *not* appeal to LP10 (ContractionMonotonicity, ASN-0098) for the *net* DELETE effect. LP10 is a per-K.μ⁻-step fact, and although DELETE's first component step *is* a K.μ⁻... the K.μ⁻ + K.μ⁺ *composite* left-shifts the suffix, so the single-step picture does not describe the net transition. Moreover LP10's conclusion is a V-position–level *projection* inclusion... which is false for the DELETE composite...)"
**Problem**: This paragraph exists only to pre-empt a reviewer who might expect LP10. The note's own derivation (`ran(M'(d)) ⊆ ran(M(d))` from DEL-LEFT/DEL-SHIFT/DEL-FSUB) stands without it. Defending against a lemma you deliberately do not use is reviewer-response material, not part of the argument. The reader must skip it to follow the actual range derivation.
**Required**: Remove the parenthetical. The range inclusion is established directly from DELETE's clauses; no disclaimer is needed.

### Issue 3: Pervasive cross-operation (insertion) essay content
**ASN-0117, multiple sections**: "The asymmetry with insertion is the heart of the matter. INSERT mints fresh I-addresses and shifts right; DELETE allocates nothing..."; "dually to insertion's resurrection branch, deletion can only orphan, never resurrect"; "For insertion the analogous wp turned out to be conditional in the *enlarging* direction... For deletion it is conditional in the *shrinking* direction... The two operations are mirror images here too."
**Problem**: INSERT is out of scope for this ASN (its reframe ASN-0116 is not a foundation). These comparisons are essay content that does not advance the DELETE argument; they import an out-of-scope operation as rhetorical scaffolding. The DELETE clauses and wp stand entirely on their own.
**Required**: State DELETE's content-layer behavior and the conditional wp directly. Drop the insertion-mirror framing.

### Issue 4: Missing boundary check — leading-span deletion (J = 1, R ≠ ∅)
**ASN-0117, "A worked deletion"**: worked examples cover interior (`q_3`, c=2), `L`-singleton (`q_2`, c=1), suffix-delete (`R = ∅`), delete-everything (`J=1, c=N`), sharing, and cross-document — but not `J = 1` with `R ≠ ∅`.
**Problem**: The note adds a dedicated `R = ∅` vs `R ≠ ∅` case split and stresses that the `R ≠ ∅` realisation is a K.μ⁻ + K.μ⁺ composite. The single unworked combination — `J = 1, R ≠ ∅` (delete the document's opening span, `L = ∅`, suffix survives) — is exactly the case where step-1 K.μ⁻ empties the text subspace to `n'_{s_C} = 0` and step-2 K.μ⁺ re-adds the survivors *into an emptied subspace*, re-pinning S8-depth from scratch. "First position with survivors" is a mandatory boundary and is the most delicate composite interaction; it is checked nowhere concretely.
**Required**: Add a worked example with `J = 1, c < N` (e.g. delete `q_1` from the `N = 5` document), verifying the K.μ⁻-to-empty then K.μ⁺-from-empty path and that `V_S(d') = {q_1,…,q_{N−1}}` with the survivors' I-addresses carried unchanged.

## OUT_OF_SCOPE

### Topic 1: Backtrack reconstructibility, concurrency, content-discovery indexing, orphaned-link obligations
**Why out of scope**: The Open Questions correctly defer these (reconstructing a prior arrangement from the store, serialization-free concurrent edits, a content-based discovery index after deletion, cross-document obligations on orphaning). They are new territory, not defects in this ASN; no action needed.

VERDICT: REVISE
