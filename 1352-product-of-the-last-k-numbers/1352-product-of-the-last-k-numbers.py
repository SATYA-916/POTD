class ProductOfNumbers:
    s,x,i=[],set(),0
    def __init__(self):
        self.s,self.i=[1],0
    def add(self, num: int) -> None:
        self.i=self.i<<1|(num!=0) #mask creation
        self.s.append(max(self.s[-1]*num,1))
    def getProduct(self, k: int) -> int:
        if self.i&(1<<k)-1==(1<<k)-1: #chk the mask with number
            return self.s[-1]//self.s[-k-1]
        return 0


# Your ProductOfNumbers object will be instantiated and called as such:
# obj = ProductOfNumbers()
# obj.add(num)
# param_2 = obj.getProduct(k)