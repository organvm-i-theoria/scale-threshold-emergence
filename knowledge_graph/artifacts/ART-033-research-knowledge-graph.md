---
artifact_id: ART-033
pair_id: TH-033
title: "Research Knowledge Graph"
artifact_type: knowledge_graph_artifact
family_dir: knowledge_graph/artifacts
prompt_sha256: 8a798890fe93817163b10b5f7bd2ca4d25d84c52739a645a889c173eee7d9d3d
response_sha256: fbe47093ac37dbbe11bdd5b597625ded6e08aafa95296c39462d6052ca53a4f7
pair_path: research/thread_pairs/TH-033-research-knowledge-graph.md
generated_at: 2026-03-11T07:48:01Z
---

# Research Knowledge Graph

Source pair: `TH-033`

## Prompt

yes

## Response

Research Knowledge Graph


Primitive–Module–Threshold–Reading Connectivity Map


This graph is the first full relational model of the framework. It connects:


readings
→ mechanisms
→ primitives
→ modules
→ thresholds
→ domains


That makes it possible to answer questions like:


Which readings most strongly support TP-05?
Which primitives recur across TP-06 and TP-08?
Which modules mediate the jump from chemistry to life?
Which authors are central to observer emergence?
Which thresholds depend on memory, model, and boundary simultaneously?


The graph is not just a visualization. It is the query structure for the whole research program.



I. Graph Schema


The graph should use six node classes.

Node Class
Meaning
Reading
a source text, paper, or monograph
Mechanism
a proposed process or explanatory model
Primitive
a controlled conceptual unit
Module
a reusable architecture pattern
Threshold
a transition package
Domain
a layer of organized reality

The graph should also use a small controlled edge vocabulary.

Edge Type
Meaning
supports
a reading supports a mechanism, primitive, module, or threshold
proposes
a reading explicitly advances a mechanism
clarifies
a reading refines a primitive
instantiates
a mechanism realizes a module
requires
a threshold requires a primitive or module
mediates
a module helps produce a threshold
emerges_in
a module or mechanism dominates in a domain
analogizes_to
one mechanism or threshold has a cross-domain analogue
critiques
a reading challenges a mechanism or model
extends
a reading deepens an earlier one


II. Node Inventory v1


A. Threshold nodes


TP-01 Formal Instantiation
TP-02 Cosmogenic Structuration
TP-03 Local Physical Regime
TP-04 Combinatorial Matter
TP-05 Biosis Threshold
TP-06 Observer Emergence
TP-07 Collective Coordination
TP-08 Symbolic Stabilization
TP-09 Reflexive Knowledge


B. Module nodes


M-01 State Engine
M-02 Feedback Regulator
M-03 Signal Transmission System
M-04 Network Interaction System
M-05 Evolution Engine
M-06 Observer–Model Loop
M-07 Symbolic Meaning System
M-08 Self-Organizing System
M-09 Resource Flow System
M-10 Narrative Dynamics Engine


C. Core primitive nodes


PR-001 Entity
PR-002 Process
PR-003 Relation
PR-004 State
PR-005 Boundary
PR-011 Cause
PR-015 Dependency
PR-018 Constraint
PR-024 Stability
PR-026 Emergence
PR-027 Information
PR-041 Network
PR-044 Flow
PR-048 Model
PR-056 System


D. Extended primitive nodes most relevant to thresholds


PR-016 Feedback
PR-019 State Space
PR-030 Entropy
PR-031 Channel
PR-032 Encoding
PR-039 Recursion
PR-040 Iteration
PR-046 Observer
PR-047 Observation
PR-049 Prediction
PR-050 Memory
PR-051 Symbol
PR-053 Meaning
PR-055 Narrative
PR-057 Environment
PR-060 Self-Organization


E. Mechanism nodes


These are the first serious mechanism set for Phase-2.


