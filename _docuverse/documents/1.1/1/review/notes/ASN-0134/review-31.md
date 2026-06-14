# Review of ASN-0134

The technical core is sound, and unusually careful — H2 handles the first-emission boundary, H1 correctly argues by `origin` to survive the nesting-homes case the bare ASN-0093 stack admits, W5's `P-tgt` trichotomy is exhaustive over arbitrary targets, and the §7/§8 traces are concrete and check out. I found no mathematical error in the load-bearing claims (A0–A7, H0–H3, G1, V0–V2, MIC, M1).

The problem is volume. This note carries the `review-mode.anti-bloat` classifier, and it is drowning in meta-prose, re-derivation, and verbatim refrains. The findings below are all of that kind. They are REVISE because the precise reader must repeatedly skip past restated content to follow the argument.

## REVISE

### Issue 1: A1 carries §8's read-taxonomy and repeats the behavioral-read roster
**ASN-0134, §1, A1**: A1's title content is the zero/one/many-step realization count. But A1 then runs four paragraphs ("One refinement, since §8 turns on it…"; "Two of ASN-0128's reads stand apart…"; "`stale`, though, does not inherit that status…") developing the single-index-vs-multi-read classification and the `stale` "`N + 1 ≥ 2` bounded accesses" derivation.
**Problem**: This is §8 machinery — it exists only to feed clause 4 vs clause 7 — parked in §1, so the reader traverses three pages of verdict-soundness setup before reaching A2. The `stale` derivation is then stated *again* in §8 ("`stale` is a §8 multi-read at *every* member-home count"). The full behavioral-read list (`members, is_K, targets_of, succs, chain, tip, is_in_chain, sources_to, target_of, targets_keyed, age, stale, is_filtered`; D1–D4/BH1–BH4) is spelled out at least three times (A1 ¶1, the A1/ASN-0128 connect paragraph, the A1 table row).
**Required**: State A1 as the realization count plus a one-line pointer that single-index read-atomicity is classified in §8. Move the `age`/`stale`/cross-type-join access-count analysis to V0/V2 where it is used. Enumerate the read roster once.

### Issue 2: The §4 both-miss duplicate and the I1a literal-vs-operative gap are derived three times
**ASN-0134, §4 instance (i); §9 clause 8; §9 M1(b)**: §4 derives the both-miss interleaving in full (including the I1a literal-vs-operative distinction). Clause 8 restates it ("the both-miss interleaving of §4 instance (i), where two coverage-equal `idem=⊤` emits each read a stale `A_K`, both miss…the execution being `K`-surface-emitted only literally, not operatively"). M1(b) restates it a third time: "the both-miss interleaving of §4 instance (i), **derived there in full**, has each of two coverage-equal emits read a stale global `A_K`, both miss…the execution is `K`-surface-emitted only literally, not operatively."
**Problem**: M1(b) explicitly says "derived there in full" and then re-derives it in full. Three copies of one argument.
**Required**: Derive once (§4). In clause 8 and M1(b), cite the §4 result and state only the delta (clause 8 fuses each `idem=⊤` dedup-read to its own deposit's pre-state, restoring operative `K`-surface-emittedness so I1a applies).

### Issue 3: A6 defends its own structure rather than stating it
**ASN-0134, §2, A6**: A6 spends a full paragraph on the A6/W3 non-contradiction ("One scope question the chain-contiguity members force into the open…no contradiction, only one invariant read two ways"); a sentence on "We keep both…but do not conflate them, because…"; and restates "No weaker 'boundary-only' class of property exists…there is no fourth class of obligation reserved for composite boundaries" — which already appeared as "with no class of properties reserved for the boundaries of multi-step composites."
**Problem**: These passages argue *why* the per-state/transition split is drawn and *why* A6 and W3 do not conflict — "why the structure is needed" prose — and repeat the "no boundary-only class" exhaustiveness claim. The transfer enumeration (RP-a/B2/RP-b per invariant) is load-bearing and should stay; the defense around it is not.
**Required**: State the per-state package, the transition clause, and the transfer once. One sentence settles the W3 relationship ("contiguity holds at every state of 𝔼 by reachability; W3 is the dual claim that an implementation must serialize per-home to produce such an execution"). Drop the second exhaustiveness restatement.

### Issue 4: Overlapping summary layers and verbatim refrains
**ASN-0134, "What this note commits" + "Claims Introduced" table; plus repeated phrasings**: The note carries an italic epigraph, an intro essay, a bulleted "What this note commits" that previews every claim cluster, and a "Claims Introduced" table that restates every claim — four summary layers for one claim set. Separately, the refrain "role-dual…but not scope-dual" / "role-dual to W4…but global" appears in the V2 statement, the §8 prose after V2, clause 7, and the V2 table row; and "cross-home by H1, same-home by clause 2's [own frontier / deposit] spacing" appears in §4 instance (i), clause 8, M1(b), and the M1 table row.
**Problem**: Multiple paragraphs say the same thing in different words (the exact compounding pattern the classifier warns of).
**Required**: Keep one detailed forward summary (the bullets or the table, not both). Collapse each refrain to one canonical statement and reference it from the other sites.

### Issue 5: This note's M1 collides with ASN-0093's M1
**ASN-0134, M1 (SafetyUnderMIC)**: The note reuses the foundation label `M1` for its own safety theorem while citing ASN-0093's `M1` (ArrangementMonotonicity) throughout (W0, A6, H0's dependency, G1, the table). A6 concedes: "distinct from this note's M1, SafetyUnderMIC of §9; the label collision is unfortunate, so the foundation reference is hereafter qualified as ASN-0093's M1."
**Problem**: Every occurrence of "M1" now requires a disambiguating qualifier, and the disambiguation prose recurs.
**Required**: Rename the local safety theorem (e.g., `SAFE` or `M★`) so "M1" unambiguously denotes the foundation invariant; the qualifier prose then vanishes.

## OUT_OF_SCOPE

### Topic 1: Document-address freshness under concurrency
**Why out of scope**: §1 scopes `K.σ` out of the conflict analysis and treats document-address freshness as an assumed precondition supplied by the excluded entity-allocation layer. The note acknowledges the same-`d` registration collision (reject-the-loser) but does not make it a contract clause. This is a defensible, clearly-stated boundary; provisioning fresh homes is genuinely upstream-layer territory.

### Topic 2: Batch read-atomicity, durability-as-substrate-predicate, cross-server composition
**Why out of scope**: These are correctly captured as Open Questions 5, 6, and 7. They are new territory (closing the A5 interior-prefix gap for a reader; promoting a sound verdict to a durable one; G1 across servers), not errors in this ASN. The note's deferrals to scheduler/fairness, agent bodies, BEBE, performance, and predicate cost are also correctly out of scope and introduce no claims.

(I considered META. The note is not implementation mechanics: MIC is a contract any concurrent realization must satisfy, stated abstractly with no lock/transaction/scheduler, and the Gregory references are evidence, not content. The topic — a concurrency/isolation contract over the existing operations — is legitimate spec material. The defect is prose volume, which is fixable by cutting, not termination. No META.)

VERDICT: REVISE
