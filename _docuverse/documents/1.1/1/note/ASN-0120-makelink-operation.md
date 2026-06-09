# ASN-0120: The MAKELINK Operation — Connection Recorded by Content Identity

*2026-06-08*

## The problem

A link in Nelson's design is "not between points, but between spans of data...
a strap between bytes." The operation that fastens such a strap is MAKELINK. The
system is handed three *endset arguments* — a from, a to, and a type — each
naming content regions somewhere in the docuverse, together with a *home
document* in which the link is to live. MAKELINK ties the regions together and
returns the link's identity.

We are asked to be exact about what that act consists of. What does the system
allocate as the link's identity, and how permanent is it? What does it record
about each endset — and in what coordinates, such that the record means the same
thing tomorrow as today? Where does the link itself reside, and what relationship
must its home document bear to the content its endsets touch? What does supplying
*three* endsets rather than two disclose about directionality, about typing, and
about the line between a bare connection and a typed relation? And what invariants
must the operation preserve once the link exists — about the permanence of the
link's identity, the immutability of the endsets it recorded, the independence of
where the link *lives* from what it *connects*, and the system's ability to
discover the link from any region its endsets reference?

We shall find that the whole content of MAKELINK is a single conversion of
coordinates. The endset arguments name content by its *arrangement position* — a
V-position in a document — but the link records each endset by *content identity*
— the I-address of the content there. Position is mutable; identity is permanent.
Everything the question asks about — survivability, immutability, discoverability
that ignores residence — is a consequence of recording at the identity level and
of the orthogonality between a link's home (where it lives) and its endsets (what
it touches).

## The substrate we build on

**Standing precondition (reachability).** Throughout, every state `Σ` ranges over
states reachable from the initial state `Σ₀` under the sequential transition order
(ASN-0047, SequentialTransitionAxiom). This licenses the per-state invariant
citations below — S0/S1 (content permanence), S2/S3 (arrangement functionality
and referential integrity), S7 (structural attribution), L0–L14 and L12 (link
structure and permanence), each of which the foundation ASNs guarantee only of
reachable states.

We take the strand and link models as given. The *content store*
`Σ.C : T ⇀ Val` (ASN-0036) binds *I-addresses* to values; it is append-only and
immutable — once `a ∈ dom(Σ.C)`, `a` persists and `Σ.C(a)` never changes (S0
ContentImmutability; S1 StoreMonotonicity). The *arrangement* of a document `d` is
a partial function `Σ.M(d) : T ⇀ T` (ASN-0036) from V-positions to I-addresses,
a genuine function (S2) whose every image lies in the content store (S3
ReferentialIntegrity), and it is the one component of state editable in place. The
*link store* `Σ.L : T ⇀ Link` (ASN-0043, ASN-0093) maps link addresses to link
values and is permanent (L12 LinkImmutability).

A *link value* is a finite sequence of `N ≥ 3` endsets,
`Link = (e₁, …, eₙ)`, each `eᵢ ∈ Endset = 𝒫_fin(Span)` (ASN-0043, L3). A span
`(s, ℓ)` satisfies T12 (ASN-0034) and denotes the order-convex set
`⟦(s, ℓ)⟧ = {t : s ≤ t < s ⊕ ℓ}`; the *coverage* of an endset is the union of its
span denotations, `coverage(e) = (∪ (s,ℓ) : (s,ℓ) ∈ e : ⟦(s,ℓ)⟧)` (ASN-0043,
ASN-0098). For a link address `a`, `home(a) = N(a).0.U(a).0.D(a)` is the
document-level prefix recovered by field projection (ASN-0043), coinciding with
`origin(a)` on link addresses (ASN-0086, HomeOriginCoincidence). We write
`subspace(v) = v₁` (ASN-0036) and fix the link subspace `s_L` and content
subspace `s_C` with `s_C ≠ s_L` (ASN-0047, SubspaceConventionAxiom). For a
document `d ∈ dom(Σ.M)`, the link sub-allocator `A_L(d)` produces fresh
link-subspace addresses scoped to `d`, with first emission `[d.0.s_L.1]` and
successors `inc(·, 0)` (ASN-0093, K.λ; FirstEmission, ChainDiscipline).

The link-creation transition is the substrate's `K.λ` (LinkAllocation, ASN-0093,
ASN-0047) followed by the link-subspace arrangement extension `K.μ⁺_L` (ASN-0047)
that seats the new link in its home document's V-stream. MAKELINK is the
user-level operation those two transitions implement; our task is to say what it
must guarantee abstractly.

