# Channels

Top-level plugin registry. Each subdirectory is a self-contained channel plugin:

```
channels/<channel-name>/
├── meta.yaml          # identity + optional channel-specific metadata
├── resources/         # source content (files, submodules, etc.)
└── consultations/
    ├── consult.py     # plugin entry point exposing generate_questions(), consult()
    └── *.md           # channel-specific consultation prompt templates
```

Campaigns reference channels by name from `lattices/<L>/campaigns/<C>/config.yaml`.
The orchestrator loads `channels/<name>/consultations/consult.py` via
`scripts/lib/consultation/consult.py::load_channel_plugin(name)`.

Channels with shared consultation shapes import factories from
`scripts/lib/consultation/patterns.py` (currently `flat_corpus`). Channels with
unique shapes hand-roll their `consult.py`.
