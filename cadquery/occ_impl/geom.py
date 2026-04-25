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

    Examples:
        >>> v = Vector(1, 2, 3)
        >>> v.length()
        3.7416573867739413
        >>> v.normalized()
        Vector(0.267, 0.535, 0.802)
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

    def __repr__(self) -> str:
        return f"Vector({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"
