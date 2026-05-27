/-
Geometry functions for the Lean to Python corpus.
Contains 2D and 3D geometry, computational geometry, etc.
-/
namespace Corpus.Geometry

-- 2D Point
structure Point2D where
  x : Float
  y : Float
deriving Repr

-- 3D Point
structure Point3D where
  x : Float
  y : Float
  z : Float
deriving Repr

-- Distance between 2D points
def dist2D (p1 p2 : Point2D) : Float :=
  let dx := p2.x - p1.x
  let dy := p2.y - p1.y
  Float.sqrt (dx * dx + dy * dy)

-- Distance between 3D points
def dist3D (p1 p2 : Point3D) : Float :=
  let dx := p2.x - p1.x
  let dy := p2.y - p1.y
  let dz := p2.z - p1.z
  Float.sqrt (dx * dx + dy * dy + dz * dz)

-- Manhattan distance 2D
def manhattan2D (p1 p2 : Point2D) : Float :=
  Float.abs (p2.x - p1.x) + Float.abs (p2.y - p1.y)

-- Chebyshev distance 2D
def chebyshev2D (p1 p2 : Point2D) : Float :=
  max (Float.abs (p2.x - p1.x)) (Float.abs (p2.y - p1.y))

-- Midpoint 2D
def midpoint2D (p1 p2 : Point2D) : Point2D :=
  { x := (p1.x + p2.x) / 2, y := (p1.y + p2.y) / 2 }

-- Midpoint 3D
def midpoint3D (p1 p2 : Point3D) : Point3D :=
  { x := (p1.x + p2.x) / 2, y := (p1.y + p2.y) / 2, z := (p1.z + p2.z) / 2 }

-- Dot product 2D
def dot2D (p1 p2 : Point2D) : Float :=
  p1.x * p2.x + p1.y * p2.y

-- Dot product 3D
def dot3D (p1 p2 : Point3D) : Float :=
  p1.x * p2.x + p1.y * p2.y + p1.z * p2.z

-- Cross product 2D (returns scalar - z component of 3D cross product)
def cross2D (p1 p2 : Point2D) : Float :=
  p1.x * p2.y - p1.y * p2.x

-- Cross product 3D
def cross3D (p1 p2 : Point3D) : Point3D :=
  { x := p1.y * p2.z - p1.z * p2.y,
    y := p1.z * p2.x - p1.x * p2.z,
    z := p1.x * p2.y - p1.y * p2.x }

-- Magnitude of 2D vector
def magnitude2D (p : Point2D) : Float :=
  Float.sqrt (p.x * p.x + p.y * p.y)

-- Magnitude of 3D vector
def magnitude3D (p : Point3D) : Float :=
  Float.sqrt (p.x * p.x + p.y * p.y + p.z * p.z)

-- Normalize 2D vector
def normalize2D (p : Point2D) : Point2D :=
  let m := magnitude2D p
  if m == 0 then p
  else { x := p.x / m, y := p.y / m }

-- Normalize 3D vector
def normalize3D (p : Point3D) : Point3D :=
  let m := magnitude3D p
  if m == 0 then p
  else { x := p.x / m, y := p.y / m, z := p.z / m }

-- Triangle area using coordinates
def triangleArea (p1 p2 p3 : Point2D) : Float :=
  Float.abs ((p2.x - p1.x) * (p3.y - p1.y) - (p3.x - p1.x) * (p2.y - p1.y)) / 2

-- Check if point is inside triangle (using barycentric coordinates)
def pointInTriangle (p p1 p2 p3 : Point2D) : Bool :=
  let d1 := sign p p1 p2
  let d2 := sign p p2 p3
  let d3 := sign p p3 p1
  let hasNeg := d1 < 0 || d2 < 0 || d3 < 0
  let hasPos := d1 > 0 || d2 > 0 || d3 > 0
  !(hasNeg && hasPos)
where
  sign (p1 p2 p3 : Point2D) : Float :=
    (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)

-- Circle area
def circleArea (radius : Float) : Float :=
  3.14159265358979 * radius * radius

-- Circle circumference
def circleCircumference (radius : Float) : Float :=
  2 * 3.14159265358979 * radius

-- Sphere volume
def sphereVolume (radius : Float) : Float :=
  (4 / 3) * 3.14159265358979 * radius * radius * radius

-- Sphere surface area
def sphereSurfaceArea (radius : Float) : Float :=
  4 * 3.14159265358979 * radius * radius

