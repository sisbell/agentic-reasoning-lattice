# Review of ASN-0047

## REVISE

### Issue 1: C1c (and TrackedEmission) inconsistently included in the per-state invariant set

**ASN-0047, *Extended reachable-state invariants* vs. *Initial state invariant verification* vs. *Properties Introduced***: The authoritative `ExtendedReachableStateInvariants` conjunction lists

> "S2 ∧ S3★ ∧ S3★-aux ∧ S4 ∧ S7a ∧ S7b ∧ **C1b ∧ C1c ∧** S7d ∧ ..."

and the Class (a) verification matrix carries a dedicated `C1c (ASN-0093)` row. But:

- the **base case** ("*Initial state invariant verification* ... We enumerate the verifications to make the base case of the inductive proof explicit") lists only "*S4, S7a, S7b, C1b (content invariants)*: dom(C₀) = ∅, vacuous." — **C1c is absent** from the explicitly-enumerated base case;
- the **Properties Introduced** summary row for `ExtendedReachableStateInvariants` reads "... ∧ **C1b ∧** S7d ∧ ..." — **C1c is dropped** from the restated invariant set.

Symmetrically, `TrackedEmission` is labelled a "*Per-state invariant (EntityEmissionTracking)*" and is given a discharge ("*TrackedEmission.* Established by the self-contained induction in its definition box"), yet it does **not** appear in the `ExtendedReachableStateInvariants` conjunction at all.

**Problem**: The note states two different versions of the same invariant set, and the base-case enumeration — whose stated purpose is to be exhaustive — omits a conjunct the matrix and authoritative list both carry. A reader cannot tell whether C1c and TrackedEmission are members of the proven invariant set. This is the precise failure mode the review standard targets: an invariant conjunct asserted in one statement and silently skipped in another.

**Required**: Pick one canonical membership list and make the base case, the matrix, the conjunction, and the Properties-Introduced summary agree. Either include C1c (and TrackedEmission) uniformly — adding the (vacuous, dom(C₀)=∅) base-case line for C1c and a TrackedEmission conjunct + base line — or, if TrackedEmission is deliberately tracked outside the conjunction, say so where the conjunction is stated.

### Issue 2: Duplicated "realisation artifact" prose across K.μ~ clause (v) and *Link V-position permanence*

**ASN-0047, *Decomposition of K.μ~* (clause (v) discussion) and *Link V-position permanence***: The same point — that single-K.μ~ link fixity is a *realisation artifact* and that a withdraw-and-re-add composite re-seats a link without violating any invariant — is stated twice:

> clause (v): "Consequently single-K.μ~ link fixity is a *realisation artifact*, not a lifetime guarantee ... a withdraw-and-re-add composite re-seats a link without violating any invariant (*Link V-position permanence* below)."

> *Link V-position permanence*: "As established at clause (v), single-K.μ~ link fixity is a realisation artifact; ... we exhibit the re-seating composite here. A withdraw-and-re-add composite re-seats a link without violating any invariant ..."

**Problem**: Two paragraphs in different sections assert the same claim, each pointing at the other (forward reference at clause (v), back reference at the section). This is the deferral-loop and say-it-twice pattern the anti-bloat classifier flags; the reader who follows the clause-(v) pointer arrives at a paragraph that restates clause (v).

**Required**: State the "realisation artifact, not lifetime guarantee" point once. Keep the *Link V-position permanence* section as the carrier (it has the actual withdraw-and-re-add construction) and reduce the clause-(v) mention to the bare fact that fixity is forced by the full-clearance realisation, without re-narrating the re-seating.

### Issue 3: Standalone multi-case lemmas embedded inside the Class (a) matrix-support prose

**ASN-0047, Class (a) verification, *Derived distinctness corollaries* / *Entity distinctness***: The "Entity distinctness (derived)" annotation — nominally a one-cell justification supporting the S4 / S7d matrix rows — carries a full standalone lemma inline, including the **CrossNodeAccountBase** sub-argument (a two-branch case split over node nesting, with its own constructed divergence position at `#N₁ + 1`). This runs for a substantial paragraph inside prose whose role is to summarise matrix cells.

**Problem**: A load-bearing, multi-case argument is buried where the reader expects a cell summary. The ASN elsewhere hoists such arguments into named lemmas (FrontierEquivalence, SubAllocatorBundle, CrossDocDisjoint) so the verification prose can cite rather than re-derive; entity/link cross-document distinctness is the one place where the full derivation is instead carried inline, making it hard to locate and hard to cite.

**Required**: Hoist CrossNodeAccountBase (and the entity/link cross-document distinctness derivation) to a named lemma within this ASN, alongside CrossDocDisjoint, and have the Class (a) S4/S7d annotations cite it. (This is placement/navigability within the ASN, not an ASN split.)

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link-arrangement contraction
The Open Question on interior `DELETEVSPAN` / compact-and-renumber contraction is correctly left for a future ASN — K.μ⁻ here models suffix removal only, faithful to the gap-free POOM for suffix deletions, and the interior-compaction operation is named operation territory.

### Topic 2: Concurrent allocation and serialization under a shared home document
The Open Questions on concurrent same-document allocation and on link-address exhaustion are genuinely new territory (concurrency/atomicity is excluded by scope), not gaps in this ASN's sequential model.

VERDICT: REVISE
