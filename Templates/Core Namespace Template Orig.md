# Core Namespace Specification


## Namespace Summary

The Core namespace defines foundational concepts serving as the basis for all SPDX-3.0 profiles.

## 1 Classes

### 1.1 Element 

#### 1.1.1 Summary

Base domain class from which all other SPDX-3.0 domain classes derive.

#### 1.1.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | Element |
| SubclassOf | none |
| Instantiability | Abstract |
| Status | stable |

#### 1.1.3 Description

An Element is a representation of a fundamental concept either directly inherent to the Bill of Materials (BOM) domain or indirectly related to the BOM domain and necessary for contextually characterizing BOM concepts and relationships. Within SPDX-3.0 structure this is the base class acting as a consistent, unifying, and interoperable foundation for all explicit and inter-relatable content objects.

#### 1.1.4 Shape

| Property | Datatype | Min Count | Max Count | Format |
|:--|:--|:--| :--| :--|
| id | idString | 1 | 1 | |
| name | xsd:string | 1 | 1 | |
| summary | xsd:string | 0 | 1 | |
| description | xsd:string | 0 | 1 | |
| comment | xsd:string | 0 | 1 | |
| specVersion | xsd:string | 0 | 1 | |
| createdTime | DateTime | 1 | 1 | |
| createdBy | Identity | 0 | * | |
| dataLicense | ?? | ?? | ?? | |
| profile | ProfileIdentifier| 1 | * | |
| externalReference | ExternalReference | 0 | * | |
| extension | Extension | 0 | * | |
| verifiedUsing | IntegrityMethod | 0 | * | |

#### 1.1.5 Examples

<This section provides any relevant serialized examples of this class.>


### 1.2.1 Document 

#### 1.2.1 Summary

A grouping of SPDX-3.0 content with no presumption of shared context.


#### 1.2.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | Document |
| SubclassOf | Element |
| Instantiability | Concrete |
| Status | stable |

#### 1.2.3 Description

A Document is a container for a grouping of SPDX-3.0 content with no presumption of shared context.

#### 1.2.4 Shape

| Property | Datatype | Min Count | Max Count | Format |
|:--|:--|:--| :--| :--|
| namespace | URI | 1 | 1 | |
| externalMap | ExternalMap | 0 | * | |
| element | Element | 1 | * | |
| rootElement | Element | 1 | * | |

#### 1.2.5 Examples

<This section provides any relevant serialized examples of this class.>


### 1.3 Relationship 

#### 1.3.1 Summary
Describes a relationship between one or more elements.

#### 1.3.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | Relationship |
| SubclassOf | Element |
| Instantiability | Concrete |
| Status | stable |

#### 1.3.3 Description

A Relationship is a grouping of characteristics unique to an assertion that one Element is related to one or more other Elements in some way.

#### 1.3.4 Shape

| Property | Datatype | Min Count | Max Count | Format |
|:--|:--|:--| :--| :--|
| from | Element | 1 | 1 | |
| to | Element | 1 | * | |
| relationshipType | RelationshipTypeVocab | 1 | 1 | |
| completeness | RelationshipCompletenessVocab | 0 | 1 | |

#### 1.3.5 Examples

<This section provides any relevant serialized examples of this class.>

### 1.4 External Map

#### 1.4.1 Summary
A map of Element identifiers that are used within a Document but defined external to that Document.

#### 1.4.2 Metadata

| Attribute | Value |
| :-------- | :---- |
| id | IRI |
| name | ExternalMap |
| SubclassOf | none |
| Instantiability | Concrete |
| Status | stable |

#### 1.4.3 Description

An External Map is a map of Element identifiers that are used within a Document but defined external to that Document. The external map provides details about the externally-defined Element such as its provenance, where to retrieve it, and how to verify its integrity.

#### 1.4.4 Shape

| Property | Datatype | Min Count | Max Count | Format |
|:--|:--|:--| :--| :--|
| externalID | IDString | 1 | 1 | |
| verifiedUsing | IntegrityMethod | 0 | * | |
| elementURL | URL | 0 | * | |
| createdBy | Identity | 0 | 1 | |
| definingDocument | IDString (Document) | 0 | 1 | |

