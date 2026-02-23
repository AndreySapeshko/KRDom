from __future__ import annotations

from typing import List, Literal, Tuple

from pydantic import BaseModel, Field, model_validator

Point2D = Tuple[float, float]


def polygon_area(points: List[Point2D]) -> float:
    area = 0.0
    n = len(points)
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        area += x1 * y2 - x2 * y1
    return abs(area) / 2.0


class PolygonFootprint(BaseModel):
    type: Literal["polygon"] = "polygon"
    points: List[Point2D] = Field(..., min_length=3)

    @model_validator(mode="after")
    def validate_polygon_min_points(self):
        # Минимум 3 точки (треугольник)
        if len(self.points) < 3:
            raise ValueError("Footprint polygon must have at least 3 points")

        return self

    @model_validator(mode="after")
    def validate_polygon(self):
        if len(set(self.points)) != len(self.points):
            raise ValueError("Polygon points must be unique")

        area = polygon_area(self.points)
        if area <= 0.1:
            raise ValueError("Polygon area must be > 0")

        return self
