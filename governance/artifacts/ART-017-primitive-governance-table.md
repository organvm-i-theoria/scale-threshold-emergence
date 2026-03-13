---
artifact_id: ART-017
pair_id: TH-017
title: "Primitive Governance Table"
artifact_type: governance_artifact
family_dir: governance/artifacts
prompt_sha256: db00df594f886bbf12958d4f1b1516ca4ad343a33adb977d6dee2507d1fa27e4
response_sha256: bfeac62d005497ea8c427fbfbe2bd05348b39b5690437277b8cc4c30d37a45ff
pair_path: research/thread_pairs/TH-017-primitive-governance-table.md
generated_at: 2026-03-11T07:48:01Z
---

# Primitive Governance Table

Source pair: `TH-017`

## Prompt

Proceed;


2/2

## Response

Primitive Governance Table


Phase-1 Controlled Core Lexicon v1


This table converts the recurrence map into a governed lexicon. Its purpose is to prevent semantic drift while the research program expands across disciplines.


Each primitive now receives:

Field
Function
Primitive ID
stable identifier
Primitive
controlled term
Canonical Status
core / extended / provisional / local
Approved Definition
current governed meaning
Synonym Warnings
nearby terms that can cause drift or false equivalence
Upstream Sources
anchor lanes for definition control
Downstream Modules
later architecture zones where the primitive will be reused
Governance Note
special handling rule

Canonical Status Rule

Status
Meaning
Core
must be defined early and used consistently everywhere
Extended
stable and reusable, but defined after the core layer stabilizes
Provisional
allowed for use, but definition remains reviewable
Local
keep lane-specific unless recurrence increases later


Layer A — Core Canonical Primitives


These are the first-pass non-negotiable terms.

Primitive ID
Primitive
Canonical Status
Approved Definition
Synonym Warnings
Upstream Sources
Downstream Modules
Governance Note
PR-001
Entity
Core
a distinguishable unit treated as existing within a modeling frame
object, thing, actor, instance are not always equivalent
P1-004, P1-058
ontology engine, system engine, observer engine, symbolic engine
do not use interchangeably with process or relation
PR-002
Process
Core
temporally extended change or activity that transforms states, relations, or systems
event, function, mechanism overlap but are not identical
P1-004, P1-010, P1-058
state engine, feedback engine, evolution engine
always specify what changes and over what interval
PR-003
Relation
Core
a structured connection holding between entities, states, or processes
link, tie, correlation, mapping may be narrower forms
P1-004, P1-006, P1-009
ontology engine, network engine, semiotic engine
distinguish structural relation from causal relation unless explicit
PR-004
State
Core
the configuration of a system or entity at a specified time or index
condition, mode, phase may be special cases
P1-010, P1-006, P1-039
state engine, observer engine, narrative engine
every state claim should imply a boundary and indexing rule
PR-005
Boundary
Core
the criterion that differentiates a system from what is treated as outside it
edge, border, membrane, scope are context-bound variants
P1-004, P1-015, P1-058
system engine, ecology engine, civilization engine
every system definition must name or imply a boundary
PR-011
Cause
Core
a dependence relation under which variation in one factor contributes to variation in another in a law-governed or intervention-sensitive way
trigger, influence, correlation, association must not be substituted casually
P1-006, P1-057
causal engine, decision engine, governance engine
causal claims require explicit evidence type or model form
PR-015
Dependency
Core
a relation in which the status of one variable, state, or structure is not independent of another
correlation, reliance, dependence, grounding require distinction by context
P1-006, P1-010, P1-058
causal engine, state engine, systems integration
broader than causation; do not collapse the two
PR-018
Constraint
Core
a condition that limits allowable states, transitions, relations, or outcomes
rule, law, limit, boundary condition overlap but differ in level
P1-006, P1-010, P1-013
state engine, rule engine, governance engine
every generative model should declare its active constraints
PR-024
Stability
Core
bounded persistence of structure or behavior under perturbation
equilibrium, homeostasis, resilience are related but not identical
P1-010, P1-029, P1-058
state engine, feedback engine, ecology engine
stability is always relative to perturbation class and timescale
PR-026
Emergence
Core
appearance of higher-order structure or behavior from interactions not reducible to isolated lower-level descriptions alone
complexity, novelty, gestalt, synergy must not be used loosely as substitutes
P1-010, P1-029, P1-034, P1-058
evolution engine, cognition engine, civilization engine
emergent claims must name lower-level basis and higher-level pattern
PR-027
Information
Core
reduction of uncertainty or distinguishable structure capable of being encoded, transmitted, or transformed
meaning, knowledge, data, signal are not interchangeable
P1-013, P1-011, P1-058
signal engine, observer engine, symbolic engine
distinguish syntactic information from semantic meaning unless specified
PR-041
Network
Core
a structured set of units and connections across which relations, flows, or influences are organized
graph is a formal subtype, web is metaphorical unless formalized
P1-015, P1-038, P1-049, P1-058
network engine, ecology engine, infrastructure engine
every network model should define node and edge semantics
PR-044
Flow
Core
directed movement of matter, energy, information, or influence through a system
transfer, circulation, diffusion, propagation are contextual forms
P1-013, P1-029, P1-038, P1-053
signal engine, ecology engine, infrastructure engine
always specify what flows, through what, and under what constraints
PR-048
Model
Core
a structured representation used to describe, explain, predict, or control a target system
map, schema, theory, simulation differ in scope and fidelity
P1-039, P1-045, P1-057
observer engine, AI engine, governance engine
every model should declare target, abstraction level, and error boundary
PR-056
System
Core
a bounded set of interacting elements whose organized relations produce identifiable behavior or structure
assemblage, collection, network, organism are possible subclasses, not synonyms
P1-004, P1-015, P1-058
all later modules
never use without implied elements, relations, and boundary


