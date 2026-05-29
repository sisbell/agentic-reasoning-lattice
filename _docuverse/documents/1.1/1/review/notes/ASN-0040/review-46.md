# Review of ASN-0040

## REVISE

### Issue 1: B0a restates the same partition three times
**ASN-0040, §The baptismal registry (B0a)**: After the two-clause partition definition, the note adds "Each `op ∈ Σ` is in exactly one class by its symbol…", then "Equivalently, `(A s, s' : s → s' : s'.B = s.B ∨ (E (p, d) : … : s'.B = s.B ∪ {next(s.B, p, d)}))`", then "The closure is structural: there is no operation symbol in Σ outside the baptismal class that touches s.B."
**Problem**: Three formulations of one partition. The "Equivalently" line and the "closure is structural" sentence carry no content beyond the operative two-clause definition — the precise reader must confirm they say the same thing.
**Required**: Keep the operative partition; delete the equivalent restatement and the "closure is structural" sentence.

### Issue 2: B4 carries formalization-choice and implementation-status meta-prose
**ASN-0040, §Atomicity (B4)**: "We state this as a constraint at the level of the transition system rather than over an undefined event vocabulary of 'read' and 'commit'." and "Gregory's implementation achieves the atomic-transition semantics through single-threaded dispatch. B4 is a specification-level requirement, not an implementation prescription: any mechanism that exhibits one Σ-transition per baptism satisfies it."
**Problem**: Both explain *why the axiom is framed this way* and *its status*, not what it says — the "Why the axiom is needed" pattern flagged for this note.
**Required**: State B4 and its per-namespace scope; drop the formalization-choice justification and the implementation-prescription disclaimer.

### Issue 3: The wp section re-derives Bop and the invariant proofs
**ASN-0040, §The high water mark (wp derivations)**: The three derivations `wp(baptize, B1)`, `wp(baptize, a ∉ B)`, `wp(baptize, B10)` reconstruct the freshness, B1-preservation, and B10-preservation arguments already given in full in Bop's *Proof of well-definedness and correctness* and in §B1 / §B10.
**Problem**: Same arguments, different words — "two paragraphs say the same thing." A reader who has read Bop's proof gains nothing here.
**Required**: Either cut the wp section, or have each line cite the already-proven result (Bop freshness, §B1, §B10) rather than re-running the case analysis.

### Issue 4: B3's prose restates the classification table
**ASN-0040, §Ghost elements (B3)**: After the four-way partition table, "The forbidden row is not a current invariant of the present ASN…" and the paragraph "B3 separates two questions that might otherwise be conflated. 'Does address t exist?'… 'Is there content at t?'… B3 binds them by a one-way implication and defers everything else."
**Problem**: The table plus the one-line forward requirement already state the content; the two trailing paragraphs re-explain it in essay form.
**Required**: Keep the table and the `Occupied(t, s) ⟹ t ∈ s.B` requirement; remove the separation essay.

### Issue 5: Redundant foundation citation in B7
**ASN-0040, §Namespace disjointness (B7 proof)**: "ASN-0034's T10a.1 (UniformSiblingLength) gives that every sibling of such a stream shares the base length, so `#cₙ = #p + d` for all `n ≥ 1`, without re-running the length induction."
**Problem**: S(p, d)'s own postconditions already establish `#cₙ = #p + d`. Invoking a foundation lemma to re-derive a property the ASN proved locally is unnecessary indirection.
**Required**: Cite S(p, d)'s postcondition directly.

### Issue 6: Gregory-evidence inventory in the depth/field section
**ASN-0040, §Depth and field structure**: "Gregory's evidence confirms the structural necessity in three independent ways. First… Second… Third… An address produced without the correct zero separators corrupts containment testing and all subsequent baptisms…"
**Problem**: An enumerated use-site inventory of implementation confirmations that does not advance B5/B5a — essay content occupying a structural slot.
**Required**: Trim to the single formal point (the `.0.` separator is produced by `inc(p, 2)`'s TA5(d) separator) or remove.

## OUT_OF_SCOPE

### Topic 1: `allocated(s) ⊆ s.B` alignment with the allocator
**Why out of scope**: The "Relationship to ASN-0034's allocated set" deferral correctly assigns this discharge to the activation-discipline ASN; this is a genuine future obligation, not an error here. (Note only: the in-text back-reference "see *Relationship to ASN-0034's allocated set* above" is the one acceptable internal pointer — do not let it multiply.)

### Topic 2: Parent-baptized prerequisite
**Why out of scope**: Whether a parent must be baptized before its children is correctly deferred to Tumbler Ownership (Open Questions); Bop's "no parent-baptized prerequisite is imposed" is a deliberate scoping choice.

The proofs themselves are sound: B1's three-way namespace case split (B6-valid via B7, fully-T4-invalid via B10, trailing-zero via S2) is exhaustive and matched against B6's necessity result; B7's three length/prefix cases cover the space; B8 correctly uses B0★ for the cross-state hwm comparison. The findings above are accretion, not correctness gaps.

VERDICT: REVISE