MECH-001 Autocatalytic Closure
MECH-002 Metabolic Throughput
MECH-003 Compartmentalization
MECH-004 Informational Inheritance
MECH-005 Predictive Processing
MECH-006 Embodied Sensorimotor Coupling
MECH-007 Internal Representation
MECH-008 Repeated Coordination
MECH-009 Norm Formation
MECH-010 Institutional Persistence
MECH-011 Sign Stabilization
MECH-012 Semantic Reinforcement
MECH-013 Archival Persistence
MECH-014 Model Comparison
MECH-015 Epistemic Correction Loop
MECH-016 Scientific Institutionalization


F. Reading nodes


Use a controlled reading ID format:


RD-<lane>-<nnn>


Examples:


RD-R201-001 Nick Lane — The Vital Question
RD-R201-002 Addy Pross — What Is Life?
RD-R201-003 Stuart Kauffman — Origins of Order
RD-R202-001 Andy Clark — Surfing Uncertainty
RD-R202-002 Karl Friston — Predictive Processing papers
RD-R203-001 Elinor Ostrom — Governing the Commons
RD-R203-002 Axelrod — The Evolution of Cooperation
RD-R204-001 Terrence Deacon — The Symbolic Species
RD-R204-002 Saussure — Course in General Linguistics
RD-R205-001 Thomas Kuhn — Structure of Scientific Revolutions
RD-R205-002 Karl Popper — Logic of Scientific Discovery



III. Core Threshold Subgraphs


TP-05 Biosis Threshold subgraph


This is the first major high-value cluster.


Threshold definition


TP-05
requires → PR-005 Boundary
requires → PR-027 Information
requires → PR-050 Memory
requires → PR-056 System
requires → PR-057 Environment
requires → PR-024 Stability
requires → M-02 Feedback Regulator
requires → M-05 Evolution Engine
requires → M-08 Self-Organizing System
requires → M-09 Resource Flow System


Mechanisms feeding TP-05


MECH-001 Autocatalytic Closure → instantiates → M-08
MECH-002 Metabolic Throughput → instantiates → M-09
MECH-003 Compartmentalization → clarifies → PR-005
MECH-004 Informational Inheritance → clarifies → PR-027 / PR-050


Readings feeding TP-05


RD-R201-001 The Vital Question → supports → MECH-002
RD-R201-002 What Is Life? → supports → MECH-001 / MECH-004
RD-R201-003 Origins of Order → proposes → MECH-001
RD-R201-004 Vital Dust → supports → MECH-003
RD-R201-005 Smith & Morowitz → supports → TP-05
RD-R201-006 Luisi — The Emergence of Life → supports → MECH-003 / MECH-004


Domain realization


TP-05 → emerges_in → D5 Biological Systems



TP-06 Observer Emergence subgraph


Threshold definition


TP-06
requires → PR-027 Information
requires → PR-048 Model
requires → PR-046 Observer
requires → PR-047 Observation
requires → PR-049 Prediction
requires → PR-050 Memory
requires → M-02 Feedback Regulator
requires → M-03 Signal Transmission System
requires → M-06 Observer–Model Loop


Mechanisms feeding TP-06


MECH-005 Predictive Processing → instantiates → M-06
MECH-006 Embodied Sensorimotor Coupling → instantiates → M-03 / M-06
MECH-007 Internal Representation → clarifies → PR-048


Readings feeding TP-06


RD-R202-001 Surfing Uncertainty → supports → MECH-005
RD-R202-002 Friston papers → proposes → MECH-005
RD-R202-003 Mind in Life → supports → MECH-006
RD-R202-004 The Embodied Mind → supports → MECH-006
RD-R202-005 Self Comes to Mind → supports → MECH-007 / PR-050
RD-R202-006 Incomplete Nature → supports → PR-048 / PR-027
RD-R202-007 Consciousness Explained → critiques / extends → internal model theories


Domain realization


TP-06 → emerges_in → D6 Cognitive Systems



TP-07 Collective Coordination subgraph


Threshold definition


TP-07
requires → PR-041 Network
requires → PR-044 Flow
requires → PR-048 Model
requires → PR-050 Memory
requires → PR-057 Environment
requires → M-04 Network Interaction System
requires → M-05 Evolution Engine
requires → M-06 Observer–Model Loop
requires → M-09 Resource Flow System


