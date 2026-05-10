# Review of ASN-0008

## REVISE

### Issue 1: LD0 biconditional contradicts LD5
**ASN-0008, "Discovery medium: I-address identity"**: `L in findlinks(e=Q) <=> iaddrs(L.e) intersection Q != empty`
**Problem**: LD0 states a biconditional: I-address intersection is *necessary and sufficient* for membership in `findlinks`. But LD5 later defines `findlinks(C, u) = {L in links : satisfies(L, C) /\ visible(L, u)}`, adding a visibility conjunct. The forward direction of LD0 (intersection implies membership) is false — a link in a private document with non-empty intersection is NOT in `findlinks` for an unauthorized user. LD0 and LD5 cannot both be correct as stated.
**Required**: LD0 should define `satisfies(L, C)`, not `L in findlinks(e=Q)`. The biconditional holds for the satisfaction predicate, not for the full discovery result. Restate LD0 as: `satisfies(L, e=Q) <=> iaddrs(L.e) intersection Q != empty`. Then LD5 composes satisfies with visible, and the layered structure is consistent.

### Issue 2: LD2 zero-constraint case contradicts conjunction semantics
**ASN-0008, "Conjunction semantics"**: "specifying no constraints at all returns an empty result, not all links"
**Problem**: LD2 says constraints compose by conjunction. The conjunction of zero predicates is vacuously true — every link satisfies an empty set of constraints. Standard conjunction semantics therefore yields ALL visible links for a zero-constraint query. But the ASN claims the opposite: empty result. This is a special-case override that contradicts the stated semantics, not a consequence of them.
**Required**: Either formalize the "at least one constraint required" rule as a separate property distinct from LD2 (e.g., a precondition on `findlinks`), or reconcile the zero-constraint behavior with the conjunction semantics by explaining why the empty conjunction is not vacuously true in this system.

### Issue 3: LD10 formalization does not match the property
**ASN-0008, "Transclusion transparency"**: The formal statement of LD10 uses the precondition `iaddrs(poom(d_1)) intersection iaddrs(poom(d_2)) supseteq iaddrs(L.e) intersection iaddrs(poom(d_1))`.
**Problem**: This precondition is strictly stronger than what transclusion guarantees. If d_2 transcludes only a *subrange* of d_1's content, d_2's POOM contains a *subset* of d_1's I-addresses — not necessarily a superset of the L.e-intersecting ones. The precondition demands that ALL of L.e's overlap with d_1 also appears in d_2, but partial transclusion doesn't ensure this. The prose syllogism (steps 1–5) assumes both documents map to the *entire* set `{a_1,...,a_n}`, which is the full-transclusion case, not the general case. The actual property is simpler and more general: `iaddrs(L.e) intersection iaddrs(poom(d_2)) != empty => L satisfies a query from d_2`. No reference to d_1 needed.
**Required**: Restate LD10 to capture the real property: any document whose POOM shares at least one I-address with L.e can discover L. This follows directly from LD0. The transclusion mechanism is just one way such sharing arises; the formalization should not encode transclusion's specific guarantees as the precondition.

### Issue 4: LD12 formalization is vacuous
**ASN-0008, "Discovery permanence"**: `L in findlinks(C, u) at time t /\ satisfies(L, C) at time t' /\ visible(L, u) at time t' => L in findlinks(C, u) at time t'`
**Problem**: Drop the first conjunct. The remaining statement — `satisfies(L, C) at t' /\ visible(L, u) at t' => L in findlinks(C, u) at t'` — is exactly LD5 applied at time t'. The time-t condition contributes nothing. The formula is a tautology beyond LD5. The *intended* property — links cannot be destroyed, span index entries cannot be lost, therefore discoverability persists — is structural and is argued well in the prose. But the formula does not capture it.
**Required**: Formalize the structural content: (a) `L in links at t => L in links at t'` for all t' > t (link permanence); (b) `entry in spanindex at t => entry in spanindex at t'` (index permanence). Then derive: if `satisfies(L, C)` holds at t and no operation can remove L from links or its entries from spanindex, then `satisfies(L, C)` still holds at t'. Combined with access persistence (if access doesn't change, visibility persists), you get the permanence property with actual content.

### Issue 5: LD18 introduces undefined Q'
**ASN-0008, "V-space independence"**: `L in findlinks(e=Q) before op /\ ... => L in findlinks(e=Q') after op` where Q' is "the I-addresses derived from the querier's V-span after the operation."
**Problem**: Q' is introduced but never defined. The relationship between Q and Q' depends on whether the querier is reading the *same document* being modified or a *different document*. If the querier is in a different document, their V-span is unchanged and Q' = Q. If the querier is in document d being operated on, then INSERT/DELETE/REARRANGE all shift V-positions, and Q' is the set of I-addresses at the querier's (now shifted) V-span. The case analysis (INSERT/DELETE/REARRANGE/COPY) analyzes I-address sets in the POOM but never connects this to Q'. What exactly are the querier's V-positions after the operation, and what I-addresses do they map to?
**Required**: Define Q' explicitly. The simplest correct statement separates two cases: (a) queries from documents other than d are unaffected (Q' = Q, since their POOM is unchanged); (b) queries from d itself require converting the shifted V-positions through d's updated POOM, which may yield a different I-address set. Case (b) needs analysis for each operation.

