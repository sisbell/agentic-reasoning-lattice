# Campaigns: Multi-Pairing Lattices

*Design note. Established 2026-04-21. Realizes the previously-abstract "campaign" level of the [six-level vocabulary hierarchy](../glossary.md) (Domain → Lattice → Campaign → Inquiry → Note → Claim) as a first-class artifact in the system.*

## What a campaign is

A **campaign** is a coordinated effort of inquiries against a target, sharing a channel pairing and a curated bridge vocabulary. It is the concrete realization of the following structure:

```
campaign = (theory channel, evidence channel, bridge vocabulary, target)
```

- **Theory channel** — the corpus the theory consultation agent reads.
- **Evidence channel** — the corpus the evidence consultation agent reads.
- **Bridge vocabulary** — unified names letting an ASN cite both authorities coherently despite the two corpora naming the same concepts differently.
- **Target** — a prose description of what the campaign is trying to discover or validate.

Each ASN binds to exactly one campaign via its manifest's `campaign:` field (or inherits the lattice's `default_campaign`). One lattice can hold many campaigns; campaigns share the lattice's addressable substrate, and ASNs across campaigns can cite each other as foundations.

## Why campaigns became first-class

The documented hierarchy (Domain → Lattice → Campaign → Inquiry → Note → Claim) had Campaign as an abstract level with no filesystem realization. Initially every lattice had exactly one (theory, evidence) pair baked into the domain configuration, so "campaign" reduced to "lattice" — no handle was needed.

This broke the moment a lattice needed to support more than one pairing:
- **Different sub-domain** — new theory + new evidence pair for a different area (e.g., electromagnetism after heat).
- **Stress-test a theory** — same theory + different evidence (Maxwell 1867 against Regnault's gas data instead of DP's solid data).
- **Framework comparison** — different theory + same evidence (Clausius 1857 vs. Maxwell 1867 on DP).

All three are legitimate research moves. None was expressible with a single domain-level pair. Campaigns are the container that holds each such pairing as a separate coherent unit while preserving the shared-lattice property.

## Why vocabulary lives at the campaign level

This is the central architectural commitment.

**Vocabulary is a bridge between two specific authorities.** Maxwell bridges to DP differently than Clausius bridges to DP. Maxwell bridges to Regnault differently than Maxwell bridges to DP. A vocabulary without a specific pairing has no referents.

The vocabulary's **primary user is the reviewer**, not the drafter. The drafter synthesizes from two channel-local consultation outputs; the reviewer has to interpret the resulting claims against *both* authorities — that is where the bridge pays off. The `{{vocabulary}}` placeholder in `review.md` is the load-bearing integration point.

Vocabulary is **curated upfront** when a new campaign is created (not emergent from synthesis). Prose-coinage during ASN writing adds at the margin, but the backbone — the core bridge terms — is authored in advance by reading both corpora and coining unified names.

## Why pairing collapsed into campaign

One might naturally distinguish "pairing" (mechanism: two channels) from "campaign" (pairing + target + inquiries). The distinction doesn't survive scrutiny: a pairing without a target or inquiries is inert, and a campaign without a pairing is meaningless. They are the same concept, and introducing both names was a second source of truth for one structure.

The collapsed form: a campaign *is* (pair, target, vocabulary, inquiries). No separate pairing entity in the filesystem.

## Filesystem layout

```
lattices/<lattice>/
├── config.yaml                              # default_campaign
├── campaigns/
│   └── <campaign-name>/
│       ├── config.yaml                      # theory, evidence, target
│       └── vocabulary.md                    # bridge vocab, curated upfront
└── manifests/
    └── ASN-NNNN/note.yaml                   # optional: campaign: <name>

channels/                                    # top-level plugin registry (cross-lattice)
└── <channel-name>/
    ├── meta.yaml                             # identity + channel-specific config
    ├── resources/                            # source material (corpus, submodules, KBs, etc.)
    └── consultations/
        ├── consult.py                        # plugin exposing generate_questions(), consult()
        └── *.md                              # channel-specific consultation prompt templates
```

Each ASN's campaign context is resolved at stage invocation: the ASN's manifest is read, the bound campaign is identified (or inherited from the lattice default), and its channels, vocabulary, and target are loaded. All discovery-stage scripts read vocabulary and corpora through this resolution step — there is no direct access to channel content bypassing the campaign.

## What campaigns do not enforce

- **Cross-campaign dependency typing.** Any ASN can depend on any foundation ASN in the lattice. Nothing prevents a Clausius-campaign ASN from depending on a Maxwell-campaign ASN — even if the dependency would be framework-confused. The **reviewer** catches such miscitations the same way it catches regime mismatches and smuggled premises.
- **Vocabulary coherence across campaigns that share a channel.** Two campaigns using the same theory channel may coin different unified names for the same theory term. This is a social convention — when creating a new campaign that shares a theory channel with an existing campaign, start by copying the shared-theory-side terms from the existing campaign's vocab. No code enforcement.
- **Framework-comparison relationships.** When two campaigns produce competing accounts of the same phenomenon, the current `depends`-only lattice cannot express "compares-to." The comparison lives in prose and in the reviewer's judgment. A richer relationship type may be added later, driven by when the first framework-comparison ASN surfaces the need.

## Extraction of shared foundations

The most important structural dynamic in multi-campaign lattices is that **duplication between independently-drafted ASNs is a discovery signal**, not a cleanup problem.

Two ASNs in different campaigns often need to state the same underlying commitments — the observational or structural claims that any framework addressing the domain must make (e.g., when two theoretical frameworks examine the same empirical regime, both will independently articulate commitments like transitivity, well-definedness, and additivity of the observable quantities). Rather than pre-splitting an existing ASN to extract its shared layer, we let both ASNs independently articulate their commitments, then:

1. The reviewer flags the duplication across the two ASNs.
2. The shared claims are extracted into a new foundation ASN both campaigns depend on.
3. The extracted foundation contains exactly what both needed — no more, no less.

The extraction is better informed by two concrete ASNs than by any pre-planned split. Splitting after a second ASN exists is pattern-matching against real content rather than guessing at the boundary in advance. Shared foundations emerge from the process; the architecture makes space for them without predicting them.

## Related

- [Channel asymmetry](../patterns/channel-asymmetry.md) — the pattern the channels realize.
- [Discovery guide](../guides/discovery.md) — practical manifest schema and campaign-binding reference.
