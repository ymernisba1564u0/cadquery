"""Core shape classes wrapping OpenCASCADE topology and geometry.

This module provides the foundational shape classes used throughout CadQuery,
wrapping the underlying OCCT (OpenCASCADE Community Edition) topology objects.
"""

from typing import Optional, Union, Tuple, List
from OCC.Core.TopoDS import (
    TopoDS_Shape,
    TopoDS_Vertex,
    TopoDS_Edge,
    TopoDS_Wire,
    TopoDS_Face,
    TopoDS_Shell,
    TopoDS_Solid,
    TopoDS_Compound,
)
from OCC.Core.BRep import BRep_Builder
from OCC.Core.BRepBuilderAPI import (
    BRepBuilderAPI_MakeVertex,
    BRepBuilderAPI_MakeEdge,
    BRepBuilderAPI_MakeFace,
    BRepBuilderAPI_MakeWire,
)
from OCC.Core.BRepPrimAPI import (
    BRepPrimAPI_MakeBox,
    BRepPrimAPI_MakeSphere,
    BRepPrimAPI_MakeCylinder,
)
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Ax2, gp_Dir
from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepGProp import brepgprop_VolumeProperties, brepgprop_SurfaceProperties
from OCC.Core.TopAbs import (
    TopAbs_VERTEX, TopAbs_EDGE, TopAbs_WIRE,
    TopAbs_FACE, TopAbs_SHELL, TopAbs_SOLID, TopAbs_COMPOUND,
)
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Core.Bnd import Bnd_Box

from .geom import Vector


class Shape:
    """Base class for all CadQuery shapes.

    Wraps a TopoDS_Shape and provides common operations such as
    bounding box computation, center of mass, and type introspection.
    """

    def __init__(self, obj: TopoDS_Shape):
        self._shape = obj

    @property
    def wrapped(self) -> TopoDS_Shape:
        """Return the underlying OCCT shape object."""
        return self._shape

    @property
    def shape_type(self) -> str:
        """Return a string describing the shape type."""
        _map = {
            TopAbs_VERTEX: "Vertex",
            TopAbs_EDGE: "Edge",
            TopAbs_WIRE: "Wire",
            TopAbs_FACE: "Face",
            TopAbs_SHELL: "Shell",
            TopAbs_SOLID: "Solid",
            TopAbs_COMPOUND: "Compound",
        }
        return _map.get(self._shape.ShapeType(), "Unknown")

    def center(self) -> Vector:
        """Compute the center of mass of the shape."""
        props = GProp_GProps()
        brepgprop_VolumeProperties(self._shape, props)
        com = props.CentreOfMass()
        return Vector(com.X(), com.Y(), com.Z())

    def bounding_box(self) -> Tuple[Vector, Vector]:
        """Return the axis-aligned bounding box as (min_corner, max_corner)."""
        bbox = Bnd_Box()
        brepbndlib_Add(self._shape, bbox)
        xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
        return Vector(xmin, ymin, zmin), Vector(xmax, ymax, zmax)

    def volume(self) -> float:
        """Compute the volume of the shape (0 for non-solid shapes)."""
        props = GProp_GProps()
        brepgprop_VolumeProperties(self._shape, props)
        return props.Mass()

    def area(self) -> float:
        """Compute the surface area of the shape."""
        props = GProp_GProps()
        brepgprop_SurfaceProperties(self._shape, props)
        return props.Mass()

    def is_null(self) -> bool:
        """Return True if the underlying shape is null/invalid."""
        return self._shape.IsNull()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.shape_type}>"


class Solid(Shape):
    """Represents a solid (3-dimensional) shape."""

    @classmethod
    def make_box(
        cls,
        length: float,
        width: float,
        height: float,
        pnt: Optional[Vector] = None,
    ) -> "Solid":
        """Create a rectangular box.

        Args:
            length: Dimension along the X axis.
            width:  Dimension along the Y axis.
            height: Dimension along the Z axis.
            pnt:    Corner point (default: origin).
        """
        origin = pnt or Vector(0, 0, 0)
        builder = BRepPrimAPI_MakeBox(
            gp_Pnt(origin.x, origin.y, origin.z),
            length, width, height,
        )
        return cls(builder.Shape())

    @classmethod
    def make_sphere(
        cls,
        radius: float,
        center: Optional[Vector] = None,
    ) -> "Solid":
        """Create a sphere.

        Args:
            radius: Radius of the sphere.
            center: Center point (default: origin).
        """
        c = center or Vector(0, 0, 0)
        builder = BRepPrimAPI_MakeSphere(
            gp_Pnt(c.x, c.y, c.z), radius
        )
        return cls(builder.Shape())

    @classmethod
    def make_cylinder(
        cls,
        radius: float,
        height: float,
        pnt: Optional[Vector] = None,
        direction: Optional[Vector] = None,
    ) -> "Solid":
        """Create a cylinder.

        Args:
            radius:    Radius of the cylinder.
            height:    Height of the cylinder.
            pnt:       Base center point (default: origin).
            direction: Axis direction (default: Z axis).
        """
        base = pnt or Vector(0, 0, 0)
        axis = direction or Vector(0, 0, 1)
        ax2 = gp_Ax2(
            gp_Pnt(base.x, base.y, base.z),
            gp_Dir(axis.x, axis.y, axis.z),
        )
        builder = BRepPrimAPI_MakeCylinder(ax2, radius, height)
        return cls(builder.Shape())