## What the endset arguments name, and what resolution recovers

The from/to/type arguments do not arrive as I-addresses. They arrive as
*content-region specifications*: each is a spec-set
`R = ⟨(d₁, σ₁), …, (dₚ, σₚ)⟩`, a finite sequence of V-specs naming an allocated
source document `d_j ∈ dom(Σ.M)` and a well-formed V-span `σ_j = (u_j, ℓ_j)` over
it. We require each `σ_j` to be *content-subspace* (`subspace(u_j) = s_C`), at the
common content V-position depth `m = #u_j ≥ 2` in `d_j` (ASN-0058), and — the
load-bearing condition — to carry an *ordinal displacement* `ℓ_j = δ(n_j, m)` for
some `n_j ≥ 1` (equivalently `actionPoint(ℓ_j) = #u_j`, the tight half of T12's
`actionPoint(ℓ_j) ≤ #u_j`; `Pos(ℓ_j)` holds since `n_j ≥ 1`, so `σ_j` is
T12-well-formed, ASN-0034). The ordinal-displacement requirement is not cosmetic.
A merely level-uniform `ℓ_j` (`#ℓ_j = #u_j`) whose action point `k < m` would let
the half-open interval `⟦σ_j⟧` escape the content subspace — e.g.
`ℓ_j = [c, 0, …, 0]` has action point 1, so `u_j ⊕ ℓ_j = [s_C + c, 0, …, 0]` and
`⟦σ_j⟧` sweeps in link-subspace V-positions such as `[s_L, 1]`, whose images lie in
`dom(Σ.L)`, not `dom(Σ.C)`. Forcing the displacement to act at depth `m` pins
position 1 of every tumbler in `⟦σ_j⟧` to `s_C` (derived below), which is exactly
what lets resolution land in the content store. An endset argument that reaches into
the link subspace — a link pointing at another link — is deferred (Open Questions). A V-span lives in *arrangement* coordinates —
the positions a reader currently sees — and arrangement is exactly the mutable
component of state.

We must ask: what would happen if MAKELINK simply *stored the V-positions*? A
subsequent edit to `d_j` — an insertion before `σ_j`, a deletion, a rearrangement
— changes `Σ.M(d_j)`, displacing the very V-positions the link named. The link
would then point at whatever content drifted into those positions, or at nothing.
Nelson's survivability requirement — "if any of the bytes are left to which a link
is attached, that link remains on them" — would fail. So storing positions cannot
be right.

What must be true for the recorded endset to survive editing? It must reference
something that editing does *not* move. The content store is precisely that: by S0
an I-address, once allocated, denotes the same content for all time and is never
removed. Editing rearranges the V-to-I mapping; it never disturbs the I-addresses
themselves. Therefore MAKELINK must, at creation, read each named V-position
*through* its source arrangement and record the I-address it currently maps to.
This is the conversion at the heart of the operation.

We define *endset resolution* accordingly. For a spec-set `R` at state `Σ`,

> `ρ(R, Σ) = (∪ j : 1 ≤ j ≤ p : { Σ.M(d_j)(v) : v ∈ dom(Σ.M(d_j)) ∧ v ∈ ⟦σ_j⟧ })`

