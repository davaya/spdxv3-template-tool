# SPDX v3 Element Serialization

In the SPDX v3 logical model the Element is the basic unit of information, and every Element is separate from
and independent of every other Element. An SPDX document is the serialized value of one or more Elements.

## UnitOfTransfer

The UnitOfTransfer type defines the structure of the serialized data in an SPDX v3 document.
An Element of the Document type contains metadata describing an SPDX document.

A document contains:
1. the document unique identifier (namespace)
2. a set of one or more related or unrelated Elements
3. optional references to other documents, allowing elements in those documents to be located, verified and referenced 
4. optional namespace prefixes used to shorten Element identifiers
5. optional default values for common element properties (specVersion, created (who and when), profiles, and dataLicense)

Elements created in the same minting operation as the document are related by having the document's creation info.
Elements created in a document have the document namespace as their id prefix.
A document thus carries Elements in three categories:
1. Elements created as part of the document (id is within document namespace, element and document creation info match)
2. References to documents containing previously-created Elements
3. Copies of previously-created Elements (id is not within document namespace, element and document creation info are different)

## Design Considerations

Every Element reference can be verified for integrity as a member of one or more documents.
An individual Element created in one document can be copied into another document,
and references to each of those documents can be verified for integrity.
In particular, serializing an Element value into a single-Element document allows each
Element to be verified by a single integrity check value regardless of any
documents it was created in or copied to.

Document Element ID (namespace or namespace + reserved name "SPDX-Document")