Mechanisms feeding TP-07


MECH-008 Repeated Coordination → instantiates → M-04
MECH-009 Norm Formation → mediates → TP-07
MECH-010 Institutional Persistence → mediates → TP-07


Readings feeding TP-07


RD-R203-001 Governing the Commons → supports → MECH-009 / MECH-010
RD-R203-002 Evolution of Cooperation → proposes → MECH-008
RD-R203-003 Institutions, Institutional Change → supports → MECH-010
RD-R203-004 Secret of Our Success → supports → MECH-009 / collective learning
RD-R203-005 Culture and the Evolutionary Process → supports → M-05 / MECH-008
RD-R203-006 Diversity and Complexity → extends → network coordination models


Domain realization


TP-07 → emerges_in → D7 Social Systems



TP-08 Symbolic Stabilization subgraph


Threshold definition


TP-08
requires → PR-048 Model
requires → PR-050 Memory
requires → PR-051 Symbol
requires → PR-053 Meaning
requires → PR-055 Narrative
requires → M-03 Signal Transmission System
requires → M-07 Symbolic Meaning System
requires → M-10 Narrative Dynamics Engine


Mechanisms feeding TP-08


MECH-011 Sign Stabilization → instantiates → M-07
MECH-012 Semantic Reinforcement → mediates → TP-08
MECH-013 Archival Persistence → clarifies → PR-050 / PR-055


Readings feeding TP-08


RD-R204-001 The Symbolic Species → supports → MECH-011
RD-R204-002 Saussure → clarifies → PR-051 / PR-053
RD-R204-003 Peirce → clarifies → PR-051 / PR-053 / sign process
RD-R204-004 Theory of Semiotics → supports → MECH-012
RD-R204-005 Metaphors We Live By → extends → semantic structuring
RD-R204-006 Structural Anthropology → supports → PR-055 / myth structure
RD-R204-007 Hero With a Thousand Faces → supports → M-10


Domain realization


TP-08 → emerges_in → D8 Symbolic Systems



TP-09 Reflexive Knowledge subgraph


Threshold definition


TP-09
requires → PR-018 Constraint
requires → PR-048 Model
requires → PR-049 Prediction
requires → PR-050 Memory
requires → PR-055 Narrative
requires → M-02 Feedback Regulator
requires → M-06 Observer–Model Loop
requires → M-07 Symbolic Meaning System
requires → M-10 Narrative Dynamics Engine


Mechanisms feeding TP-09


MECH-014 Model Comparison → mediates → TP-09
MECH-015 Epistemic Correction Loop → instantiates → M-02 / M-06
MECH-016 Scientific Institutionalization → mediates → TP-09


Readings feeding TP-09


RD-R205-001 Structure of Scientific Revolutions → supports → MECH-014 / MECH-016
RD-R205-002 Logic of Scientific Discovery → proposes → MECH-015
RD-R205-003 Methodology of Scientific Research Programmes → extends → MECH-014
RD-R205-004 Against Method → critiques → rigid correction models
RD-R205-005 Science as Social Knowledge → supports → MECH-016
RD-R205-006 Science in Action → extends → institutional reflexivity
RD-R205-007 Scientific Image → clarifies → PR-048 / representation


Domain realization


TP-09 → emerges_in → D9 Reflexive Systems



IV. Cross-Threshold Hub Analysis


Certain primitives, modules, and mechanisms act as graph hubs.


Primitive hubs

Hub
Why it matters
PR-050 Memory
appears in TP-05 through TP-09; persistence is the backbone of higher-order emergence
PR-048 Model
central from TP-06 upward; once internal or explicit representation appears, the stack becomes reflexive
PR-027 Information
decisive at life and mind thresholds
PR-005 Boundary
decisive at life and social threshold formation
PR-018 Constraint
decisive for law, regulation, and epistemic governance

Module hubs

Hub
Why it matters
M-02 Feedback Regulator
persistence and correction across life, mind, and reflexive systems
M-06 Observer–Model Loop
central engine for cognition, society, and science
M-07 Symbolic Meaning System
central engine for symbolic order and reflexive knowledge
M-05 Evolution Engine
bridges life, society, and culture

