import json
import time
import hyperloglog
from tabulate import tabulate
from typing import List


def load_ips_from_log(file_path: str) -> List[str]:
    ips = []
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            try:
                log_entry = json.loads(line)
                ip = log_entry.get("remote_addr")
                if ip:
                    ips.append(ip)
            except json.JSONDecodeError:
                continue  # Ігнорувати некоректні рядки
    return ips


def count_unique_ips_exact(ips: List[str]) -> int:
    return len(set(ips))


def count_unique_ips_hll(ips: List[str], precision: float = 0.01) -> int:
    hll = hyperloglog.HyperLogLog(precision)
    for ip in ips:
        hll.add(ip)
    return len(hll)


def main():
    log_file = "lms-stage-access.log"

    # Завантаження IP-адрес
    ips = load_ips_from_log(log_file)

    # Точний підрахунок
    start = time.time()
    exact_count = count_unique_ips_exact(ips)
    exact_time = time.time() - start

    # HyperLogLog підрахунок
    start = time.time()
    hll_count = count_unique_ips_hll(ips)
    hll_time = time.time() - start

    # Виведення результатів
    print(f"Всього IP-адрес: {len(ips)}")
    print(f"Унікальних IP-адрес: {exact_count}")

    print("Результати порівняння:")
    headers = ["Метод", "Унікальні елементи", "Час виконання (сек.)"]
    table = [
        ["Точний підрахунок", exact_count, round(exact_time, 4)],
        ["HyperLogLog", hll_count, round(hll_time, 4)],
    ]
    print(tabulate(table, headers=headers, tablefmt="grid"))


if __name__ == "__main__":
    main()
