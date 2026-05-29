# Review of ASN-0036

## REVISE

### Issue 1: S8a introduction enumerates its downstream consumers
**ASN-0036, S8a**: "S8a names the per-component quantifier form, which is the shape the contiguity and partition arguments below (S8, D-CTG, D-SEQ) reason over directly"
**Problem**: This is a use-site inventory — it names the downstream claims that consume S8a rather than advancing what S8a *says*. The classifier flags exactly this: "a definition's introduction enumerates downstream consumers." S8a's content is fully given by its formal quantifier; the consumer list is accretion.
**Required**: Delete the consumer-inventory clause. The formal statement plus the one-line equivalence to `zeros(v)=0` over ℕ is sufficient.

### Issue 2: S8a is a notational restatement carried by justificatory prose
**ASN-0036, S8a**: "Over the ℕ-carrier (T0), the domain-restriction axiom's conjunct zeros(v) = 0 is definitionally the statement that every component is strictly positive … so the depth constraint #v ≥ 2 … occupy distinct components. The domain and range of M(d) live in structurally different tumbler subsets …"
**Problem**: S8a adds no logical content beyond the domain-restriction axiom (`zeros(v)=0` over T0's carrier already *is* componentwise positivity). The surrounding paragraph — the field-separator aside (`N.0.U.0.D.0.2.1`), the subspace-identifier gloss (already defined formally three lines later in `subspace`), and the dom/ran "structurally different subsets" sentence — is explanatory essay content occupying a property slot, partly duplicating the `subspace(v)` definition that immediately follows.
**Required**: Collapse S8a to its formal statement with a one-line derivation ("per-component reading of `zeros(v)=0`; T0"). Move or drop the structural exposition; do not restate the subspace-identifier explanation in two adjacent slots.

### Issue 3: D-CTG preamble forward-inventories four unstated labels
**ASN-0036, Arrangement contiguity (preamble)**: "The properties below (D-CTG, D-MIN, D-CTG-depth, D-SEQ) bind S = 1 in their formal statements."
**Problem**: Each of those properties states `subspace(v)=1` (or `V_1(d)`) in its own formal contract, so the binding is visible at each site. Listing the four labels before they are stated is a forward inventory that the reader must hold without yet having the referents.
**Required**: Reduce to "The contiguity properties below are stated for the text subspace (S = 1)." Drop the label list.

## OUT_OF_SCOPE

### Topic 1: Operation-layer preservation of D-CTG / D-MIN / S2
**Why out of scope**: Whether INSERT/DELETE/COPY/REARRANGE preserve the contiguity invariants is operation-specific frame/postcondition territory, correctly excluded by the scope list and already routed to the Open Questions. The state-level invariants and the singleton-partition existence theorem are appropriately self-contained here; I am not flagging the absence of operation proofs as a gap.

The core results (S8 singleton partition, the within-/across-subspace uniqueness lemma, D-CTG-depth, D-SEQ) are proved case-complete, with boundaries handled (empty arrangement, m=2 vs m≥3, first/append positions) and verified against a concrete depth-2 and depth-3 worked example. No correctness defect found; the findings are bloat/clarity only.

VERDICT: REVISE
