# Citation Resolve — ASN-0036/D-CTG-depth — run 1

*2026-06-25T02:46:36Z*
*Model: sonnet*

## Output

I have all the files I need. Let me compile the classifications.

Labels found in the prose:
- **D-CTG** — the contiguity axiom invoked to force `w ∈ V_1(d)` → `depends`
- **S8-depth** — supplies common depth `m`; precondition and throughout the proof → `depends`
- **S8a** — proof applies it to `u` to verify all components of `w` are ≥ 1 → `depends`
- **S8-fin** — the finiteness fact whose contradiction closes the proof → `depends`
- **T0(a)** — directly invoked to generate infinite strictly-increasing witness sequence → `depends`
- **T1(i)** (label: `T1`) — "by T1(i)" at two comparison steps (w > u, w < x) → `depends`
- **T3** — "by T3, CanonicalRepresentation, they are unequal" to distinguish distinct tumblers → `depends`
- **T4** — mentioned only after ∎ as explanatory background for 1-based ordinals ("zero serves as a field separator (T4, ASN-0034)"); the proof's correctness does not rest on it → `forward`

```
CLASSIFICATIONS:
- label: D-CTG
  direction: depends
  bullet: "- D-CTG (VContiguity) — supplies the contiguity axiom that any tumbler strictly between two V_1(d) positions at depth m lies in V_1(d); proof invokes it to place each witness w in V_1(d)"

- label: S8-depth
  direction: depends
  bullet: "- S8-depth (Fixed-depth V-positions) — supplies the common depth m shared by all positions in V_1(d); consumed as a precondition and throughout the proof"

- label: S8a
  direction: depends
  bullet: "- S8a (Σ.M(d) domain restriction) — supplies componentwise positivity of V-positions; proof applies it to u to verify every component of the constructed w is ≥ 1, qualifying w for D-CTG's consequent"

- label: S8-fin
  direction: depends
  bullet: "- S8-fin (Finite arrangement) — supplies finiteness of dom(M(d)); the infinite sequence of distinct witnesses contradicts this, closing the proof"

- label: T0(a)
  direction: depends
  bullet: "- T0(a) (UnboundedComponentValues, ASN-0034) — supplies, for any bound M, a natural-number witness n > M; iterated to produce the strictly-increasing infinite sequence n₁ < n₂ < n₃ < … of distinct tumblers"

- label: T1
  direction: depends
  bullet: "- T1 case (i) (LexicographicOrder, ASN-0034) — supplies first-divergence comparison; used at two steps to establish u < w and w < x from the component-level inequalities"

- label: T3
  direction: depends
  bullet: "- T3 (CanonicalRepresentation, ASN-0034) — supplies that distinct component sequences yield distinct tumblers; used to establish that distinct values of n at component j+1 produce pairwise-distinct positions w"

- label: T4
  direction: forward
  bullet: "- T4 (HierarchicalParsing, ASN-0034) — cited as background for why position 0 is structurally unavailable (zero is a field separator); V-positions follow 1-based ordinals as a consequence"

RETRACTIONS: []
```
