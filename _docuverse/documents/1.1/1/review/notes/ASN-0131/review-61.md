# Review of ASN-0131

The operation is well-posed: `RE` is a pure query reading `Σ.M(d)` and `Σ.L` (via `nullified`), returning role-tagged endsets with link identity discarded. I verified the core machinery against the definition.

- **RE-DEF reformulation** `RE = {(i,e) ∈ Avail(Σ) : touch_W(e)}` is sound — `touch_W(e)` depends only on `e`, so it pulls out of the existential over `a`, and `Avail(Σ)` is region-independent. This grounds RE-UDIST and RE-CWP correctly.
- **RE-UDIST** (image-union → `touch_W` disjunction → filter) checks out, no injectivity needed. **RE-UDIST-∩**: the one-sided `⊆` follows from the image `⊆` law, and the `⊇` counterexample (`Σ.M(d) = {[1,1]↦a, [1,2]↦a}`, M14-permitted) genuinely refutes equality.
- **RE-CWP** is a correct, non-trivial wp: `image(W,d,Σ') = I_R`, `Δ = image ∖ I_R`, quantifying over `Avail(Σ)` coincides with quantifying over surfaced pairs (non-surfaced satisfy the implication vacuously), and the `R=∅` boundary collapses to `RE = ∅`. The "same-endset must reach both" refinement of D-CWP is correctly drawn.
- **RE-ADDR / RE-RET**: the antichain argument (R0a) plus unit-depth to-set correctly yields fresh-output addressability; the retraction "drops iff sole addressable bearer" is sound in both directions (R-Scope confines the new nullification to `ℓ`, so `ℓ' ≠ ℓ` survives by L12; under `coverage(Θ) ∩ dom(Σ.C) = ∅` the emitter `b` re-witnesses nothing).
- **Worked instance** verified end to end (the `θ ≼ c` separator-zero argument forcing `E(c)₁ = s_type` is valid); it exercises RE-OVL, RE-CLIP, RE-WHOLE, RE-UNIT as claimed.

No correctness, cross-reference (all citations are to foundation ASNs), or scope-drift problems. The findings are the meta-prose accretion the anti-bloat classifier targets.

## REVISE

### Issue 1: Use-site inventory tail on the `Σ.L`-evolution bridge
**ASN-0131, "When does an endset touch the region?" preceding section (bridge paragraph)**: "The one ASN-0086 fact we consume at definition time is `nullified` itself … which the bridge carries here to ground `addressable` in RE-DEF and its decidability below; **the remaining ASN-0086 lemmas this note borrows are licensed by the same bridge and cited where each is used.**"
**Problem**: The bolded clause is forward-reference bookkeeping — it enumerates downstream consumers rather than advancing the bridge's argument. The per-use "via the `Σ.L`-evolution bridge" tags (at R0a in RE-ADDR, at R-Scope in the retraction section) already convey exactly this, and the inventory clause doesn't even discharge its own promise consistently (R6a is cited later without the tag). This is the "definition's introduction enumerates downstream consumers" pattern.
**Required**: Delete the clause after the semicolon. The first half (consuming `nullified` to ground `addressable`) is load-bearing and should stay.

### Issue 2: Internal restatement in the conservative-lift paragraph
**ASN-0131, "Stability" (insert/delete sub-section)**: "That settles the `(C, M)` behaviour but cannot speak to the three stores `Σ.L`, `Σ.E`, `Σ.R` that the full state `(C, L, E, M, R)` adds and the `(C, M)` primitives never name — **a `(C, M)`-spec leaves a primitive's action on stores absent from its model entirely unconstrained.**"
**Problem**: The clause after the em-dash restates the clause before it ("cannot speak to … never name" and "leaves … unconstrained" are the same point in different words). One of the two carries the pivot to "therefore adopt the conservative lift"; the other is redundant.
**Required**: Collapse to one clause — keep the version that states "unconstrained, therefore we adopt the conservative lift," drop the duplicate.

### Issue 3: Attributed-retraction exclusion stated twice across sections
**ASN-0131, standing-assumption paragraph**: "…adopting it **excludes attributed retractions** (non-empty from-set), which ASN-0086's Convention RetractionDirectionality would otherwise permit."
**ASN-0131, "Stability" (retraction sub-section)**: "the from-set `∅` — empty because the standing commitment admits only `Nullify` retractions, **not the attributed ones ASN-0086 otherwise permits** — …"
**Problem**: The use site re-explains the exclusion the standing assumption already established. At the use site only "from-set `∅` (standing commitment)" is needed; "not the attributed ones ASN-0086 otherwise permits" recapitulates the earlier paragraph. This is the "two paragraphs in different sections say the same thing" pattern.
**Required**: At the retraction use site, drop "not the attributed ones ASN-0086 otherwise permits" — cite the standing commitment for the empty from-set and move on.

### Issue 4: Defensive and document-ordering micro-justifications
**ASN-0131, "Stability" (insert/delete)**: "So delete-stability is scoped to text depth `#p = 2` and insert-stability to every `#p ≥ 2` — **an asymmetry in which displacement primitives ASN-0082 supplies, not in the stability argument itself.**"
**ASN-0131, "Composing regions" (intersection)**: "The construction turns on one general fact about emission, **which we establish here and reuse under Stability below.**"
**Problem**: Both trailing clauses are meta-prose, not reasoning — the first preemptively defends the asymmetry ("not in the stability argument itself"), the second justifies where RE-ADDR is placed ("establish here and reuse … below"). The depth-scope is already stated by "#p = 2" vs "#p ≥ 2"; RE-ADDR's reuse is self-evident from its later citations.
**Required**: Drop "not in the stability argument itself" and "and reuse under Stability below" (keep "establish here," since RE-ADDR is genuinely introduced at first use in that section).

## OUT_OF_SCOPE

None to add — Open Questions 1–7 correctly defer the out-of-scope territory (rendered/V-order answers, injectivity-recovered intersection equality, cross-store completeness, type-slot-against-content, link-subspace regions). RE-WHOLE is appropriately held provisional under OQ1, with RE-CLIP standing firm under either resolution.

META: not applicable — the ASN defines an abstract query operation with state-reading semantics and system-level guarantees (soundness, completeness, distributivity, stability), not implementation mechanics.

VERDICT: REVISE
