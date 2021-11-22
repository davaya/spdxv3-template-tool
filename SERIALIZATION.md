# SPDX v3 Element Serialization

## Context
* An Element is metadata about an entity.
* Every Element is independent.
* An arbitrary Set of (related or unrelated) Elements may be serialized in a single file.
* Context is information shared by two or more Elements that can be factored out when serializing them into a file.
* Context is not part of any deserialized (logical) Element or Set of Elements.
* Context is not part of any serialized single Element file.
* The more Elements in a file and the more information those Elements have in common, the more efficient the serialization.

## Collection (Composition)
* A collection entity is composed of other entities.
* A Collection Element is metadata about a collection entity.

SPDX v2: *"A Package refers to any unit of content that can be associated with a distribution of software.
Typically, a Package is **composed** of one or more files."*

Physical example:
* A car is a Collection of subcomponents (engine, brakes, wheels, ...). The engine in turn is a Collection of subcomponents.
* A ferry is not a Collection of cars. A ferry carries a Set of cars without asserting composition.

Software Package example:
* A software package may be (but is not always) a single Artifact (e.g., a tar/rpm/deb file).
* An SPDX Package Element is metadata about a software package (whether one or more Artifacts).
* An SPDX Package Element may be serialized into a File that is distinct from the rpm file it describes.

The term "Contextual Collection" is an obstacle to understanding because it conflates
Context (which can exist between unrelated elements) and
Collection (which defines a hierarchical relationship between a component and its subcomponents).
The Set of cars on a ferry is not a "non-contextual collection" because it is not a collection.

The manifest for a ferry trip is a file entity that can be described by a File Element.
The file entity can be an office document or a serialized SPDX Element.
The manifest for a ferry trip is distinct from the physical entities described by the manifest,
just as the manifest for a software package is distinct from the software entities
(files, processes?, services?, container interfaces?) described by the manifest.

## Serialization

The logical model currently defines "Document" as a unit of transfer subclassed from Collection.
The information model defines "Element" as the unit of transfer; there is no separate Document type.

A serialized Element is:
1. Element properties defined in the logical model
2. Context that exists only in a serialized file containing two or more Elements, not in the logical Elements used by applications.

Context may be serialized as either:
1. data concatenated with Element: [context, element], or
2. a "context" Element pseudo-property that is created at serialization and discarded at de-serialization.

Context defines:
1. default values for common Element properties (specVersion, created (who and when), profiles, and dataLicense)
2. left part of an IRI common to more than one Element id
3. other related or unrelated Elements serialized in this file
4. references to other verifiable serialized Element files
