# Review of ASN-0042

## REVISE

### Issue 1: O14 prose contradicts formal clause and multi-node example
**ASN-0042, O14 (BootstrapPrincipal)**: "The initial state contains at least one principal whose domain covers all initially allocated addresses..."
**Problem**: The prose naturally reads as "there exists a single principal P such that P's domain ⊇ Σ₀.B" — the strong reading. The formal clause `(A a ∈ Σ₀.B : (E π ∈ Π₀ : pfx(π) ≼ a))` is the weak reading: each address is covered by some principal, possibly different principals for different addresses. The multi-node example later in O14 ("In a multi-node system, Π₀ contains one initial principal per node ... each independently covering its node's allocatable addresses") explicitly requires the weak reading — neither π_N (prefix [1]) nor π_M (prefix [2]) alone covers all addresses, but together they cover both nodes. The strong prose reading would exclude multi-node bootstrap.
**Required**: Rewrite the prose to "every initially allocated address is covered by at least one principal" so it matches the formal clause and the multi-node example.

### Issue 2: AccountLevelPermanence is formally single-step despite multi-step intent
**ASN-0042, AccountLevelPermanence**: Formal statement quantifies over `Σ → Σ'` (single step); the "Discussion (multi-step chain to π)" paragraph extends to multi-step informally.
**Problem**: Compare to O8 (IrrevocableDelegation), which uses `Σ →⁺ Σ'` (transitive closure) and proves a multi-step claim directly. The worked example traces O8 across multiple states (Σ₁, Σ₂, Σ₃) but does not similarly trace AccountLevelPermanence. The property name suggests permanence (multi-step), the prose ("no external delegation can ever alter") suggests multi-step, but the formal statement only constrains a single transition and the bootstrap-chain argument that closes to π is left informal. A reader cannot extract a formal multi-step guarantee.
**Required**: Either (a) restate AccountLevelPermanence using `Σ →⁺ Σ'` (matching O8's form) and prove multi-step directly via induction on the transition path, or (b) keep the single-step formal property and add an explicit named corollary (e.g., `AccountLevelPermanence★`) stating and formally proving the multi-step closure.

### Issue 3: Transitivity of ≼ invoked without citation
**ASN-0042, proof of O6 (StructuralProvenance) reverse direction**: "Reverse: suppose pfx(π) ≼ acct(a). By AccountPrefix, acct(a) ≼ a. By transitivity of the prefix relation, pfx(π) ≼ a."
**Problem**: The foundation's Prefix (PrefixRelation) lists only the definition, reflexivity, and the proper-prefix length consequence — transitivity is not among its exported postconditions. The proof invokes it by name without inline derivation or foundation citation. The same gap appears in step 3 of AccountLevelPermanence's proof ("Both pfx(π) and pfx(π_d) are prefixes of pfx(π')... Hence pfx(π) ≼ pfx(π_d)") and in the proof structure of FiniteRegistry's downstream consumers.
**Required**: Add a one-line inline derivation at the first invocation site (`p ≼ q ∧ q ≼ r ⟹ p ≼ r` follows from the component-wise definition: `#p ≤ #q ≤ #r` by NAT-order transitivity, and for each `i ≤ #p`, `pᵢ = qᵢ = rᵢ` chains through both prefix relations), or strengthen Prefix (PrefixRelation)'s postcondition list to include transitivity explicitly.

### Issue 4: O10 formal contract has state ambiguity for ω(a')
**ASN-0042, O10 (DenialAsFork) Postconditions**: "(E a' ∈ dom(π) : ω(a') = π ∧ a ∈ Σ.B)"
**Problem**: ω is defined only on Σ.B (precondition `a ∈ Σ.B` of O2). For `ω(a') = π` to be well-formed, a' must be in some Σ.B. The proof constructs a' as a tumbler in T (showing pfx(π) is the longest match in Π_Σ for a'), but does not state in which `Σ.B` the address a' resides. The intended interpretation — that after π baptizes a' in a successor state Σ', `a' ∈ Σ'.B` and `ω_{Σ'}(a') = π` — is implicit and discoverable only from the prose ("π may create a new address") and the worked example ("π_A creates a fork"). The authorization step (O5 + the baptism mechanism) and the construction of Σ' are not traced through the formal contract.
**Required**: Restructure the postcondition to expose the post-baptism state explicitly, for example: `(E Σ', a' : Σ → Σ' ∧ a' ∈ dom(π) ∩ Σ'.B ∧ ω_{Σ'}(a') = π ∧ a ∈ Σ'.B)`, and add a sentence in the proof noting that π's right to baptize a' is supplied by O5 since π is the most-specific covering principal for the constructed a' in Π_Σ.

### Issue 5: "since Σ is a state past bootstrap" remark is misleading
**ASN-0042, proof of AccountLevelPermanence Step 1**: "By O15, π' entered Π either through bootstrap or through delegation; since π' ∈ Π_{Σ'} ∖ Π_Σ and Σ is a state past bootstrap, the second clause of O15 applies."
**Problem**: O15's second clause applies to *any* transition Σ → Σ' that introduces new principals, including Σ₀ → Σ₁. The qualifier "Σ is a state past bootstrap" is unnecessary and may suggest the second clause excludes the first delegation transition. The simpler statement is: π' ∉ Π_Σ excludes the bootstrap clause (since Π₀ ⊆ Π_Σ by O12), leaving only the delegation clause.
**Required**: Replace the misleading qualifier with "Since π' ∉ Π_Σ and Π₀ ⊆ Π_Σ by O12, π' ∉ Π₀, so the first clause of O15 is excluded and the second clause applies."

## OUT_OF_SCOPE

[None — the seven Open Questions at the end of the ASN already enumerate the topics properly deferred to future ASNs (transfer mechanism, overlap enforcement, cross-node federation, etc.).]

VERDICT: REVISE
