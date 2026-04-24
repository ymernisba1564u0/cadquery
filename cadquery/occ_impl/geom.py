"""Geometry primitives and transformations for CadQuery.

This module provides core geometric types including vectors, matrices,
planes, and bounding boxes used throughout the CadQuery modeling pipeline.
"""

import math
from typing import Optional, Tuple, Union, overload

from OCP.gp import (
    gp_Ax1,
    gp_Ax2,
    gp_Ax3,
    gp_Dir,
    gp_Pnt,
    gp_Trsf,
    gp_Vec,
    gp_XYZ,
)
from OCP.BRep import BRep_Builder
from OCP.BRepBndLib import BRepBndLib
from OCP.Bnd import Bnd_Box
from OCP.TopoDS import TopoDS_Shape

VectorLike = Union["Vector", Tuple[float, float, float], Tuple[float, float]]


class Vector:
    """A 3D vector with standard arithmetic operations.

    Wraps OCC gp_Vec to provide a more Pythonic interface.
    """

    def __init__(self, *args):
        if len(args) == 3:
            self._v = gp_Vec(args[0], args[1], args[2])
        elif len(args) == 2:
            self._v = gp_Vec(args[0], args[1], 0.0)
        elif len(args) == 1:
            arg = args[0]
            if isinstance(arg, gp_Vec):
                self._v = arg
            elif isinstance(arg, gp_Pnt):
                self._v = gp_Vec(arg.X(), arg.Y(), arg.Z())
            elif isinstance(arg, gp_Dir):
                self._v = gp_Vec(arg)
            elif isinstance(arg, gp_XYZ):
                self._v = gp_Vec(arg)
            elif isinstance(arg, (tuple, list)) and len(arg) == 3:
                self._v = gp_Vec(*arg)
            elif isinstance(arg, (tuple, list)) and len(arg) == 2:
                self._v = gp_Vec(arg[0], arg[1], 0.0)
            else:
                raise TypeError(f"Cannot create Vector from {type(arg)}")
        elif len(args) == 0:
            self._v = gp_Vec(0.0, 0.0, 0.0)
        else:
            raise TypeError(f"Expected 0-3 arguments, got {len(args)}")

    @property
    def x(self) -> float:
        return self._v.X()

    @property
    def y(self) -> float:
        return self._v.Y()

    @property
    def z(self) -> float:
        return self._v.Z()

    def length(self) -> float:
        """Return the magnitude of the vector."""
        return self._v.Magnitude()

    def normalized(self) -> "Vector":
        """Return a unit vector in the same direction."""
        return Vector(self._v.Normalized())

    def dot(self, other: "Vector") -> float:
        """Dot product with another vector."""
        return self._v.Dot(other._v)

    def cross(self, other: "Vector") -> "Vector":
        """Cross product with another vector."""
        return Vector(self._v.Crossed(other._v))

    def to_pnt(self) -> gp_Pnt:
        """Convert to OCC gp_Pnt."""
        return gp_Pnt(self._v.X(), self._v.Y(), self._v.Z())

    def to_dir(self) -> gp_Dir:
        """Convert to OCC gp_Dir (unit direction)."""
        return gp_Dir(self._v)

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self._v.Added(other._v))

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self._v.Subtracted(other._v))

    def __mul__(self, scalar: float) -> "Vector":
        return Vector(self._v.Multiplied(scalar))

    def __rmul__(self, scalar: float) -> "Vector":
        return self.__mul__(scalar)

    def __neg__(self) -> "Vector":
        return Vector(self._v.Reversed())

    def __repr__(self) -> str:
        return f"Vector({self.x:.6g}, {self.y:.6g}, {self.z:.6g})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return self._v.IsEqual(other._v, 1e-9, 1e-9)


class BoundingBox:
    """Axis-aligned bounding box computed from a TopoDS_Shape."""

    def __init__(self, shape: Optional[TopoDS_Shape] = None, tol: float = 1e-6):
        self._bbox = Bnd_Box()
        self._bbox.SetGap(tol)
        if shape is not None:
            BRepBndLib.Add_s(shape, self._bbox)

        xmin, ymin, zmin, xmax, ymax, zmax = (
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        )
        if not self._bbox.IsVoid():
            xmin, ymin, zmin, xmax, ymax, zmax = self._bbox.Get()

        self.xmin = xmin
        self.ymin = ymin
        self.zmin = zmin
        self.xmax = xmax
        self.ymax = ymax
        self.zmax = zmax

    @property
    def center(self) -> Vector:
        """Return the center of the bounding box."""
        return Vector(
            (self.xmin + self.xmax) / 2.0,
            (self.ymin + self.ymax) / 2.0,
            (self.zmin + self.zmax) / 2.0,
        )

    @property
    def diagonal_length(self) -> float:
        """Return the length of the bounding box diagonal."""
        return math.sqrt(
            (self.xmax - self.xmin) ** 2
            + (self.ymax - self.ymin) ** 2
            + (self.zmax - self.zmin) ** 2
        )

    def __repr__(self) -> str:
        return (
            f"BoundingBox(xmin={self.xmin:.6g}, ymin={self.ymin:.6g}, "
            f"zmin={self.zmin:.6g}, xmax={self.xmax:.6g}, "
            f"ymax={self.ymax:.6g}, zmax={self.zmax:.6g})"
        )
