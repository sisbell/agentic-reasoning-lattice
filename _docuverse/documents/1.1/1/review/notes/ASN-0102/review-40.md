# Review of ASN-0102

## REVISE

### Issue 1: X8 within-reference non-coalescence skips the load-bearing contiguity step

**ASN-0102, X8 (RunFragmentation)**: "resolve(d_s, σ) already returns the maximally-merged decomposition (ASN-0058, C1a/M12), which by definition contains no pair satisfying M7's conjunction of V- *and* I-adjacency. Hence no within-reference pair is a merge candidate."

**Problem**: The inference does not close. A merge candidate in the *target* requires target-V-adjacency (which every consecutive copied block has *by construction*, `c_{j+1} = c_j + n_j`) plus I-adjacency (I-coords are unchanged). The source's maximal-merge property only tells you no pair is *both* V- and I-adjacent *in the source*. To transfer that to the target you must know that consecutive resolved runs are V-adjacent *in the source* — only then does maximal-merge forbid their I-adjacency. As written, a hypothetical source pair that is I-adjacent but V-*separated* would re-lay contiguously in the target and coalesce, directly contradicting the claim. The conclusion is in fact correct, but only because the source content-subspace V-domain is gap-free (D-SEQ, ASN-0036), so the span's restriction `f = M(d_s)|⟦σ⟧` has a contiguous V-domain and consecutive maximal runs are V-adjacent. That bridge is exactly what makes "maximally-merged ⟹ no within-reference target merge candidate" valid, and it is never stated.

**Required**: Insert the missing step — consecutive resolved runs are source-V-adjacent because the source content subspace is contiguous (D-SEQ), whence maximal-merge rules out their I-adjacency, whence the target-V-adjacent copied blocks are not I-adjacent. Without it, "Hence no within-reference pair is a merge candidate" is a claim, not a derivation.

### Issue 2: composite-boundary fact established twice (anti-bloat)

**ASN-0102, Definition (Amendment) and X14**: Definition — "A standalone COPY `Σ → Σ'` is then a valid composite … so its endpoints `Σ` and `Σ'` are **composite boundaries**, at which … P4★ … hold." X14 — "As established in the Definition, a standalone COPY is a valid length-1 composite whose endpoints `Σ`, `Σ'` are composite boundaries — so the coupling clauses J0/J1★/J1'★ are evaluated between them and the composite-boundary property P4★ holds at `Σ`."

**Problem**: The same conclusion (standalone COPY ⟹ endpoints are composite boundaries ⟹ P4★/J-couplings evaluated between Σ and Σ') is constructed in full in two places. The Definition states it as setup; X14 re-states it in different words before consuming it. One is enough.

**Required**: State the composite-boundary consequence once (in the Definition), and have X14 invoke it by name rather than reconstruct it.

## OUT_OF_SCOPE

### Topic 1: The four Open Questions
**Why out of scope**: Continued discoverability under later displacement, transitive containment-recording when a referencing document is itself a source, time-varying resolution views, and identity when the allocating document becomes unreachable are all genuine future-ASN territory (link-projection/displacement, reachability, version semantics), not defects in this operation's contract. The ASN correctly parks them rather than half-answering.

VERDICT: REVISE
