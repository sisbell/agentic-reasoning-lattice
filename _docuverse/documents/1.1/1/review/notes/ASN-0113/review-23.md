# Review of ASN-0113

## REVISE

### Issue 1: Link extent equals "number of links" is never derived from CL-UNIQ
**ASN-0113, "What the caller must be handed" / W18**: W0 inherits Nelson's purpose — the span-set "indicates both the number of characters of text and the number of links" (4/68) — and W18 says "The link count is specifically the count of home links — links the document owns (CL-OWN)."
**Problem**: The note proves `n_S(d) = |V_S(d)|` (W1) and reports it as the subspace "extent," but it never bridges `|V_{s_L}(d)|` to *the number of links*, which is the operation's stated reason for existing. That equivalence holds only because each home link occupies **exactly one** link-subspace V-position — CL-UNIQ's injectivity — combined with CL-OWN. The note lists CL-UNIQ in its foundation-facts inventory but never invokes it: W18 cites only CL-OWN. Without the CL-UNIQ step, a link occupying two V-positions would double-count, and the link member would not "indicate the number of links" at all. A derived guarantee that is the whole point of the operation is asserted without its derivation.
**Required**: State and discharge the bridge explicitly — `|V_{s_L}(d)|` = number of home links via CL-OWN (only own links present) and CL-UNIQ (a bijection between home links and link-subspace V-positions). Without this, the content side (`n_{s_C}` = number of characters, one I-address per content position by S2/S3★) is also stronger than the link side, and the asymmetry should be noted.

### Issue 2: An invented "subspace s = 3" to justify exhaustiveness
**ASN-0113, "The operation: one span per occupied subspace"**: "A link is internally a three-ended structure, and its endpoint sub-addresses inhabit a third region of the address tree (a type/endpoint subspace, `s = 3`)."
**Problem**: This conflates a link's *arity* (three endsets: from/to/type) with a *subspace identifier*. The model fixes only `s_C = 1` and `s_L = 2` (SubspaceConventionAxiom); no foundation establishes a content-bearing "subspace 3," and a link's endsets reference arbitrary addresses (L4, EndsetGenerality, ASN-0043), not addresses confined to some third subspace. The paragraph invents structure to motivate "no third member arises," but W9's actual grounding — S3★-aux restricting `subspace(v) ∈ {s_C, s_L}` — is cited two lines later and needs none of this. The prose is both factually loose and redundant.
**Required**: Delete the `s = 3` invention. W9 follows directly from S3★-aux + SC-NEQ; the exhaustiveness argument is complete without imagining a third subspace.

### Issue 3: W17 restates W4
**ASN-0113, W17 (ExtentDeterminesPopulation)**: "the active positions of `S` are exactly those V-slice tumblers lying within `ext(d, S)` (this is W4 restated as a fidelity claim)".
**Problem**: The note itself admits the claim restates W4. The only increment over W4 is the trailing "each such position carries content" (a one-step S3★ consequence). A separate labeled claim that is acknowledged to be a rewording of an existing one is the duplication pattern the anti-bloat pass targets.
**Required**: Either fold the content-carrying observation into W4 as a corollary, or reduce W17 to that single added consequence rather than re-stating the coverage equality.

### Issue 4: Doubled prose restatement in the W12 section
**ASN-0113, "What the pair reveals that neither member alone could"**: "A single extent gives a size; the pair gives a proportion. Ask for the text extent alone and you learn how much matter the document carries, but nothing about how connected it is; ask for the link extent alone..."
**Problem**: The formal W12 statement (neither projection is injective on the profile) is preceded by two successive prose paraphrases of the same point. This is essay content restating a formal claim twice before stating it; one motivating sentence suffices.
**Required**: Trim to a single motivating line and let the formal statement and its reachability witness carry the argument.

## OUT_OF_SCOPE

(none — the note correctly routes version-fork permanence, transclusion, and overall-extent consistency to Open Questions rather than defining claims for them.)

VERDICT: REVISE