— the set of I-addresses to which the named, currently-active V-positions map. We
must discharge `ρ(R, Σ) ⊆ dom(Σ.C)`, and this turns on a confinement step the
ordinal-displacement precondition now supplies. Because `ℓ_j = δ(n_j, m)` acts at
depth `m = #u_j`, `u_j ⊕ ℓ_j = shift(u_j, n_j)` agrees with `u_j` on positions
`1..m−1` and differs only in the last (ASN-0034, OrdinalShift). Both endpoints of
`⟦σ_j⟧ = {t : u_j ≤ t < u_j ⊕ ℓ_j}` therefore share the length-`(m−1)` prefix
`p = (u_j)_1 … (u_j)_{m−1}` (non-empty since `m ≥ 2`), so `p ≼ u_j` and
`p ≼ u_j ⊕ ℓ_j`; by T5 (ContiguousSubtrees, ASN-0034) every `t` with
`u_j ≤ t ≤ u_j ⊕ ℓ_j` satisfies `p ≼ t`, hence in particular every `t ∈ ⟦σ_j⟧` has
`t₁ = (u_j)₁ = s_C`. Thus every `v ∈ ⟦σ_j⟧` — a fortiori every active such
`v ∈ dom(Σ.M(d_j))` — has `subspace(v) = s_C`. Generalized referential integrity
(S3★, ASN-0047) discharges containment on exactly these content-subspace positions
(`subspace(v) = s_C ⟹ Σ.M(d_j)(v) ∈ dom(Σ.C)`), giving `ρ(R, Σ) ⊆ dom(Σ.C)`: every
recovered address is real content. (In the ASN-0047 substrate S3★ supersedes
ASN-0036's S3, which alone would not discharge the containment, since a document's
arrangement also maps link-subspace V-positions into `dom(Σ.L)`; the
subspace-confinement step just shown is what restricts `ρ` to the content store.
Note we cannot lean on ASN-0058's C0/C0a here — those force action point `= m` only
for a *well-formed* content reference, and `ρ` deliberately admits partial spans
below — so the confinement is re-derived directly from the ordinal-displacement form,
which holds whether or not the reference is well-formed.) This is ASN-0058's `resolve` lifted to a spec-set: writing
`resolve(d_j, σ_j)` for that ASN's recovery of the I-address runs under `σ_j`,
`ρ(R, Σ)` is the union over `j` of the I-addresses those runs name. We diverge from
`resolve` in one deliberate respect and name it as such: `resolve` is defined only
for a *well-formed content reference* — one in which every depth-`m` position of
`⟦σ_j⟧` is active in `d_j`'s arrangement — whereas `ρ` filters to the
currently-active positions (`v ∈ dom(Σ.M(d_j))`) and so resolves *partial* spans as
well. MAKELINK must accept a span some of whose positions have since been deleted,
so this generalization is required, not incidental.

The resolved set is then packaged as an endset. We fix the *canonical*
representation: each I-address `aₖ ∈ ρ(R, Σ)` is recorded by its unit-depth span
`(aₖ, δ(1, #aₖ))`, whose denotation is the subtree `{t : aₖ ≼ t}` (ASN-0043,
PrefixSpanCoverage). The endset is the finite set of these spans (ASN-0058 supplies
the block decomposition that may merge adjacent runs into a wider span where the
content is contiguous in I-space; the merge is a representation choice and changes
nothing below). This representation does *not* make `coverage(e)` equal to
`ρ(R, Σ)`: coverage is a union of order-convex intervals, while `ρ(R, Σ)` is a bare
finite set, and ASN-0053 (S7, CoveringExistence) guarantees only *covering*,
`coverage(e) ⊇ ρ(R, Σ)`, never exact equality. What *is* exact is the recovery of
content — the only content addresses in `coverage(e)` are the resolved ones:

> `coverage(e_j) ⊇ ρ(R_j, Σ)` and `coverage(e_j) ∩ dom(Σ.C) = ρ(R_j, Σ)`.

The extra coverage points — the tumblers lying in a resolved address's subtree but
strictly below it — are never content: every content address sits on a sub-allocator
chain `A_C(d)` with element-field depth `#E = 2` (ASN-0093, C1b and ChainDiscipline),
whereas a proper descendant of such an address has `#E ≥ 3`, so it lies on no content
chain and is not in `dom(Σ.C)`. We name this **ML1 (EndsetResolution)**: each endset
argument is recorded as I-addresses recovered by reading the source arrangement at
creation time, so the stored endset references content by identity, not by position;
its coverage *covers* the resolved set and meets the content store in exactly the
resolved set.

Two structural facts about resolution deserve emphasis, both abstract. First, a
single V-span may resolve to *several non-contiguous* I-address runs: if the
source document's span covers content transcluded from two origins, the two runs
carry different I-addresses and cannot be merged into one contiguous span (ASN-0058,
M16 CrossOriginMergeImpossibility). The observable guarantee is *completeness of
recovery*: `coverage(e_j) ∩ dom(Σ.C) = ρ(R_j, Σ)` regardless of how the supplied
span fragments in I-space — every referenced content address is recovered, and no
spurious content address is introduced, whatever the contiguity structure or the
number of V-spans supplied. We name this **ML2 (FaithfulRecovery)**. (How many
spans the endset's representation happens to use to cover those addresses is *not*
abstractly observable: the model exposes no span-positional accessor (ASN-0043, L5)
and projection depends only on coverage, not decomposition (ASN-0098, LP21). The
span-set cardinality is therefore a representation matter, left to the
implementation note.) Second, the same resolution applies *uniformly* to all three
endset arguments — from, to, and type are read through their sources by one
procedure, with no slot privileged at the conversion step (**ML3,
UniformResolution**).

