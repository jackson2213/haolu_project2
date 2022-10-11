FPS = 25
SECOND =5



def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return inner

@singleton
class RingBuffer:
    """ class that implements a not-yet-full buffer """
    def __init__(self):
        self.max = FPS*SECOND
        self.data = []

    class __Full:
        """ class that implements a full buffer """
        def append(self, x):
            """ Append an element overwriting the oldest one. """
            self.data[self.cur] = x
            self.cur = (self.cur+1) % self.max
        def get(self):
            """ return list of elements in correct order """
            return self.data[self.cur:]+self.data[:self.cur]

    def append(self,x):
        """append an element at the end of the buffer"""
        self.data.append(x)
        if len(self.data) == self.max:
            self.cur = 0
            # Permanently change self's class from non-full to full
            self.__class__ = self.__Full

    def get(self):
        """ Return a list of elements from the oldest to the newest. """
        return self.data




# sample usage
# sample usage

# if __name__=='__main__':
#     pass

    # x=RingBuffer()
    # x.append(1)
    # print(id(x), x.get())
    # x.append(2)
    # print(id(x), x.get())
    # x.append(3); x.append(4),; x.append(4)
    # print(id(x), x.get())
    # x.append(5)
    # print(id(x), x.get())
    # x.append(6)
    # print(x.__class__, x.get())
    # x.append(7)
    # print(x.__class__, x.get())
    # x.append(8)
    # print(x.__class__, x.get())
    # x.append(9)
    # print(x.__class__, x.get())
    # x.append(10)
    # print(x.__class__, x.get())