Mechanism hubs

Hub
Why it matters
MECH-005 Predictive Processing
best current bridge into observer emergence
MECH-010 Institutional Persistence
bridges coordination into durable society
MECH-013 Archival Persistence
bridges symbol into long-lived culture
MECH-015 Epistemic Correction Loop
converts symbolic culture into reflexive knowledge


V. Cross-Lane Bridge Edges


These are the most important inter-lane graph links.


TP-05 → enables → TP-06
because life must stabilize memory and information before observers appear

TP-06 → enables → TP-07
because observers must exist before coordinated supra-individual systems can form

TP-07 → enables → TP-08
because social coordination must stabilize before durable symbolic systems emerge

TP-08 → enables → TP-09
because symbolic order must exist before explicit model comparison and correction norms can arise


This yields the upper-stack causal chain:


life
→ observer
→ society
→ symbolic order
→ reflexive knowledge



VI. Minimal Research Graph Table


This is the smallest first-pass graph matrix you can actually use while reading.

Reading ID
Supports Threshold
Key Mechanism
Key Primitives
Key Module
RD-R201-001
TP-05
Metabolic Throughput
Boundary, Information, Stability
Resource Flow
RD-R201-003
TP-05
Autocatalytic Closure
System, Emergence, Constraint
Self-Organization
RD-R202-001
TP-06
Predictive Processing
Model, Prediction, Memory
Observer–Model Loop
RD-R202-003
TP-06
Embodied Coupling
Observation, Information, Boundary
Signal Transmission
RD-R203-001
TP-07
Institutional Persistence
Network, Constraint, Memory
Network Interaction
RD-R203-002
TP-07
Repeated Coordination
Flow, Network, Strategy
Evolution Engine
RD-R204-001
TP-08
Sign Stabilization
Symbol, Meaning, Memory
Symbolic Meaning System
RD-R204-002
TP-08
Structural Signification
Symbol, Meaning, Relation
Symbolic Meaning System
RD-R205-001
TP-09
Model Comparison
Model, Narrative, Memory
Observer–Model Loop
RD-R205-002
TP-09
Epistemic Correction
Constraint, Prediction, Model
Feedback Regulator


VII. Recommended Local Storage Model


Store the graph in two forms.


The first is human-readable markdown:


research/indexes/research-knowledge-graph.md


The second is machine-readable JSON:


data/research_knowledge_graph.json


Recommended JSON shape:


{
  "nodes": [
    {"id": "TP-05", "type": "threshold", "label": "Biosis Threshold"},
    {"id": "M-05", "type": "module", "label": "Evolution Engine"},
    {"id": "PR-050", "type": "primitive", "label": "Memory"},
    {"id": "MECH-001", "type": "mechanism", "label": "Autocatalytic Closure"},
    {"id": "RD-R201-001", "type": "reading", "label": "The Vital Question"}
  ],
  "edges": [
    {"source": "RD-R201-001", "target": "MECH-002", "relation": "supports"},
    {"source": "MECH-002", "target": "M-09", "relation": "instantiates"},
    {"source": "TP-05", "target": "PR-050", "relation": "requires"}
  ]
}



VIII. Query Logic


Once the graph exists, the highest-value queries are:


show all readings supporting TP-05
show all thresholds requiring Memory
show all modules connected to Model
show all mechanisms shared by TP-08 and TP-09
show all readings that clarify Symbol and Meaning


These are the queries that turn the framework into a research operating system.



IX. Most Important Consequence


The graph makes the system navigable in a way the reading list alone cannot.


A reading list tells you:


what to read


The graph tells you:


why it matters
where it connects
what it unlocks
what else it depends on


That is the difference between a bibliography and a knowledge engine.



X. What should come next


The strongest next move is to convert this graph into a Research Dashboard Pack, meaning three concrete artifacts:


1. Reading Tracker
2. Mechanism Tracker
3. Threshold Progress Board


That would let you track, in one place, which sources are acquired, read, annotated, mapped to mechanisms, and integrated into threshold models.