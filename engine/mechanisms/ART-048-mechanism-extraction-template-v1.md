---
artifact_id: ART-048
pair_id: TH-048
title: "MECHANISM EXTRACTION TEMPLATE v1"
artifact_type: mechanism_artifact
family_dir: engine/mechanisms
prompt_sha256: 119792136aa24c129810a8c2d0920e3fdff09e7276f6c9d105d447a62de4dd90
response_sha256: cb69cdc410f979fda9b5a29f575908b2aed4ae47f1361a35c28efd9bfc481ef7
pair_path: research/thread_pairs/TH-048-mechanism-extraction-template-v1.md
generated_at: 2026-03-11T07:48:01Z
---

# MECHANISM EXTRACTION TEMPLATE v1

Source pair: `TH-048`

## Prompt

proceed

## Response

MECHANISM EXTRACTION TEMPLATE v1


Protocol for Converting Readings → Mechanisms → Modules → Simulation


The purpose of the template is to standardize how insights are extracted from literature so that research outputs can directly feed:


primitive canon
module library
mechanism registry
simulation engine


Without a strict extraction protocol, readings produce interesting notes but no executable theory.


This template forces each reading to produce structured knowledge artifacts.



I. Extraction Workflow


Each reading passes through five steps.


read
→ summarize claims
→ extract mechanisms
→ map primitives
→ map modules
→ record simulation relevance


Every reading should generate one Mechanism Extraction Record.



II. Mechanism Extraction Record


File format suggestion:


MECHANISM_EXTRACTION_<reading_id>.md


Example:


MECHANISM_EXTRACTION_R201-001.md



III. Metadata Section


Basic bibliographic information.

Field
Description
reading_id
unique identifier
title
book or paper
author
author(s)
year
publication year
research_lane
life / cognition / society / symbolic / reflexive
importance
core / secondary

Example:


reading_id: R201-001
title: The Vital Question
author: Nick Lane
year: 2015
research_lane: origin_of_life
importance: core



IV. Core Thesis Summary


A concise description of the central claim.


Structure:


1–3 paragraph explanation


Questions to answer:


What problem does the author address?
What explanation do they propose?
What evidence supports it?


Example:


Lane argues that the origin of life depends on natural proton gradients at alkaline hydrothermal vents, which provide the energy necessary for metabolic networks to arise.



V. Mechanism Identification


Identify explicit or implicit mechanisms proposed by the text.


Fields:

Field
Description
mechanism_name
concise label
description
explanation
mechanism_type
chemical / biological / cognitive / social
threshold
relevant threshold

Example:

Mechanism
Description
Threshold
metabolic_throughput
energy gradients drive biochemical cycles
TP-05


VI. Primitive Mapping


Map the mechanism to primitives from the canon.


Example:

Primitive
Role
flow
energy movement
constraint
reaction pathways
process
chemical transformations
system
metabolic network

Purpose:


connect mechanism to conceptual vocabulary



VII. Module Mapping


Identify which modules are required to simulate the mechanism.


Example:

Module
Role
resource_flow
energy gradients
self_organization
metabolic network emergence
feedback_regulator
reaction stabilization

Purpose:


connect theory to computational architecture



VIII. Evidence Evaluation


Evaluate the empirical support.

Evidence Type
Description
theoretical
conceptual or mathematical
experimental
laboratory data
observational
empirical observation
computational
simulation results

Example:


evidence_type: experimental
example: hydrothermal vent chemistry experiments


Confidence rating:


low
medium
high



IX. Competing Theories


Record alternative explanations discussed in the literature.


Example:

Theory
Description
RNA world
life began with self-replicating RNA
metabolism first
metabolic networks predate genetic systems

Purpose:


avoid premature theoretical closure



X. Simulation Relevance


Assess whether the mechanism can be simulated.


Fields:

Field
Meaning
simulation_ready
yes / partial / no
required_modules
modules needed
parameter_estimates
known parameter ranges

Example:


simulation_ready: partial
required_modules: resource_flow, self_organization



XI. Open Questions


Each reading must produce unresolved questions.


Examples:


How stable are prebiotic metabolic cycles?
What chemical pathways enable early replication?
What environmental conditions are necessary?


These questions feed the Open Problem Register.



XII. Mechanism Extraction Example


Example from Surfing Uncertainty.



Metadata


reading_id: R202-001
title: Surfing Uncertainty
author: Andy Clark
year: 2015
research_lane: origin_of_cognition



Core Thesis


The brain is a prediction engine that continually anticipates sensory input and minimizes prediction errors.



Mechanism

Mechanism
Description
predictive_processing
hierarchical prediction and error correction

Threshold:


TP-06 Observer Emergence



Primitive Mapping

Primitive
Role
model
internal representation
prediction
anticipated signal
feedback
error correction
signal
sensory input


Module Mapping

Module
Role
observer_model_loop
prediction generation
feedback_regulator
error correction
signal_transmission
sensory input flow


Evidence


evidence_type: experimental neuroscience
confidence: high



Competing Theories


symbolic cognition
reactive cognition



Simulation Relevance


simulation_ready: yes


Possible implementation:


predictive_agent_pack



XIII. Extraction Output


Each reading should produce three outputs.


reading notes
mechanism extraction record
mechanism registry update


Optional fourth output:


module implementation candidate



XIV. Expected Mechanism Yield


From the first 30 readings you should expect roughly:

Output
Estimate
mechanisms
40–60
module patterns
10–15
threshold insights
5–8

These are sufficient to start simulation experiments.



XV. Extraction Workflow in Practice


Recommended workflow per reading:


read chapter
→ summarize thesis
→ list mechanisms
→ map primitives
→ map modules
→ update dashboard


Time per core reading:


3–5 hours



XVI. Research Feedback Loop


Once mechanisms are extracted:


mechanisms
→ mechanism registry
→ module mapping
→ simulation pack
→ experiment log
→ theoretical refinement


This closes the research → simulation loop.



XVII. Result


With this template the research phase becomes a structured knowledge production pipeline.


Instead of:


reading → notes


you get:


reading
→ mechanism
→ module
→ simulation


Which is exactly what the project needs.



If you'd like, the next extremely useful artifact is the Knowledge Graph Schema, because it connects:


readings
mechanisms
primitives
modules
thresholds


into a queryable structure that prevents the research corpus from becoming fragmented as it grows.