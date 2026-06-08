# Review of ASN-0102

## REVISE

### Issue 1: S7d discharged under the wrong justification

**ASN-0102, X14 invariant inventory**: "S7a–S7d, C-fin. Content store unchanged by X1."

**Problem**: S7d is DocumentAllocationDiscipline — a constraint on document tumblers and allocation events (entity set), not on the content store. It is preserved by COPY because `Σ'.E = Σ.E` (no document allocated), *not* because `dom(Σ'.C) = dom(Σ.C)`. Grouping it with "content store unchanged by X1" attaches the wrong premise to a real obligation. (S7a, S7b, S7 are content-address claims, so the premise is correct for them.) Separately, "S7a–S7d" written as a range implies an S7c that does not exist in the foundation; the foundation defines S7a, S7b, S7d, S7.

**Required**: Discharge S7d (and the document-level conjuncts) from `Σ'.E = Σ.E`, and name the actual conjuncts rather than a range spanning a nonexistent label.

### Issue 2: J1'★ argument imagines a later step COPY does not perform

**ASN-0102, X14, J1'★ discharge**: "(Should a *later* step contract `a` out of range while retaining the record, that J1'★ violation is charged to that step's coupling, not COPY's.)"

**Problem**: COPY's carrier is a single elementary transition that only extends the arrangement and provenance; it performs no contraction. This parenthetical reasons about a hypothetical later step's coupling violation and pre-assigns blame — content that does not advance COPY's own discharge of J1'★. It is the defensive-aside pattern the precise reader must skip past to follow the actual argument.

**Required**: Remove the aside. COPY discharges its own J1'★ obligation via the B-boundary split already given; ownership of other steps' couplings is not COPY's to argue.

### Issue 3: P4★ boundary-only nature re-justified by another operation's behavior

**ASN-0102, X14, P4★ induction**: "P4★ is asserted only at composite boundaries, not as a per-state invariant — a K.μ⁺ step grows `Contains_C` without growing `R` (frame `R' = R`), refuting any per-elementary-step `Contains_C ⊆ R`."

**Problem**: That P4★ is a composite-boundary property (not per-state) is fixed by the foundation (ASN-0047). Re-deriving that fact here by appealing to K.μ⁺'s frame is rationale about the framework's design rather than COPY's content — prose explaining *why the property is shaped as it is* rather than discharging it for COPY. It explains a sibling operation to motivate a proof structure.

**Required**: State the induction over boundaries directly (base `Σ₀`, step from P4★ at `B` plus composite-wide J1★); drop the K.μ⁺ motivation, which belongs to the foundation, not this note.

## OUT_OF_SCOPE

### Topic 1: Persistence of origin/discoverability when copied content is later re-displaced

**Why out of scope**: The first Open Question concerns invariants under *subsequent* operations acting on already-copied addresses. That is INSERT/DELETE/REARRANGE interaction territory and belongs to a later ASN, not COPY's contract. The note correctly leaves it as an open question rather than a claim.

### Topic 2: Transitive containment when a reference-holding document is itself a source

**Why out of scope**: The second Open Question (chained containment records across reference hops) is a cross-operation provenance property, not part of single-COPY semantics. Appropriately deferred.

VERDICT: REVISE
