# Formalize — ASN-0036 / S9

*2026-04-12 14:20*

**S9 (Two-stream separation).** No modification to any arrangement `Σ.M(d)` can alter the content store `Σ.C`:

`[Σ'.M(d) ≠ Σ.M(d) ⟹ (A a ∈ dom(Σ.C) :: a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a))]`

*Proof.* S0 (content immutability) guarantees that for every state transition `Σ → Σ'`, unconditionally:

`[a ∈ dom(Σ.C) ⟹ a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a)]`

That is: every address in `dom(Σ.C)` persists with unchanged value in `Σ'`, regardless of what else changes in the transition. Call this guarantee Q.

S9 has the form `P ⟹ Q`, where P is `Σ'.M(d) ≠ Σ.M(d)`. The consequent Q is exactly S0's universal guarantee. Since S0 establishes Q for every transition without qualification, the implication `P ⟹ Q` holds for every transition: when P obtains (some arrangement was modified), Q holds by S0; when P does not obtain (no arrangement changed), the implication is vacuously satisfied. ∎

S9 is the formal statement of Nelson's claim: "The integrity of each document is maintained by keeping the two aspects separate: derivative documents are permanently defined (and stored) in terms of the originals and the changes." It says: the two state components are coupled only through S3 (referential integrity). Arrangements depend on the content store — S3 requires every V-reference to resolve — but the content store is independent of all arrangements. This is a one-way dependency:

```
C ← M(d₁), M(d₂), M(d₃), ...
```

Changes to any `M(d)` cannot break `C`. But changes to `C` could break `M` — which is precisely why `C` is immutable. S0 (content immutability) is the mechanism; S9 (two-stream separation) is the consequence.

The asymmetry is deliberate and load-bearing. Nelson enumerates the guarantees that depend on it: link survivability (links point to I-addresses, which S0 preserves), version reconstruction (historical states are assembled from Istream fragments, which S0 preserves), transclusion integrity (transcluded content maintains its value because S0 prevents mutation), and origin traceability (I-addresses encode provenance permanently because S0 prevents reassignment).

Gregory's implementation confirms the separation operationally. Every editing command in the FEBE protocol works exclusively on arrangement state. Of the editing commands Nelson specifies, none modifies existing Istream content. Commands that create content (INSERT, APPEND) extend `dom(C)` with fresh addresses and simultaneously update some `M(d)`. Commands that modify arrangement (DELETE, REARRANGE, COPY) touch only `M(d)`, leaving `C` untouched. No command crosses the boundary in the dangerous direction — no arrangement operation can corrupt stored content.

*Formal Contract:*

- *Invariant:* For every `Σ → Σ'`: `[Σ'.M(d) ≠ Σ.M(d) ⟹ (A a ∈ dom(Σ.C) :: a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a))]`. Arrangement modifications cannot alter stored content.
- *Frame:* `Σ.C` is preserved across all state transitions (by S0); in particular, arrangement-modifying transitions cannot alter `C`.
