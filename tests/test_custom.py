from compas.geometry import Frame

import compas_rrc as rrc


def test_pickup_stirrup_payload():
    instruction = rrc.PickupStirrup(
        Frame.worldXY(),
        100,
        rrc.Zone.FINE,
        Frame([10, 20, 30], [1, 0, 0], [0, 1, 0]),
        50,
        rrc.Zone.Z5,
        25,
        10,
        "gripper_open",
        "gripper_close",
        "laser_on",
        "laser_is_on",
        True,
        3,
        2.5,
        -4.0,
    )

    assert instruction.string_values == ["gripper_open", "gripper_close", "laser_on", "laser_is_on"]
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
        25,
        10,
        1.0,
        3,
        2.5,
        -4.0,
    ]


def test_pickup_stirrup_defaults_to_legacy_y_correction():
    instruction = rrc.PickupStirrup(
        Frame.worldXY(),
        100,
        rrc.Zone.FINE,
        Frame.worldXY(),
        50,
        rrc.Zone.FINE,
        25,
        10,
        "gripper_open",
        "gripper_close",
        "laser_on",
        "laser_is_on",
    )

    assert instruction.float_values[-3:] == [1, 0.0, 0.0]
