from compas_fab.backends.ros.messages import ROSmsg

from compas_rrc.common import ExecutionLevel
from compas_rrc.common import FeedbackLevel

__all__ = ["CustomInstruction", "PickupStirrup", "MoveToFrameTrigger", "WaitForDigital", "PromptContinue"]


class CustomInstruction(ROSmsg):
    """Custom instruction is a call that invokes a custom RAPID instruction. The name has to match a ``RAPID`` procedure.

    Examples
    --------
    .. code-block:: python

        # Custom instruction
        string_values = ['Custom Text']
        float_values = [42]
        done = abb.send_and_wait(rrc.CustomInstruction('r_RRC_CustomInstruction', string_values, float_values))

    RAPID Instruction: ``All usable``

    .. include:: ../abb-reference.rst

    """

    def __init__(
        self,
        name,
        string_values=[],
        float_values=[],
        feedback_level=FeedbackLevel.NONE,
        execution_level=ExecutionLevel.ROBOT,
    ):
        """Create a new instance of the instruction.

        Parameters
        ----------
        name : :obj:`str`
            Name of the procedure to invoke on the robot code. Maximum of 80 characters.
        string_values : :obj:`list` of :obj:`str`
            List of up to 8 strings values, each of them with a maximum of 80 characters.
        float_values : :obj:`list` of :obj:`float`
            List of up to 36 float values.
        feedback_level : :obj:`int`
            Defines the feedback level requested from the robot. Defaults to :attr:`FeedbackLevel.NONE`.
        execution_level : :obj:`int`
            Defines the execution level of the instruction. Defaults to :attr:`ExecutionLevel.ROBOT`.
        """
        self.instruction = name
        self.feedback_level = feedback_level
        self.exec_level = execution_level
        self.string_values = string_values
        self.float_values = float_values


class PickupStirrup(CustomInstruction):
    """Custom instruction to pick up a stirrup. This is a wrapper around :class:`CustomInstruction`."""

    def __init__(
        self,
        grasping_frame,
        speed,
        zone,
        entry_frame,
        speed_entry,
        zone_entry,
        max_gap_width,
        center_x_bound,
        gripper_open_io_name,
        gripper_closed_io_name,
        laser_on_io_name,
        laser_is_on_io_name,
        is_mirrored=False,
        correction_mode=1,
        direct_y_correction=0.0,
        direct_z_correction=0.0,
    ):
        string_values = [gripper_open_io_name, gripper_closed_io_name, laser_on_io_name, laser_is_on_io_name]
        float_values = [
            *grasping_frame.point,  # x, y, z
            *grasping_frame.quaternion,  # qw, qx, qy, qz
            speed,  # speed grasp
            zone,  # zone grasp
            *entry_frame.point,  # x, y, z
            *entry_frame.quaternion,  # qw, qx, qy, qz
            speed_entry,  # speed_entry
            zone_entry,  # zone_entry
            max_gap_width,  # max_gap_width
            center_x_bound,  # center_x_bound
            float(is_mirrored),  # is_mirrored
            correction_mode,  # correction_mode
            direct_y_correction,  # direct_y_correction
            direct_z_correction,  # direct_z_correction
        ]
        super().__init__(
            "PickupStirrup",
            string_values=string_values,
            float_values=float_values,
        )

    def parse_feedback(self, result):
        success = result.get("float_values", [0])[0] == 1.0
        return success


class MoveToFrameTrigger(CustomInstruction):
    """Custom instruction to move to a frame with a trigger. This is a wrapper around :class:`CustomInstruction`."""

    def __init__(self, target_frame, speed, zone, signal_name, signal_value=1):
        zone_value = getattr(zone, "value", zone)
        string_values = [signal_name]
        float_values = [*target_frame.point, *target_frame.quaternion, speed, zone_value, signal_value]
        super().__init__(
            "MoveToFrameTrigger",
            string_values=string_values,
            float_values=float_values,
        )


class WaitForDigital(CustomInstruction):
    """Custom instruction to wait for a digital signal. This is a wrapper around :class:`CustomInstruction`."""

    def __init__(self, signal_name, value, timeout=None):
        if timeout is None:
            timeout = -1.0
        string_values = [signal_name]
        float_values = [value, timeout]
        super().__init__(
            "WaitForDigital",
            string_values=string_values,
            float_values=float_values,
        )


class PromptContinue(CustomInstruction):
    """Custom instruction to prompt the user to continue. This is a wrapper around :class:`CustomInstruction`."""

    def __init__(self, message):
        string_values = [message]
        float_values = []
        super().__init__(
            "PromptContinue",
            string_values=string_values,
            float_values=float_values,
        )

    def parse_feedback(self, result):
        success = result.get("string_values", [""])[0] == "Yes"
        return success