#### 1.4.5 Examples

<This section provides any relevant serialized examples of this class.>


### 1.5 Extension
#### 1.5.1 Summary

A grouping of characteristics unique to a particular aspect of an Element.

#### 1.5.2 Metadata

| Attribute | Value |
| :-------- | :---- |
| id | IRI |
| name | Extension |
| SubclassOf | none |
| Instantiability | Abstract |
| Status | stable |

#### 1.5.3 Description

An Extension is a grouping of characteristics unique to a particular aspect of an Element.
Extension acts as an abstract class basis for defining specific subclasses for characterizing some particular aspect of an Element. This supports custom extension of SPDX-3.0 in a structured fashion for specific adopting contexts, for agile evolution of practical use of SPDX-3.0, and for SPDX-3.0 internal specification of aspect characterization relevant across different Element subclasses.

####1.5.4 Shape

| Property | Datatype | Min Count | Max Count | Format |
|:--|:--|:--| :--| :--|

#### 1.5.5 Examples

<This section provides any relevant serialized examples of this class.>


### 1.6 External Reference
#### 1.6.1 Summary

A reference to a resource outside of the scope of SPDX-3.0 content.

#### 1.6.2 Metadata

| Attribute | Value |
| :-------- | :---- |
| id | IRI |
| name | ExternalReference |
| SubclassOf | none |
| Instantiability | Concrete |
| Status | stable |

#### 1.6.3 Description

An External Reference is a grouping of characteristics unique to the identity, location and context of a resource outside of the scope of SPDX-3.0 content.

#### 1.6.4 Shape

| Property | Datatype | Min Count | Max Count | Format |
|:--|:--|:--| :--| :--|
| externalReferenceType | ExternalReferenceTypeVocab | 0 | 1 | |
| locator | URI | 0 | * | |
| comment | xsd:string | 0 | 1 | |

#### 1.6.5 Examples

<This section provides any relevant serialized examples of this class.>


### 1.7 Annotation
#### 1.7.1 Summary

An assertion made in relation to one or more elements.

#### 1.7.2 Metadata

| Attribute | Value |
| :-------- | :---- |
| id | IRI |
| name | Annotation |
| SubclassOf | Element |
| Instantiability | Concrete |
| Status | stable |

#### 1.7.3 Description

An Annotation is an assertion made in relation to one or more elements.

#### 1.7.4 Shape

| Property | Datatype | Min Count | Max Count | Format |
|:--|:--|:--| :--| :--|
| annotationType | AnnotationTypeVocab | 1 | 1 | |
| statement | xsd:string | 1 | 1 | |
| element | Element | 1 | * | |

#### 1.7.5 Examples

<This section provides any relevant serialized examples of this class.>


### 1.8 Artifact


#### 1.8.1 Summary

A distinct article or unit within the digital domain.

#### 1.8.2 Metadata

| Attribute | Value |
| :-------- | :---- |
| id | IRI |
| name | Artifact |
| SubclassOf | Element; Agent |
| Instantiability | Abstract |
| Status | unstable |

#### 1.8.3 Description

An artifact is a distinct article or unit within the digital domain such as an electronic file, a software package, a device or an element of data.

#### 1.8.4 Shape

| Property | Datatype | Min Count | Max Count | Format |
|:--|:--|:--| :--| :--|
| artifactURL | ArtifactURL | 0 | 1 | |
| originatedBY | Identity | 0 | 1 | |

#### 1.8.5 Examples

<This section provides any relevant serialized examples of this class.>


### 1.9 Contextual Collection 

#### 1.9.1 Summary

A container for a grouping of SPDX-3.0 content with a specific shared context.

#### 1.9.2 Metadata

| Attribute | Value |
| :-------- | :---- |
| id | IRI |
| name | ContextualCollection |
| SubclassOf | Artifact |
| Instantiability | Concrete |
| Status | stable |

#### 1.9.3 Description

A Contextual Collection is a container for a grouping of SPDX-3.0 content with a specific shared context.

#### 1.9.4 Shape

