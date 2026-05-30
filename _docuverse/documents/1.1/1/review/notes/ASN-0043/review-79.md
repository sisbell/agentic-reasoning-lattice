# Review of ASN-0043

## REVISE

### Issue 1: Foundation invariants from ASN-0036 are relabeled with invented names, inconsistently

**ASN-0043, Worked Example and L9 verification**: The note glosses ASN-0036's labeled claims with names that do not match the foundation, and uses *different* invented names for the same claim in different places:

- S7b is glossed "ContentElementLevel" (Worked Example) — foundation name is **ElementLevelIAddresses**.
- S7d is glossed "ArrangementDocumentScope" (Worked Example) — foundation name is **DocumentAllocationDiscipline**.
- S8a is glossed "ArrangementSubspaceScope" (Worked Example) *and* "ArrangementVPositions" (L9 state-local block) — foundation name is **VPositionWellFormedness**. Two invented names for one claim, in one document.
- S8-depth is glossed "VPositionDepth" — foundation name is **FixedDepthVPositions**.
- D-CTG/D-MIN/D-SEQ are glossed "Contiguity"/"Minimum"/"Sequentiality" — foundation names are **VContiguity**/**VMinimumPosition**/**SequentialPositions**.

**Problem**: A precise reader cross-referencing the foundation cannot confirm which claim is being invoked, and the S8a case shows the names are not even internally stable. This is exactly the "don't reinvent notation a foundation already defines" failure (Standard 7).
**Required**: Use the foundation's claim names verbatim wherever an ASN-0036 invariant is cited, or carry the label alone with no renamed gloss.

### Issue 2: Duplicate Nelson [LM 4/79] quote and N-endset argument

**ASN-0043, "The Endset Structure" and L3**: The same quote and gloss appear twice:
- "He explicitly lists support for higher-arity links… '4-sets, 5-sets … n-sets supported in link storage and search' [LM 4/79]."
- L3: "Nelson [LM 4/79] explicitly calls for N-endset support beyond three: '4-sets, 5-sets … n-sets supported in link storage and search.'"

**Problem**: Two paragraphs in different sections make the identical point with the identical citation — the "same thing in different words" pattern the anti-bloat pass is meant to surface. The "standard triple is a floor not a ceiling" theme is restated a third time in the Summary.
**Required**: State the N-endset point once (at L3, where it is normative) and remove the duplicate from the motivating prose.

### Issue 3: Defensive meta-prose explaining what the L1c existential omits

**ASN-0043, L1c Chain**: "Per-(t, k') uniqueness across distinct allocator events anywhere in the system is the GlobalUniqueness consequence… — it is a cross-chain global property of the allocator landscape, not a within-chain local constraint, so it does not appear inside the existential here."

**Problem**: This paragraph justifies an *absence* from the formula rather than advancing the claim — a "why the construction is shaped this way" digression the reader must skip to follow the chain. It explains why something is not present, which is noise unless the omission was a live hazard, and it is not (GlobalUniqueness is invoked in its own right at L11a).
**Required**: Delete the paragraph; the chain stands on its locally-T10a-admissible step conditions alone.

### Issue 4: Use-site inventory in the CPP table entry

**ASN-0043, Properties Introduced table, CPP row**: "...the terminus agrees with `t₀` on positions `1..p`; **cited by L1c, Home/Ownership, L9, and L11b**."

**Problem**: Enumerating a lemma's downstream consumers is the "definition introduction enumerates downstream consumers" pattern — it adds no meaning to CPP and rots as consumers change.
**Required**: Drop the "cited by …" clause; the lemma statement is self-contained.

### Issue 5: Boundary-policing prose distinguishing L11a from L12

**ASN-0043, L11a, "Consequence — identification within a state"**: "...the substantive content of L11a is that this within-state identification extends across allocation events. Persistence of the address-to-link binding across transitions is L12, not L11a."

**Problem**: The second sentence exists only to fence L11a off from L12 — adjudicating scope between two claims rather than establishing either. This is reviser-drift meta-prose; the reader already has L12 stated separately.
**Required**: Cut the "...is L12, not L11a" sentence. State the within-state identification and stop.

### Issue 6: `h(a)` and `home(a)` are the same object under two notations, never reconciled

**ASN-0043, L1c and "Home and Ownership"**: L1c uses `h(a) = N(a).0.U(a).0.D(a)` (postcondition `s = h(a)`); the next section defines `home(a) = N(a).0.U(a).0.D(a)` — the identical formula. The CPP applications and L11b also use `h(·)`.

**Problem**: Two symbols for one quantity, with no statement that `h(a) = home(a)`. A reader meeting `s = h(a)` in L1c and `home(a)` later cannot be sure they coincide without re-deriving the formula.
**Required**: Either use `home(a)` throughout (forward-declaring the formula at first use) or add one line stating `h(a) ≡ home(a)`.

## OUT_OF_SCOPE

(none — the open-questions list already routes future topics correctly.)

VERDICT: REVISE
