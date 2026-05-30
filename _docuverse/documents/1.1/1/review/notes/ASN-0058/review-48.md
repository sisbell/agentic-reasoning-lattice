# Review of ASN-0058

## REVISE

### Issue 1: Forward-reference accretion in the OrdinalShiftBase and "+" overloading paragraphs

**ASN-0058, The Mapping Block (Convention OrdinalShiftBase)**: "The `k = 0` case is the base of every correspondence run: when `β = (v, a, n)` is in a decomposition of `M(d)`, B3 (Consistency) at `k = 0` reduces to `M(d)(v) = a` — no displacement, no arithmetic. This convention is in force in every claim, every definition, and every proof below; M-aux establishes its associativity..."

**Problem**: The convention is a one-line definition (`t + 0 = t`). The trailing sentences justify *why* the `k=0` base matters by forward-referencing B3 and M-aux — meta-prose that explains the convention's downstream role rather than stating the convention. The subsequent "+" overloading paragraph compounds this: its final sentence ("M-aux's statement ... uses both senses simultaneously ... the equation is the bridge between the two") forward-references M-aux to editorialize about notation. A reader must skip past both to reach M-aux.

**Required**: Reduce to the definition plus the minimal disambiguation that tumbler-natural `+` is shift and natural-natural `+` is ordinary addition. Drop the B3/M-aux justifications; they belong (and already appear) at B3 and M-aux.

### Issue 2: M-int dependency/availability inventory header

**ASN-0058, M-int**: "The lemma uses S8a, S8-depth (ASN-0036), T5 (ContiguousSubtrees), TumblerAdd, T1, T3, and OrdinalShiftBase (ASN-0034); no block-decomposition fact (B1, B2, B3, M0, ...) is invoked, so M-int is available wherever its premises hold."

**Problem**: This is a dependency inventory plus a reusability justification ("available wherever its premises hold") sitting between the statement and the proof. The dependencies are evident from the proof; the reusability assertion is the kind of meta-claim that accretes across cycles. The "T3 ... is what licenses the final 'hence `y = x + k`' step" sentence is an in-proof forward pointer that duplicates what the proof already shows at that step.

**Required**: Remove the inventory and the reusability assertion. If M-int's reuse on the restriction `f` (C1a) needs justification, make that argument once at C1a's site, not as a standing claim here.

### Issue 3: M-sub is a non-load-bearing lemma carrying use-site-inventory prose

**ASN-0058, M-sub (concluding paragraph)**: "The two clauses act in concert: a single mapping block (with `#v ≥ 2`) is confined to one V-subspace and (when its I-start resides in `dom(C)`) one I-subspace. When `β` participates in a decomposition ... clause (b) applies unconditionally to decomposition members; clause (a) further requires `#v ≥ 2` ..."

**Problem**: This paragraph enumerates downstream applicability without deriving anything. Worse, M-sub is never actually consumed: C1a's only mention — "M-sub clause (a) and OrdShiftHom ... apply to every position in dom(f)" — derives no conclusion (the subspace fact C1a uses is supplied by C0a, `t₁ = u₁`), and clause (b) (I-subspace confinement) is invoked nowhere; M16a establishes origin preservation directly from TumblerAdd's prefix-copy, not from M-sub. M-sub is dead weight with an inventory paragraph attached.

**Required**: Either consume M-sub where it is genuinely needed (and delete the vacuous C1a mention) or remove M-sub entirely. In either case, delete the "act in concert" use-site inventory.

### Issue 4: M16a enumerates its downstream consumers

**ASN-0058, M16a (closing sentence)**: "This is the load-bearing fact that M16 and M16b (below) both turn on: ordinal increment never crosses an origin boundary, because the document prefix lies strictly below the action point."

**Problem**: The clause "the load-bearing fact that M16 and M16b (below) both turn on" is a consumer enumeration — exactly the accretion pattern flagged for this note. The substantive content ("ordinal increment never crosses an origin boundary, because the document prefix lies strictly below the action point") is a fair one-line summary and may stay; the consumer list should go.

**Required**: Keep the summary clause, delete the "load-bearing fact that M16 and M16b turn on" inventory.

### Issue 5: M2 misattributes ASN-0036's S8 postcondition labels

**ASN-0058, M2**: "*S8(b) ⟺ B3.* S8(b) asserts `M(d)(shift(vⱼ, k)) = shift(aⱼ, k)` ..." and "*S8(a) ⟺ B1 ∧ B2 via V-extent translation.* S8(a) is stated in interval form, `(A v ∈ dom(M(d)) :: (E! j :: vⱼ ≤ v < shift(vⱼ, nⱼ)))`". Also: "This is S8 (SpanDecomposition, ASN-0036) restated".

**Problem**: ASN-0036's S8 (CorrespondenceRunPartition) labels the lockstep `M(d)(shift(vⱼ,k)) = shift(aⱼ,k)` as postcondition **(a)**, not (b); its (b) is the well-defined-label clause and (c) is uniqueness. There is no interval-form postcondition labeled S8(a) in the foundation — the partition claim is stated as prose plus (c). So M2's S8(a)/S8(b) citations are swapped relative to the foundation, and the interval form is attributed to a label that carries different content. The name "SpanDecomposition" also does not match the foundation's "CorrespondenceRunPartition."

**Required**: Correct the sub-claim citations to match ASN-0036's actual S8 labels (lockstep = (a), partition/uniqueness = prose + (c)), and use the foundation's name. If M2 relies on an interval-form statement, derive it from the foundation's partition claim rather than citing it as "S8(a)."

## OUT_OF_SCOPE

(none — the Open Questions and the excluded operation-effect topics are appropriately deferred.)

VERDICT: REVISE
