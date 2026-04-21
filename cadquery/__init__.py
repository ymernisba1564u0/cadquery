"""CadQuery - A parametric 3D CAD scripting framework built on top of Open CASCADE Technology (OCCT).

CadQuery is a Python library that allows you to build 3D models using a fluent, chainable API.
It wraps the powerful Open CASCADE Technology (OCCT) geometry kernel via the OCP Python bindings.

Basic usage::

    import cadquery as cq

    result = (
        cq.Workplane("XY")
        .box(10, 10, 10)
        .faces(">Z")
        .hole(5)
    )

    cq.exporters.export(result, "output.step")
"""

from .cq import (
    CQContext,
    CQObject,
    Workplane,
)
from .occ_impl.geom import (
    BoundBox,
    Location,
    Matrix,
    Plane,
    Vector,
)
from .occ_impl.shapes import (
    Compound,
    Edge,
    Face,
    Shell,
    Solid,
    Vertex,
    Wire,
    Shape,
)
from .occ_impl.assembly import (
    Assembly,
    Constraint,
)
from .selectors import (
    AndSelector,
    AreaNthSelector,
    BaseDirSelector,
    BoxSelector,
    CenterNthSelector,
    DirectionMinMaxSelector,
    DirectionNthSelector,
    DirectionSelector,
    EdgeLengthSelector,
    FaceAreaSelector,
    HasCenterOfMassSelector,
    InverseSelector,
    LengthNthSelector,
    NearestToPointSelector,
    OrSelector,
    ParallelDirSelector,
    PerpendicularDirSelector,
    RadiusNthSelector,
    StringSyntaxSelector,
    SubtractSelector,
    SumSelector,
    TypeSelector,
)
from . import exporters
from . import importers
from .assembly import (
    Color,
    Assembly as ConstraintAssembly,
)

__version__ = "2.5.0.dev0"

__all__ = [
    # Core workplane
    "CQContext",
    "CQObject",
    "Workplane",
    # Geometry primitives
    "BoundBox",
    "Location",
    "Matrix",
    "Plane",
    "Vector",
    # Topology shapes
    "Compound",
    "Edge",
    "Face",
    "Shell",
    "Solid",
    "Vertex",
    "Wire",
    "Shape",
    # Assembly
    "Assembly",
    "Color",
    "Constraint",
    # Selectors
    "AndSelector",
    "AreaNthSelector",
    "BaseDirSelector",
    "BoxSelector",
    "CenterNthSelector",
    "DirectionMinMaxSelector",
    "DirectionNthSelector",
    "DirectionSelector",
    "EdgeLengthSelector",
    "FaceAreaSelector",
    "HasCenterOfMassSelector",
    "InverseSelector",
    "LengthNthSelector",
    "NearestToPointSelector",
    "OrSelector",
    "ParallelDirSelector",
    "PerpendicularDirSelector",
    "RadiusNthSelector",
    "StringSyntaxSelector",
    "SubtractSelector",
    "SumSelector",
    "TypeSelector",
    # Submodules
    "exporters",
    "importers",
    # Version
    "__version__",
]