Layer B — Extended Canonical Primitives


These are stable and reusable, but governed after the core layer.

Primitive ID
Primitive
Canonical Status
Approved Definition
Synonym Warnings
Upstream Sources
Downstream Modules
Governance Note
PR-008
Hierarchy
Extended
an ordered nesting of levels, parts, or authorities such that some elements are above, below, or inclusive of others
scale, rank, tree, stack can mislead if structure differs
P1-004, P1-007, P1-049
ontology engine, civilization engine, archive design
specify whether ontological, causal, scale, or governance hierarchy
PR-010
Identity
Extended
the persistence criterion by which something counts as the same across time, change, or representation
self, sameness, equivalence, continuity must not be conflated
P1-004, P1-043, P1-048
observer engine, narrative engine, ontology engine
identity claims require persistence rule
PR-016
Feedback
Extended
a process in which outputs of a system re-enter as inputs influencing subsequent behavior
recursion, response, adaptation, control overlap but differ
P1-015, P1-045, P1-058
feedback engine, cognition engine, governance engine
distinguish positive from negative feedback when possible
PR-017
Control
Extended
directed regulation of system behavior relative to a target, setpoint, or permissible region
power, governance, steering, management are not always identical
P1-015, P1-044, P1-052
feedback engine, governance engine, AI agents
do not assume teleology unless target condition is explicit
PR-019
State Space
Extended
the set of possible states a system may occupy under a given representation
phase space may be specific mathematical subtype
P1-010, P1-029, P1-045
state engine, simulation engine, narrative engine
must be tied to representation scheme
PR-030
Entropy
Extended
a measure of uncertainty, disorder, or multiplicity depending on formal context
chaos, randomness, disorder are not equivalent in all disciplines
P1-013, P1-011, P1-029
signal engine, thermodynamic engine, cognition engine
always name the entropy formalism being used
PR-031
Channel
Extended
the medium or pathway through which signals or flows are transmitted
medium, conduit, pathway may be narrower or broader
P1-013, P1-054, P1-055
signal engine, infrastructure engine, semiotic engine
define channel capacity or transmission limits where relevant
PR-032
Encoding
Extended
transformation of a source state, message, or structure into another representational form
inscription, translation, transcription are context-specific cases
P1-013, P1-054, P1-055
signal engine, symbolic engine, archive engine
every encoding implies a code or mapping rule
PR-034
Compression
Extended
reduction of representation length or complexity while preserving selected structure
simplification, summary, abstraction are related but distinct
P1-011, P1-013, P1-057
primitive library, ontology compression, archive design
specify what information is preserved or lost
PR-037
Complexity
Extended
a measure of structural, computational, or descriptive richness under a stated formalism
complicatedness, richness, density are too vague
P1-011, P1-012, P1-029
evaluation engine, simulation scaling, emergence studies
complexity claims must name metric or formal basis
PR-038
Computation
Extended
rule-governed transformation of representations or states
calculation, processing, simulation overlap but differ by context
P1-011, P1-018, P1-047
AI engine, simulation engine, signal engine
distinguish abstract computation from physical implementation
PR-039
Recursion
Extended
self-reference or self-application in a process, definition, or structure
iteration and feedback are related but not identical
P1-011, P1-015, P1-048
narrative engine, AI engine, meta-system design
define recursion depth or stopping condition when operationalized
PR-040
Iteration
Extended
repeated application of an operation across steps or cycles
looping, recurrence, recursion differ in technical meaning
P1-010, P1-011, P1-019
state engine, world generation, optimization
iteration alone does not imply self-reference
PR-046
Observer
Extended
a system capable of acquiring, registering, or using information about another system or itself
subject, agent, witness, sensor can be narrower or broader
P1-039, P1-041, P1-045
observer engine, AI engine, epistemic governance
specify whether passive, active, or self-observing
PR-047
Observation
Extended
an information-acquisition event or process linking observer and observed
perception, measurement, sensing, recording differ by modality
P1-039, P1-042, P1-057
observer engine, signal engine, scientific method
observation claims should include interface or method
PR-049
Prediction
Extended
model-based anticipation of future or hidden states
forecast, expectation, inference may differ by evidence type
P1-039, P1-045, P1-047
observer engine, AI engine, governance engine
define whether probabilistic, deterministic, or heuristic
PR-050
Memory
Extended
persistence and retrievability of information across time within a system
storage, archive, trace, recollection are context-specific forms
P1-013, P1-043, P1-055
observer engine, symbolic engine, archival systems
distinguish short-term state retention from long-term structured memory
PR-051
Symbol
Extended
a representational unit that stands for or points beyond itself within a code or interpretive system
sign, token, image, icon, marker must not be collapsed blindly
P1-055, P1-056, P1-054
symbolic engine, myth engine, archive engine
require code context or interpretive regime
PR-053
Meaning
Extended
the structured interpretive relation linking signifying forms to referents, uses, or effects
content, semantics, significance, value differ by level
P1-055, P1-054, P1-050
symbolic engine, narrative engine, governance rhetoric
do not treat meaning as identical with information
PR-055
Narrative
Extended
temporally ordered symbolic structuring of states, agents, events, and transformations
story, myth, discourse, plot overlap but differ in scope
P1-056, P1-043, P1-045
narrative engine, myth engine, identity architecture
narrative must include change over time, not mere description
PR-057
Environment
Extended
what lies outside a system boundary yet can affect or be affected by the system
world, context, setting, milieu vary by scale and model
P1-015, P1-038, P1-058
system engine, ecology engine, cognition engine
environment is always relative to a named system
PR-060
Self-Organization
Extended
spontaneous emergence of ordered structure from local interactions without centralized control
emergence and adaptation overlap but are not identical
P1-029, P1-031, P1-058
evolution engine, network engine, civilization engine
claims require local-rule basis and absence of central orchestrator


