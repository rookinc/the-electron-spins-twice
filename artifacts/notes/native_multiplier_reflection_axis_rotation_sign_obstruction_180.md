# Native mirror-axis and rotation-sign obstruction 180

## Result

The Audit019-free native transport reaches a sharp bounded obstruction.

On the reflected-offset domain, let

- `T(k) = k + 2 mod 5`;
- `T_inverse(k) = k - 2 mod 5`;
- `U(k) = 3 - k mod 5`.

The intrinsic reflection `U` fixes offset 4 uniquely, exchanges offsets 1 and
2, and satisfies

`U T U = T_inverse`.

For every clean positive intertwiner `beta_plus`, the map

`beta_minus = U composed with beta_plus`

is an equally valid negative intertwiner. The two bridges preserve the same
reflection axis, but they send its oriented successor to different offsets:

- positive generator sign: `4 -> 1`;
- negative generator sign: `4 -> 2`.

The clean minimum-return grammar does not remove this ambiguity. It admits 36
instances of profile `1,2,1,3,1` and 36 instances of profile
`1,3,1,2,1`.

## Theorem boundary

The current clean structure canonically selects the mirror axis, offset 4. It
does not select offset 1 rather than offset 2. This is a bounded theorem about
the pinned source domain, not a proof that no deeper native orientation can
exist.

A future positive claim must supply independently sourced oriented structure
that identifies one common C5 generator on both domains before consulting
multiplier values or the registered offset-1 assignment.

## Keeper

The mirror is native. The turn is registered.
