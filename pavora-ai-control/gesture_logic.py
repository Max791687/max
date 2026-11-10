"""Pure hand geometry classification; no camera needed for tests."""
from dataclasses import dataclass
from typing import Sequence

@dataclass(frozen=True)
class Point:
    x: float
    y: float

def distance(a: Point, b: Point) -> float:
    return ((a.x-b.x)**2+(a.y-b.y)**2)**0.5

def raised(points: Sequence[Point], tip: int, pip: int) -> bool:
    return points[tip].y < points[pip].y - 0.018

def classify(points: Sequence[Point]) -> str:
    if len(points) != 21:
        return "idle"
    ix, md, rg, pk = [raised(points, tip, pip) for tip,pip in ((8,6),(12,10),(16,14),(20,18))]
    if ix and md and rg and pk:
        return "stop"
    palm=max(distance(points[0],points[9]),0.06)
    pinch=distance(points[4],points[8])/palm < 0.38
    if pinch and not md and not rg and not pk:
        return "click"
    if ix and md and not rg and not pk:
        return "scroll"
    if ix and not md and not rg and not pk:
        return "pointer"
    return "idle"