Layer C — Provisional Primitives


These are active and useful, but should remain reviewable until more lane coverage is complete.

Primitive ID
Primitive
Canonical Status
Approved Definition
Synonym Warnings
Upstream Sources
Downstream Modules
Governance Note
PR-013
Counterfactual
Provisional
an alternative conditional state or history used to test dependence or explanation
hypothetical, imaginary, possible-world variant may differ by formalism
P1-006, P1-001
causal engine, narrative branching, multiverse logic
preserve formal distinction from simple fiction
PR-014
Intervention
Provisional
deliberate or modeled alteration of a variable, state, or process to test or redirect system behavior
action, control, perturbation overlap but differ in intent
P1-006, P1-044
causal engine, governance engine, AI action
specify whether epistemic, experimental, or operational
PR-021
Attractor
Provisional
a stable or recurrent region in state space toward which trajectories converge
equilibrium, endpoint, basin can be nearby but not identical
P1-010, P1-029
state engine, cognition engine, social dynamics
retain technical dynamical meaning unless clearly broadened
PR-022
Bifurcation
Provisional
a parameter-driven split into qualitatively different dynamical regimes
branching, divergence, rupture are looser analogues
P1-010, P1-031
state engine, narrative branching, phase-change models
use carefully outside formal dynamics
PR-023
Phase Transition
Provisional
an abrupt regime shift produced by threshold conditions in system organization
transformation, upheaval, tipping point may be informal variants
P1-029, P1-031
emergence engine, civilization dynamics, cognition analogies
name the threshold variable when possible
PR-028
Signal
Provisional
a structured carrier of information through a channel or interface
message, cue, data stream differ by coding assumptions
P1-013, P1-042, P1-054
signal engine, perception engine, communication systems
likely promotable after more lane coverage
PR-029
Noise
Provisional
variation or interference that reduces recoverable structure relative to a signal or model
randomness, disturbance, error differ by formal setting
P1-013, P1-042
signal engine, cognition engine, infrastructure monitoring
always define relative to signal or model
PR-033
Decoding
Provisional
transformation from encoded representation into an inferred or reconstructed state
interpretation, reading, parsing overlap but vary in formal precision
P1-013, P1-055
symbolic engine, communication systems, AI parsing
likely promotable with later symbolic coverage
PR-035
Algorithm
Provisional
a finite, well-defined procedure for transforming inputs into outputs
rule, method, routine, procedure can be broader or narrower
P1-011, P1-047
AI engine, simulation engine, generation engine
distinguish algorithm from program and implementation
PR-045
Gradient
Provisional
a directional difference across a space that can drive flow or change
slope, bias, field, pressure differ by domain
P1-029, P1-038, P1-045
flow engine, optimization, morphogenesis
requires domain-specific metric or field
PR-052
Sign
Provisional
an interpreted symbolic unit situated within a signifying system
symbol, token, marker, cue are not identical
P1-055, P1-054
semiotic engine, culture engine, interface systems
keep distinct from symbol until semiotic layer stabilizes
PR-054
Language
Provisional
a structured symbolic system for expression, coordination, and interpretation
discourse, code, grammar, speech each capture only part
P1-054, P1-055
symbolic engine, narrative engine, governance rhetoric
likely promotable after full Band VI coverage