> *Implementation note.* Gregory's CREATELINK realizes ρ in `vspanset2sporglset`,
> which calls `permute` to walk each source document's arrangement and emit one
> *sporgl* — an `(I-origin, I-width, source-doc)` triple — per contiguous I-region
> (Q12, Q13). The result is stored, never the input V-positions. This is the
> behavioral ground truth for ML1–ML3; the sporgl layout itself is implementation,
> not an abstract claim.

## The link's identity

With the endsets resolved, MAKELINK must mint the link's identity. The home
document `d` names which document owns the link, and the link's address is
allocated under `d`'s prefix: `a` is the fresh emission of `A_L(d)` (ASN-0093,
K.λ). Three properties of this address are abstract and load-bearing.

It is *fresh*: `a ∉ dom(Σ.L)` at the creating state (FirstEmissionFreshness /
SubsequentEmissionFreshness, ASN-0093). It is *home-scoped*: `home(a) = d`, by the
sub-allocator's construction (the address extends `[d.0.s_L]`). And it is
*permanent and never reused*: by GlobalUniqueness (ASN-0034) no other allocation
event in the system ever produces `a`; by allocation permanence (T8, ASN-0034) `a`
is never removed from the allocated set; and by L12 (ASN-0043) the value `Σ.L(a)`
is fixed for all time once written. We name this **ML0 (IdentityAllocation)**: the
link's identity is a fresh, permanent, never-reused link-subspace address
allocated under the home document.

Nelson's premise that a link's home "does not change" is now a theorem rather than
an assumption: the home fields `N(a).0.U(a).0.D(a)` are the leftmost components of
the link's *own* address, fixed at allocation, and no operation rewrites an
address. Residence is built into identity; there is no mutable home attribute that
could drift.

> *Implementation note.* Gregory allocates the link orgl at `docISA.0.2.N`,
> independently per home document, the counter advancing monotonically (Q11). The
> "shift" that `findnextlinkvsa` could in principle perform is structurally a no-op
> because links are appended at the document's V-extent (Q17). Abstractly this is
> just ML0's freshness; the append-at-end mechanism is implementation.

## Residence, and its independence from what the link connects

Where does the link reside? In two senses, both recorded by MAKELINK. The link
*object* enters the link store, `Σ'.L = Σ.L ∪ {a ↦ (e₁, e₂, e₃)}`. And the link
*reference* enters the home document's arrangement in the link subspace, via
`K.μ⁺_L` (ASN-0047): a fresh link-subspace V-position `v_a` of `d` is bound to `a`,
making the link a member of `d`'s V-stream (so `d`'s owner can enumerate the links
it homes). The home document is thereby the link's residence and the locus of its
ownership.

Now the orthogonality. The home `d` was supplied independently of the endset
arguments, and nothing in the operation couples them. MAKELINK admits a home `d`
together with endsets whose coverage is *disjoint* from everything under `d`'s
prefix — a link living in document C that connects regions of A and B, touching
nothing in C. Formally, the precondition imposes no constraint relating `d` to
`ρ(R_j, Σ)`; the address `a` extends `d`'s prefix, while each `coverage(e_j)` is an
arbitrary subset of allocated I-addresses (ASN-0043, L4 EndsetGenerality). We name
this **ML4 (ResidenceApplicationOrthogonality)**: a link's home document and the
content its endsets reference are independent; connecting two documents never
forces the link to live inside either, and a link need not point anywhere in its
home. The home determines *ownership*; the endsets determine *connection*; the two
are separate coordinates. This is the invariant that makes annotation possible — a
reader comments on another's published document by homing a link at *her own*
address whose endsets reach into *his* content, modifying nothing of his.

## Three endsets: directionality, typing, and relation versus connection

MAKELINK records the endsets as an *ordered* triple, and the order carries
meaning. By slot distinction (ASN-0043, L6), the recorded link is positionally
addressable, and `(F, G, Θ) ≠ (G, F, Θ)` whenever `F ≠ G`: the from-side and the
to-side are a *stable, recoverable* distinction. We name this **ML5
(OrderedEndsets)**: MAKELINK preserves which region plays which role.

