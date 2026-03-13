---
artifact_id: ART-046
pair_id: TH-046
title: "RESEARCH_DASHBOARD_v1"
artifact_type: mechanism_artifact
family_dir: engine/mechanisms
prompt_sha256: 119792136aa24c129810a8c2d0920e3fdff09e7276f6c9d105d447a62de4dd90
response_sha256: 3cbea1120cbc01db14b4f5c2827264714778e55cddd138a8a8e69a2e37aad8d9
pair_path: research/thread_pairs/TH-046-research-dashboard-v1.md
generated_at: 2026-03-11T07:48:01Z
---

# RESEARCH_DASHBOARD_v1

Source pair: `TH-046`

## Prompt

proceed

## Response

RESEARCH_DASHBOARD_v1


Operational Control System for the Research Program


The Research Dashboard is the command center of the entire project.
Its purpose is to prevent the research phase from dissolving into scattered notes, forgotten sources, or disconnected insights.


The dashboard tracks four things simultaneously:


research progress
mechanism extraction
simulation readiness
open problems


Conceptually:


reading → mechanisms → thresholds → modules → simulation


The dashboard monitors each stage.



I. Dashboard Structure


The dashboard contains six major sections.


program overview
lane tracker
reading tracker
mechanism tracker
simulation readiness
open problem register


Each section can be stored in a single structured document or database.


File:


RESEARCH_DASHBOARD.md



II. Program Overview


This section summarizes the entire research program.


Fields:

Field
Meaning
research_phase
current program stage
total_lanes
number of active research lanes
core_readings
canonical literature count
mechanisms_identified
mechanisms discovered
threshold_models
completed threshold syntheses
simulation_modules
implemented modules

Example:


research_phase: phase_1_literature
total_lanes: 5
core_readings: 180
mechanisms_identified: 16
threshold_models: 0
simulation_modules: 3


This provides a quick snapshot of project status.



III. Research Lane Tracker


Each research lane is tracked independently.


Initial lanes:


Origin of Life
Origin of Cognition
Origin of Society
Origin of Symbolic Systems
Origin of Reflexive Knowledge


Lane tracker fields:

Field
Description
lane_id
lane identifier
lane_name
research topic
core_readings
total canonical texts
readings_completed
completed readings
mechanisms_extracted
mechanisms identified
synthesis_status
none / draft / complete
simulation_relevance
yes / no

Example:

Lane
Readings
Completed
Mechanisms
Synthesis
R1
30
6
2
none
R2
40
4
1
none

This prevents losing track of research progress.



IV. Reading Tracker


This tracks individual sources.


Each reading entry contains:

Field
Meaning
reading_id
unique identifier
title
source title
author
author
year
publication year
lane
associated research lane
importance
core / secondary
status
queued / reading / completed
mechanisms_identified
extracted mechanisms

Example entry:


reading_id: R201-001
title: The Vital Question
author: Nick Lane
lane: Origin of Life
importance: core
status: completed
mechanisms_identified: metabolic_throughput


This ensures the literature review remains organized.



V. Mechanism Tracker


The mechanism tracker monitors extracted mechanisms.


Fields:

Field
Description
mechanism_id
registry ID
mechanism_name
description
threshold
associated threshold
supporting_readings
literature sources
implementation_status
conceptual / planned / implemented
confidence_level
low / medium / high

Example:

Mechanism
Threshold
Readings
Implementation
autocatalytic_closure
TP-05
3
conceptual
predictive_processing
TP-06
5
planned

This bridges research with simulation.



VI. Simulation Readiness Tracker


Tracks which mechanisms are ready to be simulated.


Fields:

Field
Meaning
mechanism_pack
mechanism implementation
required_modules
modules needed
implementation_status
pending / partial / complete
simulation_world
test world
results
summary

Example:

Mechanism Pack
Modules
Status
autocatalytic_network_pack
resource_flow, self_organization
pending
predictive_agent_pack
observer_model_loop
partial

This ensures research results are translated into simulations.



VII. Open Problem Register


This section prevents intellectual stagnation.


Fields:

Field
Meaning
problem_id
identifier
description
unresolved issue
related_lane
associated research lane
possible_solutions
hypotheses
priority
low / medium / high

Example:


problem_id: OP-12
description: unclear origin of informational inheritance before RNA
lane: origin_of_life
priority: high


Every research report should add open problems.



VIII. Weekly Research Log


A short log tracks ongoing work.


Fields:


date
readings completed
mechanisms extracted
notes
next tasks


Example:


week: 2026-03-09

readings_completed:
- Vital Question
- Origins of Order (chapters 1–2)

mechanisms_extracted:
- metabolic_throughput

next_tasks:
- analyze hypercycle theory


This keeps the research momentum visible.



IX. Research Metrics


The dashboard should automatically calculate key metrics.


Examples:

Metric
Meaning
reading_completion_rate
progress through literature
mechanism_density
mechanisms per lane
simulation_conversion_rate
mechanisms implemented
open_problem_ratio
unresolved research questions

These metrics help evaluate research progress.



X. Dashboard Visualization (Optional)


The dashboard can also drive visualization tools.


Possible views:


mechanism network graph
reading progress timeline
threshold readiness chart
simulation pipeline


These make large-scale research easier to navigate.



XI. Research Phase Workflow


Using the dashboard, the research cycle becomes:


read literature
→ record reading notes
→ extract mechanisms
→ update mechanism registry
→ track readiness for simulation
→ test mechanisms in world instances
→ record results


The dashboard ensures each step is visible.



XII. Minimal Dashboard Example


PROGRAM OVERVIEW
----------------
phase: literature review
readings_total: 180
readings_completed: 12
mechanisms_identified: 4

LANE STATUS
-----------
Origin of Life: 6 / 30 readings
Origin of Cognition: 3 / 40 readings

MECHANISMS
----------
autocatalytic_closure
metabolic_throughput
predictive_processing

SIMULATION
----------
autocatalytic_network_pack: pending
predictive_agent_pack: planned

OPEN PROBLEMS
-------------
OP-01: pre-RNA information storage
OP-02: transition from neural activity to symbolic cognition



XIII. Why This Artifact Matters


Large research systems fail because:


insights become lost
research scope grows uncontrollably
simulation work drifts from theory


The dashboard prevents these failures.


It acts as the navigation map of the entire project.



XIV. Pre-Phase Completion


With this artifact the pre-phase is effectively complete.


The project now has:


conceptual architecture
primitive vocabulary
mechanism registry
simulation kernel
module interface
world instance schema
research dashboard


This is the minimum infrastructure required to begin the research phase.



XV. Research Phase Launch


The research phase can now start with a clear loop:


1. read canonical sources
2. extract mechanisms
3. map mechanisms to primitives/modules
4. implement mechanism packs
5. simulate in world instances
6. analyze results
7. refine theory


This cycle becomes the engine of the entire project.



XVI. Final Observation


At this point the project has transitioned from:


idea


to


research platform


The next real work is reading, mechanism extraction, and experimentation.



If you'd like, I can also show you something extremely useful now that the pre-phase is finished:


the optimal first 30 readings that should launch the research phase with maximum leverage across all lanes.