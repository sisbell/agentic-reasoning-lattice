# Review of ASN-0132

## REVISE

### Issue 1: The version-refraction multiplicity is raised as a competing unit but never dispatched

**ASN-0132, Introduction / CN-UNIT**: The introduction names *four* multiplicities a link possesses and frames the entire note as the argument that forces a choice among them: "It may surface at many places in many arrangements, **and refract into many versions**. Each of these admits its own count. We must decide which count the operation reports... in a way an alternative implementation could not reasonably deviate from."

CN-UNIT then formally excludes only three: "(a) the number of spans or addresses its endsets reference, (b) the number of documents through which its endpoint content is reachable, and (c) the number of arrangement positions at which it surfaces." There is no clause for the **version count**.

**Problem**: The note's stated purpose is to rule out the competing units ("most of this note is the argument that forces it"), and one of the four units it explicitly raises — the per-version count — is never explicitly ruled out. A reader following the intro's own framing is left asking which claim disposes of versions. The likely resolution (a version is a document with its own arrangement, so "refraction into many versions" is a special case of appearance multiplicity (c), excluded by CN-LOC because the count never reads `Σ.M`) is correct but unstated. Worse, the load-bearing structural fact behind it is also unstated: a link is **one address regardless of the version DAG** — links are not forked per-version the way content is (the fork composite populates only the content subspace, not the link store, so a link homed at `d_src` yields no copy at `d_new`). Without saying this, an alternative implementation that re-homes/refracts a link per version and counts each occurrence is not provably "unreasonable" — precisely the deviation the intro promised to foreclose.

**Required**: Add a clause (d) to CN-UNIT (and/or a sentence to CN-TRANSCL) explicitly dispatching version-refraction multiplicity — stating whether it is subsumed under appearance (c) or genuinely distinct, and grounding the contribution-of-one in the fact that a link's identity is a single address that the version structure does not multiply. Alternatively, drop versions from the intro's enumeration of competing units. As written, the central "a number of what?" argument resolves three of the four cases it sets up.

### Issue 2: The worked census never exercises a constrained home-set

**ASN-0132, "A census, computed"**: The sole worked scenario uses `q = (∗, F, ∗, ∗)` and `q* = (∗, ∗, ∗, ∗)`. In both, the home component `H` is wildcard.

**Problem**: `sat` is the AND of four slot-criteria, and the home criterion is the one *structurally distinct* test — `liftH(a, H) ≡ athome(a, H) ≡ home(a) ∈ coverage(H)`, an address-projection membership test, not the endset-coverage overlap `touch` that the from/to/type slots use. The example verifies the `lift`/`touch` machinery thoroughly (via `a₁`, `a₃`, `a₄`, and the empty-from `a_R`) but never once computes `liftH` against a real region, so a quarter of the matching apparatus — and the only structurally different quarter — is left unverified against the concrete store. This matters because the ASN makes a *novel* claim about exactly this slot in CN-STAB's sharp instance ("a *home-bounded* count... still includes the link, because `home(a)` is a projection of the permanent address `a`"), which is asserted but never checked against any specific scenario.

**Required**: Extend the worked census (or add a second request) that constrains `H` — e.g., a home-set selecting `d₁` that admits the `d₁`-homed links and a home-set selecting `d₂` that excludes them — so that `athome`/`liftH` is exercised concretely and CN-STAB's home-bounded behavior (residence determined by address identity, unmoved by arrangement edits) is verified rather than only asserted.

## OUT_OF_SCOPE

No improperly-scoped claims appear. The federation, concurrency/single-snapshot, count-caching, endset-fragmentation deduplication, and cost-vs-enumeration questions are correctly deferred to Open Questions rather than claimed, and the implementation notes are cleanly cordoned from the abstract guarantees (including the candid record that Gregory's back end deviates from CN-UNIT via a dedup defect and pays full enumeration cost for the cardinality).

VERDICT: REVISE
