# Citation Resolve — ASN-0036/D-CTG — run 1

*2026-06-25T02:28:46Z*
*Model: sonnet*

## Output

The claim bodies confirm enough to classify. Now applying the test to each label in the D-CTG prose:

**S8a** — The preconditions explicitly cite it for `zeros(v) = 0` well-formedness (the axiom's quantifier restricts to V-positions satisfying this). The axiom itself uses `zeros(v) = 0` which S8a defines as the domain restriction. → **depends**

**T0** — Cited as "by T0" in the precondition `zeros(v) = 0 ⟺ S8a positivity, by T0`. T0 supplies the equivalence that grounds the axiom's `zeros(v) = 0` condition. → **depends**

**S8-depth** — Listed in preconditions as supplying the common-depth invariant (#v = #u in the axiom's quantifier). The axiom's guard `#v = #u` directly uses this. → **depends**

**T1** — Listed in the Depends block as "defines the order" for `u < v < q`. The axiom's strict ordering relation `<` is the lexicographic order T1 supplies. → **depends**

**S8-fin** — Appears in the closing prose: "Combined with S8-fin (dom(M(d)) is finite), contiguity at depth 2 says…" — this is a consequence/elaboration remark; D-CTG's axiom does not consume finiteness; S8-fin is named as a companion that, together with D-CTG, yields a corollary. → **forward**

```
CLASSIFICATIONS:
- label: S8a
  direction: depends
  bullet: "- S8a (Σ.M(d) domain restriction) — supplies the V-position well-formedness constraint `zeros(v) = 0` used in the axiom's quantifier guard and the S8a positivity precondition"

- label: T0
  direction: depends
  bullet: "- T0 (ASN-0034) — supplies the equivalence `zeros(v) = 0` iff every component is positive, invoked in the precondition `zeros(v) = 0 ⟺ S8a positivity, by T0`"

- label: S8-depth
  direction: depends
  bullet: "- S8-depth (Fixed-depth V-positions) — supplies the common-depth invariant `#v = #u` used in the axiom's quantifier guard to restrict intermediates to the same tumbler depth"

- label: T1
  direction: depends
  bullet: "- T1 (LexicographicOrder, ASN-0034) — defines the strict total order `<` on tumblers used throughout the axiom's ordering guards `u < q`, `u < v < q`"

- label: S8-fin
  direction: forward
  bullet: "- S8-fin (Finite arrangement) — combined with D-CTG, yields the corollary that V_1(d) occupies a single unbroken finite block of ordinals; named as a downstream companion, not a dependency of this claim's axiom"

RETRACTIONS: []
```
