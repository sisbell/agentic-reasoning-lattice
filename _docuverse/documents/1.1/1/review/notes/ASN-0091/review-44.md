# Review of ASN-0091

## REVISE

### Issue 1: Wrong directional cross-reference to the Interior Cuts worked example

**ASN-0091, "In-Subspace Exterior Frame (REARRANGE_K-specific)"**: "RE-ext is exercised concretely in the third Worked Example ("Interior Cuts (R-EXT Exercised)") **above**, where in-subspace exterior positions [1, 1] and [1, 5] are pointwise preserved..."

**Problem**: The "Interior Cuts" worked example appears *after* (below) the In-Subspace Exterior Frame section, not above it. The directional pointer is reversed. This is exactly the kind of forward/backward-reference rot the precise reader trips on.

**Required**: Change "above" to "below," or remove the cross-reference entirely. Note also that both RE-sub and RE-ext defer to downstream worked examples to do their illustrating — consider whether the deferral pointers earn their place at all.

### Issue 2: Defensive/justificatory meta-prose around the abstract-class definition

**ASN-0091, "REARRANGE as Vstream-Only Operation"**: e.g. "RA-reg names `d` as a registered document at Σ — without it, `Σ.M(d)` would be undefined and every subsequent clause of the definition would lack a referent"; "RA-π's signature ... is type-correct without presupposing any equality of these two domains — it asserts only that π is a bijection between two sets"; and the parenthetical "(The notation `Σ.M(d)⁻¹(a)` ... are the set-valued pre-images ... not π's inverse, which is a permutation ... and would type-mismatch as an argument to an I-address.)"

**Problem**: These passages explain *why each clause is needed* and *what the notation does not mean*, rather than advancing the definition's content. They are noise the reader must skip past to reach the actual claims. The `review-mode.anti-bloat` classifier targets exactly this: prose around a definitional clause that justifies the clause instead of stating it.

**Required**: State RA-reg, RA-π, RA-frame as clauses and let the formal statements carry their own type-correctness. Delete the "without it X would be undefined," "type-correct without presupposing," and type-mismatch-warning asides.

### Issue 3: Over-complete characterization of the collapse case

**ASN-0091, "REARRANGE as Vstream-Only Operation"**: the multi-paragraph analysis deriving that the affected-range value sequence is fixed "iff `x` is fixed by this reindexing," with the pivot case "`x` periodic with period `gcd(w_α, w_α + w_β)` (= `gcd(w_α, w_β)`)" and the swap case "the α- and β-blocks are positionally equal ... forces `w_α = w_β` ...".

**Problem**: The realization argument needs only that REARRANGE_K admits a degenerate no-op with π ≠ id (so K.μ~'s clause (ii) can fail). A single witness — the period-2 example already given — discharges that. The full gcd/block-cycle characterization of *exactly which* invocations collapse exceeds what any downstream claim consumes; it is essay-grade mathematical completeness in service of an existence claim.

**Required**: Reduce to the existence witness plus the one-line consequence (collapse ⇒ Σ'=Σ ⇒ K.μ~ clause (ii) fails ⇒ identity composite is the realiser). Drop the period/gcd and α=β-block characterization unless a later claim actually uses it (none does).

### Issue 4: Proof-organization meta-prose presented as a section

**ASN-0091, "ASN-0036 S3/S8 Supersession and the Move to Per-Invariant Discharges"**: the subsection narrates why discharges are done per-invariant rather than as a whole package, e.g. "any ASN-0084 lemma whose hypothesis requires pre-state S3 or S8 lacks a valid hypothesis at a unified-state pre-state with a populated link subspace ... The replacements S3★ and S8★ are discharged in the ... subsection below."

**Problem**: This advances no reasoning about REARRANGE — it explains the document's own bookkeeping and defers to a downstream subsection. It is structural rationale, not content.

**Required**: Fold the single load-bearing fact (S3/S8 superseded by S3★/S8★; the latter are discharged below) into the discharge subsection's opening sentence and delete the standalone narration.

### Issue 5: Dependency-audit paragraph belongs in inquiry metadata, not the ASN body

**ASN-0091, "Claims Introduced"**: "*Dependency audit.* Of the inquiry's declared dependencies — ASN-0034, 0036, ... — every one is invoked above by explicit citation except span-algebra ASN-0053 ... ASN-0053 is therefore flagged as a candidate for removal from the inquiry's `depends:` set."

**Problem**: This is a use-site inventory of the inquiry's `depends:` field — process/metadata bookkeeping, not a system guarantee about rearrangement. The classifier flags exactly this pattern (enumerating which dependencies are/aren't consumed).

**Required**: Move the ASN-0053-removal observation to the inquiry's metadata or a PR note; remove the audit paragraph from the ASN body.

### Issue 6: Redundant full-admissibility recitation across five worked examples

**ASN-0091, the five "Worked Example" sections**: each re-verifies the foundation-invariant package (S2, S3★, S8★, D-CTG★, D-MIN★, D-SEQ★, S3★-aux, CL-OWN, CL-UNIQ, P4★, P4a, the state-component-only set). The later ones say "discharge exactly as in the first Worked Example" yet still enumerate the list.

**Problem**: One worked example satisfies the mandatory-concrete-example standard; the distinct phenomena (4-cut swap, RE-ext, bijection non-uniqueness, two-step composition) justify additional *traces*, but re-reciting the identical admissibility package in each is duplication ("two paragraphs say the same thing in different words," repeated five times).

**Required**: In the first worked example, verify the full package once. In the later examples, verify only the clauses whose witness genuinely differs (e.g. S8★'s run decomposition, P4★'s pair set, S5 in the sharing example) and state the rest as inherited by one sentence — which several already attempt but then undercut by re-enumerating.

## OUT_OF_SCOPE

### Topic 1: Link-subspace rearrangement semantics
The ASN fixes the cut subspace at S = s_C (CS3), so REARRANGE_K never reorders the link subspace. What an analogous link-subspace reordering operation would be and what it must preserve is correctly deferred to an Open Question — a future ASN, not a gap here.

### Topic 2: Upper bound on run-decomposition cardinality growth
RE-frag establishes that fragmentation is possible and the multi-step section shows per-step direction is arbitrary; a tight bound on cardinality increase per invocation is genuinely new territory (listed as an Open Question), not an error in this ASN.

VERDICT: REVISE