| Property | Datatype | Min Count | Max Count | Format |
|:--|:--|:--| :--| :--|
| element | Element | 1 | * | |
| rootElement | Element | 1 | * | |

#### 1.9.5 Examples

<This section provides any relevant serialized examples of this class.>


### 1.9 Contextual Collection 

#### 1.9.1 Summary

A container for a grouping of SPDX-3.0 content with a specific shared context.

#### 1.9.2 Metadata

| Attribute | Value |
| :-------- | :---- |
| id | IRI |
| name | ContextualCollection |
| SubclassOf | Artifact |
| Instantiability | Concrete |
| Status | stable |

#### 1.9.3 Description

A Contextual Collection is a container for a grouping of SPDX-3.0 content with a specific shared context.

#### 1.9.4 Shape

| Property | Datatype | Min Count | Max Count | Format |
|:--|:--|:--| :--| :--|
| element | Element | 1 | * | |
| rootElement | Element | 1 | * | |

#### 1.9.5 Examples

<This section provides any relevant serialized examples of this class.>


### 1.10 BOM
#### 1.10.1 Summary

A container for a grouping of SPDX-3.0 content characterizing details (provenence, composition, licensing, etc.) about a product.

#### 1.10.2 Metadata

| Attribute | Value |
| :-------- | :---- |
| id | IRI |
| name | BOM|
| SubclassOf | ContextualCollection |
| Instantiability | Concrete |
| Status | stable |

#### 1.10.3 Description

An BOM is a container for a grouping of SPDX-3.0 content characterizing details about a product. This could include details of the content and composition of the product, provenence details of the product and/or its composition, licensing information, known quality or security issues, etc.

#### 1.10.4 Shape

| Property | Datatype | Min Count | Max Count | Format |
|:--|:--|:--| :--| :--|
| element | Element | 1 | * | |
| rootElement | Element | 1 | * | |

#### 1.10.5 Examples

<This section provides any relevant serialized examples of this class.>


### 1.11 Hash 

#### 1.11.1 Summary

A hash is a mathematically calculated representation of a grouping of data commonly used for integrity checking of the data.

#### 1.11.2 Metadata

| Attribute | Value |
| :-------- | :---- |
| id | IRI |
| name | Hash |
| SubclassOf | IntegrityMethod |
| Instantiability | Concrete |
| Status | stable |

#### 1.11.3 Description

A hash is a grouping of characteristics unique to the result of applying a mathematical algorithm that maps data of arbitrary size to a bit string (the ‘hash’) and is a one-way function, that is, a function which is practically infeasible to invert. This is commonly used for integrity checking of data.

#### 1.11.4 Shape

| Property | Datatype | Min Count | Max Count | Format |
|:--|:--|:--| :--| :--|
| hashAlgorithm | HashAlgorithm | 1 | 1 | |
| hashValue | xsd:string | 1 | 1 | |

#### 1.11.5 Examples

<This section provides any relevant serialized examples of this class.>


### 1.12 Public Key 

#### 1.12.1 Summary

<public key summary>

#### 1.12.2 Metadata

| Attribute | Value |
| :-------- | :---- |
| id | IRI |
| name | PublicKey |
| SubclassOf | IntegrityMethod |
| Instantiability | Concrete |
| Status | stable |

#### 1.12.3 Description

<public key description>

#### 1.12.4 Shape

| Property | Datatype | Min Count | Max Count | Format |
|:--|:--|:--| :--| :--|
| ??| ?? | ?? | ?? | |
| ??| ?? | ?? | ?? | |

#### 1.12.5 Examples

<This section provides any relevant serialized examples of this class.>


### 1.13 Agent

#### 1.13.1 Summary

An entity responsible for an action taking place.

#### 1.13.2 Metadata

| Attribute | Value |
| :-------- | :---- |
| id | IRI |
| name | Agent |
| SubclassOf | Element |
| Instantiability | Abstract |
| Status | stable |

#### 1.13.3 Description

An Agent is an entity responsible for an action taking place.

#### 1.13.4 Shape

| Property | Datatype | Min Count | Max Count | Format |
|:--|:--|:--| :--| :--|
| ?? | ?? | ?? | ?? | |
| ?? | ?? | ?? | ?? | |

