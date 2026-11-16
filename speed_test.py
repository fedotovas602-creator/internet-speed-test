#!/usr/bin/env python3
"""Measure download speed by making 10 sequential HTTP(S) requests."""

import argparse
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


REQUEST_COUNT = 10
TIMEOUT_SECONDS = 30


def check_url(url):
    """Check that the address is a valid HTTP or HTTPS URL."""
    parsed_url = urlsplit(url)

    if parsed_url.scheme not in ("http", "https") or not parsed_url.netloc:
        raise ValueError("Укажите корректный URL, начинающийся с http:// или https://")


def measure_speed(url):
    """Download the URL 10 times in a row and calculate timing and speed."""
    request_times = []
    total_bytes = 0

    for request_number in range(1, REQUEST_COUNT + 1):
        request = Request(
            url,
            headers={"User-Agent": "InternetSpeedTest/1.0"}
        )

        start_time = time.perf_counter()

        # The context manager closes the response after the full body is read.
        with urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            downloaded_data = response.read()

        elapsed_time = time.perf_counter() - start_time
        downloaded_size = len(downloaded_data)

        request_times.append(elapsed_time)
        total_bytes += downloaded_size

        print(
            f"Запрос {request_number}/{REQUEST_COUNT}: "
            f"{elapsed_time:.3f} сек., {downloaded_size:,} байт"
        )

    total_time = sum(request_times)
    average_time = total_time / REQUEST_COUNT

    # Decimal megabytes are used: 1 MB = 1,000,000 bytes.
    speed_mb_per_second = (total_bytes / total_time) / 1_000_000
    speed_mbit_per_second = speed_mb_per_second * 8

    print("\n--- Результаты ---")
    print(f"Успешных запросов: {REQUEST_COUNT}")
    print(f"Среднее время запроса: {average_time:.3f} сек.")
    print(f"Общий объём скачанных данных: {total_bytes:,} байт")
    print(f"Общий объём: {total_bytes / 1_000_000:.3f} MB")
    print(f"Средняя скорость скачивания: {speed_mb_per_second:.3f} MB/s")
    print(f"Средняя скорость скачивания: {speed_mbit_per_second:.3f} Mbit/s")


def main():
    parser = argparse.ArgumentParser(
        description="Проверка скорости скачивания по указанному URL."
    )
    parser.add_argument("url", help="Адрес файла или ресурса для скачивания")
    args = parser.parse_args()

    try:
        check_url(args.url)
        measure_speed(args.url)
    except HTTPError as error:
        print(f"Ошибка HTTP: сервер вернул статус {error.code}.")
        raise SystemExit(1)
    except (URLError, TimeoutError, OSError) as error:
        print(f"Ошибка соединения или загрузки: {error}")
        raise SystemExit(1)
    except ValueError as error:
        print(f"Ошибка: {error}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
