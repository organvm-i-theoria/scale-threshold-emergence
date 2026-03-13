---
artifact_id: ART-014
pair_id: TH-014
title: "Phase-1 Primitive Extraction Seed Library"
artifact_type: primitive_artifact
family_dir: engine/primitives
prompt_sha256: f01847dfc94126426b4849004762a12557de2332ae0ca1b4602210b341f0281b
response_sha256: bfd3fa394e1810f173aaddc6683fe010da409c221a65d2dfe89668ae5c63d39e
pair_path: research/thread_pairs/TH-014-phase-1-primitive-extraction-seed-library.md
generated_at: 2026-03-11T07:48:01Z
---

# Phase-1 Primitive Extraction Seed Library

Source pair: `TH-014`

## Prompt

Proceed

## Response

Phase-1 Primitive Extraction Seed Library


Wave-1 Candidate Primitives (Initial Recognition Set)


This library is a recognition scaffold for the first research wave.
When reading the Wave-1 sources, these primitives are the most likely reusable abstractions that appear repeatedly across ontology, causation, dynamical systems, algorithmic information, and information theory.


The purpose is not to force the primitives but to accelerate detection during literature synthesis.


Each primitive includes:

Field
Meaning
Primitive ID
stable identifier
Primitive Class
entity / relation / operator / process / constraint / topology
Core Definition
minimal abstract definition
Source Lanes
where it will likely appear
Downstream Reach
how widely it propagates


I. Ontological Primitives


These stabilize the basic object language of the system.

Primitive ID
Primitive
Class
Core Definition
Source Lanes
Downstream Reach
PR-001
Entity
entity
something that exists as a distinguishable unit
ontology
universal
PR-002
Process
process
change occurring across time
ontology, dynamics
universal
PR-003
Relation
relation
structural connection between entities
ontology
universal
PR-004
State
entity
configuration of a system at time t
dynamics
universal
PR-005
Boundary
constraint
condition separating system from environment
ontology
high
PR-006
Composition
operator
combination of parts into wholes
mereology
high
PR-007
Decomposition
operator
partition of wholes into parts
mereology
high
PR-008
Hierarchy
topology
nested ordering of entities
set theory
high
PR-009
Category
entity
class defined by shared structure
category theory
high
PR-010
Identity
relation
persistence condition across time
ontology
high


II. Causal Primitives


These formalize intervention and explanation.

Primitive ID
Primitive
Class
Core Definition
Source Lanes
Downstream Reach
PR-011
Cause
relation
relation where one event produces another
causation
universal
PR-012
Effect
entity
result of causal process
causation
universal
PR-013
Counterfactual
operator
alternate state under modified conditions
causation
high
PR-014
Intervention
operator
external modification of causal system
causation
high
PR-015
Dependency
relation
variable change implies another change
causation
high
PR-016
Feedback
process
output influencing its own input
cybernetics
universal
PR-017
Control
process
regulation toward target state
cybernetics
high
PR-018
Constraint
constraint
limitation restricting possible states
causation
universal


III. Dynamical Primitives


These govern state evolution.

Primitive ID
Primitive
Class
Core Definition
Source Lanes
Downstream Reach
PR-019
State Space
topology
set of all possible system states
dynamical systems
universal
PR-020
Trajectory
process
path of system states through time
dynamical systems
universal
PR-021
Attractor
topology
stable region toward which systems evolve
dynamics
high
PR-022
Bifurcation
process
qualitative change in system behavior
dynamics
high
PR-023
Phase Transition
process
abrupt macro change from micro variation
thermodynamics
high
PR-024
Stability
constraint
persistence under perturbation
dynamics
high
PR-025
Instability
constraint
divergence under perturbation
dynamics
high
PR-026
Emergence
process
macro-order from micro interactions
complexity
universal


IV. Information Primitives


These define signal and structure.