#### 1.13.5 Examples

<This section provides any relevant serialized examples of this class.>



### 1.14 Identity 

#### 1.14.1 Summary

An individual or organization.

#### 1.14.2 Metadata

| Attribute | Value |
| :-------- | :---- |
| id | IRI |
| name | Identity |
| SubclassOf | Agent |
| Instantiability | Concrete |
| Status | stable |

#### 1.14.3 Description

An Identity is a grouping of identifying characteristics unique to an individual or organization.

#### 1.14.4 Shape

| Property | Datatype | Min Count | Max Count | Format |
|:--|:--|:--| :--| :--|
| name | xsd:string | 1 | 1 | |
| ?? | ?? | ?? | ?? | |

#### 1.14.5 Examples

<This section provides any relevant serialized examples of this class.>


### 1.15 Person 

#### 1.15.1 Summary

An individual human being.

#### 1.15.2 Metadata

| Attribute | Value |
| :-------- | :---- |
| id | IRI |
| name | Person |
| SubclassOf | Identity |
| Instantiability | Concrete |
| Status | stable |

#### 1.15.3 Description

An Person is an individual human being.

#### 1.15.4 Shape

| Property | Datatype | Min Count | Max Count | Format |
|:--|:--|:--| :--| :--|
| name | xsd:string | 1 | 1 | |
| ?? | ?? | ?? | ?? | |

#### 1.15.5 Examples

<This section provides any relevant serialized examples of this class.>


### 1.16 Organization 

#### 1.16.1 Summary

A group of people who work together in an organized way for a shared purpose.

#### 1.16.2 Metadata

| Attribute | Value |
| :-------- | :---- |
| id | IRI |
| name | Organization |
| SubclassOf | Identity |
| Instantiability | Concrete |
| Status | stable |

#### 1.16.3 Description

An Organization is a group of people who work together in an organized way for a shared purpose.

#### 1.16.4 Shape

| Property | Datatype | Min Count | Max Count | Format |
|:--|:--|:--| :--| :--|
| name | xsd:string | 1 | 1 | |
| ?? | ?? | ?? | ?? | |

#### 1.16.5 Examples

<This section provides any relevant serialized examples of this class.>


### 1.17 Tool 

#### 1.17.1 Summary

An element of hardware and/or software utilized to carry out a particular function.

#### 1.17.2 Metadata

| Attribute | Value |
| :-------- | :---- |
| id | IRI |
| name | Tool |
| SubclassOf | Agent |
| Instantiability | Concrete |
| Status | stable |

#### 1.17.3 Description

A Tool is an element of hardware and/or software utilized to carry out a particular function.

#### 1.17.4 Shape

| Property | Datatype | Min Count | Max Count | Format |
|:--|:--|:--| :--| :--|
| name | xsd:string | 1 | 1 | |
| ?? | ?? | ?? | ?? | |

#### 1.17.5 Examples

<This section provides any relevant serialized examples of this class.>


.>



## 2 Properties

### 2.1 id 

#### 2.1.1 Summary

<Brief summary description of the purpose and semantic meaning of the property.>

#### 2.1.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | id |
| Property Nature | DatatypeProperty |
| Range | IDString |
| Status | stable|

#### 2.1.3 Description

<Full description of the purpose and semantic meaning of the property.>

#### 2.1.5 Examples

<This section provides any relevant serialized examples of this property.>



### 2.2 name

#### 2.2.1 Summary

<Brief summary description of the purpose and semantic meaning of the property.>

#### 2.2.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | name |
| Property Nature | DatatypeProperty |
| Range | xsd:string |
| Status | stable |

#### 2.2.3 Description

<Full description of the purpose and semantic meaning of the property.>

#### 2.2.5 Examples

<This section provides any relevant serialized examples of this property.>



### 2.3 summary 

#### 2.3.1 Summary

<Brief summary description of the purpose and semantic meaning of the property.>

#### 2.3.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | summary |
| Property Nature | DatatypeProperty |
| Range | xsd:string |
| Status | stable |

#### 2.<n>.3 Description

