from random import choice


class SessionName:
    _length: int
    _allow_char: str

    def __init__(self):
        self._length = 64
        allow_digit = self._get_range_str('0', '9')
        allow_lowcase = self._get_range_str('a', 'z')
        allow_uppercase = self._get_range_str('A', 'Z')
        self._allow_char = allow_digit + allow_lowcase + allow_uppercase

    def _get_range_str(self, lhs: str, rhs: str) -> str:
        return ''.join(map(chr, range(ord(lhs), ord(rhs) + 1)))

    def _get_random_char(self) -> str:
        return choice(self._allow_char)

    def get_session_name(self):
        union_name = ''
        for _ in range(self._length):
            union_name += self._get_random_char()
        return union_name