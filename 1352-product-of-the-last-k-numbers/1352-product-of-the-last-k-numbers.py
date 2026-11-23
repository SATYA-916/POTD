class ProductOfNumbers:
    s,x,i=[],set(),0
    def __init__(self):
        self.s,self.i,self.x=[1],0,-1
    def add(self, num: int) -> None:
        self.i+=1
        if num==0:
            self.x=self.i #last index of 0
        self.s.append(max(self.s[-1]*num,1))
    def getProduct(self, k: int) -> int:
        print(self.i)
        if self.x>=self.i-k+1:
            return 0
        return self.s[-1]//self.s[-k-1]


# Your ProductOfNumbers object will be instantiated and called as such:
# obj = ProductOfNumbers()
# obj.add(num)
# param_2 = obj.getProduct(k)