<Full description of the purpose and semantic meaning of the property.>

#### 2.<n>.5 Examples

<This section provides any relevant serialized examples of this property.>



### 2.4 description

#### 2.4.1 Summary

<Brief summary description of the purpose and semantic meaning of the property.>

#### 2.4.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | description|
| Property Nature | DatatypeProperty |
| Range | xsd:string |
| Status | stable |

#### 2.4.3 Description

<Full description of the purpose and semantic meaning of the property.>

#### 2.4.5 Examples

<This section provides any relevant serialized examples of this property.>


### 2.5 comment

#### 2.5.1 Summary

<Brief summary description of the purpose and semantic meaning of the property.>

#### 2.5.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | comment|
| Property Nature | DatatypeProperty |
| Range | xsd:string |
| Status | stable |

#### 2.5.3 Description

<Full description of the purpose and semantic meaning of the property.>

#### 2.5.5 Examples

<This section provides any relevant serialized examples of this property.>


### 2.6 specVersion

#### 2.6.1 Summary

<Brief summary description of the purpose and semantic meaning of the property.>

#### 2.6.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | specVersion |
| Property Nature | DatatypeProperty |
| Range | xsd:string |
| Status | stable |

#### 2.6.3 Description

<Full description of the purpose and semantic meaning of the property.>

#### 2.6.5 Examples

<This section provides any relevant serialized examples of this property.>



### 2.7 createdTime

#### 2.7.1 Summary

<Brief summary description of the purpose and semantic meaning of the property.>

#### 2.7.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | createdTime|
| Property Nature | DatatypeProperty |
| Range | xsd:dateTime |
| Status | stable |

#### 2.7.3 Description

<Full description of the purpose and semantic meaning of the property.>

#### 2.7.5 Examples

<This section provides any relevant serialized examples of this property.>



### 2.8 profile

#### 2.8.1 Summary

<Brief summary description of the purpose and semantic meaning of the property.>

#### 2.8.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | profile|
| Property Nature | DatatypeProperty |
| Range | ProfileIdentifier |
| Status | stable |

#### 2.8.3 Description

<Full description of the purpose and semantic meaning of the property.>

#### 2.8.5 Examples

<This section provides any relevant serialized examples of this property.>



### 2.9 dataLicense

#### 2.9.1 Summary

<Brief summary description of the purpose and semantic meaning of the property.>

#### 2.9.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | dataLicense |
| Property Nature | ?? |
| Range | ?? |
| Status | stable |

#### 2.9.3 Description

<Full description of the purpose and semantic meaning of the property.>

#### 2.9.5 Examples

<This section provides any relevant serialized examples of this property.>


### 2.10 createdBy

#### 2.10.1 Summary

<Brief summary description of the purpose and semantic meaning of the property.>

#### 2.10.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | createdBy |
| Property Nature | ObjectProperty |
| Range | Agent |
| Status | stable |

#### 2.10.3 Description

<Full description of the purpose and semantic meaning of the property.>

#### 2.10.5 Examples

<This section provides any relevant serialized examples of this property.>


### 2.11 externalReference

#### 2.11.1 Summary

<Brief summary description of the purpose and semantic meaning of the property.>

#### 2.11.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | externalReference |
| Property Nature | ObjectProperty |
| Range | ExternalReference |
| Status | stable |

#### 2.11.3 Description

<Full description of the purpose and semantic meaning of the property.>

#### 2.11.5 Examples

<This section provides any relevant serialized examples of this property.>


### 2.12 extension

#### 2.12.1 Summary

<Brief summary description of the purpose and semantic meaning of the property.>

#### 2.12.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | extension |
| Property Nature | ObjectProperty |
| Range | Extension |
| Status | stable |

#### 2.12.3 Description

<Full description of the purpose and semantic meaning of the property.>

#### 2.12.5 Examples

<This section provides any relevant serialized examples of this property.>



### 2.13 verifiedUsing

#### 2.13.1 Summary

<Brief summary description of the purpose and semantic meaning of the property.>

#### 2.13.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | everifiedUsing |
| Property Nature | ObjectProperty |
| Range | IntegrityMethod |
| Status | stable |

