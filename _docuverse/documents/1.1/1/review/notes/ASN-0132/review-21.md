# Review of ASN-0132

I checked the rigor first, and it holds. CN-DEF's well-definedness (finite/computable subset of `dom(Σ.L)`), CN-LOC's `Σ.L`-locality, CN-UNIT's four-case reduction (including the J4-based version-refraction argument — I verified J4's components K.δ/K.μ⁺/K.ρ all frame `L' = L`), CN-MONO's two-case wp derivation (ordinary vs. retraction, multi-step `≤` grounded in FL-MON), and the worked example all check out arithmetically. The example correctly exercises CN-RETRACT (`a₂`), CN-ORPHAN (`a₃`), both zero kinds (`q_H'` genuine vs. FL-EMP degenerate), and the census-in-motion realizes the very case CN-MONO's hypothesis excludes (step 3, net −1). No rigor or boundary-case errors found.

The REVISE items below are narrow prose-economy findings, surfaced under the note's `review-mode.anti-bloat` mandate. They do not touch correctness.

## REVISE

### Issue 1: The independence-from-enumeration point is stated twice
**ASN-0132, "The satisfying set is already named" and "One description, two views" (CN-ENUM)**:
- Framing: *"We will count by consulting this relation directly, never by appeal to the operation that enumerates."*
- CN-ENUM: *"Neither mentions the other; both bottom out at sat. The four-set matching criterion lives once, in sat; each operation is a query over it..."*

**Problem**: The framing section's load-bearing job is to establish that `sat` and `addressable` are *reused* from the foundation (anti-reinvention). The appended clause "never by appeal to the operation that enumerates" previews the count/enumeration independence that CN-ENUM then fully delivers. The two passages say the same thing in different words — a reader who reaches CN-ENUM gains nothing new from the earlier preview.

**Required**: Trim the framing passage to its substantive content (sat and addressable come from ASN-0121); let CN-ENUM carry the "both bottom out at sat, neither appeals to the other" point once.

### Issue 2: Defensive well-definedness prose and a forward-duplicated cost parenthetical
**ASN-0132, "The satisfying set is already named" (well-definedness paragraph)**: *"There is no loop to terminate and no bound function to exhibit: the count is the cardinality of a finite comprehension, not the result of a search that might run away. (That a particular back end realises the cardinality by a search that does run over the store is a matter of cost, and does not bear on what the number is.)"*

**Problem**: The finiteness/computability argument (subset of finite `dom(Σ.L)`, decidable per FL-DEC) is complete and correct on its own. The sentence about "no loop to terminate, no bound function" is a defensive justification pre-empting a termination concern that does not arise for a set cardinality — it answers a question the claim does not raise. The parenthetical's value/cost distinction is then restated at the close ("the specification is silent: cost-asymmetry is a quality of service... not a correctness obligation" / "That same realisation ... pays full enumeration cost"). The same value-vs-cost point is thus made in two places.

**Required**: Drop the "no loop / no bound function" sentence; the finiteness argument stands without it. Fold the cost parenthetical into the single closing cost discussion rather than anticipating it inside the well-definedness proof.

## OUT_OF_SCOPE

(none — the ASN properly defers delivery/retrieval to CN-OBT, and concurrency, caching, fragmentation-dedup, federation, and content-identity/position reconciliation to the Open Questions, without making claims in those areas.)

VERDICT: REVISE
