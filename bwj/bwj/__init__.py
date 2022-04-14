from inspect import signature
from typing import Any, Callable, Container, Iterator, Optional


__all__ = ["execute", "set_open", "set_input"]


def execute(solution: Callable[[Callable], None]) -> Callable[[Optional[str]], None]:
    def execute_example(input_: Optional[str] = None) -> None:
        params: Container[str] = signature(solution).parameters

        if input_ == None:
            solution()

        elif "open" in params:

            class open:
                def __init__(self, _: Any):
                    self.read: Callable = lambda: input_

                def __iter__(self):
                    return iter(input_.split("\n"))

            solution(open)

        elif "input" in params:
            input_: Iterator[str] = iter(input_.split("\n"))
            input: Callable[[None], str] = input_.__next__
            solution(input)

        else:
            raise NameError(
                f"solution 함수가 input, open 등의 매개변수를 받지 않습니다.\nsolution 의 매개변수: {params}"
            )

    return execute_example


def set_open(input_: str) -> "open":
    class open:
        def __init__(self, _):
            self.read = lambda: input_

        def __iter__(self):
            return iter(input_.split("\n"))

    return open


def set_input(input_: str) -> Iterator[str]:
    return iter(input_.split("\n")).__next__
