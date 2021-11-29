# SPDX v3 Element Serialization

A document is a sequence of bytes such as an image or text file or the serialized value of SPDX information.
Two characteristics of the SPDX v3 logical model are the basis for the syntax of SPDX documents:
1. Every unit of information is a subtype of the abstract Element type.
2. Every Element is an independent unit of information separate from all other Elements.

As a result of these characteristics:

* Every Element type can be serialized into a document. In v2 only the Document type can be serialized into a document.
* Every document contains the serialized value of an Element plus optional Context.
* Every Element can be verified by serializing it into a single-Element document with no Context. 
* An arbitrary set of related or unrelated Elements may be included in a document's Context.
* No Element contains another Element. A Collection Element contains the IDs of its member Elements.
* A document is a file that can be described by a File element. A Document Element type is not needed to serialize Elements.

### Context

* Context is information shared by two or more Elements that can be factored out when serializing them as a document.
* Deserializing a document results in one or more Elements. Context is not included in any deserialized Element.
* The more Elements in a document and the more information those Elements have in common, the more efficient the serialization of those Elements.

Context defines:
1. default values for common Element properties (specVersion, created (who and when), profiles, and dataLicense)
2. the left part of an IRI ("namespace") common to more than one Element ID
3. other related or unrelated Elements serialized in this document
4. references to verifiable documents containing other Elements

A document's Context may be serialized either separately from the Element: (element, context),
or as a "context" pseudo-property of the Element that is created at serialization and discarded at de-serialization.

### Collection
In SPDX v2: *A Package refers to any unit of content that can be associated with a distribution of software.
Typically, a Package is composed of one or more files.*  Composition implies that the artifacts in a
package are contained within it and are destroyed if it is destroyed.

In SPDX v3 a package is collection entity - a persistent grouping of one or more artifacts.
* A Collection Element is syntactically a group Element with a set of member/child Elements 
* A Collection Element is semantically metadata about a collection entity that allows the grouping be referenced and re-used.
* A Collection Element is not a UML composition because if the collection entity is destroyed the grouping is gone but members continue to exist.

A software package may be (but is not always) a single Artifact (e.g., a tar/rpm/deb file).
* An SPDX Package Element is metadata about a software package (whether one or more Artifacts).
* An SPDX Package Element may be serialized as a File that is distinct from the rpm file it describes.

The term "Contextual Collection" is an obstacle to understanding because it conflates
Context (which exists among unrelated elements as a result of serializing them into a document)
and Collection (which defines a hierarchical relationship between a Collection element and its members).
* A document is not a Collection, contextual or otherwise.
* A document is the result of serializing any set of one or more Elements.

### Serialized Examples

**document containing a single Element**
* Artifact: can be serialized with or without context. For single-Element documents Context is overhead with little or no benefit.
* Annotation: can be serialized with 1) subject Element, 2) reference to subject Element, or 3) neither.
* Collection: can be serialized with 1) member Elements, 2) references to member Elements, or 3) neither.

**document containing three unrelated Elements**

**document containing a Collection Element, its members, and unrelated Elements**