-- Rectangle area
def rectangleArea (width height : Float) : Float :=
  width * height

-- Rectangle perimeter
def rectanglePerimeter (width height : Float) : Float :=
  2 * (width + height)

-- Polygon area (shoelace formula)
def polygonArea (vertices : List Point2D) : Float :=
  let rec go (vs : List Point2D) (first : Point2D) (prev : Point2D) (acc : Float) : Float :=
    match vs with
    | [] => (acc + cross2D prev first) / 2
    | v :: rest => go rest first v (acc + cross2D prev v)
  match vertices with
  | [] => 0
  | [_] => 0
  | first :: rest => Float.abs (go rest first first 0)

-- Check if polygon is convex
def isConvexPolygon (vertices : List Point2D) : Bool :=
  match vertices with
  | [] => true
  | [_] => true
  | [_, _] => true
  | first :: second :: rest =>
    let rec check (prev2 prev1 : Point2D) (vs : List Point2D) (sign : Option Bool) : Bool :=
      match vs with
      | [] =>
        let c1 := cross2D (sub prev1 prev2) (sub first prev1)
        let c2 := cross2D (sub first prev1) (sub second first)
        checkSign c1 sign && checkSign c2 sign
      | v :: rest' =>
        let c := cross2D (sub prev1 prev2) (sub v prev1)
        match checkSign c sign with
        | false => false
        | true =>
          let newSign := if c == 0 then sign else some (c > 0)
          check prev1 v rest' newSign
    check first second rest none
where
  sub (a b : Point2D) : Point2D := { x := a.x - b.x, y := a.y - b.y }
  checkSign (c : Float) (sign : Option Bool) : Bool :=
    match sign with
    | none => true
    | some s => c == 0 || (c > 0) == s

-- Orientation of three points (0: collinear, 1: clockwise, 2: counter-clockwise)
def orientation (p q r : Point2D) : Nat :=
  let val := (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
  if val == 0 then 0
  else if val > 0 then 1 else 2

-- Check if two line segments intersect
def segmentsIntersect (p1 q1 p2 q2 : Point2D) : Bool :=
  let o1 := orientation p1 q1 p2
  let o2 := orientation p1 q1 q2
  let o3 := orientation p2 q2 p1
  let o4 := orientation p2 q2 q1
  (o1 != o2 && o3 != o4) ||
  (o1 == 0 && onSegment p1 p2 q1) ||
  (o2 == 0 && onSegment p1 q2 q1) ||
  (o3 == 0 && onSegment p2 p1 q2) ||
  (o4 == 0 && onSegment p2 q1 q2)
where
  onSegment (p q r : Point2D) : Bool :=
    q.x <= max p.x r.x && q.x >= min p.x r.x &&
    q.y <= max p.y r.y && q.y >= min p.y r.y

-- Rotate point around origin by angle (in radians)
def rotate2D (p : Point2D) (angle : Float) : Point2D :=
  let c := Float.cos angle
  let s := Float.sin angle
  { x := p.x * c - p.y * s, y := p.x * s + p.y * c }

-- Scale point from origin
def scale2D (p : Point2D) (factor : Float) : Point2D :=
  { x := p.x * factor, y := p.y * factor }

-- Translate point
def translate2D (p : Point2D) (dx dy : Float) : Point2D :=
  { x := p.x + dx, y := p.y + dy }

-- Reflect point over x-axis
def reflectX (p : Point2D) : Point2D :=
  { x := p.x, y := -p.y }

-- Reflect point over y-axis
def reflectY (p : Point2D) : Point2D :=
  { x := -p.x, y := p.y }

-- Angle between two vectors
def angleBetween (v1 v2 : Point2D) : Float :=
  let dot := dot2D v1 v2
  let m1 := magnitude2D v1
  let m2 := magnitude2D v2
  if m1 == 0 || m2 == 0 then 0
  else Float.acos (dot / (m1 * m2))

-- Project point onto line (from a through b)
def projectOntoLine (p a b : Point2D) : Point2D :=
  let ap := { x := p.x - a.x, y := p.y - a.y : Point2D }
  let ab := { x := b.x - a.x, y := b.y - a.y : Point2D }
  let t := dot2D ap ab / dot2D ab ab
  { x := a.x + t * ab.x, y := a.y + t * ab.y }

-- Distance from point to line
def distanceToLine (p a b : Point2D) : Float :=
  let proj := projectOntoLine p a b
  dist2D p proj

end Corpus.Geometry
