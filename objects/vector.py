class VectorForm():
    """A math vector form, with multiple values
    """
    def __init__(self, *args):
        """Create a math vector form
        *Args(int):
            values of the vector
        """
        self.__vector = list(args)
    
    def print(self) -> list:
        """print 2D list

        Returns:
            list: vector in list form
        """
        return self.__vector
    
    def printx(self) -> float:
        """return value of x of the vector

        Returns:
            float: value of x
        """
        return self.__vector[0]
    
    def printy(self) -> float:
        """return value of y of the vector

        Returns:
            float: value of y
        """
        return self.__vector[1]
    
    def len(self) -> int:
        """return length of vector

        Returns:
            int: legnth of vector
        """
        return len(self.__vector)

class VectorCalculation():
    """Includes different vector calculation
    """
    
    def sum(self, *args: VectorForm) -> VectorForm:
        """Calculate the sum of vectors
        *Args(vectorForm):
            vectors that will be summed up
        Returns:
            VectorForm: sum of vectors
        """
        args = list(map(lambda x: x.print(), args))
        return VectorForm(*list(map(sum, zip(*args))))
    
    def difference(self, a: VectorForm, b: VectorForm) -> VectorForm:
        """Calculate the difference of vectors (a-b)

        Args:
            a (VectorForm): first vector
            b (VectorForm): second vector

        Returns:
            VectorForm: difference of vectors
        """
        a = a.print()
        b = b.print()
        return VectorForm(*[i-j for i, j in zip(a, b)])
    
    def norm(self, a: VectorForm) -> float:
        """calculatorm the norm of the vector

        Args:
            a (VectorForm): vector

        Returns:
            float: norm of the vector
        """
        a = a.print()
        return (sum(i**2 for i in a)) ** 0.5
    
    def scalarProduct(self, vector: VectorForm, scalar: float) -> VectorForm:
        """Scalar Prodcut k(a)

        Args:
            vector (VectorForm): vector
            scalar (float): scalar

        Returns:
            VectorForm: scalar vector
        """
        return VectorForm(*[i*scalar for i in vector.print()])
    
def main():
    pass
    
if __name__ == "__main__":
    main()