#### 2.13.3 Description

<Full description of the purpose and semantic meaning of the property.>

#### 2.13.5 Examples

<This section provides any relevant serialized examples of this property.>



### 2.14 relationshipType

#### 2.14.1 Summary

<Brief summary description of the purpose and semantic meaning of the property.>

#### 2.14.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | relationshipType |
| Property Nature | DatatypeProperty |
| Range | RelationshipTypeVocab |
| Status | stable |

#### 2.14.3 Description

<Full description of the purpose and semantic meaning of the property.>

#### 2.14.5 Examples

<This section provides any relevant serialized examples of this property.>


### 2.15 from

#### 2.15.1 Summary

<Brief summary description of the purpose and semantic meaning of the property.>

#### 2.15.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | from |
| Property Nature | ObjectProperty |
| Range | Element |
| Status | stable |

#### 2.15.3 Description

<Full description of the purpose and semantic meaning of the property.>

#### 2.15.5 Examples

<This section provides any relevant serialized examples of this property.>


### 2.16 to

#### 2.16.1 Summary

<Brief summary description of the purpose and semantic meaning of the property.>

#### 2.16.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | to |
| Property Nature | ObjectProperty |
| Range | Element |
| Status | stable |

#### 2.16.3 Description

<Full description of the purpose and semantic meaning of the property.>

#### 2.16.5 Examples

<This section provides any relevant serialized examples of this property.>



### 2.17 completeness

#### 2.17.1 Summary

<Brief summary description of the purpose and semantic meaning of the property.>

#### 2.17.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | completeness |
| Property Nature | DatatypeProperty |
| Range | RelationshipCompletenessVocab |
| Status | stable |

#### 2.17.3 Description

<Full description of the purpose and semantic meaning of the property.>

#### 2.17.5 Examples

<This section provides any relevant serialized examples of this property.>


### 2.18 annotationType

#### 2.18.1 Summary

<Brief summary description of the purpose and semantic meaning of the property.>

#### 2.18.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | annotationType |
| Property Nature | DatatypeProperty |
| Range | AnnotationTypeVocab |
| Status | stable |

#### 2.18.3 Description

<Full description of the purpose and semantic meaning of the property.>

#### 2.18.5 Examples

<This section provides any relevant serialized examples of this property.>



### 2.19 statement

#### 2.19.1 Summary

<Brief summary description of the purpose and semantic meaning of the property.>

#### 2.19.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | statement |
| Property Nature | DatatypeProperty |
| Range | xsd:string |
| Status | stable |

#### 2.19.3 Description

<Full description of the purpose and semantic meaning of the property.>

#### 2.19.5 Examples

<This section provides any relevant serialized examples of this property.>



### 2.20 element

#### 2.20.1 Summary

<Brief summary description of the purpose and semantic meaning of the property.>

#### 2.20.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | element |
| Property Nature | ObjectProperty |
| Range | Element |
| Status | stable |

#### 2.20.3 Description

<Full description of the purpose and semantic meaning of the property.>

#### 2.20.5 Examples

<This section provides any relevant serialized examples of this property.>



### 2.21 rootElement

#### 2.21.1 Summary

<Brief summary description of the purpose and semantic meaning of the property.>

#### 2.21.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | rootElement |
| Property Nature | ObjectProperty |
| Range | Element |
| Status | stable |

#### 2.20.3 Description

<Full description of the purpose and semantic meaning of the property.>

#### 2.20.5 Examples

<This section provides any relevant serialized examples of this property.>



### 2.22 namespace

#### 2.22.1 Summary

<Brief summary description of the purpose and semantic meaning of the property.>

#### 2.22.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | namespace |
| Property Nature | DatatypeProperty |
| Range | URI |
| Status | stable |

#### 2.22.3 Description

<Full description of the purpose and semantic meaning of the property.>

#### 2.22.5 Examples

<This section provides any relevant serialized examples of this property.>



### 2.23 externalMap

#### 2.23.1 Summary

<Brief summary description of the purpose and semantic meaning of the property.>

#### 2.23.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | externalMap |
| Property Nature | ObjectProperty |
| Range | ExternalMap |
| Status | stable |