But what kind of distinction is it? Two readings are possible — a *semantic*
direction (this end is "from," that end is "to," for the user to interpret) or a
*traversal* restriction (the link may be followed only from→to). The consultation
forces the first reading and forbids the second. Nelson: "what 'from' and 'to'
mean depend on the specific case" — the system attaches no universal semantics —
and the discoverability invariant below indexes *every* endset symmetrically, so a
reader at the to-side finds the link as readily as one at the from-side. The
ordering is therefore a labeling the user may rely on, not a one-way valve. We
record this as the directionality half of ML5: the recorded order fixes roles
without restricting reachability. The degenerate one-sided case is consistent —
when there is no meaningful from, the first endset alone designates what is
pointed at.

The third endset reveals the difference between a *connection* and a *relation*.
A link with only from and to asserts that two regions are tied together — a bare
connection. The third endset is a *type*: a classifying address-set that says in
*what way* they are tied. The substrate transition `K.λ` requires a non-empty type
endset (`e₃ ≠ ∅`, L3, ASN-0093). Since the type argument is `ρ`-resolved like the
others (ML3), MAKELINK must carry this as an *operation precondition on its type
argument*: the supplied type spec must resolve non-empty,

> `ρ(R₃, Σ) ≠ ∅`  (equivalently, `R₃` names at least one currently-active V-position).

A type spec whose V-positions are all inactive — content deleted, or a document
opened that never held the type content — resolves to `∅`; on such input the
operation is *undefined* and must be rejected before `K.λ` is attempted, since an
empty `e₃` violates L3. (Gregory's CREATELINK does *not* enforce this: an empty type
sporgl set resolves to `NULL`, passes the two insertion guards `do2.c:122` and
`do2.c:136` silently — the latter even debug-prints the missing-type pointer, an
acknowledged accommodation rather than a rejection — and a link is stored with no
type endset at all. The abstract operation forbids what the implementation tolerates;
the precondition is the correct contract.) With the precondition met, every link
MAKELINK creates carries a classifier, and by L8
(TypeByAddress) the type is matched by the *addresses* its endset covers, not by
any content stored there. So the type may even reference a region where nothing is
stored (a ghost type, L9), because what the system records and compares is the
address, not its content. We name this **ML6 (TypedRelation)**: the third endset,
recorded identically to from and to but read as a classifier by address, is what
distinguishes a typed relation from an untyped connection. The structural cost of
typing is one more I-address endset; the semantic gain is the difference between
"these are linked" and "these are linked *thus*."

## The invariants MAKELINK preserves

We collect the guarantees, each now a consequence of how the operation records.

