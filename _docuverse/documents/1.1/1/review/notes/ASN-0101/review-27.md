# Review of ASN-0101

## REVISE

### Issue 1: History-length argument mixes atomic and named-operation counting conventions

**ASN-0101, "The operation" (obstacle-1 paragraph)**: "Applied to a starting history of length `n + 1` ... the two-step composite `K.μ~`-then-`K.μ⁻` yields a post-composite history of length `n + 3` (indices `0, ..., n + 2`, with `Σ_{n+1} = Σ_mid` and `Σ_{n+2} = Σ_post`). DEL as a single elementary transition yields a post-DELETE history of length `n + 2` ... The post-transition history lengths differ by exactly one ... This length difference ... is the load-bearing formal property, derived entirely from the foundation's state-space semantics under SequentialAtomicTransitions."

**Problem**: The argument explicitly invokes SequentialAtomicTransitions, whose semantics counts histories as sequences of *elementary* transitions ("each obtained from its predecessor by a single elementary transition"). But ASN-0047 defines K.μ~ as a **named composite** of `K.μ⁻ + K.μ⁺` that "is not atomic; it may appear in the sequence as shorthand for its K.μ⁻ + K.μ⁺ decomposition." Under the elementary-transition semantics the argument cites, "K.μ~-then-K.μ⁻" expands to three elementary transitions (`K.μ⁻, K.μ⁺, K.μ⁻`), giving a post-composite history of length `n + 4` and a difference of **two**, not one. The assignment `Σ_{n+1} = Σ_mid` treats K.μ~ as producing a single state increment, contradicting the foundation's own definition. The "differ by exactly one" / "one entry shorter" claim — repeated and elevated to "the load-bearing formal property" — holds only under named-operation counting, which is incompatible with the SequentialAtomicTransitions apparatus the proof rests on.

**Required**: Either (a) count at elementary granularity consistently, expanding K.μ~ to its two atomic steps (post-composite length `n + 4`, difference two), and revise every "exactly one"/"one entry shorter" statement accordingly; or (b) reframe the argument at named-operation granularity without invoking SequentialAtomicTransitions' elementary-transition semantics as the source of the property. The qualitative conclusion (composite produces a strictly longer history) survives either way, but the specific quantitative claim must be made consistent with the counting convention actually in force.

### Issue 2: D8 discharge of S8★ does not establish condition (c) on the content subspace

**ASN-0101, D8 Group (i) justification**: "S8★ holds at the post-state by the trivial singleton decomposition `{(v, M'(d)(v), 1) : v ∈ V_S(M'(d))}` for the affected subspace — S8-fin establishes finiteness, S8's condition (a) holds by construction ... and condition (b) holds trivially..."

**Problem**: ASN-0047's S8★ retains condition (c) — uniqueness of the *maximal-run* decomposition — on the content subspace. The discharge explicitly establishes only conditions (a) and (b) via the singleton decomposition. The singleton decomposition is in general *not* the maximal-run decomposition, so it cannot witness condition (c). The follow-up prose ("M11 supplies a coarser canonical decomposition ...; if it does not, the singleton decomposition remains the available witness") concerns *existence* of a satisfying decomposition, not the *uniqueness* that (c) demands. Condition (c) is in fact satisfied — `M'(d)|_{V_{s_C}}` is a function (S2, established in D8) and finite (S8-fin), so M12 (CanonicalUniqueness) gives a unique maximal-run decomposition — but the proof never makes this argument; it conflates witness-existence with uniqueness.

**Required**: For the content subspace, invoke M12 on the post-state arrangement function to discharge condition (c) explicitly (post-state functionality + finiteness ⇒ unique maximal-run decomposition), separate from the singleton-decomposition argument that handles (a) and (b).

## OUT_OF_SCOPE

None. The ASN confines itself to the DELETE operation; the recoverability and versioning material is explicitly deferred ("a multi-step composite mechanism outside DEL's scope") rather than specified here, and no claims are defined for the excluded operations.

VERDICT: REVISE
