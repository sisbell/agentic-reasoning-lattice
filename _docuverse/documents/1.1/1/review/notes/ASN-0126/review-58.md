# Review of ASN-0126

The technical core checks out. I verified the projection bridge, the wp inheritance (gate ∧ ASN-0086 Case-2, with L3 / `T_admissible` / arity-(0) correctly absorbed), the RegisteredAdmissible lemma, and the P3/P5/P6 proofs; the born-nullified worked illustration is arithmetically correct end to end (`a_R = …2.3`, `g = …2.4`, `coverage(G_rng) = […2.4, …2.7)`, `g ∈ coverage(G_rng)`, citation born nullified). The findings below are accretion/duplication, which is what this note's anti-bloat classifier asks me to surface.

## REVISE

### Issue 1: "Properties established" restates P1–P6 already stated at their home sections
**ASN-0126, Properties established**: "The canonical formal statement and proof of each live at the section named in parentheses; the glosses here are pointers, not restatements."
**Problem**: The glosses *are* restatements. P1's gloss "the registry never drifts from `Σ_init.registry`" repeats P1's own statement "the registry never drifts"; P6's gloss "the guarantee a consuming app relies on" is copied verbatim from the P6 statement in *Reachable conformance*. Each property now has two statement sites — the formal one inline at its home section, and the English gloss here — so this section is a use-site inventory that adds no reasoning. The disclaimer that the glosses are "pointers, not restatements" is itself a tell that the slot is doing restatement work.
**Required**: Reduce the section to bare navigation pointers (property name → home section) with no re-gloss, or cut it. State each property once.

### Issue 2: P2's coverage-class conjunct re-derives what "Registration entries" already established
**ASN-0126, Registration entries → P2**: *Registration entries* already derives "for `K ~ K'`, `shape(K) = shape(K')` and `Sh-conf(K, F, G) = Sh-conf(K', F, G)` … This is what makes `shape(·)` a function of the type-as-coverage-class." P2 then re-derives the same fact: "For `K ~ K'`, `shape(K) = shape(K')`, so `shape(·)` is a function of `[K]` … exactly what was shown above to make `shape` and `Sh-conf` respect `~`."
**Problem**: Two paragraphs say the same thing; P2 admits it ("exactly what was shown above"). The coverage-class well-definedness is proved twice.
**Required**: Derive it once (in *Registration entries*); in P2's second conjunct, cite that derivation rather than repeating it.

### Issue 3: Self-referential and redundant back-pointers
**ASN-0126, The shape-gated emit**: "the arity guard (0) is omitted from `g_sh` because the postcondition's arity-3 slice `|Σ.L(a)| = 3` already forces it — **see The shape-gated emit**."
**Problem**: The pointer "see The shape-gated emit" appears inside the section titled *The shape-gated emit* — it points at its own section, so the reader has nowhere to go. Separately, the span-count definition `|e|` is introduced once in *Single-source* but re-flagged "(Single-source)" at each subsequent use (*Three shapes*, *Shape-conformance*); after the first, these courtesy pointers don't advance the argument.
**Required**: Drop the self-reference (or point to the actual locus where (0) is defined). Introduce `|e|` once and use it without re-citing.

## OUT_OF_SCOPE

### Topic 1: Registration as an operation
The registry is fixed at `Σ_init` and frozen by P1; there is no `Register` step, so every type an app will use must be present at substrate construction. That is a coherent design choice for *this* note ("an immutable registry whose contents do not drift"), and a dynamic-registration operation — if wanted — is a successor concern, not a defect here.
**Why out of scope**: The framing "apps register against" is satisfied by static membership in `Σ_init.registry`; adding a registration operation is new territory, not an error in this note.

### Topic 2: Retraction semantics under non-Binary R
The framework permits registering `[R]`'s coverage class under any shape, and the retraction semantics depend on that choice (Unary-R would make `nullified` inert; Multi-R would allow multi-span withdrawal). The note works out only the canonical Binary registration.
**Why out of scope**: Cataloguing which behaviors compose with which shapes is the note's own open question 2; one canonical retraction registration suffices here.

VERDICT: REVISE
