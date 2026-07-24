from models.point import Point


class GeometryUtils:

    @staticmethod
    def center(points: list[Point]) -> Point:

        x = sum(p.x for p in points) / len(points)

        y = sum(p.y for p in points) / len(points)

        return Point(
            x=x,
            y=y,
        )

    @staticmethod
    def bounding_box(points: list[Point]):

        xs = [p.x for p in points]

        ys = [p.y for p in points]

        return (
            min(xs),
            min(ys),
            max(xs),
            max(ys),
        )