#### 2.23.3 Description

<Full description of the purpose and semantic meaning of the property.>

#### 2.23.5 Examples

<This section provides any relevant serialized examples of this property.>



### 2.24 externalID

#### 2.24.1 Summary

<Brief summary description of the purpose and semantic meaning of the property.>

#### 2.24.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | externalID |
| Property Nature | DatatypeProperty |
| Range | IDString |
| Status | stable |

#### 2.24.3 Description

<Full description of the purpose and semantic meaning of the property.>

#### 2.24.5 Examples

<This section provides any relevant serialized examples of this property.>



### 2.25 elementURL

#### 2.25.1 Summary

<Brief summary description of the purpose and semantic meaning of the property.>

#### 2.25.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | elementURL |
| Property Nature | DatatypeProperty |
| Range | URI |
| Status | stable |

#### 2.24.3 Description

<Full description of the purpose and semantic meaning of the property.>

#### 2.24.5 Examples

<This section provides any relevant serialized examples of this property.>



### 2.26 definingDocument

#### 2.26.1 Summary

<Brief summary description of the purpose and semantic meaning of the property.>

#### 2.26.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | definingDocument |
| Property Nature | ObjectProperty |
| Range | Document |
| Status | stable |

#### 2.26.3 Description

<Full description of the purpose and semantic meaning of the property.>

#### 2.26.5 Examples

<This section provides any relevant serialized examples of this property.>



### 2.27 externalReferenceType

#### 2.27.1 Summary

<Brief summary description of the purpose and semantic meaning of the property.>

#### 2.27.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | externalReferenceType |
| Property Nature | DatatypeProperty |
| Range | ExternalReferenceTypeVocab |
| Status | stable |

#### 2.27.3 Description

<Full description of the purpose and semantic meaning of the property.>

#### 2.27.5 Examples

<This section provides any relevant serialized examples of this property.>



### 2.28 locator

#### 2.28.1 Summary

<Brief summary description of the purpose and semantic meaning of the property.>

#### 2.28.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | locator |
| Property Nature | DatatypeProperty |
| Range | URI |
| Status | stable |

#### 2.28.3 Description

<Full description of the purpose and semantic meaning of the property.>

#### 2.28.5 Examples

<This section provides any relevant serialized examples of this property.>



### 2.29 artifactURL

#### 2.29.1 Summary

<Brief summary description of the purpose and semantic meaning of the property.>

#### 2.29.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | artifactURL |
| Property Nature | DatatypeProperty |
| Range | URI |
| Status | stable |

#### 2.29.3 Description

<Full description of the purpose and semantic meaning of the property.>

#### 2.29.5 Examples

<This section provides any relevant serialized examples of this property.>



### 2.30 hashAlgorithm

#### 2.30.1 Summary

<Brief summary description of the purpose and semantic meaning of the property.>

#### 2.30.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | hashAlgorithm |
| Property Nature | DatatypeProperty |
| Range | HashAlgorithmVocab |
| Status | stable |

#### 2.30.3 Description

<Full description of the purpose and semantic meaning of the property.>

#### 2.30.5 Examples

<This section provides any relevant serialized examples of this property.>



### 2.31 hashValue

#### 2.31.1 Summary

<Brief summary description of the purpose and semantic meaning of the property.>

#### 2.31.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | hashValue |
| Property Nature | DatatypeProperty |
| Range | xsd:string |
| Status | stable |

#### 2.31.3 Description

<Full description of the purpose and semantic meaning of the property.>

#### 2.31.5 Examples

<This section provides any relevant serialized examples of this property.>



### 2.32 originatedBy

#### 2.32.1 Summary

<Brief summary description of the purpose and semantic meaning of the property.>

#### 2.32.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | originatedBy |
| Property Nature | ObjectProperty |
| Range | Agent |
| Status | stable |

#### 2.32.3 Description

<Full description of the purpose and semantic meaning of the property.>

#### 2.32.5 Examples

<This section provides any relevant serialized examples of this property.>





### 2.<n> <Property Name> 

#### 2.<n>.1 Summary

