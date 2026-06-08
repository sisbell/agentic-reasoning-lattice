# Review of ASN-0114

## REVISE

### Issue 1: Disclosure derivation assumes all covered addresses are T4-valid and document-bearing

**ASN-0114, "Confinement" section (F6 disclosure analysis)**: "by the hierarchical structure of tumbler addresses (ASN-0034, T4), every covered address structurally contains its node, user, and document fields; so the home documents the selected end points into are readable directly off the result, with no separate disclosure step (Q4). Revealing the region *is* revealing the documents it lands in — the two are one disclosure, not a choice."

**Problem**: This derivation over-generalizes. `coverage(Σ.L(a).eᵢ)` is a set of arbitrary tumblers, not a set of T4-valid document-bearing addresses. The substrate this ASN builds on (ASN-0043, L4 — EndsetGenerality) explicitly states endset spans "may reference *any* addresses in the tumbler space ... no constraint confining spans to ... content addresses only, or to addresses at which content currently exists," and L9 permits ghost targets. An endset may therefore target a node-level address (`zeros = 0`, no document field) or a user-level address (`zeros = 1`). Furthermore, `coverage` is the union of half-open intervals `{t : s ≤ t < s ⊕ ℓ}`, which by construction include *interior* tumblers that need not be T4-valid at all (e.g., tumblers with adjacent zeros). T4b's field projections `N`, `U`, `D` are undefined on such addresses, so "every covered address structurally contains its node, user, and document fields" is false in general — even though it happens to hold for the (deliberately document-bearing) worked example.

**Required**: Restrict the disclosure claim to the T4-valid, document-bearing covered addresses (`zeros ≥ 2`), and state explicitly that for arbitrary or non-conforming covered addresses no document field is disclosed. The equivalence "revealing the region *is* revealing the documents it lands in" must be qualified accordingly, since L4 permits ends whose covered addresses name no document.

### Issue 2: Undefined/inconsistent term "spec-set"

**ASN-0114, Open Questions**: "What must the operation guarantee about the spec-set when the selected end's coverage includes addresses in more than one document..."

**Problem**: The body uses "span-set" consistently (per ASN-0053) as the type of the result. "spec-set" appears only here (and in the out-of-scope Scope list) and is never defined. If it denotes the same object as the returned span-set, the inconsistent vocabulary is a clarity defect; if it denotes something else, it is an undefined term in a load-bearing question.

**Required**: Replace "spec-set" with "span-set" (or define the term explicitly if it is intended to differ).

## OUT_OF_SCOPE

(none — the ASN correctly excludes resolution against a document's arrangement, link discovery, and full-link reading, and does not define claims for them.)

VERDICT: REVISE
