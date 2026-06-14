# Review of ASN-0123

I read the note in full and checked the load-bearing proofs, the boundary cases, self-containment, and ran the anti-bloat pass the classifier asks for. My findings are below; the short version is that the technical content holds and the prose accretion I could find dissolves into load-bearing content on inspection.

## REVISE

(none)

## What I verified

**The hard proofs check out.**

- **SA (antichain).** With `a = [d₀,0,s,k] ≺ b = [d',0,s',k']`: `#d' ≥ #d₀+1`, so `b`'s separator at position `#d₀+1` falls inside `d'`, which already carries `d₀`'s two zeros on positions `1…#d₀`; three zeros contradicts `zeros(d')=2`. Sound, and the displayed `{a}` follows by reflexivity.
- **VN-B1 (contiguity).** I walked every K.δ case for both `g=1` and `g=2`: Node excluded by `zeros=2`; the base-tier spawn `k=g` forces `t=p, j=1` by length-then-T3; the other inter-tier spawn `k=3−g` excluded by the penultimate component (separator `0` vs `p_{#p}≠0`); the `k=0` sibling forces `t=c_{j−1}`, and freshness + IH pin `j=m+1`. The unified `sig(c_{j−1})=#c_{j−1}` step is correct for the `g=2` stream too (the rightmost nonzero is the trailing ordinal, separator untouched). The induction is genuinely complete.
- **nextv/nextd.** The frontier identity `next = c_{hwm+1}` is re-derived from VN-B1 + S0 + the `next` definition, *not* via ASN-0040 B2 (whose global-B1 precondition `E` does not meet) — the correct non-transfer.
- **V-WF.** Both branches discharged: owned (single version K.δ), account-tier cross-owner (single document K.δ in `A_doc(pfx(π)) = S(pfx(π),2)`), each with operand/parent/freshness preconditions, then K.μ⁺ over the canonical content positions and `|A|` K.ρ steps; couplings J0/J1★/J1'★ evaluated initial-to-final; `n=0` collapses to the lone K.δ. The boundary-property lift (P4★∧P4a∧P7a at Σ′ via P-bdy) is correctly justified.
- **PS / ω-totality.** The position-1 preservation induction (TA5(b)/(d) for `k>0`; `sig(t)=#t≥3` for `k=0` non-node operands) correctly yields `n₀ ≼ e` for all `e∈E`, feeding O2's coverage hypothesis. The cross-foundation hybrid is honestly flagged as an assumption, not a theorem.
- **V8 / V9.** V8's coverer-set equality is sound (Z-mono + O1a kills the long-coverer case). V9's O5(ii)-as-theorem is clean (`w=[pfx(π),0]` has `zeros=2`, prefixes `pfx(π'')`, contradicts O1a), and both branches of the severance comparison genuinely close. This is the reviewer-protected discharge and it holds.
- **V9w / V10 / V13.** Source-side row via P4★ at the boundary (needs P-bdy — load-bearing); V10 is LP12 at `d=v` with `ran(Σ′.M(v))=A` and `L'=L`; V13 is pinned both ways by J1★/J1'★.

**Boundaries.** Empty source (`n=0`), shared content within a document (`|A|<n`, two provenance rows for three positions in the worked instance), a source carrying a link subspace (V2b makes link transcription impossible, not merely omitted), iterated forks (V6, no separator-budget pressure at depth 1), and `d_src ≠ v` always (v fresh) — all handled.

**Self-containment.** Every ASN reference is to a foundation (0034/0036/0040/0042/0043/0045/0047/0053/0058/0086/0093/0098). No reinvented notation — `trunc`, `Z-mono`, `SA`, `nextv/nextd`, `VN-B1` are new local apparatus, and the cited `derives`/`acct`/`origin`/`hwm`/`next` are used per their foundation definitions.

## OUT_OF_SCOPE

The note defers document-from-nothing, version comparison, content/link operations, delivery, and replication, and its Open Questions capture the genuine future work (non-VERSION allocations into a version namespace; recovering derivation direction across ownership; link-about-link versioning; concurrent-fork serialization; location-fixed windowing). I have nothing to add here — scope is drawn correctly.

## Anti-bloat pass

I examined the candidates this classifier targets and found each load-bearing:

- The forward references VD/V7/V5 → V9 are cross-links in an interlocking argument, not content-deferrals (severance is an ownership fact whose *consequences* legitimately surface in the identity section); only V5's "under VD below" is a true pointer, and it is singular.
- V0's "P-tier confines the operation to exactly these two branches … so no third branch contributes to the count" reads as defensive at first, but the node-tier exclusion is genuinely what preserves single-mint (a node-tier cross-owner fork would have to mint an account *and* a document), so the clause carries weight.
- The GlobalUniqueness collision-type restatement sets up the specific same-allocator invocation two sentences later; the J4 remark and the V2b/V10 channel statements are "what the operation does/does not do," which the guidance explicitly excludes from meta-prose.

Replacing any of these with a bare citation is the shape of the previously declined post-convergence dep audit, and the conclusion is the same: nothing replaceable.

VERDICT: CONVERGED
