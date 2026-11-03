import threading
import time

from compas_rrc.client import SequenceCounter


def test_sequence_id_rollover():
    counter = SequenceCounter()
    assert counter.value == 0

    for i in range(1, 1000000):
        counter.increment()
        assert counter.value == i
    assert counter.value == 999999

    counter.increment()
    assert counter.value == 1000000

    counter.increment()
    assert counter.value == 1


def test_sequence_id_increments():
    counter = SequenceCounter()
    assert counter.value == 0
    counter.increment()
    assert counter.value == 1


def test_multithreaded_consistency():
    nr_of_threads = 4
    nr_of_increments = 1000
    counter = SequenceCounter()

    def incrementer(c):
        for i in range(nr_of_increments):
            c.increment()
            time.sleep(0.001)

    threads = []
    for _ in range(nr_of_threads):
        t = threading.Thread(target=incrementer, args=(counter,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    assert counter.value == nr_of_threads * nr_of_increments


def test_parser_error_resolves_future_with_exception():
    from compas_rrc.client import AbbClient
    from compas_rrc.common import FutureResult, InstructionException
    from compas_rrc.custom import WaitForDigital

    class BrokenWait(WaitForDigital):
        def parse_feedback(self, result):
            return result["float_values"][0]

    instruction = BrokenWait("gripper_closed", 1)
    client = AbbClient.__new__(AbbClient)
    future = FutureResult()
    client.futures = {"msg:7": dict(result=future, parser=instruction.parse_feedback, label="WaitForDigital(gripper_closed)")}

    client.feedback_callback({"feedback_id": 7, "feedback": "Done", "float_values": []})

    assert "msg:7" not in client.futures
    try:
        future.result(timeout=0.1)
    except InstructionException as exc:
        assert "WaitForDigital(gripper_closed)" in str(exc)
        assert "IndexError" in str(exc)
    else:
        raise AssertionError("expected InstructionException")


def test_describe_instruction_uses_first_string_value():
    from compas_rrc.client import _describe_instruction
    from compas_rrc.custom import WaitForDigital

    assert _describe_instruction(WaitForDigital("gripper_closed", 1)) == "WaitForDigital(gripper_closed)"
