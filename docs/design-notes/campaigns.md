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

This is the central architectural commitment. See memory: `project_vocabulary_is_pairing_level.md`.

**Vocabulary is a bridge between two specific authorities.** Maxwell bridges to DP differently than Clausius bridges to DP. Maxwell bridges to Regnault differently than Maxwell bridges to DP. A vocabulary without a specific pairing has no referents.

Xanadu's existing `lattices/xanadu/vocabulary.md` looks lattice-wide only because xanadu happens to have one pairing (nelson × gregory). Under the campaign model it is correctly understood as "the nelson+gregory campaign's bridge vocab."

The vocabulary's **primary user is the reviewer**, not the drafter. The drafter synthesizes from two channel-local consultation outputs; the reviewer has to interpret the resulting claims against *both* authorities — that is where the bridge pays off. The `{{vocabulary}}` placeholder in `review.md` is the load-bearing integration point.

Vocabulary is **curated upfront** when a new campaign is created (not emergent from synthesis). Prose-coinage during ASN writing adds at the margin, but the backbone — the core bridge terms — is authored in advance by reading both corpora and coining unified names.

## Why pairing collapsed into campaign

Initial design distinguished "pairing" (mechanism: two channels) from "campaign" (pairing + target + inquiries). External design review pushed back: a pairing without a target or inquiries is inert, and a campaign without a pairing is meaningless. They are the same concept. Two names for one thing was the pattern the broader refactor has been systematically eliminating.

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

domains/<lattice>/channels/
└── <channel-name>/
    ├── corpus*.md                            # source material
    └── meta.yaml                             # description, type
```

Each ASN's campaign context is resolved at pipeline invocation via `scripts/lib/shared/campaign.py::resolve_campaign(asn_id)`, which returns the channel names, vocabulary path, and target. All discovery-stage scripts read vocabulary and corpora through this resolver.

## What campaigns do not enforce

- **Cross-campaign dependency typing.** Any ASN can depend on any foundation ASN in the lattice. Nothing prevents a Clausius-campaign ASN from depending on a Maxwell-campaign ASN — even if the dependency would be framework-confused. The **reviewer** catches such miscitations the same way it catches regime mismatches and smuggled premises.
- **Vocabulary coherence across campaigns that share a channel.** Two campaigns using the same theory channel may coin different unified names for the same theory term. This is a social convention — when creating a new campaign that shares a theory channel with an existing campaign, start by copying the shared-theory-side terms from the existing campaign's vocab. No code enforcement.
- **Framework-comparison relationships.** When two campaigns produce competing accounts of the same phenomenon, the current `depends`-only lattice cannot express "compares-to." The comparison lives in prose and in the reviewer's judgment. A richer relationship type may be added later, driven by when the first framework-comparison ASN surfaces the need.

## Extraction of shared foundations

The most important structural dynamic in multi-campaign lattices is that **duplication between independently-drafted ASNs is a discovery signal**, not a cleanup problem. See memory: `project_duplication_is_discovery_signal.md`.

Two ASNs in different campaigns (e.g., Maxwell+DP and Clausius+DP) will both need to state the observational commitments their framework rests on (temperature transitivity, heat-flow direction, specific-heat well-definedness). Rather than pre-splitting ASN-0002 to extract its observational layer, we let both ASNs independently articulate their observational commitments, then:

1. The reviewer flags the duplication across the two ASNs.
2. The shared claims are extracted into a new foundation ASN both campaigns depend on.
3. The extracted foundation contains exactly what both needed — no more, no less.

The extraction is better informed by two concrete ASNs than by any pre-planned split. "Splitting after the second ASN exists is pattern-matching against real content." Shared foundations emerge from the process; the architecture makes space for them without predicting them.

## Migration status

- **Materials** — adopted campaign architecture (this refactor, 2026-04-21). One campaign so far: `dulong-petit-maxwell`.
- **Xanadu** — not migrated. Deferred as a separate effort because xanadu's prompts have byte-identity constraints and its ASN count (60+) makes migration delicate. When xanadu migrates, its current lattice becomes a single-campaign lattice (`campaigns/xanadu-docuverse/` with channels = `nelson-design-corpus`, `udanax-harness`). No ASN-manifest edits needed — lattice default inheritance covers them all.

## CLI

No user-facing flag. The campaign is resolved from the ASN's manifest (or lattice default) at pipeline invocation. Users create new campaigns by scaffolding the directory structure (or using the `new-campaign` helper), author ASNs with `campaign: <name>` if non-default, and run the pipeline as usual:

```bash
LATTICE=materials ./run/run-discovery.sh 2
```

## Related

- [Vocabulary is pairing-level](project_vocabulary_is_pairing_level memory) — the load-bearing architectural commitment.
- [Duplication is a discovery signal](project_duplication_is_discovery_signal memory) — how shared foundations emerge.
- [Channel asymmetry](../patterns/channel-asymmetry.md) — the pattern the channels realize.
- [Discovery guide](../guides/discovery.md) — practical manifest schema and campaign-binding reference.
