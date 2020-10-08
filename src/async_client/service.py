import asyncio
from asyncio import AbstractEventLoop, transports
from typing import Optional


class Client(asyncio.Protocol):
    server_host: str
    server_port: int
    loop: AbstractEventLoop
    transport: transports.Transport
    connected: bool

    def __init__(self, host: str, port: int):
        self.loop = asyncio.get_event_loop()
        self.connected = False
        self.server_host = host
        self.server_port = port

    def data_received(self, data: bytes) -> None:
        print(data.decode().strip())

    def connection_made(self, transport: transports.Transport) -> None:
        print("Соединение установлено")
        self.transport = transport
        self.connected = True

    def connection_lost(self, exc: Optional[Exception]) -> None:
        print("Соединение потеряно")
        self.connected = False
        self.loop.stop()

    async def on_input(self):
        while True:
            content = await self.loop.run_in_executor(None, input)

            if content.strip().lower() == 'exit':
                self.on_stop()
                break

            if self.connected:
                self.transport.write(content.encode())

    def on_stop(self):
        print("Закрытие соединения...")

        if self.connected:
            self.transport.close()

        self.loop.stop()

    async def start(self):
        try:
            connection_coroutine = self.loop.create_connection(
                lambda: self,
                self.server_host,
                self.server_port,
            )

            input_coroutine = self.loop.create_task(self.on_input())

            await asyncio.gather(
                input_coroutine,
                connection_coroutine
            )
        except ConnectionRefusedError:
            print(f"Сервер недоступен - {self.server_host}:{self.server_port}")
            self.on_stop()
        except asyncio.CancelledError:
            print("Асинхронная операция прервана")
