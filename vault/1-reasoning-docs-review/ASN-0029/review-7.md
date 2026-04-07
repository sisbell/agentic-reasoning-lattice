# Review of ASN-0029

## REVISE

### Issue 1: D7a formal statement is too weak to support the home-document derivation

**ASN-0029, Document Identity / D7a**: "INSERT on document `d` allocates fresh I-addresses under `d`'s tumbler prefix: `(A a ∈ fresh : d ≼ a)`"

**Problem**: The formal property states only `d ≼ a` — that `d` is a prefix of each fresh address. The derivation that `home(a) = d` requires the stronger claim that the element-field separator immediately follows `d`'s prefix: `a = d.0.E₁...Eδ`. Without this, a fresh address could have the form `d.X₁...Xₘ.0.E₁...Eδ` with `m > 0` positive components extending the document field, giving `zeros(a) = 3` and `d ≼ a` but `home(a) = N.0.U.0.D₁...Dγ.X₁...Xₘ ≠ d`.

The prose states the stronger property — "Each fresh address has the form `d.0.E₁...Eδ`" — but the formal statement does not. The derivation of `home(a) = d` (which D7b depends on) uses the element separator at position `#d + 1`, citing "the zero at position `#d + 1` in `a`," but this is not a consequence of `d ≼ a`.

**Required**: Strengthen D7a's formal statement to match the prose:

    (A a ∈ fresh : d ≼ a ∧ a_{#d+1} = 0 ∧ zeros(a) = 3)

or equivalently require each fresh address to have the form `d.0.E₁...Eδ` with all `Eᵢ > 0` and `δ ≥ 1`. This captures both the prefix relationship and the element-separator placement that the home derivation requires.

### Issue 2: D14's ≺ definition admits degenerate tumblers, breaking the forest derivation

**ASN-0029, Version Forest / D14**: "d_s ≺ d_v iff d_s ≼ d_v ∧ d_s ≠ d_v ∧ zeros(d_s) = zeros(d_v) = 2"

**Problem**: The condition `zeros(d_s) = 2` includes tumblers with empty document fields. The tumbler `N.0.U.0` has `zeros = 2` (two zero-valued components, both field separators) and satisfies T4's constraints vacuously (no non-separator components to check). This tumbler is a proper prefix of every root document under account `N.0.U`: for root `d = N.0.U.0.D₁`, we have `N.0.U.0 ≼ d`, `N.0.U.0 ≠ d`, and `zeros(N.0.U.0) = zeros(d) = 2`, so `N.0.U.0 ≺ d`.

Consequence: `parent(d) = max≼ {d' : d' ≺ d} = N.0.U.0` for every root document `d`. This contradicts D0's postcondition `parent(d) undefined` and breaks the forest derivation, which argues: "D0 produces only root documents (postcondition: `parent(d)` undefined), so non-root documents in Σ.D are created only by D12 Case 1." If `parent(d)` is defined for root documents (pointing to `N.0.U.0 ∉ Σ.D`), then the property `(A d : d ∈ Σ.D ∧ parent(d) defined : parent(d) ∈ Σ.D)` fails.

**Required**: Either:
- (a) Restrict `parent` to search within `Σ.D`: `parent(d) = max≼ {d' ∈ Σ.D : d' ≺ d}`, or
- (b) Add a non-degeneracy constraint to `≺`: require the document field to be non-empty (e.g., add `fields(d_s).document ≠ ε` to the ≺ definition), or
- (c) Refine the document-identifier definition to exclude empty document fields, and restrict ≺ to document identifiers.

Option (a) is the most economical — it aligns parent with the operational derivation (which already argues from Σ.D membership via D0 and D12).

### Issue 3: D2 verification for DELETE, COPY, REARRANGE is unsubstantiated

**ASN-0029, Address Allocation / D2**: "The ASN-0026 operations — INSERT, DELETE, COPY, REARRANGE — modify V-space within an existing document but never remove a document from Σ.D: P7 (CrossDocVIndependent) preserves non-target documents, and the target document retains its V-space (modified but not destroyed)."

**Problem**: For non-target documents, P7 gives `Σ'.V(d') = Σ.V(d')`, and the DocumentSet biconditional (`Σ.V(d)` defined iff `d ∈ Σ.D`) yields `d' ∈ Σ'.D` — but the ASN doesn't show this step. For the target document, the claim "retains its V-space (modified but not destroyed)" requires that the operation's postconditions establish `Σ'.V(d)` as a defined function. INSERT has P9 (formal postconditions for length, positions, shifting). DELETE, COPY, and REARRANGE have no formal postconditions in the ASN-0026 foundation — they appear only in the +_ext classification (`fresh = ∅`). The assertion that these operations preserve Σ.D membership for the target is informal.

**Required**: Either:
- Show the full reasoning chain for non-targets (P7 → V-space defined → DocumentSet biconditional → Σ.D membership), or
- Acknowledge that D2 verification for DELETE, COPY, REARRANGE depends on their yet-to-be-formalized postconditions preserving V-space definedness for the target. State this as a proof obligation on those future specifications.

### Issue 4: ASN-0026 invariants not verified for new operations

**ASN-0029, throughout**: The ASN introduces four operations (D0, D10a, D12, D17) and verifies D2 (DocumentPermanence) and D10 (PublicationMonotonicity) against all of them. It does not verify ASN-0026 invariants P0, P1, P2, P3, P7 against these operations.

**Problem**: P2 (ReferentiallyComplete) must hold for the newly created `d_v` in D12: every position in `Σ'.V(d_v)` must map to an address in `dom(Σ'.I)`. The derivation is trivial — `Σ'.V(d_v)(p) = Σ.V(d_s)(p)` by D12(c), `Σ.V(d_s)(p) ∈ dom(Σ.I)` by P2 on Σ, `dom(Σ'.I) = dom(Σ.I)` by D12(e) — but it is not stated. Similarly, P0 and P1 are trivially preserved (I-space unchanged for D0, D10a, D12, D17) but not noted.

**Required**: Add a brief verification that ASN-0026 invariants are preserved. The verifications are trivial for all four operations — a one-paragraph summary suffices.

## OUT_OF_SCOPE

### Topic 1: Formal postconditions for DELETE, COPY, REARRANGE
**Why out of scope**: These operations are classified in ASN-0026's +_ext but lack formal pre/post/frame specifications. Formalizing them is ASN-0026's responsibility (or a dedicated future ASN), not ASN-0029's.

### Topic 2: Accessibility filtering in FINDDOCSCONTAINING
**Why out of scope**: D17 quantifies over all `d ∈ Σ.D` regardless of publication status. Whether the query should respect `Σ.pub` (returning only accessible documents) is a design question the ASN correctly lists as open.

### Topic 3: Privashed state transitions
**Why out of scope**: Within the current model, `privashed` is permanent (no operation exits it). Nelson's design intent — that privashed documents should be freely revertible to private — requires a WITHDRAW or UNPRIVASH operation, properly deferred.

VERDICT: REVISE
