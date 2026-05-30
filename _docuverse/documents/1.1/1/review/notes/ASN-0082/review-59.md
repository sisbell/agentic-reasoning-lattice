# Review of ASN-0082

## REVISE

### Issue 1: Reviser-drift remark referencing a deleted clause

**ASN-0082, Post-Contraction Worked Example (main case)**: "The addresses are reused by the shift — D-DOM characterizes this correctly, where the former D-X ('positions in X are absent from dom(M'(d))') would have been contradicted."

**Problem**: This sentence explains why a *prior version* of the contract (a clause "D-X" that no longer exists in the ASN) would have been wrong. It is commentary on the note's own revision history, not on the system being specified. A reader who never saw D-X must work around this to follow the example. This is exactly the accreted meta-prose the anti-bloat classifier targets — a prior finding's content relocated into the body rather than removed.

**Required**: Delete the clause from "where the former D-X..." onward. The preceding sentence ("any X address that reappears in Q₃ carries the shifted I-address...") already states the object-level fact; the revision rationale belongs in the commit message.

### Issue 2: Dangling reference to a non-existent "Depth axiom discussion"

**ASN-0082, wp analysis (contraction), conjunct 3**: "...because TA4's zero-prefix precondition is incompatible with S8a's componentwise positivity at those positions — see the *Depth axiom* discussion above."

**Problem**: The *Depth axiom* paragraph states only "#p = 2. V-positions in the text subspace have depth 2 (ordinal depth 1) — single-component ordinals." It contains no discussion of the TA4/S8a incompatibility. The pointer "see ... above" directs the reader to content that lives only here, in the wp paragraph itself. The reference is either broken or circular.

**Required**: Either remove the "see ... above" pointer (the wp conjunct is itself the argument and is self-contained), or move the TA4-incompatibility rationale to the Depth axiom paragraph so the pointer resolves. Do not leave a pointer that resolves to nothing.

### Issue 3: Registry entries enumerate downstream consumers

**ASN-0082, Statement Registry**: NAT-CA — "...discharges the scalar reordering in I3-S(a) and D-S(a)"; ordinal-level — "...level-uniformity #s = #ℓ is a separate condition stated where invoked (e.g., I3-S and D-S)."

**Problem**: Both registry entries append a use-site inventory to a definition. The main-text introductions of NAT-CA and ordinal-level are clean; the registry duplicates them and adds "used by I3-S/D-S." This is the "definition introduction enumerates downstream consumers" pattern — the inventory rots as use sites change and adds nothing to the definition's meaning.

**Required**: Trim the use-site clauses from both registry rows. State what NAT-CA and ordinal-level *are*; let the lemmas that cite them record the dependency.

## OUT_OF_SCOPE

### Topic 1: Contraction at ordinal depth > 1
**Why out of scope**: The contraction is scoped to #p = 2 (single-component ordinals) because the gap-closure round-trip rests on TA4 at depth 1 (vacuous zero-prefix). Generalizing to deeper ordinals (which would need D0/D1-style round-trips instead) is already captured by Open Question 2; it is a future ASN, not a defect here.

### Topic 2: Contraction on the link subspace and link cleanup under DELETE
**Why out of scope**: The contraction is deliberately restricted to S = 1. How DELETE interacts with links pointing into removed content is link semantics, not arrangement displacement, and belongs in a link-model ASN.

VERDICT: REVISE
