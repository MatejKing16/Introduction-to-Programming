class Vector():

    def __init__(self,x: int | float,y: int | float,z: int|float) -> "Vector":
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __str__(self) -> str:
        return f"Vector (x:{self.x} y:{self.y} z:{self.z})"


    def __add__(self, other: "Vector") -> "Vector":
        if isinstance(other, Vector):
            return Vector(
                self.x + other.x,
                self.y + other.y,
                self.z + other.z,
                )
        elif isinstance(other, (int,float)):
            return Vector(
                self.x + other,
                self.y + other,
                self.z + other, 
            )
        else: 
            raise NotImplemented

    def __radd__(self, other: "Vector" | float | int) -> "Vector":
        return self.__add__(other)

    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)

    def __sub__(self, other: "Vector" | float | int) -> "Vector":
        return self.__add__(-other)

    def __rsub__(self, other: "Vector" | float | int) -> "Vector":
        return self.__neg__().__add__(other)

   
    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z
    
    def __mul__(self, other: "Vector" | float | int) -> "Vector":
        if isinstance(other, Vector):
            return Vector(
            self.x * other.x,
            self.y * other.y,
            self.z * other.z,
                )
        elif isinstance(other, (int,float)):
            return Vector(
            self.x * other,
            self.y * other,
            self.z * other, 
            )
        else: 
            raise NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __eq__(self, other):
        return (
            self.x == other.x and
            self.y == other.y and
            self.z == other.z
        )



if __name__ == "__main__":
    a = Vector(1,2,3)
    b = Vector(1,2,3)

    print(a * b)
    print(b * a)
    print(a * 2)
    print(2 * a)