Layer D — Local or Deferred Terms


These remain usable, but should not yet enter the tightly controlled universal lexicon.

Primitive ID
Primitive
Canonical Status
Approved Definition
Synonym Warnings
Upstream Sources
Downstream Modules
Governance Note
PR-006
Composition
Local
combination of parts into a whole under a specified rule
assembly, aggregation, synthesis may differ
P1-005
ontology engine, modular architecture
defer until mereology lane is synthesized
PR-007
Decomposition
Local
partition of a whole into constituent parts under a specified rule
analysis, breakdown, segmentation differ in method
P1-005
ontology engine, archive design
pair-govern with composition later
PR-012
Effect
Local
resulting state, event, or condition linked to a cause
outcome, result, consequence may not carry causal precision
P1-006
causal engine
usually governed implicitly by cause and state
PR-020
Trajectory
Local
ordered path through a state space across time
path, curve, development may be looser
P1-010
simulation engine, narrative dynamics
promote later if dynamic modeling becomes central everywhere
PR-036
Program
Local
encoded specification of a procedure executable by an interpreter or machine
script, code, algorithm not interchangeable
P1-011, P1-047
AI engine, computation layer
too implementation-specific for core lexicon now
PR-042
Node
Local
a unit within a network representation
actor, vertex, point, site vary by domain
P1-041, P1-049
network engine
keep as network-subtype term
PR-043
Edge
Local
a relation represented as a connection in a network
arc, tie, link are possible subtypes or variants
P1-041, P1-049
network engine
keep as graph-formal term
PR-058
Adaptation
Local
adjustment of system structure or behavior relative to environmental conditions
learning, optimization, acclimation differ in mechanism
P1-036, P1-038, P1-046
evolution engine, cognition engine
likely promotable after broader Band IV/V coverage
PR-059
Optimization
Local
improvement relative to an objective function or criterion
efficiency, maximization, fitting can mislead
P1-044, P1-047
decision engine, AI systems
defer until decision-theoretic and engineering lanes mature


Synonym Control Notes


The most dangerous drift zones are the following.

Controlled Term
Drift Risk
Information
commonly confused with meaning, knowledge, data, and signal
System
often used loosely for any collection whatsoever
Emergence
often invoked without specifying lower-level interactions
Model
often confused with theory, simulation, or representation generally
Cause
often reduced to correlation or narrative sequence
Observer
often confused with agent, subject, sensor, or consciousness
Symbol
often confused with sign, image, token, and metaphor
Constraint
often confused with boundary, law, rule, and limit

These should be reviewed whenever a new lane synthesis is written.



Governance Priority Queue


The next glossary stabilization order should be:

Priority Order
Terms
1
Entity, Relation, Process, State, System
2
Boundary, Constraint, Dependency, Cause
3
Information, Model, Flow, Network
4
Stability, Emergence, Environment
5
Feedback, Observer, Prediction, Memory
6
Symbol, Meaning, Narrative

That order follows the dependency backbone already established.



Immediate Operational Consequence


This table now enables four concrete actions.

Action
Result
glossary drafting
one governed entry per primitive
lane writing discipline
synthesis memos must use approved definitions
primitive extraction filtering
extracted terms can be accepted or rejected against status rules
downstream architecture design
only core and extended terms should drive first-pass module design


Minimal Controlled Core Lexicon v1


The first strict lexicon for system-wide use is therefore:


Entity
Process
Relation
State
Boundary
Cause
Dependency
Constraint
Stability
Emergence
Information
Network
Flow
Model
System


That is the smallest stable vocabulary currently justified by cross-lane recurrence.


The strongest next artifact is the Glossary Draft Pack v1, meaning one filled controlled-glossary entry for each term in this Minimal Controlled Core Lexicon.