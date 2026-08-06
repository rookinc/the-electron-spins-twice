# B32K Native D5 Offset Selector Boundary 157

Status: bounded current-source obstruction passed

## Result

The current B32K contract is compatible with registering sixty distinct
G60 addresses. It supplies 32768 catalogue positions, a registered
NULL_WELL boundary, an exact 15-bit symbol coordinate law, and the
periodic anchor law

    anchor_number = (wire_index % 15) + 1

These facts do not define which address belongs to any G60 vertex.

## Missing construction

A B32K-native selector would require all of the following:

1. A source-derived injection f from G60 vertices to B32K addresses.
2. An independently defined action rho of Aut(G60) on those addresses.
3. Covariance f(g.v) = rho(g).f(v).
4. An equivariant bridge beta from a B32K-derived five-domain to the
   actual reflected D5 offset torsor.
5. A unique premultiplier offset selected through that bridge.

The current pinned sources define none of f, rho, or beta.

## Symmetry boundary

Transporting declared addresses with vertices transports a
registration. Holding an injective address assignment fixed under all
nontrivial G60 automorphisms is incompatible with moved vertices. A
nontrivial enrichment therefore needs an independently sourced address
action and bridge.

The arithmetic projection

    projected_residue = (anchor_number - 1) % 5

is available, but it is not declared or derived as an action on the D5
offset domain. Equal cardinality is not an equivariant bridge.

## B32K contract condition

The canonical alphabet is internally hash-pinned, but 27648 alphabet
rows use plane values outside both the strict schema maximum and the
five declared top-level plane definitions. This drift is recorded as a
source boundary. It is not repaired here.

## Claim levels

- Bare G60 native selection: not reached.
- B32K native selection: not reached.
- Registered selection after declaring an address map: possible in
  principle, but not native.
- Registered multiplier offset 1 reconstruction: unchanged.

## Theorem statement

Under the current pinned B32K, B32Kv2, and registered multiplier
sources, B32K supplies a finite source-bound address origin, an exact
15-bit symbol coordinate law, and a registered periodic 15-anchor
decoration. It does not supply a source-derived injection from G60
vertices to B32K addresses, an Aut(G60) action on those addresses, or
an equivariant bridge from any B32K-derived five-set to the reflected
D5 offset torsor. Therefore current B32K does not independently select
the unresolved reflected D5 rotational offset before multiplier
decoration.

## Boundary

This is a bounded current-source obstruction. It does not prove that no
future B32K enrichment can work, does not prove a global bare-G60
impossibility, does not repair B32K schema drift, and does not change
the registered multiplier theorem.

## Keeper

B32K supplies the origin of its page. It does not transport that origin
into the pentagonal torsor.
