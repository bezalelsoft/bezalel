from collections import deque
import itertools


def combine_func_join_arrays(array_of_arrays):
    return list(itertools.chain(*array_of_arrays))


class BufferingIterator:
    def __init__(self, it, buffer_size, combine_func=combine_func_join_arrays):
        self._it = iter(it)
        self._buffer_size = buffer_size
        self._combine_func = combine_func

    def __iter__(self):
        return self

    def __next__(self):
        if self._it is None:
            raise StopIteration

        pages = deque()

        for i in range(0, self._buffer_size):
            val = next(self._it, None)
            if val is None:
                self._it = None
                if not pages:
                    # edge case, never had any lines to begin with
                    raise StopIteration
                break
            pages.append(val)

        return self._combine_func(pages)
