# Repository layout

Top-level directories and what they hold:

- **`scripts/`** — pipeline engine (domain-neutral). `scripts/consult.py` is the ad-hoc consultation CLI; `scripts/discovery-*.py` are stage entrypoints; `scripts/lib/` holds shared infrastructure (campaign resolver, plugin loader, consultation patterns, pipeline orchestrators).
- **`channels/`** — channel plugin registry. Each channel is a self-contained directory: `meta.yaml`, `resources/` (source content), `consultations/` (channel-specific prompts + `consult.py` exposing `generate_questions()` and `consult()`). Campaigns reference channels by bare name.
- **`prompts/`** — pipeline-stage prompt templates. `prompts/shared/` holds cross-lattice defaults; `prompts/<lattice>/` holds lattice-specific overrides. The resolver (`scripts/lib/shared/paths.py::prompt_path`) prefers lattice override, falls through to shared.
- **`lattices/`** — per-lattice accumulated state. `lattices/<L>/config.yaml` declares the default campaign; `lattices/<L>/campaigns/` holds per-campaign configs and bridge vocabularies; `lattices/<L>/{discovery,blueprinting,formalization,verification,manifests}/` hold pipeline-stage outputs. **Nothing executable or configurable lives here** — agents browsing the lattice see state only (firewall).
- **`docs/`** — architecture, design notes, and guides.

## Firewall

Agents doing work on a note (ASN) are pointed at `lattices/<L>/` and may browse freely there. To prevent agents from reading their own instructions or bypassing consultation, **prompts and channel sources live outside `lattices/<L>/`**. The pipeline loads prompts and dispatches channel consultations from outside the lattice; agents see rendered prompts as input but not as files they can inspect.

## Key abstractions

- **Campaign** (`lattices/<L>/campaigns/<name>/config.yaml`): binds (theory channel, evidence channel, target). Each ASN inherits the lattice default or declares `campaign:` in its manifest.
- **Channel** (`channels/<name>/`): self-contained plugin. Its `consult.py` exposes `generate_questions(inquiry, n, model, out_of_scope)` and `consult(question, label, model, effort, **extra)`. Channels with a shared shape use a pattern factory (currently `flat_corpus` in `scripts/lib/consult_patterns.py`); channels with unique shapes write `consult.py` from scratch.
- **Resolver**: `scripts/lib/shared/campaign.py::resolve_campaign(asn_id)` returns `CampaignContext(name, theory_channel, evidence_channel, target, vocabulary_path)`. `scripts/lib/consult.py::load_channel_plugin(name)` loads a channel's plugin module.
