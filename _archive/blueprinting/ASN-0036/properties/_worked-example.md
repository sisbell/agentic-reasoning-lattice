## Worked example

We instantiate the state model with specific tumblers to ground the abstractions. Consider two documents: document `d₁` at tumbler `1.0.1.0.1` and document `d₂` at tumbler `1.0.1.0.2`. The user creates `d₁` with the text "hello" (five characters), then creates `d₂` which transcludes three characters ("llo") from `d₁` and appends two new characters ("ws").

**Initial state Σ₀**: empty. `dom(C) = ∅`, `dom(M(d₁)) = dom(M(d₂)) = ∅`.

**After creating d₁ with "hello"** — state Σ₁. Five I-addresses are allocated under `d₁`'s prefix, with element-level tumblers (`zeros = 3`):

| I-address `a` | `C(a)` |
|---|---|
| `1.0.1.0.1.0.1.1` | 'h' |
| `1.0.1.0.1.0.1.2` | 'e' |
| `1.0.1.0.1.0.1.3` | 'l' |
| `1.0.1.0.1.0.1.4` | 'l' |
| `1.0.1.0.1.0.1.5` | 'o' |

The arrangement `M(d₁)` maps V-positions (in subspace 1, text) to these I-addresses:

| V-position `v` | `M(d₁)(v)` |
|---|---|
| `1.1` | `1.0.1.0.1.0.1.1` |
| `1.2` | `1.0.1.0.1.0.1.2` |
| `1.3` | `1.0.1.0.1.0.1.3` |
| `1.4` | `1.0.1.0.1.0.1.4` |
| `1.5` | `1.0.1.0.1.0.1.5` |

*Check S0*: no prior content existed, so the implication holds vacuously. *Check S3*: every V-reference resolves — `ran(M(d₁)) ⊆ dom(C)`. *Check S7*: for `a = 1.0.1.0.1.0.1.3`, `origin(a) = 1.0.1.0.1 = d₁` — the document-level prefix directly identifies the allocating document. *Check S8*: the arrangement decomposes into a single correspondence run `(1.1, 1.0.1.0.1.0.1.1, 5)`. Verify: `M(d₁)(1.1 + k) = 1.0.1.0.1.0.1.1 + k` for `k = 0, 1, 2, 3, 4`. One run — the five characters were typed sequentially, receiving consecutive I-addresses by T10a (allocator discipline). *Check D-SEQ*: V₁(d₁) = {[1, k] : 1 ≤ k ≤ 5}, satisfying D-SEQ with n = 5. D-CTG holds (no gaps in the ordinal range 1..5) and D-MIN holds (min = [1, 1]).

**After creating d₂ with transclusion + append** — state Σ₂. The transclusion of "llo" from `d₁` shares the original I-addresses. The append of "ws" allocates two new I-addresses under `d₂`'s prefix:

| I-address `a` | `C(a)` |
|---|---|
| `1.0.1.0.2.0.1.1` | 'w' |
| `1.0.1.0.2.0.1.2` | 's' |

The content store now has 7 entries (5 from `d₁`, 2 new from `d₂`).

The arrangement `M(d₂)`:

| V-position `v` | `M(d₂)(v)` | origin |
|---|---|---|
| `1.1` | `1.0.1.0.1.0.1.3` | `d₁` (transcluded 'l') |
| `1.2` | `1.0.1.0.1.0.1.4` | `d₁` (transcluded 'l') |
| `1.3` | `1.0.1.0.1.0.1.5` | `d₁` (transcluded 'o') |
| `1.4` | `1.0.1.0.2.0.1.1` | `d₂` (native 'w') |
| `1.5` | `1.0.1.0.2.0.1.2` | `d₂` (native 's') |

*Check S0*: all 5 prior entries in `dom(C)` remain with unchanged values. The transition added 2 new entries. *Check S3*: every V-reference in `M(d₂)` resolves — positions `1.1`–`1.3` reference I-addresses from `d₁` (which exist by S1), positions `1.4`–`1.5` reference the newly allocated addresses. *Check S7*: for `a = 1.0.1.0.1.0.1.4` (the second 'l' in `d₂`), `origin(a) = 1.0.1.0.1 = d₁` — attribution traces to the originating document, not to `d₂` where the content currently appears. *Check S5*: the I-address `1.0.1.0.1.0.1.3` now appears in both `ran(M(d₁))` and `ran(M(d₂))` — sharing multiplicity is 2. *Check S8*: `M(d₂)` decomposes into two correspondence runs: `(1.1, 1.0.1.0.1.0.1.3, 3)` for the transclusion, and `(1.4, 1.0.1.0.2.0.1.1, 2)` for the native content. Two runs partition the five V-positions exactly. *Check D-SEQ*: V₁(d₁) is unchanged — {[1, k] : 1 ≤ k ≤ 5}, D-SEQ with n = 5. V₁(d₂) = {[1, k] : 1 ≤ k ≤ 5}, D-SEQ with n = 5. Both satisfy D-CTG and D-MIN.

**After deleting "llo" from d₁** — state Σ₃. DELETE removes V-positions `1.3`–`1.5` from `M(d₁)`:

| V-position `v` | `M(d₁)(v)` |
|---|---|
| `1.1` | `1.0.1.0.1.0.1.1` |
| `1.2` | `1.0.1.0.1.0.1.2` |

*Check S0*: all 7 entries in `dom(C)` remain. The I-addresses `1.0.1.0.1.0.1.3`–`.5` are no longer in `ran(M(d₁))` but persist in `dom(C)`. *Check S6*: these three addresses are now "orphaned" from `d₁`'s perspective, but still referenced by `M(d₂)` — persistence is unconditional. *Check S9*: the deletion modified `M(d₁)` but `C` is unchanged — separation holds. *Check S8*: `M(d₁)` is now a single run `(1.1, 1.0.1.0.1.0.1.1, 2)`. The prior 1-run decomposition became a 1-run decomposition (the deletion removed an entire suffix, not a middle segment). `M(d₂)` is unchanged — still two runs. *Check D-SEQ*: V₁(d₁) = {[1, k] : 1 ≤ k ≤ 2}, D-SEQ with n = 2. D-CTG holds (no gaps in 1..2) and D-MIN holds (min = [1, 1]). V₁(d₂) is unchanged — D-SEQ with n = 5.
