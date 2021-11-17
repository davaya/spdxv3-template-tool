# SPDX v3 Element Serialization

Design principles:
* Elements processed by applications are Information items described by an Information Model. Elements are serialized into Data items for transfer or storage.
* Abstraction includes forgetting details - after deserializing Data into an application the transfer syntax doesn't matter; multiple syntaxes yield identical processing values.
* Every Element in an application stands alone (Elements are independent). If elements are collected into groups for transfer, the grouping details are forgotten after deserializing those Elements back into an application.

These principles lead to the requirement that an Information Model must be able to
serialize any arbitrary set of Elements without imposing any constraints on their values.
Nonetheless, authors of Element sets may choose values that facilitate efficient serialization.
