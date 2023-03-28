import math

class VectorForm():
    
    def __init__(self, *args):
        self.__vector = list(args)
    
    def print(self):
        return self.__vector
    
    def len(self):
        return len(self.__vector)

class VectorCalculation():
    
    def sum(self, *args: VectorForm):
        args = list(map(lambda x: x.print(), args))
        return VectorForm(*list(map(sum, zip(*args))))
    
    def difference(self, a: VectorForm, b: VectorForm):
        a = a.print()
        b = b.print()
        return VectorForm(*[i-j for i, j in zip(a, b)])
    
    def norm(self, a: VectorForm):
        a = a.print()
        return math.sqrt(sum(i**2 for i in a)) 
    
    def scalarProduct(self, vector: VectorForm, scalar: float):
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