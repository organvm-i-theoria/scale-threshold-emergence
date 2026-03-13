#!/usr/bin/env python3
"""
Research Pipeline Manager
=========================
Manages the R0-R6 research pipeline for scale-threshold-emergence.

Usage:
    python pipeline.py status                    # Show current status
    python pipeline.py advance <lane>          # Advance to next stage
    python pipeline.py add-reading <lane> <id> # Add reading to queue
    python pipeline.py extract-mechanism <id>  # Create mechanism extraction
    python pipeline.py update-dashboard        # Refresh dashboard
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DASHBOARD_JSON = REPO_ROOT / "research/dashboards/research_dashboard_state.json"
READING_NOTES_DIR = REPO_ROOT / "research/reading_notes"
MECHANISM_EXTRACTIONS_DIR = REPO_ROOT / "research/mechanism_extractions"

STAGES = ["R0", "R1", "R2", "R3", "R4", "R5", "R6"]
STAGE_NAMES = {
    "R0": "Orientation",
    "R1": "Source Acquisition",
    "R2": "Structured Reading",
    "R3": "Mechanism Extraction",
    "R4": "Mechanism Integration",
    "R5": "Simulation Translation",
    "R6": "Theoretical Synthesis",
}


def load_dashboard():
    with open(DASHBOARD_JSON, "r") as f:
        return json.load(f)


def save_dashboard(data):
    data["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    with open(DASHBOARD_JSON, "w") as f:
        json.dump(data, f, indent=2)


def cmd_status(args):
    data = load_dashboard()
    print("\n" + "=" * 50)
    print("RESEARCH PIPELINE STATUS")
    print("=" * 50)
    print(f"\nPhase: {data['program']['phase']}")
    print(f"Lanes: {data['program']['active_lanes']}/{data['program']['total_lanes']}")
    print("\nPipeline:")
    for stage, info in data["pipeline"].items():
        status = (
            "🔴"
            if info["status"] == "not_started"
            else "🟡"
            if info["status"] == "in_progress"
            else "✅"
        )
        print(f"  {status} {stage}: {info['name']}")
    print()


def cmd_advance(args):
    if not args:
        print("Usage: pipeline.py advance <lane_id>")
        return
    lane_id = args[0]
    data = load_dashboard()
    if lane_id not in data["lanes"]:
        print(f"Lane {lane_id} not found")
        return
    current = "R0"
    for s in STAGES:
        if data["pipeline"][s]["status"] == "in_progress":
            current = s
            break
    idx = STAGES.index(current)
    if idx < len(STAGES) - 1:
        next_stage = STAGES[idx + 1]
        data["pipeline"][current]["status"] = "completed"
        data["pipeline"][next_stage]["status"] = "in_progress"
        data["program"]["phase"] = (
            f"{next_stage}_{STAGE_NAMES[next_stage].replace(' ', '')}"
        )
        data["lanes"][lane_id]["status"] = "in_progress"
        save_dashboard(data)
        print(f"Advanced {lane_id}: {current} → {next_stage}")
    else:
        print("Already at R6")


def cmd_add_reading(args):
    if len(args) < 2:
        print("Usage: pipeline.py add-reading <lane> <reading_id>")
        return
    lane_id, reading_id = args[0], args[1]
    data = load_dashboard()
    if lane_id not in data["reading_queue"]:
        data["reading_queue"][lane_id] = []
    data["reading_queue"][lane_id].append({"id": reading_id, "status": "queued"})
    data["metrics"]["core_readings"] = data["metrics"].get("core_readings", 0) + 1
    save_dashboard(data)
    print(f"Added {reading_id} to {lane_id}")


def cmd_extract_mechanism(args):
    if not args:
        print("Usage: pipeline.py extract-mechanism <mechanism_id>")
        return
    mech_id = args[0]
    data = load_dashboard()
    timestamp = datetime.now().strftime("%Y%m%d")
    filename = f"MECH-{mech_id}_{timestamp}.md"
    filepath = MECHANISM_EXTRACTIONS_DIR / filename
    content = f"""---
id: MECH-{mech_id}
title: Mechanism Extraction {mech_id}
type: mechanism-extraction
status: candidate
created: {datetime.now().strftime("%Y-%m-%d")}
---

# Mechanism Extraction: {mech_id}

## Source Reading
- ID: 
- Title: 
- Author: 

## Mechanism Description
### What is the mechanism?
/

### How does it work?
/

### Why is it significant?
/

## Evidence
### Primary Evidence
/

### Supporting Evidence
/

## Primitive Mappings
| Primitive | Role |
|-----------|------|
| | |

## Module Relevance
### Potential Applications
/
### Parameters
/

## Cross-Lane Relevance
- R2-01: 
- R2-02: 
- R2-03: 

## Status History
| Date | Status | Notes |
|------|--------|-------|
| {datetime.now().strftime("%Y-%m-%d")} | candidate | Initial extraction |

## Review Notes
### Reviewer 1
/
### Reviewer 2
/

## Decision
- [ ] Admit to registry
- [ ] Request revision
- [ ] Reject
"""
    with open(filepath, "w") as f:
        f.write(content)
    data["mechanisms"]["candidates"].append(
        {"id": mech_id, "status": "candidate", "created": datetime.now().isoformat()}
    )
    data["metrics"]["mechanisms_identified"] = (
        data["metrics"].get("mechanisms_identified", 0) + 1
    )
    save_dashboard(data)
    print(f"Created: {filename}")


def cmd_update_dashboard(args):
    data = load_dashboard()
    data["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    save_dashboard(data)
    print(f"Dashboard updated: {data['last_updated']}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]
    args = sys.argv[2:]
    commands = {
        "status": cmd_status,
        "advance": cmd_advance,
        "add-reading": cmd_add_reading,
        "extract-mechanism": cmd_extract_mechanism,
        "update-dashboard": cmd_update_dashboard,
    }
    if cmd in commands:
        commands[cmd](args)
    else:
        print(f"Unknown: {cmd}")
        print(__doc__)


if __name__ == "__main__":
    main()
