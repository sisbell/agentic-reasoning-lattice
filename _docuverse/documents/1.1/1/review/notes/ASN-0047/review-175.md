# Review of ASN-0047

## REVISE

### Issue 1: K.σ subsumption enumerates only two routes into E_doc, omitting the k = 0 sibling-document route

**ASN-0047, *Elementary transitions*, "Subsumption of ASN-0093's K.σ"**: "The K.δ case (ii) k = 2 event with parent(e) ∈ E_account ... and the K.δ case (ii) k = 1 event with t ∈ E_doc (creating a version) are both routes by which an entity enters E_doc; either is the single atomic event that, under ASN-0093's vocabulary, would be reported as K.σ."

**Problem**: There are **three** routes into E_doc, not two. The ASN's own S7d verification (*Extended reachable-state invariants*) states it explicitly: "Documents enter E_doc by three K.δ routes ... k = 2 ... k = 1 ... k = 0 (sibling off a document, zeros = 2 preserved)." The entity-hierarchy worked example Step 4 demonstrates exactly this third route — `1.2.0.1.0.2 = inc(1.2.0.1.0.1, 0)`, a sibling **document** (zeros = 2, IsDocument), entering E_doc with `M₄(1.2.0.1.0.2) = ∅` (the IsDocument-case effect, i.e. a document registration). J4 further confirms the k = 0 sibling-document is a distinct allocation (`docreatenewdocument`, "not a fork"). The subsumption paragraph's "both routes" is therefore incomplete: the k = 0 sibling-document is a K.σ-equivalent document registration that is omitted.

**Required**: Add the k = 0 sibling-document case to the enumeration (or restate it as "every K.δ event with IsDocument(e) — k = 2 descent, k = 1 version, or k = 0 sibling — is the K.σ-equivalent registration"), matching S7d's three-route account.

### Issue 2: K.δ "Effect on M" and frame contradict the total-M typing override — M is unchanged for IsDocument(e)

**ASN-0047, *Elementary transitions*, K.δ**: "*Effect on M, per case.* When IsDocument(e): M'(e) = ∅ ... *Frame:* ... M is per-case (above). The IsDocument case's M'(e) = ∅ matches M(e) in value by the totality convention but enters e into E_doc, changing M's typing."

**Problem**: Under this ASN's own total-M override (`M(d) = ∅` for every `d ∉ E_doc`, document-set role carried by E_doc), `e` is fresh (`e ∉ E` precondition) so `M(e) = ∅` *before* the transition and `M'(e) = ∅` after. M is therefore literally unchanged as a function in **all three** cases — the entire document-registration effect is carried by `E' = E ∪ {e}`. Two specific defects follow: (a) "changing M's typing" has no referent — M's signature `T → (T ⇀ T)` is fixed; nothing about M's type changes. (b) Presenting an "Effect on M, per case" and listing M in the frame as "per-case" misrepresents K.δ as modifying M, when the typing note's whole point is that existence is tracked by E, not M.

**Required**: State that K.δ leaves M unchanged (`M' = M`) and that registration is effected solely through E; drop "changing M's typing." This also keeps the frame uniform across the IsNode/IsAccount/IsDocument cases.

### Issue 3: SubAllocatorAxiom is declared "inherited without modification" yet its Disjointness clause is re-derived in full

**ASN-0047, *Allocator hierarchy under documents*, SubAllocatorAxiom**: "The axiom is taken from ASN-0093 directly. ... The five sub-clauses are inherited from ASN-0093 without modification" — followed by **SubAllocatorAxiom.Disjointness**, which carries a full re-derivation ("*Within-document discharge:* ... T7 ... ; *Cross-document discharge:* ... the Cross-document disjointness chain lemma ...").

**Problem**: An axiom that is "inherited without modification" should be cited, not re-proved. The Disjointness clause re-establishes a property ASN-0093 already asserts, via T7/SC-NEQ/CrossDocDisjoint. This is the accretion pattern the note flags: prose around an inherited axiom that re-argues the result rather than stating it. It also duplicates machinery already given by CrossDocDisjoint and L14 elsewhere in the section.

**Required**: Either cite ASN-0093's Disjointness clause and delete the within/cross-document re-derivation, or, if the discharge is genuinely ASN-0047's obligation (because the anchors are ASN-0047 constructs), drop the "inherited without modification" framing for that clause and label it a local lemma.

### Issue 4: P4a is proved twice — the four-component derivation is subsumed by the extended-state derivation

**ASN-0047, *Coupling and isolation*, P4a**: two consecutive blocks, "*Derivation (four-component state)*" (using J1', P2, P0) and "*Derivation (extended state, with J1'★)*" (using J1'★), establish the same property P4a.

**Problem**: By the final theorem only the extended state is in force (ExtendedReachableStateInvariants discharges P4a via J1'★), and the link-free fragment is a special case of the extended state (every V-position is content-subspace, so J1'★ reduces to J1'). The four-component derivation is vestigial — it restates the same inductive argument for a strictly weaker state model that the second derivation already covers. This is the "two paragraphs say the same thing in different words" accretion pattern.

**Required**: Drop the four-component derivation and keep only the extended-state one, noting in one clause that the link-free fragment is the special case where J1'★ ≡ J1'.

## OUT_OF_SCOPE

None.

VERDICT: REVISE
