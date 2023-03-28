import math

#math 2D vector form
class VectorForm():
    
    def __init__(self, *args):
        self.__vector = list(args)
    
    #return in 2D list
    def print(self) -> list:
        return self.__vector
    
    #return x only
    def printx(self) -> float:
        return self.__vector[0]
    #return y only
    def printy(self) -> float:
        return self.__vector[1]
    
    #return dimension of the vector
    def len(self) -> int:
        return len(self.__vector)

class VectorCalculation():
    
    #vector sum a+b
    def sum(self, *args: VectorForm) -> VectorForm:
        args = list(map(lambda x: x.print(), args))
        return VectorForm(*list(map(sum, zip(*args))))
    
    #vector difference a-b
    def difference(self, a: VectorForm, b: VectorForm) -> VectorForm:
        a = a.print()
        b = b.print()
        return VectorForm(*[i-j for i, j in zip(a, b)])
    
    #vector norm |a|
    def norm(self, a: VectorForm) -> float:
        a = a.print()
        return math.sqrt(sum(i**2 for i in a)) 
    
    #vector scalar product k(a)
    def scalarProduct(self, vector: VectorForm, scalar: float) -> VectorForm:
        return VectorForm(*[i*scalar for i in vector.print()])
    
def main():
    x = VectorForm(3, 4)
    y = VectorForm(1, 2)
    acc = [x]
    print(acc)
    print(VectorCalculation().sum(*acc).print())
    
    x = VectorForm
    acc = [x]
    print(acc)
    x = VectorCalculation.sum(*acc)
    print(x.print())
    return VectorCalculation.sum(*acc)
    
if __name__ == "__main__":
    main()