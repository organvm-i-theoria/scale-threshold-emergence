---
id: uaks_v1_graphql_spec_20260311
title: GraphQL Interface Specification
type: technical-spec
status: drafted_in_chat
version: 1
---

# GraphQL Interface Specification

## Purpose

Defines the GraphQL API for querying the knowledge substrate.

## Schema Overview

```graphql
type Query {
  atom(id: ID!): Atom
  atoms(filter: AtomFilter, limit: Int): [Atom!]!
  search(query: String!, limit: Int): [Atom!]!
  related(id: ID!, limit: Int): [Atom!]!
}

type Mutation {
  importAtoms(input: ImportInput!): ImportResult!
  updateAtom(id: ID!, input: AtomInput!): Atom!
  deleteAtom(id: ID!): Boolean!
}

type Atom {
  id: ID!
  name: String!
  type: AtomType!
  definition: String
  relations: [Relation!]!
  provenance: Provenance!
  trust: TrustLevel!
}

enum AtomType {
  PRIMITIVE
  MECHANISM
  MODULE
  THRESHOLD
}
```

## TODO Implementation

```python
# src/api/graphql/schema.py

import strawberry

@strawberry.type
class Query:
    @strawberry.field
    def atom(self, id: strawberry.ID) -> Atom:
        # TODO: Implement
        pass
    
    @strawberry.field
    def search(self, query: str, limit: int = 10) -> list[Atom]:
        # TODO: Implement
        pass
```

## Acceptance Criteria

- [ ] All CRUD operations supported
- [ ] Filtering works on all atom fields
- [ ] Pagination works correctly
- [ ] Error handling returns useful messages
