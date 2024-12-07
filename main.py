def get_sequence(number: int):
    """Возвращает n первых элементов последовательности"""
    numbers = range(1, number+1)
    sequence = map(lambda num: str(num) * num, numbers)
    sequence = "".join(sequence)
    return sequence


if __name__ == "__main__":
    print(get_sequence(6))
