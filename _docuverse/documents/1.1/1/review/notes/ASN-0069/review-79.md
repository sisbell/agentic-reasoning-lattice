# Review of ASN-0069

## REVISE

### Issue 1: Empty-case property-status inventory is redundant, misclassified, and incomplete
**ASN-0069, "The Empty-Source Case" (closing paragraph)**: "Under V7's normative behavior, V1, V2, V3, V5, V10, V11, V12 hold unconditionally; V6 holds substantively ...; V9 holds vacuously ...; V4 and V8 are vacuous when `V_{s_C}(d_op) = ∅` (their universal quantifiers range over the empty set...)."

**Problem**: This is a use-site/status inventory of the anti-bloat kind, and it is defective on three counts:
- **Duplication.** The worked example's "Empty source (V7)" paragraph already establishes, concretely on `d_src°`, which properties hold vacuously vs. substantively. The abstract inventory restates the same content in different words.
- **Misclassification.** V11 and V8a quantify over `V_{s_C}(d_src)`. On a first fork of an empty source, `d_op = d_src` and `V_{s_C}(d_src) = ∅`, so their conclusions are vacuous — exactly like V4 and V8, which the inventory *does* list as vacuous. Yet V11 is filed under "hold unconditionally" and V8a is omitted from the inventory entirely. The same quantifier-over-empty-set reasoning the paragraph applies to V4/V8 contradicts its placement of V11.
- **Incompleteness.** The inventory silently omits V3a, V4b, V5a, V6a, V8a, V8c, V9a, V9b, V10a, V11a — so as an inventory it is neither exhaustive nor reliable.

**Required**: Remove the inventory and let the concrete worked-example paragraph carry the empty case. If an abstract statement is retained, classify strictly by quantifier domain (everything ranging over `V_{s_C}(d_op)` / `V_{s_C}(d_src)` is vacuous; only the structural properties V1, V2, V3, V12(a) are substantive) and make the list complete rather than partial.

## OUT_OF_SCOPE

### Topic 1: Link discoverability projection machinery (V6a)
**ASN-0069, "Subspace Selectivity" (V6a and its `coverage` / `project` / `discoverable_from` definitions)**

**Why out of scope**: V6a introduces three new link-query definitions (endset coverage, V-position projection, link discoverability) and proves a three-part inheritance lemma over them. This is link-query semantics — the explicitly excluded "link semantics" topic — not a fork-operation invariant. The fork's actual survivability guarantee already rests on V4 (literal I-address sharing): once the fork holds the same I-addresses, any link-query apparatus defined elsewhere projects identically. The projection/coverage/discoverability definitions and their preservation proof belong in a link-operations ASN that owns those primitives; importing them here to restate a V4 corollary is new territory rather than a guarantee this ASN must establish.

VERDICT: REVISE
