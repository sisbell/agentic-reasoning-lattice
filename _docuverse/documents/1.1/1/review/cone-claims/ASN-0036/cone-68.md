## Audit

**AX-1, AX-2, S0** are well-formed axioms. Each is stated as a protocol design posit with no derivation obligations, and their formal contracts are internally consistent. Nothing to flag.

**S1** proof is one step: S0 gives `a ∈ dom(Σ'.C)` directly, which is `dom(Σ.C) ⊆ dom(Σ'.C)` by universal generalization. The step is sound. The Forward References entry for GlobalUniqueness is noted below.

**S3** proof: base case is vacuous by AX-1 (empty domain, no witness possible). Inductive step fixes arbitrary `v ∈ dom(Σ'.M(d))` and splits on inherited vs. new/redirected. The inherited case uses J0 + S1 correctly: IH gives the address in `dom(Σ.C)`, S1 lifts it to `dom(Σ'.C)`. The new/redirected case matches AX-2's range condition exactly (`v ∈ dom(Σ'.M(d))` is already given; the disjunction on `dom(Σ.M(d))` membership matches AX-2's explicit guard), yielding `Σ'.M(d)(v) ∈ dom(Σ'.C)` directly. The two cases are exhaustive (P / not-P on the inherited predicate). The proof is sound.

---

### Document order inverts S1's declared dependency on S0

**Class**: REVISE
**Foundation**: N/A (internal consistency)
**ASN**: S1 (StoreMonotonicity) — proof opens "By S0 (content immutability), `a ∈ dom(Σ.C)` implies..."; document order: AX-2 (pos 1), S1 (pos 2), AX-1 (pos 3), S0 (pos 4), S3 (pos 5)
**Issue**: S1's proof invokes S0 as a premise, and S1's Formal Contract correctly lists S0 in Depends. But S1 appears in document position 2 while S0 is in position 4. A reader processing the document sequentially encounters "By S0..." before S0's axiom statement has been made; a tool resolving symbols linearly would find S0 undefined at the point of use. The dependency graph and the document order are inconsistent.
**What needs resolving**: Reorder so that all axioms with no proof obligations (AX-1, S0, AX-2) precede the theorems that cite them (S1, then S3). The natural dependency-respecting order is AX-1 → S0 → AX-2 → S1 → S3.

---

### Reviser drift in S3 — "the earlier reading" paragraph

**Class**: REVISE
**Foundation**: N/A (internal consistency)
**ASN**: S3 (ReferentialIntegrity) — paragraph beginning "It is worth saying why S1 alone does not close the argument" through "the new-reference half that AX-2, not S1, supplies"
**Issue**: The phrase "the earlier reading" names a historically contested interpretation and the paragraph explains why that reading was wrong. This is the relocated-rather-than-removed pattern: the proof's case split (inherited / new-or-redirected) already correctly separates the roles of S1 and AX-2; the paragraph then repeats the same case structure in meta-form as a refutation of a past error. The paragraph does not advance the proof — it defends against a prior finding. Defensive prose of this kind accumulates across cycles and signals that a declined finding has been absorbed into the argument body rather than discarded.
**What needs resolving**: Remove the "It is worth saying..." paragraph. The proof's case structure speaks for itself; the roles of S1 (inherited case) and AX-2 (new/redirected case) are already named at the point where each is applied.

---

### Forward References slot used as a disclaimer for a non-dependency prose citation

**Class**: OBSERVE
**Foundation**: N/A (internal consistency)
**ASN**: S1 (StoreMonotonicity) — prose: "each at a fresh address guaranteed unique by GlobalUniqueness (ASN-0034)"; Formal Contract Forward References: "GlobalUniqueness... not used in S1's proof, whose single step is S0"
**Issue**: GlobalUniqueness appears in S1's prose as if grounding a claim, then the Formal Contract's Forward References slot is used to disclaim the dependency: "not used in S1's proof." Forward References conventionally lists claims cited before their definition appears in this document; GlobalUniqueness is defined in ASN-0034, a declared ASN dependency — not a later section of this document. The slot is absorbing a disclaimer that exists because the prose citation creates a false appearance of dependency. The disclaimer is correct but placed in the wrong structural position.
**What needs resolving**: Either remove the GlobalUniqueness citation from S1's prose (it is not load-bearing for S1's monotonicity argument and its proper home is whichever claim — S4, S7 — actually needs it), or retain it with an explicit inline qualifier ("as context for later claims") and remove the Forward References entry. The Forward References slot should not be used as a disclaimer for prose citations.

---

VERDICT: REVISE