Primitive ID
Primitive
Class
Core Definition
Source Lanes
Downstream Reach
PR-027
Information
entity
reduction of uncertainty
information theory
universal
PR-028
Signal
entity
structured information transmission
information theory
universal
PR-029
Noise
entity
random variation corrupting signal
information theory
universal
PR-030
Entropy
measure
uncertainty of information distribution
information theory
universal
PR-031
Channel
topology
medium through which signals propagate
information theory
high
PR-032
Encoding
operator
transformation of message into signal
information theory
high
PR-033
Decoding
operator
reconstruction of message from signal
information theory
high
PR-034
Compression
operator
reduction of representation length
algorithmic information
high


V. Algorithmic Primitives


These capture computational structure.

Primitive ID
Primitive
Class
Core Definition
Source Lanes
Downstream Reach
PR-035
Algorithm
process
finite procedure producing output
algorithmic info
universal
PR-036
Program
entity
encoded algorithm
algorithmic info
universal
PR-037
Complexity
measure
resources required to compute
complexity theory
universal
PR-038
Computation
process
transformation of information by rules
digital physics
universal
PR-039
Recursion
operator
function defined in terms of itself
computation
universal
PR-040
Iteration
operator
repeated application of process
computation
universal


VI. Structural Primitives


These appear across networks and systems.

Primitive ID
Primitive
Class
Core Definition
Source Lanes
Downstream Reach
PR-041
Network
topology
set of nodes and edges
systems science
universal
PR-042
Node
entity
unit within network
network theory
universal
PR-043
Edge
relation
connection between nodes
network theory
universal
PR-044
Flow
process
movement of resources through network
systems science
high
PR-045
Gradient
measure
directional difference across space
dynamics
high


VII. Observer Primitives


These will later anchor cognition lanes.

Primitive ID
Primitive
Class
Core Definition
Source Lanes
Downstream Reach
PR-046
Observer
entity
system capable of acquiring information
cognition
universal
PR-047
Observation
process
acquisition of information from system
cognition
universal
PR-048
Model
entity
representation of system
cognition
universal
PR-049
Prediction
process
model-based expectation of future state
cognition
high
PR-050
Memory
process
retention of information across time
cognition
universal


VIII. Symbolic Primitives


These will appear strongly in later civilization lanes.

Primitive ID
Primitive
Class
Core Definition
Source Lanes
Downstream Reach
PR-051
Symbol
entity
representation standing for something else
semiotics
universal
PR-052
Sign
entity
interpreted symbol within system
semiotics
universal
PR-053
Meaning
relation
mapping between symbol and referent
semiotics
universal
PR-054
Language
system
structured symbolic communication
linguistics
high
PR-055
Narrative
process
temporal symbolic structure
mythology
high


IX. System-Level Primitives


These unify the full architecture.

Primitive ID
Primitive
Class
Core Definition
Source Lanes
Downstream Reach
PR-056
System
entity
bounded interacting set of elements
systems theory
universal
PR-057
Environment
entity
external context influencing system
systems theory
universal
PR-058
Adaptation
process
system adjustment to environment
evolution
high
PR-059
Optimization
process
improvement relative to objective
decision theory
high
PR-060
Self-Organization
process
spontaneous order without central control
complexity
universal


Primitive Count Summary

Category
Count
Ontological
10
Causal
8
Dynamical
8
Informational
8
Algorithmic
6
Structural
5
Observer
5
Symbolic
5
System-Level
5

Total candidate primitives: 60



How the Library Is Used During Wave-1


When reading Wave-1 literature:


source → detect primitive
→ verify definition
→ create PRIMITIVE_EXTRACT
→ increment primitive count in master index


Most primitives should appear repeatedly across different disciplines.
Those with cross-lane recurrence become canonical primitives.



Expected Wave-1 Outcome


Typical results after completing the five Wave-1 lanes:

Output
Expected Quantity
lane notes
15–20
synthesis documents
5
primitives extracted
25–40
glossary entries
30–50
cross-lane relations
100+

These primitives become the building blocks of the later multiversal architecture.



High-Value Next Artifact


The next artifact that significantly improves the research engine would be the Primitive Interaction Map — a graph showing how these 60 primitives interact to produce higher-order systems such as:


• dynamical systems
• cybernetic systems
• evolutionary systems
• cognitive systems
• symbolic systems


This map usually reveals the minimal grammar of universal systems.