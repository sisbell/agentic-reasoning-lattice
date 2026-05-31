# Review of ASN-0043

## REVISE

### Issue 1: L1d's siting paragraph is a use-site inventory plus document-ordering justification
**ASN-0043, L1d — SubspaceDisjointness**: "This lemma is sited here because its discharge requires L0, L0a, L0b, and L1; it is consumed downstream by L0's preservation argument (FSP), L9, L14, L14a, and the worked example — none of which is L1b — so it is stated as a free-standing result rather than threaded through the element-field-depth claim."
**Problem**: This sentence advances no reasoning about subspace disjointness. It is a use-site inventory ("consumed downstream by … L9, L14, L14a, and the worked example"), a document-ordering rationale ("sited here because …", "stated as a free-standing result rather than threaded through …"), and carries the residue of a prior L1b finding ("none of which is L1b"). The reader must skip it to reach the actual lemma content. This is precisely the forward-reference/reviser-drift accretion the anti-bloat classifier targets.
**Required**: Delete the siting sentence. State L1d's two parts directly; dependencies are evident from the proof, and downstream consumers cite L1d where they use it.

### Issue 2: L0b enumerates its own downstream consumers
**ASN-0043, L0b — LinkAddressValidity**: "Every subsequent claim that needs these projections on `dom(Σ.L)` — L0, L1a, and the link-address instances of Definition — home — invokes this fact by citing L0b rather than re-deriving the T4b domain argument."
**Problem**: A use-site inventory in a definition/theorem slot. It does not advance the meaning of L0b (that every link address is T4-valid); it merely catalogs who cites it later. Whether L0, L1a, and `home` cite L0b is visible at those sites.
**Required**: Remove the sentence. The preceding clause already establishes that T4-validity makes the projections well-defined on `dom(Σ.L)`; that is the load-bearing content.

### Issue 3: The same Gregory evidence is restated verbatim in two sections
**ASN-0043, Convention — StandardTriple**: "Gregory's implementation hardcodes three V-addresses (1.1, 2.1, 3.1) and three spanfilade index constants (`LINKFROMSPAN = 1`, `LINKTOSPAN = 2`, `LINKTHREESPAN = 3`)."
**ASN-0043, L6 — SlotDistinction**: "in the link's own permutation matrix (V-addresses 1.1, 2.1, 3.1 for from, to, and type) and in the spanfilade index (ORGL-range prefixes `LINKFROMSPAN = 1`, `LINKTOSPAN = 2`, `LINKTHREESPAN = 3`)."
**Problem**: Two paragraphs in the same document present identical implementation evidence (the 1.1/2.1/3.1 V-addresses and the three spanfilade constants) in slightly different words. The duplication is the flagged "two paragraphs say the same thing" pattern.
**Required**: Cite the evidence once — it most directly supports L6 (the structural slot-distinction claim). In Convention — StandardTriple, retain only the fact that the implementation fixes arity 3, dropping the repeated address/constant list.

## OUT_OF_SCOPE

### Topic 1: Global content-subspace invariant
The first Open Question (extending content-side disjointness from the `s_C`-resident slice to all of `dom(Σ.C)`) would require a content-side invariant fixing a global content subspace.
**Why out of scope**: That invariant belongs to a content-model ASN (the ASN-0036 family), not the link model; scoping disjointness to the `s_C`-slice is the correct local decision here.

VERDICT: REVISE
