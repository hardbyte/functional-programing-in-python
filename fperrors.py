class Maybe:
    def map(self, f):
        raise NotImplementedError

    def flat_map(self, f):
        raise NotImplementedError

    def get_or_else(self, default):
        raise NotImplementedError

    def and_then(self, action):
        raise NotImplementedError

    def followed_by(self, action):
        return self.and_then(lambda _: action)

    def or_else(self, other: "Maybe"):
        raise NotImplementedError

    def filter(self, f):
        raise NotImplementedError


class _MaybeNothing(Maybe):
    def __repr__(self):
        return "Nothing"

    def map(self, f):
        return Nothing

    def flat_map(self, f):
        return Nothing

    def get_or_else(self, default):
        return default

    def and_then(self, action):
        return Nothing

    def or_else(self, other: "Maybe"):
        return other

    def filter(self, f):
        return Nothing


Nothing = _MaybeNothing()


class Just(Maybe):
    def __init__(self, v):
        self.value = v

    def __repr__(self):
        return "Just({})".format(self.value)

    def get_or_else(self, default):
        return self.value

    def map(self, f):
        return Just(f(self.value))

    def flat_map(self, f):
        return f(self.value)

    def and_then(self, action):
        return action(self.value)

    def or_else(self, other: "Maybe"):
        return self

    def filter(self, f):
        return self if f(self.value) else Nothing


def mean(xs: '[Float]'):
    l = len(xs)
    return Nothing if l == 0 else Just(sum(xs) / l)


def variance(xs: '[Float]'):
    return mean(xs).flat_map(lambda m: mean(list((x - m) ** 2 for x in xs)))


def test_mean_and_var():
    seq = [6.3, 9.0, 56.8, 9.2]

    print(mean(seq))
    print(mean([]))

    mean(seq).and_then(print)
    mean([]).and_then(print)

    print("variance:")
    print("var of seq: ", variance(seq))
    print("Var of empty: ", variance([]))
    variance([]).and_then(print)


def map2(oa, ob, f):
    """

    :param oa: Option[A]
    :param ob: Option[B]
    :param f: A function that takes A,B and returns a C
    :return: Option[C]
    """
    return oa.flat_map(lambda a: ob.map(lambda b: f(a, b)))

    # versus:
    # if isinstance(oa, Just) and isinstance(ob, Just):
    # return f(oa.value, ob.value)
    # else:
    # return Nothing


if __name__ == "__main__":
    test_mean_and_var()

    three = Just(3)
    four = Just(4)
    nill = Nothing

    three.map(lambda x: x ** 2).and_then(print)

    print(nill.or_else(three))

    # a list of MaybeInts
    aList = [three, four, nill]

    three.filter(lambda x: x == 3).and_then(print)

    print(map2(three, four, lambda a, b: a + b))
    print(map2(three, nill, lambda a, b: a + b))

