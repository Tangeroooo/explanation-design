"""Small delivery worker. External broker policy is deliberately unspecified."""
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Message:
    id: str
    payload: str


class Sink(Protocol):
    async def send(self, message: Message) -> None: ...


class Broker(Protocol):
    async def ack(self, message_id: str) -> None: ...


async def deliver(message: Message, sink: Sink, broker: Broker) -> str:
    await sink.send(message)
    await broker.ack(message.id)
    return "acked"
