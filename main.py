# ./client --host=127.0.0.1 --port=8888
import asyncio
from argparse import ArgumentParser
from asyncio import transports, AbstractEventLoop
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
        message = data.decode().strip()
        print(f">>> {message}")

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
            client_coroutine = self.loop.create_connection(
                lambda: self,
                self.server_host,
                self.server_port,
            )

            input_coroutine = self.loop.create_task(client.on_input())

            await asyncio.gather(
                input_coroutine,
                client_coroutine
            )
        except ConnectionRefusedError:
            print(f"Сервер недоступен - {self.server_host}:{self.server_port}")
            self.on_stop()
        except asyncio.CancelledError:
            print("Асинхронная операция прервана")


if __name__ == '__main__':
    parser = ArgumentParser(description="Параметры соединения")

    parser.add_argument("--host", default="127.0.0.1", type=str)
    parser.add_argument("--port", default=8888, type=int)

    print("Для завершения сеанса введите 'exit' \n")

    args = parser.parse_args()
    event_loop = asyncio.get_event_loop()

    client = Client(args.host, args.port)

    try:
        event_loop.create_task(client.start())
        event_loop.run_forever()
    except KeyboardInterrupt:
        client.on_stop()
        print("Принудительная остановка Ctrl^C, нажмите Enter ...")
