## Objective

Materialize the missing second-ring artifacts implied by the knowledge-engine close-out pack, using archived thread artifacts where possible and explicit placeholders only where the thread never drafted substantive content.

## Steps

1. Audit missing second-ring files against the recreated knowledge-engine repo.
2. Extend `scripts/materialize_thread_outputs.py` so second-ring outputs are reproducible.
3. Regenerate the materialized outputs and manifests in-place.
4. Add regression coverage for the new second-ring layer.
5. Run validation and summarize what is substantive versus placeholder.