**Permanence (ML7).** The link's address persists and its value is fixed: for
every later transition `Σ' → Σ''`, `a ∈ dom(Σ''.L)` and `Σ''.L(a) = Σ'.L(a)`
(L12, ASN-0043). The link, once made, is not unmade by any editing of the content
it connects — because editing touches `Σ.M`, and the link lives in `Σ.L`. (Whether
a link's *owner* may delete it is a separate operation outside this ASN; MAKELINK
guarantees that no one *else's* edit can break it.)

**Endset immutability (ML8).** The recorded endset value `Σ'.L(a)` is frozen at the
creating state `Σ`, with `coverage(e_j) ∩ dom(Σ.C) = ρ(R_j, Σ)` (ML1). No
subsequent operation rewrites an endset:
the link store is immutable (L12), and editing a source document changes
`Σ.M(d_j)` but never the I-addresses already recorded in `Σ.L(a)`. Suppose content
is later inserted before, deleted from, or rearranged around a referenced region:
the V-positions move, but the stored I-addresses do not, and by S0 those
I-addresses still denote their original content. So the endset remains valid as
long as any of its content survives — which, for published content that S0 keeps
forever, is always. This is exactly Nelson's survivability, and it is *bought* by
the V→I conversion of ML1: had MAKELINK stored positions, immutability of the
record would not yield survival of the reference.

**Residence-independence of discoverability (ML9).** This is the operation's
sharpest guarantee, and it follows by a short weakest-precondition argument. Take
as postcondition that the new link is discoverable from a document `d'` — meaning,
in the abstract characterization of ASN-0098 (LP12),

> `discoverable_from(a, d', Σ') ⟺ (E i : 1 ≤ i ≤ 3 : coverage(Σ'.L(a).eᵢ) ∩ ran(Σ'.M(d')) ≠ ∅)`.

Since MAKELINK sets `Σ'.L(a) = (e₁, e₂, e₃)`, the right-hand side reduces in two
steps.

*Fact (a) — the coverage/`ρ` gap collapses on the content store.* By generalized
referential integrity (S3★, ASN-0047) an arrangement's images split by subspace:
`ran(Σ'.M(d')) ⊆ dom(Σ.C) ∪ dom(Σ.L)`, the content-subspace V-positions mapping
into `dom(Σ.C)` and the link-subspace ones into `dom(Σ.L)`. Each `coverage(eᵢ)`
lies in content subtrees (subspace `s_C`): every recorded span is a unit-depth span
on a resolved content address or its descendants, and the specs resolve only
content-subspace V-positions (above), so every covered tumbler carries
`subspace_I = s_C`. The link-subspace images, by contrast, lie in subspace `s_L`;
since `s_C ≠ s_L`, `coverage(eᵢ)` meets no link-subspace image, and the
intersection consults only the content images. By ML1 the content part of
`coverage(eᵢ)` is exactly the resolved set, giving
`coverage(eᵢ) ∩ ran(Σ'.M(d')) = ρ(R_i, Σ) ∩ ran(Σ'.M(d'))`. The covering
surplus — the non-content descendants in `coverage(eᵢ)` — cannot meet a content
range and so drops out.

*Fact (b) — the post-state range equals the pre-state range for the test.* For
`d' ≠ d`, `K.μ⁺_L` touches only the home document's arrangement, so
`Σ'.M(d') = Σ.M(d')` and `ran(Σ'.M(d')) = ran(Σ.M(d'))`. For the boundary case
`d' = d` — the home document itself, exactly the case ML4 highlights — `K.μ⁺_L`
extends the arrangement by the single binding `v_a ↦ a`, so
`ran(Σ'.M(d)) = ran(Σ.M(d)) ∪ {a}`; but the added address `a` is a link-subspace
address (`subspace_I(a) = s_L`), while `coverage(eᵢ)` and its surplus lie in content
subtrees (subspace `s_C`) — every supplied spec is content-subspace, the type spec
of ML6 included, and a ghost type (L9) is a content-subspace address not yet in
`dom(Σ.C)`, still carrying `subspace_I = s_C` — so `a ∉ coverage(eᵢ)` and the added
point is inert:
`coverage(eᵢ) ∩ ran(Σ'.M(d)) = coverage(eᵢ) ∩ ran(Σ.M(d))`. In both cases the test
reads against the pre-state range.

Composing (a) and (b) — and conjoining the operation's definedness, since
`makelink` is *partial* (ML0 requires `d ∈ dom(Σ.M)`, ML6 requires
`ρ(R₃, Σ) ≠ ∅`) and the postcondition `discoverable_from(a, d', ·)` is itself
defined only for `d' ∈ dom(Σ.M)`,

> `wp(makelink(d, R₁, R₂, R₃), discoverable_from(a, d', ·))`
> `≡ enabled(makelink(d, R₁, R₂, R₃)) ∧ d' ∈ dom(Σ.M) ∧ (E i : 1 ≤ i ≤ 3 : ρ(R_i, Σ) ∩ ran(Σ.M(d')) ≠ ∅)`,

where `enabled(makelink(d, R₁, R₂, R₃)) ≡ d ∈ dom(Σ.M) ∧ ρ(R₃, Σ) ≠ ∅` unfolds the
operation's own preconditions (paralleling the `enabled(K.μ⁻[d,R])` conjunct of
ASN-0098 LP12a). Source-document allocation is *not* a separate conjunct of
`enabled`, and its absence is deliberate, not an omission. Every well-formed
spec-set argument already names allocated sources (`d_j ∈ dom(Σ.M)`, by the spec-set
definition above), and the definedness of each `ρ(R_i, Σ)` requires exactly that
every source document it names lie in `dom(Σ.M)`. So definedness of `ρ(R₁, Σ)`,
`ρ(R₂, Σ)`, and `ρ(R₃, Σ)` alike is presupposed by well-formed input rather than
guarded by `enabled`; `enabled` folds in only the genuinely operation-level guards
that well-formedness does not already secure — home-document allocation and a
non-empty type resolution. The remaining definedness conjuncts shown are essential:
without them the formula would assert the postcondition reachable on inputs the
operation rejects — e.g. an empty type spec, which ML6 forbids.

Beyond the operation's own enabledness, the home document `d` does not appear in
the discoverability test on the right. The condition for finding the
link from `d'` is solely that `d'`'s arrangement reaches one of the I-addresses the
link recorded — and that holds for *any* document sharing the content, the home
document among them only incidentally. Residence fixes ownership; it imposes no
restriction whatever on discoverability scope. Because the criterion is symmetric
across all three endsets, the link is reachable from the from-regions, the
to-regions, and the type-regions alike. We name this **ML9
(DiscoverabilityDecoupledFromResidence)**: MAKELINK makes the link discoverable
from every content region any of its endsets references, independently of where
the link resides.

