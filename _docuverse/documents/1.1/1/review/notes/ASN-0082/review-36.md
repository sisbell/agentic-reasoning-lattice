# Review of ASN-0082

## REVISE

### Issue 1: Implementation-specific historical notes pollute the specification
**ASN-0082, "Necessity from TA4 (mathematical)" section**: The "Historical notes" subsection contains specific code references — `do2.c:169–183`, `mantissa[1] == 0`, `is1story(width)`, `setlinkvsas`, `findaddressofsecondcutforinsert`, `retrievevspansetpm`, `beheadtumbler`, and the comment `NPLACES 16`.

**Problem**: A specification document should be stated abstractly enough that an alternative implementation would need to satisfy it. The udanax-green file references and function names describe one particular implementation's choices, not abstract requirements. Even with the disclaimer that they "do not contribute to the necessity argument," their presence dilutes the spec/implementation separation and ties this ASN to a specific codebase's nomenclature.

**Required**: Remove the "Implementation reality" bullet entirely, or move both the Literary Machines and udanax-green notes to a separate companion document (e.g., a design-notes file). The mathematical necessity argument from TA4 already stands on its own without them.

## OUT_OF_SCOPE

### Topic 1: Spans straddling region boundaries
I3-S applies only to spans with `s ≥ p` (entirely in the shifted region); D-S applies only with `s ∈ R` (entirely in the right region). Spans that straddle the boundary (start in L, end in or past X, or start in X) are not addressed.
**Why out of scope**: This belongs to a future link-update or external-reference ASN — the current scope is V-arrangement transformation, and the first Open Question already names this gap.

### Topic 2: Link-subspace contraction via tombstoning
The depth/subspace scoping axioms restrict contraction to S = 1, depth 2. Link-subspace mutation (V_2 with tombstones) is mentioned but deferred.
**Why out of scope**: Tombstoning has a different mutation discipline (sparse arrangements, no shift); a dedicated ASN should specify it.

### Topic 3: Generalization to depth > 2
The TA4 obstruction argument shows why contraction at depth > 2 needs a separate derivation.
**Why out of scope**: Already captured in the second Open Question.

VERDICT: REVISE
