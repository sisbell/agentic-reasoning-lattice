**S8-depth (FixedDepthVPositions).** Within a given subspace `s` of document `d`, all V-positions share the same tumbler depth:

`(A d, v₁, v₂ : v₁ ∈ dom(Σ.M(d)) ∧ v₂ ∈ dom(Σ.M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)`

This is a design requirement, not a convention — parallel to S7a. Gregory's evidence supports it: V-addresses in the text subspace consistently use the form `s.x` — two tumbler digits, where `s` is the subspace identifier and `x` is the ordinal. The two-blade knife computation (which sets the second blade at `(N+1).1` for any insertion at `N.x`) works only if all positions within a subspace share the same depth. Any correct implementation must satisfy this constraint.

S8-depth allows us to define "consecutive V-positions" precisely — see S8-depth(a) (ConsecutiveVPositions). A parallel uniformity holds for I-addresses within a correspondence run: all I-addresses share the same tumbler depth and prefix, differing only at the element ordinal — see S8-depth-C1 (IAddressRunUniformity). We introduce notation for ordinal displacement at S8-depth(b) (OrdinalDisplacementExtension) and write `v + k` for ordinal displacement applied to V-positions and `a + k` for the same applied to the element ordinal of I-addresses.

(Why non-trivial runs arise in practice is a separate question. Allocator discipline — T10a, ASN-0034 — establishes that each allocator produces sibling outputs exclusively by `inc(·, 0)`, and TA5(c) guarantees the successor has the same depth as the predecessor. Consecutive allocations therefore produce consecutive I-addresses, which is why sequential content creation naturally yields correspondence runs of length greater than one. But this operational fact is motivation for the definition of correspondence runs, not a dependency of the decomposition proof.)

A *correspondence run* formalises the notion of a contiguous block where arrangement preserves ordinal displacement — see S8-depth(c) (CorrespondenceRun).
