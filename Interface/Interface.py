import escavenge
class Interface:
    def process(self, s, u):
        e = escavenge.Escavenge()
        return e.main(s, u)