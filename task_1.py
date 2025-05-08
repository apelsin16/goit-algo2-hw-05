import mmh3
from typing import List, Dict


class BloomFilter:
    def __init__(self, size: int, num_hashes: int):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def _get_hashes(self, item: str) -> List[int]:
        return [
            mmh3.hash(item, seed=i) % self.size
            for i in range(self.num_hashes)
        ]

    def add(self, item: str):
        for hash_index in self._get_hashes(item):
            self.bit_array[hash_index] = 1

    def __contains__(self, item: str) -> bool:
        return all(self.bit_array[hash_index] for hash_index in self._get_hashes(item))


def check_password_uniqueness(bloom_filter: BloomFilter, passwords: List[str]) -> Dict[str, str]:
    results = {}
    for password in passwords:
        if not isinstance(password, str) or not password.strip():
            results[password] = "некоректний пароль"
            continue

        if password in bloom_filter:
            results[password] = "вже використовувався"
        else:
            results[password] = "унікальний"
            bloom_filter.add(password)

    return results


# Приклад використання
if __name__ == "__main__":
    bloom = BloomFilter(size=1000, num_hashes=5)

    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest", "", None]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    for password, status in results.items():
        print(f"Пароль '{password}' - {status}.")
