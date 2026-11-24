import importlib.util
from pathlib import Path
import sys
import unittest

path = Path(__file__).resolve().parents[1] / "examples/code/input/worker.py"
spec = importlib.util.spec_from_file_location("sample_worker", path)
worker = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = worker
spec.loader.exec_module(worker)


class WorkerTests(unittest.IsolatedAsyncioTestCase):
    async def test_success_and_distinct_failure_windows(self):
        for fail, expected in [(None, ["send", "ack"]), ("send", ["send"]), ("ack", ["send", "ack"])]:
            events = []

            class Sink:
                async def send(self, message):
                    events.append("send")
                    if fail == "send":
                        raise OSError("send failed")

            class Broker:
                async def ack(self, message_id):
                    events.append("ack")
                    if fail == "ack":
                        raise OSError("ack failed")

            if fail:
                with self.assertRaises(OSError):
                    await worker.deliver(worker.Message("m1", "payload"), Sink(), Broker())
            else:
                self.assertEqual(await worker.deliver(worker.Message("m1", "payload"), Sink(), Broker()), "acked")
            self.assertEqual(events, expected)

    async def test_retry_can_duplicate_completed_send(self):
        sent, attempts = [], []

        class Sink:
            async def send(self, message):
                sent.append(message.id)

        class Broker:
            async def ack(self, message_id):
                attempts.append(message_id)
                if len(attempts) == 1:
                    raise OSError("ack failed after send")

        message, sink, broker = worker.Message("m1", "payload"), Sink(), Broker()
        with self.assertRaises(OSError):
            await worker.deliver(message, sink, broker)
        await worker.deliver(message, sink, broker)
        self.assertEqual(sent, ["m1", "m1"])


if __name__ == "__main__":
    unittest.main()