<Brief summary description of the purpose and semantic meaning of the property.>

#### 2.<n>.2 Metadata

<This section specifies the metadata for the definition of this property.>

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | <Property name> |
| Property Nature | <DatatypeProperty or ObjectProperty> |
| Range (Property Type)_ | <data type (e.g., xsd:string), core:Relationship, etc.> |
| Status | <proposed or unstable or stable or deprecated> |

#### 2.<n>.3 Description

<Full description of the purpose and semantic meaning of the property.>

#### 2.<n>.5 Examples

<This section provides any relevant serialized examples of this property.>









## 3 Vocabularies

### 3.1 Hash Algorithm Vocabulary 

#### 3.1.1 Summary

<Brief summary description of the purpose and usage scope of the vocabulary.>

#### 3.1.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | HashAlgorithmVocab |
| Status | proposed |

#### 3.1.3 Description

<Full description of the purpose and semantic meaning of the vocabulary.>

#### 3.1.4 Vocabulary Entries

<This section specifies the defined entry value for this vocabulary.>

| Entry Value| Entry Description | 
|:--|:--|
| SHA1 | ?? |
| SHA224 | ?? |
| SHA256 | ?? |
| SHA384 | ?? |
| SHA512 | ?? |
| SHA3-224 | ?? |
| SHA3-256 | ?? |
| SHA3-384 | ?? |
| SHA3-512 | ?? |
| MD2 | ?? |
| MD4 | ?? |
| MD5 | ?? |
| MD6 | ?? |
| SPDX-PVC | ?? |
| BLAKE2b-256 | ?? |
| BLAKE2b-384 | ?? |
| BLAKE2b-512 | ?? |
| BLAKE3 | ?? |



### 3.2 Relationship Completeness Vocabulary 

#### 3.2.1 Summary

<Brief summary description of the purpose and usage scope of the vocabulary.>

#### 3.2.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | RelationshipCompletnessVocab|
| Status | proposed |

#### 3.2.3 Description

<Full description of the purpose and semantic meaning of the vocabulary.>

#### 3.2.4 Vocabulary Entries

<This section specifies the defined entry value for this vocabulary.>

| Entry Value| Entry Description | 
|:--|:--|
| Known | ?? |
| INCOMPLETE | ?? |
| UNKNOWN | ?? |



### 3.3 External Reference Type Vocabulary

#### 3.3.1 Summary

<Brief summary description of the purpose and usage scope of the vocabulary.>

#### 3.3.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | ExternalReferenceTypeVocab |
| Status | proposed |

#### 3.3.3 Description

<Full description of the purpose and semantic meaning of the vocabulary.>

#### 3.3.4 Vocabulary Entries

<This section specifies the defined entry value for this vocabulary.>

| Entry Value| Entry Description | 
|:--|:--|
| ?? | ?? |
| ?? | ?? |
| ?? | ?? |



### 3.4 Annotation Type Vocabulary

#### 3.4.1 Summary

<Brief summary description of the purpose and usage scope of the vocabulary.>

#### 3.4.2 Metadata

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | AnnotationTypeVocab |
| Status | proposed |

#### 3.4.3 Description

<Full description of the purpose and semantic meaning of the vocabulary.>

#### 3.4.4 Vocabulary Entries

<This section specifies the defined entry value for this vocabulary.>

| Entry Value| Entry Description | 
|:--|:--|
| ?? | ?? |
| ?? | ?? |
| ?? | ?? |



### 3.<n> <Vocabulary Name> 

#### 3.<n>.1 Summary

<Brief summary description of the purpose and usage scope of the vocabulary.>

#### 3.<n>.2 Metadata

<This section specifies the metadata for the definition of this vocabulary.>

| Attribute | Value |
|:--|:--|
| id | IRI |
| name | <Vocabulary name> |
| Status | <proposed or unstable or stable or deprecated> |

#### 3.<n>.3 Description

<Full description of the purpose and semantic meaning of the vocabulary.>

#### 3.<n>.4 Vocabulary Entries

<This section specifies the defined entry value for this vocabulary.>

| Entry Value| Entry Description | 
|:--|:--|
| ?? | ?? |



