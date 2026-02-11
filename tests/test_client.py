import threading
import time
import types

from compas_rrc.client import AbbClient, SequenceCounter, _build_protocol_param_names


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


def test_abb_client_default_topic_configuration(monkeypatch):
    captured = {"topics": []}

    class FakeTopic(object):
        def __init__(self, ros, name, type_, queue_size):
            captured["topics"].append((name, type_, queue_size))

        def subscribe(self, callback):
            pass

        def advertise(self):
            pass

        def unadvertise(self):
            pass

        def unsubscribe(self):
            pass

    fake_roslibpy = types.SimpleNamespace(Topic=FakeTopic, Param=object)
    monkeypatch.setattr("compas_rrc.client.roslibpy", fake_roslibpy)

    class FakeRos(object):
        def on_ready(self, callback):
            pass

        def on(self, event_name, callback):
            pass

    abb = AbbClient(FakeRos(), namespace="/rob1")

    assert abb._server_protocol_check["param_names"] == [
        "/rob1/protocol_version",
        "/rob1:protocol_version",
    ]
    assert captured["topics"][0][0] == "/rob1/robot_command"
    assert captured["topics"][0][1] == "compas_rrc_driver/RobotMessage"
    assert captured["topics"][1][0] == "/rob1/robot_response"
    assert captured["topics"][1][1] == "compas_rrc_driver/RobotMessage"


def test_abb_client_supports_ros2_message_type_and_absolute_names(monkeypatch):
    captured = {"topics": []}

    class FakeTopic(object):
        def __init__(self, ros, name, type_, queue_size):
            captured["topics"].append((name, type_, queue_size))

        def subscribe(self, callback):
            pass

        def advertise(self):
            pass

        def unadvertise(self):
            pass

        def unsubscribe(self):
            pass

    fake_roslibpy = types.SimpleNamespace(Topic=FakeTopic, Param=object)
    monkeypatch.setattr("compas_rrc.client.roslibpy", fake_roslibpy)

    class FakeRos(object):
        def on_ready(self, callback):
            pass

        def on(self, event_name, callback):
            pass

    abb = AbbClient(
        FakeRos(),
        namespace="/rob1",
        robot_message_type="compas_rrc_driver/msg/RobotMessage",
        command_topic="/robot_command",
        response_topic="/robot_response",
        protocol_param="/protocol_version",
    )

    assert abb._server_protocol_check["param_names"] == [
        "/protocol_version",
        "/rob1:protocol_version",
    ]
    assert captured["topics"][0][0] == "/robot_command"
    assert captured["topics"][0][1] == "compas_rrc_driver/msg/RobotMessage"
    assert captured["topics"][1][0] == "/robot_response"
    assert captured["topics"][1][1] == "compas_rrc_driver/msg/RobotMessage"


def test_build_protocol_param_names_for_ros1_and_ros2():
    assert _build_protocol_param_names("/rob1/", "protocol_version") == [
        "/rob1/protocol_version",
        "/rob1:protocol_version",
    ]

    assert _build_protocol_param_names("/rob1/", "/protocol_version") == [
        "/protocol_version",
        "/rob1:protocol_version",
    ]

    assert _build_protocol_param_names("/rob1/", "/rob1:protocol_version") == [
        "/rob1:protocol_version"
    ]


def test_version_check_falls_back_to_ros2_param_name(monkeypatch):
    captured = {"requested": []}

    class FakeTopic(object):
        def __init__(self, ros, name, type_, queue_size):
            pass

        def subscribe(self, callback):
            pass

        def advertise(self):
            pass

        def unadvertise(self):
            pass

        def unsubscribe(self):
            pass

    class FakeParam(object):
        def __init__(self, ros, name):
            self.name = name
            captured["requested"].append(name)

        def get(self):
            if self.name == "/rob1/protocol_version":
                raise Exception("Malformed parameter name")
            if self.name == "/rob1:protocol_version":
                return 2
            return None

    fake_roslibpy = types.SimpleNamespace(Topic=FakeTopic, Param=FakeParam)
    monkeypatch.setattr("compas_rrc.client.roslibpy", fake_roslibpy)

    class FakeRos(object):
        def on_ready(self, callback):
            pass

        def on(self, event_name, callback):
            pass

    abb = AbbClient(FakeRos(), namespace="/rob1")
    abb.version_check()

    assert captured["requested"] == ["/rob1/protocol_version", "/rob1:protocol_version"]
    assert abb._server_protocol_check["version"] == 2
