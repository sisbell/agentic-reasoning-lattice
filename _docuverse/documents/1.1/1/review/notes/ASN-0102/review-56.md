# Review of ASN-0102

## REVISE

### Issue 1: P4★ / J1'★ discharge assumes containment-in-R at a state that may not be a composite boundary

**ASN-0102, X14 (P4★ paragraph)**: "Each pre-state pair lies in `R_Σ ⊆ Σ'.R` by (i)/(ii) at B; each new pair `(a_j + i, d)` lies in `Σ'.R` by COPY's effect. Hence `Contains_C(Σ') ⊆ Σ'.R` at `Σ_clo`."

**ASN-0102, self-transclusion example (J1'★ discharge)**: "`(x_3, d) ∈ Contains_C(Σ)` ... so by P4★ it is already in `Σ.R`."

**Problem**: Both steps assume `Contains_C(Σ) ⊆ Σ.R` — i.e. P4★ evaluated at COPY's *local* pre-state `Σ`. But P4★ is a *composite-boundary* property (ASN-0047 lists it under composite-boundary properties, not per-state invariants), and COPY is an elementary transition applicable at intermediate states. The premise actually established is only `R_B ⊆ Σ.R` (boundary `B`'s recorded pairs persist), which does **not** give `Contains_C(Σ) ⊆ Σ.R` when `Σ` is mid-composite. The worked example never declares its `Σ` a boundary, so "by P4★ it is already in `Σ.R`" is unsupported as written; and the general P4★ paragraph inherits the same gap when it routes pre-state containment pairs through `R_Σ`.

**Required**: Recast the discharge as step-local preservation of the inclusion `Contains_C ⊆ R`: assume `Contains_C(Σ) ⊆ Σ.R` as the inductive hypothesis entering COPY, then show COPY preserves it because every containment it adds (`{(a_j+i, d)}`) is matched by a provenance write into `Σ'.R` and no containment is removed. This closes `Contains_C(Σ') ⊆ Σ'.R` from the hypothesis without claiming P4★ holds at an arbitrary `Σ`. Correspondingly, state in the self-transclusion example that `Σ` is a composite boundary (or route the `Old`-branch through the inductive form).

### Issue 2: Duplicated statement that COPY is added to the transition vocabulary

**ASN-0102, Definition of COPY**: "COPY is added to the system's transition vocabulary `𝒦` (ASN-0047) as an elementary transition in its own right, with the complete frame stated below." — immediately followed by — "**Amendment to `ValidComposite★`.** COPY is added to `ValidComposite★`'s atomic vocabulary (ASN-0047) as a new elementary transition kind, changing two state components — the arrangement `M` and the provenance relation `R`."

**Problem**: Two adjacent sentences assert the same fact (COPY is a new elementary transition in the vocabulary) in different words — the "two paragraphs say the same thing" pattern flagged for this note. The only non-duplicated content in the second is "changing `M` and `R`," which the effect clauses already make explicit.

**Required**: Collapse to a single statement of the vocabulary/`ValidComposite★` amendment; drop the redundant first sentence.

## OUT_OF_SCOPE

### Topic 1: Re-displacement of copied content and continued discoverability (Open Question 1)
**Why out of scope**: This concerns the interaction of a *subsequent* operation with origin/discoverability, which is INSERT/DELETE/REARRANGE mechanics and link-projection territory — future ASNs, not a defect here.

### Topic 2: Reachability of the allocating document and identity persistence (Open Question 4)
**Why out of scope**: Garbage-collection / reachability semantics are not part of COPY's state-transition contract.

VERDICT: REVISE
