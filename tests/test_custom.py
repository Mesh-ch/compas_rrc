from compas.geometry import Frame

import compas_rrc as rrc


def test_pickup_stirrup_direct_payload():
    instruction = rrc.PickupStirrupDirect(
        Frame.worldXY(),
        100,
        rrc.Zone.FINE,
        Frame([10, 20, 30], [1, 0, 0], [0, 1, 0]),
        50,
        rrc.Zone.Z5,
        "gripper_open",
        "gripper_close",
        2.5,
        42.0,
        True,
    )

    assert instruction.instruction == "PickupStirrupDirect"
    assert instruction.string_values == ["gripper_open", "gripper_close"]
    assert instruction.float_values == [
        0.0,
        0.0,
        0.0,
        1.0,
        0.0,
        0.0,
        0.0,
        100,
        -1,
        10.0,
        20.0,
        30.0,
        1.0,
        0.0,
        0.0,
        0.0,
        50,
        5,
        0.0,
        0.0,
        1.0,
        0.0,
        2.5,
        42.0,
    ]


def test_pickup_stirrup_aliases_direct_variant():
    instruction = rrc.PickupStirrup(
        Frame.worldXY(),
        100,
        rrc.Zone.FINE,
        Frame.worldXY(),
        50,
        rrc.Zone.FINE,
        "gripper_open",
        "gripper_close",
        0.0,
        10.0,
    )

    assert isinstance(instruction, rrc.PickupStirrupDirect)
    assert instruction.instruction == "PickupStirrupDirect"


def test_pickup_stirrup_oxm_payload():
    instruction = rrc.PickupStirrupOXM(
        Frame.worldXY(),
        100,
        rrc.Zone.FINE,
        Frame.worldXY(),
        50,
        rrc.Zone.FINE,
        "gripper_open",
        "gripper_close",
        "laser_on",
        "laser_is_on",
        25.0,
        10.0,
        True,
        2,
    )

    assert instruction.instruction == "PickupStirrupOXM"
    assert instruction.string_values == ["gripper_open", "gripper_close", "laser_on", "laser_is_on"]
    assert instruction.float_values[-4:] == [25.0, 10.0, 1.0, 2]


def test_pickup_stirrup_uncorrected_payload():
    instruction = rrc.PickupStirrupUncorrected(
        Frame.worldXY(),
        100,
        rrc.Zone.FINE,
        Frame.worldXY(),
        50,
        rrc.Zone.FINE,
        "gripper_open",
        "gripper_close",
    )

    assert instruction.instruction == "PickupStirrupUncorrected"
    assert instruction.string_values == ["gripper_open", "gripper_close"]
    assert len(instruction.float_values) == 18
