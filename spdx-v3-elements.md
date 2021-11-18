# SPDX v3 Element Serialization

## Context
* An Element is metadata about an entity.
* In the logical model (information as processed by applications) every Element is independent.
* An arbitrary set of Elements may be serialized as an ephemeral Bag for transfer between applications.
* Context is content shared by two or more Elements that is factored out for efficient serialization. The more the arbitrary Elements have in common, the more efficient the serialization.
* Context is **not** a part of any Element.

## Collection (Composition)
* A Collection is an entity that is **composed** of other entities.
* A Collection Element is metadata about the Collection entity.

SPDX v2:

"A Package refers to any unit of content that can be associated with a distribution of software.
Typically, a Package is composed of one or more files."

Physical example:
* A ferry load is a Bag of cars and people that have no intrinsic relationship other than being together at a specific place and time.
* A car is a Collection that is **composed** of subcomponents (engine, brakes, wheels, ...). The engine in turn is also a Collection of subcomponents.

The term "Contextual Collection" is an obstacle to understanding because it conflates
Context (which can exist between unrelated or related elements) and
Composition (which defines a hierarchical relationship between elements).
The logical model should use the term Collection for every entity that is composed of other entities.
A set of cars on a ferry is not a "non-contextual collection" because it is not a collection.
The manifest for a specific ferry trip is either an entity (e.g., a file) that can be described by a Collection Element, or the serialized Collection Element itself.

## Serialization

The logical model currently defines "Document" as a unit of transfer subclassed from Collection.
The information model uses "Element" as the unit of transfer; Document is subclassed from Artifact
and is metadata about serialized data.

A serialized Element is:
1. Element properties defined in the logical model
2. Context that exists only in a serialized unit of transfer, not in the deserialized Elements used by applications.

Context may be serialized as either a unit concatenated with Element or as a "context" Element
pseudo-property that is created at serialization and discarded at de-serialization.
The examples use the "context" property for convenience instead of a [Context, Element] pair.

Context defines:
1. default values for common properties (specVersion, created (who and when), profiles, and dataLicense)
2. IRI left substring ("namespace") values shared by more than one Element id
3. other Elements serialized in the same unit of transfer, not necessarily related
4. references to Elements not serialized in this unit that can be verified without serializing a document.
