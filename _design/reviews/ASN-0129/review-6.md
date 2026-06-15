This is an unusually careful digest. I checked the conjecture/theorem/lemma taxonomy, the forced/conventional split, every Green claim against the evidence, and the proposed approaches against the note's own commitments. I found no material problem. A few genuine but non-load-bearing tightenings follow, most-valuable first.

**Solid, for the record:** The proof-status taxonomy (PC6 theorem / PC6a proven / C-reach·C-emit·parity conjectured) is meticulous — including the non-obvious and *correct* logic that C-reach ⟹ PC6a but not conversely, and that C-emit's baseline is a *separate* read-off-V grammar fact (frontier arithmetic, not closure) on which no-fixpoint has no bearing. The forced/conventional discipline is right throughout (AM-keying/BH3-opt-in conventional; UV's per-codomain content forced). The cross-type footprint warning for footprint-indexed dispatch correctly identifies the one place a naive implementation silently skips a changed trigger (a real correctness trap, not decoration). Every Green claim is evidence-backed. The V-TUP regime asymmetry (`addrs` irreducible, coverage derivable from `addrs+≼`, admitted for parity) is a sound and useful reading of the note's own derivability discussion.

---

**Revision list**

1. **[SHARPENING]** "What must be built / read-base adapter" and "Guarantees / structural-reads-only": the digest gives the document store's read *scope* correctly (membership-only, no enumeration — grounded in Green's no-document-census) but underweights *why a document read is admitted at all*. Add the note's QD-audit/V-DOC rationale: `is_doc` exists because a gating discipline written in PL must be able to *state the home-residence check the emit surface itself performs* (on every `idem=⊤` miss I1, every admitted `idem=⊥` call I5, every `Nullify_Binary` call P0) — which is exactly what bounds the read to membership-at-an-address. This justifies the precise scope rather than leaving the document store's special status as an unexplained asymmetry a builder might either over-extend or strip.

2. **[SHARPENING]** "Design commitments / dynamics" (worked trace uncaptured): the digest states the dynamics classes abstractly (PD0 ST locks, PD1 active oscillates) but omits the concrete gate-author trap the note's trace exists to demonstrate — a quiescence/emptiness predicate is *vacuously true at the empty store*, so a fire-until-Q termination gate fires before any activity occurs; a sound gate needs an *activity witness* (e.g. an audit-view ST companion that is ⊥ at the empty store and locks ⊤ thereafter). One line, since it's the clearest payoff of the whole dynamics theory for the protocol layer the note hands work to.

3. **[SHARPENING]** "What must be built / read-base adapter": "resolving `home(a')` out of the stored record … *which is why* home-grouping is no atom" — the causal link is loose. Home-grouping is no atom because the vocabulary admits none (a design choice; C-emit: "no atom to regroup it by home"); resolving `home` inside the leaf (whether by record-read à la Green or T4 extraction à la the note, both valid — only prefix testing is barred) is the *companion* fact, not the cause. Tighten so the implementation choice isn't presented as producing the vocabulary fact.

---

VERDICT: CONVERGED
