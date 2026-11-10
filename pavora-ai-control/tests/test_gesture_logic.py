import unittest
from gesture_logic import Point, classify, distance

def hand(index=False,middle=False,ring=False,pinky=False,pinch=False):
    p=[Point(.5,.8) for _ in range(21)]
    p[0],p[9]=Point(.5,.9),Point(.5,.5)
    for tip,pip,active in ((8,6,index),(12,10,middle),(16,14,ring),(20,18,pinky)):
        p[pip]=Point(.5,.5)
        p[tip]=Point(.5,.35 if active else .65)
    p[4]=Point(.5,.35) if pinch else Point(.1,.8)
    return p

class TestGestures(unittest.TestCase):
    def test_pointer(self): self.assertEqual(classify(hand(index=True)),"pointer")
    def test_scroll(self): self.assertEqual(classify(hand(index=True,middle=True)),"scroll")
    def test_stop(self): self.assertEqual(classify(hand(True,True,True,True)),"stop")
    def test_click(self): self.assertEqual(classify(hand(index=True,pinch=True)),"click")
    def test_idle(self): self.assertEqual(classify(hand()),"idle")
    def test_invalid(self): self.assertEqual(classify([]),"idle")
    def test_distance(self): self.assertEqual(distance(Point(0,0),Point(3,4)),5)

if __name__=="__main__": unittest.main()
