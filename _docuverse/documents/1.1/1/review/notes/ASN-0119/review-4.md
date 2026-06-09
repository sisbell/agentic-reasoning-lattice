# Review of ASN-0119

## REVISE

### Issue 1: The scope-restriction justification misstates the link subspace's invariants

**ASN-0119, "The two streams" and "Cuts and regions"**: "These contiguity invariants hold for the text subspace `s_C` and *not* in general for other subspaces — the link subspace `s_L`, in particular, is exempt"; and "in particular the link subspace — lacking D-CTG/D-SEQ/D-MIN — does not admit the cut-naming this operation relies on."

**Problem**: This is the note's stated reason for confining REARRANGE to text, and it is inconsistent with the foundations the note itself relies on. The unstarred D-CTG/D-SEQ/D-MIN (ASN-0036) are indeed text-only, but the note works in and cites ASN-0047's model — it invokes `D-CTG★`, `D-SEQ★`, `D-MIN★`, `S3★-aux`, and the entire K.μ family. In ASN-0047 those starred invariants are explicitly *per-subspace*: `D-CTG★`, `D-MIN★`, `D-SEQ★` all quantify `(A d, S : V_S(d) ≠ ∅ : …)` over `S ∈ {s_C, s_L}`, and they appear in `ExtendedReachableStateInvariants`. So in the ambient model the link subspace at depth 2 *is* contiguous, has a minimum `[s_L,1]`, and is densely sequential `{[s_L,k]}` — exactly the structure needed to name cuts. The note cannot cite `D-CTG★` as a preserved invariant while simultaneously asserting `s_L` "lacks" contiguity and "does not admit cut-naming."

**Required**: Reconcile the model and give the correct reason for the text-only scope. The genuine grounds are that (a) REARRANGE_K (ASN-0084) is *defined* only for `S = 1` (CutSequence CS3, and the postconditions reference `V_S(d)` with `S = s_C`), and (b) rearranging the link subspace would interact with CL-UNIQ / CL-OWN (ASN-0047), not with any absence of contiguity. Either drop the false "s_L is exempt from contiguity" premise, or state plainly that the note works strictly in ASN-0036+0043 and then do not cite ASN-0047's starred per-subspace results.

### Issue 2: The P7a claim-table phrase overstates fragmentation

**ASN-0119, Claims Introduced, P7a row**: "a link's V-footprint is relocated through `π`; footprints split by a cut become discontiguous span-sets."

**Problem**: As a general consequence this is contradicted by the note's own worked pivot. The `{B, E} = {a₂, a₅}` footprint straddles the cut `c₁` (B in α, E in β) yet `π` carries it from the *discontiguous* `{ord 2, ord 5}` to the *contiguous* `{ord 4, ord 5}` — contiguity is *gained*, not lost. The prose later states the correct, precise condition ("a single contiguous endset becoming discontiguous occurs exactly when a single pre-run straddles a cut"), but the summary row reads as a universal claim that the example refutes.

**Required**: Make the table row match the prose — fragmentation occurs precisely when a *single contiguous run* straddles a cut; a footprint merely "split by a cut" may become more, less, or equally contiguous.

## OUT_OF_SCOPE

None. The Open Questions are appropriately deferred (transclusion-shared cuts, concurrent rearrangements, content-index invariants under fragmentation, prior-arrangement recovery, subspace-boundary preservation, V-extent boundary cuts), and none are wrongly converted into claims here.

VERDICT: REVISE
