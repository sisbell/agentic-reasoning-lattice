# Guide: Discovery

*Practical reference for the note manifest schema and campaign binding.*

## Note manifest (`note.yaml`)

Every ASN has a manifest at `lattices/<lattice>/manifests/ASN-NNNN/note.yaml` describing the inquiry and the ASN's relationships to the rest of the lattice.

### Minimal example

```yaml
# lattices/materials/manifests/ASN-0002/note.yaml
title: "Constitution and the Nature of Heat"
stage: "discovery"
topic: "foundation"
depends: []
out_of_scope: ""
consultations:
  question: "What does the theory commit to about the constitution of bodies and the nature of heat?"
  agents:
    theory: 10
    evidence: 10
```

### Fields

- **`title`** (string, required) — human-readable title of the ASN.
- **`stage`** (string) — current pipeline stage (`discovery`, `blueprinting`, etc.).
- **`topic`** (string) — a rough subject area for the ASN. Used by listing tools.
- **`depends`** (list of ASN ids) — foundation ASNs this note builds on.
- **`out_of_scope`** (string) — semicolon-separated list of topics the ASN deliberately excludes. Passed to the reviewer and the question generator.
- **`consultations.question`** (string, required) — the inquiry the ASN answers.
- **`consultations.agents.theory`** (int) — number of theory-channel questions to decompose the inquiry into.
- **`consultations.agents.evidence`** (int) — same for evidence.
- **`campaign`** (string, optional) — the name of the campaign this ASN belongs to. If omitted, the ASN inherits the lattice's `default_campaign` from `lattices/<lattice>/config.yaml`.

### Campaign binding

A campaign binds a (theory channel, evidence channel) pair to a target and a curated bridge vocabulary. Each ASN belongs to exactly one campaign.

**Default inheritance.** An ASN with no explicit `campaign:` field inherits the lattice's default. This is the common case — most ASNs in a lattice belong to the same campaign and don't need to specify it.

```yaml
# lattices/materials/config.yaml
default_campaign: dulong-petit-maxwell
```

**Explicit binding.** An ASN in a non-default campaign specifies it in its manifest:

```yaml
title: "Heat capacity via Clausius's kinetic theory"
campaign: dulong-petit-clausius
consultations:
  question: "..."
```

The pipeline resolves the active campaign when running any discovery step on that ASN: the ASN's `campaign:` takes precedence; if absent, the lattice default applies; if neither is set, the resolver raises an error (no silent fallback).

### Campaign artifacts

Each campaign lives at `lattices/<lattice>/campaigns/<name>/` with two files:

- **`config.yaml`** — binds the campaign's channels and target:
  ```yaml
  theory: maxwell-1867
  evidence: dulong-petit-1819
  target: "Rediscover Dulong-Petit's atomic-heat regularity via Maxwell's dynamical theory of gases"
  ```
- **`vocabulary.md`** — the campaign's bridge vocabulary, curated upfront and accreted through the campaign's ASN cycle. Primary consumer is the reviewer. See [Vocabulary is pairing-level](../design-notes/campaigns.md) for the rationale.

### Channel artifacts

Channels live at `channels/<name>/` (top-level, cross-lattice registry) and are self-contained plugins:
```
channels/<name>/
├── meta.yaml                  # identity + channel-specific config
├── resources/                 # source content (files, submodules, etc.)
└── consultations/
    ├── consult.py             # plugin exposing generate_questions() and consult()
    └── *.md                   # channel-specific consultation prompts
```
The `meta.yaml` declares the channel's identity and description:
```yaml
name: maxwell-1867
role_hint: theory
description: "Maxwell's dynamical theory of gases (1867). The theory of this period."
type: single-source
```
Campaigns reference channels by bare name; the orchestrator loads `channels/<name>/consultations/consult.py` via the plugin loader at `scripts/lib/consult.py::load_channel_plugin`.

## Creating a new ASN

1. Author `lattices/<lattice>/manifests/ASN-NNNN/note.yaml` with the inquiry and (if needed) a non-default `campaign:`.
2. Run the pipeline:
   ```bash
   LATTICE=<lattice> ./run/run-discovery.sh NNNN
   ```

The pipeline resolves the ASN's campaign at every stage (draft, review, revise, consult), loading the campaign's bridge vocabulary and the bound channels' corpora.

## Creating a new campaign

See [the `new-campaign` helper](../../scripts/new-campaign.py) when implemented. Manually:

1. Ensure the theory and evidence channel plugins exist at `channels/<name>/` (meta.yaml, resources/, consultations/ with consult.py + prompts).
2. Create `lattices/<lattice>/campaigns/<name>/config.yaml` with the channel bindings and target.
3. Curate `lattices/<lattice>/campaigns/<name>/vocabulary.md` by reading both corpora and coining unified names for terms the authorities name differently.
4. Author an ASN with `campaign: <name>` in its manifest and run the pipeline.