### Issue 6: LD19 takes no normative position
**ASN-0008, "The reverse-orphan anomaly"**: "Whether this is a desirable property or a consistency gap depends on what 'deleted' means."
**Problem**: A specification must decide. The ASN identifies the reverse orphan — a link removed from V-space but still discoverable through the span index — and then explicitly declines to specify whether this is correct behavior. The sentence beginning "Whether this is a desirable property..." is a question, not a specification. This leaves implementors without guidance: should link deletion update the span index or not?
**Required**: Take a position. The ASN's own analysis leans toward "deletion is a V-space operation" (paralleling content deletion), and Nelson's language about deleted links "awaiting historical backtrack functions" supports treating the span index as permanent. If this is the specified behavior, state it: "Link deletion is a V-space operation. Span index entries are permanent. A deleted link remains discoverable." If the ASN cannot resolve this without further analysis, explicitly state the dependency and which open question must be answered first.

### Issue 7: No concrete worked example
**ASN-0008, throughout**
**Problem**: The ASN describes scenarios in prose (INSERT fragmenting a link's V-appearance, transclusion across documents) but never works through a specific instance with concrete addresses. No POOM states are shown. No span index contents are shown. No findlinks query is traced from V-position to I-address to span index lookup to result set. The prose scenarios describe mechanisms; a worked example would verify them.
**Required**: At minimum, one concrete scenario exercising the core properties. For example: Document d has POOM {v1→i3, v2→i4, v3→i5}. Link L has L.to = span(i4, 2) = {i4, i5}. Show findlinks(to={i4, i5}) returning L. Then DELETE v2 from d, yielding POOM {v1→i3, v2→i5}. Show that findlinks from d's remaining content still discovers L (via i5). Then show document d2 with POOM {v1→i4} (transclusion) — findlinks from d2 discovers L via i4. Trace through LD0, LD1, LD10.

### Issue 8: Membership in "links" is undefined at the boundary
**ASN-0008, "The state we need"**: "links: the set of all link objects in the system"
**Problem**: Several properties depend on precise membership in `links`. LD14 (completeness) says every link in `links` that satisfies the query is returned. LD12 (permanence) says links cannot leave the set. But the ASN never defines when a link *joins* `links`. Is it at I-space allocation? At span index registration? After all three endset entries are indexed? This interacts with the atomicity open question. If a link is in `links` before its span index entries exist, LD14 requires it to be found, which is impossible. If a link joins `links` only after full indexing, LD14 is satisfiable but the definition is implementation-coupled.
**Required**: Define the point at which a link becomes a member of `links`. The cleanest option: a link joins `links` when it has a permanent I-space address and all endset entries are recorded in the span index. This makes LD14 achievable and pushes atomicity to the creation operation's postcondition.

### Issue 9: Edge cases not addressed
**ASN-0008, LD0, LD1, LD2**
**Problem**: Several boundary conditions are unexamined:
- **Empty query set**: If Q = ∅, then `iaddrs(L.e) intersection Q = empty` for all L, so findlinks returns nothing. This is sensible but unstated.
- **Link with empty endset**: If `iaddrs(L.from) = empty`, no query can ever discover L via the from-role. Can a link have an empty endset? If yes, what does LD8 (symmetry) mean — is the link discoverable only from its non-empty endsets? If no, this should be a precondition on link creation.
- **Orphaned I-addresses**: If all documents delete content at I-addresses referenced by L.e, those addresses exist in no POOM. The span index still has entries. A user who somehow queries those exact I-addresses finds L. But no document provides a V-space path to those addresses. Is L "discoverable" or effectively hidden? LD18's DELETE case acknowledges this ("discovery from the system as a whole is not [lost] as long as any POOM anywhere still references the relevant I-addresses") — the parenthetical qualifier is doing heavy lifting. State explicitly what happens when no POOM references the addresses.
**Required**: Address each boundary. State whether empty endsets are permitted. State the findlinks result for empty Q. State the discovery status of links whose endset I-addresses appear in no POOM.

## OUT_OF_SCOPE

### Topic 1: Document unpublishing (published → private transition)
**Why defer**: The ASN addresses private → published as an open question and assumes access states as given. The reverse transition — what happens to incoming link visibility when a document is unpublished — is a question about state transitions in the access model, which belongs in a future ASN on access control or publication contracts.

### Topic 2: Link creation atomicity
**Why defer**: The ASN correctly identifies this as an open question. The atomicity of span index registration is an operation specification concern, not a discovery semantics concern. A future ASN defining the MAKELINK operation should specify the postcondition (all three endset entries indexed) and the atomicity guarantee.

### Topic 3: Span index garbage collection under economic failure
**Why defer**: The ASN notes economic failure as a boundary of the permanence guarantee. The conditions under which span index entries may be collected require the economic model (ASN-0015's territory) and storage lifecycle semantics, neither of which is within this ASN's scope.