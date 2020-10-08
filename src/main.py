# async_client --host=127.0.0.1 --port=8888
import asyncio
from argparse import ArgumentParser

from async_client.service import Client


def run_app():
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


if __name__ == '__main__':
    run_app()
