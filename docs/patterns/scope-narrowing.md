# Scope Narrowing

## Pattern

A broad investigation produces broad results — internally consistent at a high level but imprecise in the details. To harden the work, narrow the scope. Break the whole into pieces, converge each piece independently against fixed context. The narrowing is what enables convergence: each piece is small enough to fully verify, and its context doesn't shift while you work on it.

When narrowing overshoots — when the pieces are too coupled to converge independently — widen until the problem is visible. The right scope matches the coupling strength of the problem. Loosely coupled pieces converge at narrow scope. Tightly coupled pieces need wider scope. The pattern is the narrowing and the adjustment when it goes too far.

## Forces

- **Broad scope can't harden.** Discovery produces a reasoning document with 29 properties. Reviewing the whole document at once can't make each property precise — there's too much to hold in focus.
- **Narrow scope enables convergence.** One property at a time, dependencies fixed. The piece is small enough to fully check. Changes don't cascade to neighbors. This is [review/revise iteration](review-revise-iteration.md) — and it works for most properties.
- **Over-narrowing hides coupling.** Some properties can't be verified in isolation. S8 depends on 7 other properties — checking S8 alone misses the seams between them. This is the [dependency cone](dependency-cone.md).
- **The right width is discovered, not prescribed.** You don't know the coupling in advance. You narrow, hit a wall, widen to the cluster, check again. The three scopes that formalization settled on (property, cluster, full ASN) weren't planned — they're where the system found equilibrium.

## Structure

```
broad (discovery)
  │
  narrow ──→ per-property (formalization)
  │            │
  │            stalls on coupling
  │            │
  │            widen ──→ per-cluster (cone review)
  │                        │
  │                        verify coherence
  │                        │
  └── verify the whole ←──┘
```

The narrowing is progressive. Discovery works at full-ASN scope. Blueprinting breaks it into properties. Formalization reviews each property. When property-level review stalls on a [dependency cone](dependency-cone.md), cone review widens to the cluster. [Verify the whole](verify-the-whole.md) checks that the hardened pieces cohere.

## Leads to

[Verify the whole](verify-the-whole.md) — narrowing without verification produces pieces that don't fit together. Every narrowing step needs a corresponding coherence check at the original width.

[Dependency cone](dependency-cone.md) — the signal that narrowing has overshot. One property thrashing against stable dependencies means the scope is too narrow for the coupling.

## Applications

### Blueprinting

Discovery produces a 15-page reasoning document. Blueprinting narrows: decompose into sections, enrich each section with type/dependencies/vocabulary, disassemble into per-property file pairs. Each property is now a self-contained unit that formalization can work on independently.

### Formalization

Formalization narrows further: review one property at a time. Proof review checks the proof. Contract review checks the contract. Each review cycle operates within the property's scope, with dependencies as fixed context.

When proof review converged 31 of 32 properties but kept cycling on S8, the narrowing had overshot. S8's 7 dependencies created coupling that property-scope review couldn't resolve. Widening to the S8 cone (apex + dependencies) gave the reviewer enough context to see the constraint system. The scope matched the coupling.

### Discovery

Even discovery uses scope narrowing. Scoped inquiry narrows the question along authority boundaries — theory gets theory questions, evidence gets evidence questions. Each authority works within its narrowed scope. The synthesis step verifies the whole.

## Origin

The narrowing was present from the start — blueprinting was created because discovery-scale documents were too broad to formalize. The adjustment (widening when stuck) was discovered through the dependency cone on ASN-0036. The pattern was recognized when the history showed a consistent sequence: narrow to make progress, hit a wall at tight coupling, widen until the problem is visible, settle at the scope that matches.
