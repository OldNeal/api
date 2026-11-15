GET_ACTIVITY_POINTS_LIMIT = 1200

class Sequence:
    def __init__(self, number: int, days: int, rsp_factor: int = 1):
        self.number = number
        self.days = days
        self.rsp_factor = rsp_factor
        self.rsp = GET_ACTIVITY_POINTS_LIMIT*days*rsp_factor//2

sequence_list = [
    Sequence(9, 7),
    Sequence(8, 14),
    Sequence(7, 21),
    Sequence(6, 30),
    Sequence(5, 60),
    Sequence(4, 90),
    Sequence(3, 120),
    Sequence(2, 150),
    Sequence(1, 180),
    Sequence(0, 30),
]

sequences = {s.number:s for s in sequence_list}

if __name__ == '__main__':
    print([s.rsp for s in sequence_list])