Note what discharges ML9: *nothing beyond recording the endsets as I-addresses in
the store.* The discoverability is not a separate indexing action MAKELINK must
remember to perform; it is the standing meaning of having content-identity endsets
present in `Σ.L`. (Gregory's spanfilade is the concrete index that realizes this
biconditional, keyed by I-address with the home dimension explicitly nulled out —
Q14, Q20 — which is the implementation's way of guaranteeing exactly that home
plays no role. The abstract claim is the biconditional, not the index.)

**Frame (ML10).** MAKELINK allocates no content and edits no other document:
`Σ'.C = Σ.C` (the operation reads source arrangements, it does not write content),
and `Σ'.M(d') = Σ.M(d')` for every `d' ≠ d` (only the home document's link
subspace is extended). Existing link-store entries are untouched — the store only
gains `a ↦ (e₁, e₂, e₃)`. The sources the endsets read are unmodified by the act
of being linked into: a link *to* a region changes nothing about that region,
which is why links can be made to published material one does not own.

These ten claims are not independent demands the operation must separately satisfy.
They are facets of one decision — record connection at the level of content
identity, in an owned home, by a permanent address — refracted through the
permanence of the I-address space and the orthogonality of ownership and
application.

## A worked example

Fix three documents `A`, `B`, `C`, all in `dom(Σ.M)`, and create a link homed in
`C` that connects content of `A` to content of `B` — touching nothing in `C`. This
is the annotation shape of ML4.

*Source content.* In `A`, two active V-positions map to content I-addresses
`a₁ = A.0.s_C.1` and `a₂ = A.0.s_C.2`, so `{a₁, a₂} ⊆ ran(Σ.M(A))`. In `B`, one
active V-position maps to `b₁ = B.0.s_C.1`, so `b₁ ∈ ran(Σ.M(B))`. A type address
`θ₁` is held somewhere stable.

*Arguments.* `from = R₁` resolves to `ρ(R₁, Σ) = {a₁, a₂}`; `to = R₂` resolves to
`ρ(R₂, Σ) = {b₁}`; `type = R₃` resolves to `ρ(R₃, Σ) = {θ₁} ≠ ∅`, so the type
precondition of ML6 is met; `home = C`.

*Identity (ML0).* `A_L(C)` emits the fresh link address `a = C.0.s_L.1` — `C`'s
first link. It is fresh (`a ∉ dom(Σ.L)`), home-scoped
(`home(a) = N(a).0.U(a).0.D(a) = C`), and distinct from every content address
(`subspace_I(a) = s_L ≠ s_C`).

*Record (ML1, ML2).* `Σ'.L(a) = (e₁, e₂, e₃)` with
`e₁ = {(a₁, δ(1,#a₁)), (a₂, δ(1,#a₂))}`, `e₂ = {(b₁, δ(1,#b₁))}`,
`e₃ = {(θ₁, δ(1,#θ₁))}`. Checking ML1/ML2: `coverage(e₁) ∩ dom(Σ.C) = {a₁, a₂} =
ρ(R₁, Σ)` — the subtrees of `a₁` and `a₂` hold no other content address, their
proper descendants having `#E ≥ 3` — and likewise `coverage(e₂) ∩ dom(Σ.C) = {b₁}`.
The two runs of `e₁` stay separate when `a₁, a₂` are non-adjacent in I-space, but
nothing observable hangs on whether they are recorded as two unit spans or one
wider span; only the content-coverage `{a₁, a₂}` is observable.

