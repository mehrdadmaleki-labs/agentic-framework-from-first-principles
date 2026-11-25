
def operation(x: float, y: float, op: str) -> float:
    if op == "ADD":
        return x + y

    elif op == "SUBTRACT":
        return x - y

    elif op == "MULTIPLY":
        return x * y

    elif op == "DIVISION":
        if y == 0:
            raise ValueError("Denominator in division is zero")
        return x / y

    else:
        raise ValueError(f"The operation {op} is not supported")
