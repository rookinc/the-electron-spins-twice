# Finite covariant receipt apparatus contract 204

## Status

This artifact seeds a general finite action-response apparatus.

It is not defined as an electron, gravity, or radiation theorem. Those names
may later label representations or observables of the apparatus, but they are
not part of its abstract definition.

## Algebra

The visible carrier has orientation group

    C4 = <r | r^4 = 1>

with one quarter-turn represented by r.

The lifted carrier is

    C8 = <h | h^8 = 1>

with projection

    pi(h^k) = r^(k mod 4).

The projection has kernel

    {1, kappa}
    kappa = h^4
    kappa^2 = 1.

A full turn is therefore visibly trivial but lifted-nontrivial:

    pi(kappa) = 1
    kappa != 1.

## Signed history

C8 alone does not distinguish positive and negative full turns because

    h^4 = h^(-4).

The apparatus therefore includes a signed action latch with values 0, +1, and
-1. The completed receipts are

    (kappa,+1,receipt)
    (kappa,-1,receipt).

## Typed control

The control modes are

    idle
    drive
    limit
    g900_return
    half_turn
    emit
    g15_rebound
    receipt.

The complete state space is a finite product of lifted phase, action sign, and
control mode. Only 19 of the 192 product states are reachable. All 19 remain
distinct under deterministic transducer minimization.

## Response

The positive response is

    0
    90 drive
    180 drive
    270 drive
    360 limit
    270 return
    180 half-turn
    180 emission
    270 rebound
    360 receipt.

The negative response is its exact reversal.

The response core is

    360 -> 180 -> 360.

The first and last visible orientations agree. Their lifted state, action
sign, and completion mode do not.

## Artifact201 correction

Artifact201 remains a valid historical candidate under its declared rules. It
is not rewritten or invalidated.

The present apparatus retains its loading, boundedness, reversal covariance,
G900 return, conditional offsets, and receipt logic.

The following current-theory claims are superseded:

    G15 sends the half-turn state to lifted zero;
    the response ends at lifted identity;
    the finite ledger closes at integer zero.

The corrected apparatus says:

    G15 rebounds from half-turn to full-turn receipt;
    visible orientation returns only after C4 projection;
    the final lifted state is kappa;
    the receipt retains winding direction and completion history.

## Claim boundary

The apparatus is an exact finite algebra and transducer within the declared
contract.

It is not yet:

- a physical model of an electron;
- a theory of gravity;
- a theory of radiation;
- a physical G900 or G15 dynamics;
- an energy or momentum theorem;
- an experimental prediction.

## Keeper

The visible carrier returns. The lifted sheet, action sign, and completion
mode remember why.
