# ALIMIND CITY SIGNAL — PROJECT BASELINE V1

## Date
2026-05-19

## Status
BASELINE LOCKED

## Current module
Earthquake Signal Pipeline

## Working chain

source_registry
→ fetch
→ fallback
→ raw storage
→ parser
→ region filter
→ normalizer
→ dedup
→ message render
→ pipeline runner
→ status persistence
→ status view

## Completed modules

- SOURCE_REGISTRY_V1
- FETCH_CORE_V1
- FALLBACK_USGS_V1
- USGS_PARSER_V1
- USGS_REGION_FILTER_V1
- SIGNAL_NORMALIZER_V1
- DEDUP_V1
- SIGNAL_MESSAGE_RENDER_V1
- PIPELINE_RUNNER_V1
- PIPELINE_STATUS_V1
- PIPELINE_STATUS_INTEGRATION_V1
- STATUS_VIEW_V1

## Current behavior

KOERI is the primary source.

If KOERI fails:
system falls back to USGS.

Latest verified behavior:
- KOERI timeout handled
- USGS fallback worked
- raw saved
- events parsed
- region filter applied
- no relevant Alanya event found
- pipeline finished without crash
- status saved to app/data/system/pipeline_status.json

## Core invariants

- Raw data must be saved before parsing
- Parser must not publish directly
- Normalize before publish
- Dedup before publish
- Source failure must not crash the system
- Status must be saved after each pipeline run
- No Telegram publishing before preview/test layer
- No new signal modules before current baseline is stable

## Current file structure

app/
├── core/
│   ├── dedup.py
│   ├── fetcher.py
│   ├── pipeline_status.py
│   ├── source_registry.py
│   └── status_view.py
│
├── data/
│   ├── raw/
│   ├── sources/
│   │   └── source_registry.json
│   └── system/
│       ├── pipeline_status.json
│       └── published_signals.json
│
└── modules/
    └── city_signals/
        └── earthquake/
            ├── filter_region.py
            ├── message_render.py
            ├── normalizer.py
            ├── pipeline_runner.py
            ├── usgs_parser.py
            └── test files

## Next allowed module

SCHEDULER_LOOP_V1

## Not allowed yet

- Telegram publish
- VPS deploy
- Water module
- Sea module
- Electricity module
- News module
- AI text generation layer