*Discoverability (ML9).* Evaluate `discoverable_from(a, d', Σ')` for each document.
From `A`: `coverage(e₁) ∩ ran(Σ'.M(A)) ⊇ {a₁} ≠ ∅` — discoverable. From `B`:
`coverage(e₂) ∩ ran(Σ'.M(B)) ⊇ {b₁} ≠ ∅` — discoverable. From the home `C`: the
link's endsets reference only `A`- and `B`-content, none of it in `ran(Σ'.M(C))`;
the one address `C`'s arrangement gained is `a` itself, in the link subspace and
outside every `coverage(eᵢ)`. So `coverage(eᵢ) ∩ ran(Σ'.M(C)) = ∅` for all `i`, and
the link is *not* discoverable from its own home. This is ML9 made concrete:
discovery follows the content the endsets name (`A` and `B`), not the residence
(`C`). The link lives in `C` yet is found from `A` and `B` — residence and
reachability are orthogonal.

## Claims Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| ML0 | IdentityAllocation: the link's identity is a fresh (`a ∉ dom(Σ.L)`), permanent (never removed, never reused — GlobalUniqueness, T8), value-fixed (L12) link-subspace address allocated by `A_L(d)` under home `d`, with `home(a) = d` | introduced |
| ML1 | EndsetResolution: each endset argument `R` is recorded as `ρ(R,Σ) = {Σ.M(d_j)(v) : v ∈ dom(Σ.M(d_j)) ∧ v ∈ ⟦σ_j⟧}` ⊆ dom(Σ.C) (ASN-0058 `resolve` generalized to partial spans) — I-addresses read through source arrangements at creation; canonical unit-depth spans give `coverage(e_j) ⊇ ρ(R_j,Σ)` with `coverage(e_j) ∩ dom(Σ.C) = ρ(R_j,Σ)` (covering, not exact — ASN-0053 S7) | introduced |
| ML2 | FaithfulRecovery: `coverage(e_j) ∩ dom(Σ.C) = ρ(R_j,Σ)` regardless of I-space fragmentation — every referenced content address recovered, none spurious; recorded span-set cardinality is a representation matter (no span-positional accessor, L5; projection by coverage only, LP21), not an abstract observable | introduced |
| ML3 | UniformResolution: from, to, and type arguments are resolved by one procedure with no slot privileged at the V→I conversion step | introduced |
| ML4 | ResidenceApplicationOrthogonality: home document and endset content are independent; the precondition relates `d` to no `ρ(R_j,Σ)`; a link may home anywhere and point anywhere, connecting two documents without residing in either | introduced |
| ML5 | OrderedEndsets: the recorded triple is ordered, `(F,G,Θ) ≠ (G,F,Θ)` for `F ≠ G` (L6); the order fixes from/to roles semantically without restricting reachability (discovery is endset-symmetric) | introduced |
| ML6 | TypedRelation: operation precondition `ρ(R₃,Σ) ≠ ∅` (the operation is undefined on a type spec that resolves empty, since K.λ requires `e₃ ≠ ∅`, L3); the third endset, recorded like from/to but matched by address (L8), distinguishes a typed relation from a bare connection; type-by-address admits ghost types | introduced |
| ML7 | Permanence: `(A Σ' → Σ'' : a ∈ dom(Σ'.L) : a ∈ dom(Σ''.L) ∧ Σ''.L(a) = Σ'.L(a))` — the made link is not broken by any editing of the content it connects | introduced |
| ML8 | EndsetImmutability: the recorded value `Σ'.L(a)` is frozen at creation (L12), with `coverage(e_i) ∩ dom(Σ.C) = ρ(R_i,Σ)`; editing source documents changes `Σ.M` but never the recorded I-addresses, so by S0 the endset survives as long as any referenced content persists | introduced |
| ML9 | DiscoverabilityDecoupledFromResidence: `wp(makelink, discoverable_from(a, d', ·)) ≡ enabled(makelink) ∧ d' ∈ dom(Σ.M) ∧ (E i : ρ(R_i,Σ) ∩ ran(Σ.M(d')) ≠ ∅)`, with `enabled(makelink) ≡ d ∈ dom(Σ.M) ∧ ρ(R₃,Σ) ≠ ∅`; beyond enabledness the home `d` does not appear in the discoverability test — the link is discoverable from every region its endsets reference, residence-independently and endset-symmetrically | introduced |
| ML10 | Frame: `Σ'.C = Σ.C`; `(A d' ≠ d : Σ'.M(d') = Σ.M(d'))`; existing `Σ.L` entries unchanged; the linked-into sources are unmodified by being linked into | introduced |

## Open Questions

What must MAKELINK guarantee about the relative order in which a single endset's resolved I-address runs are recorded, and is any ordering across runs observable through later operations?

Under what conditions, if any, may the resolution `ρ(R, Σ)` legitimately recover an empty set for the from or to endset, and what does an empty non-type endset mean for the link's connection?

What invariant must hold so that two MAKELINK calls supplying identical endset arguments and identical home necessarily produce distinct link identities rather than coalescing?

What must the operation guarantee when an endset argument references content in the link subspace — a link whose endset points at another link — for the resolved record to remain well-formed?

What is the precise condition under which a newly created link is discoverable from *no* document, and what must be true for a later operation to bring it into discoverability without altering the link?
