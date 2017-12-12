import escavenge
class Interface:
    def process(self, s, u):
        e = escavenge.Escavenge()
        print(s, u)
        return e.main(s, u)