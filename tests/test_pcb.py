import unittest
from classes.pcb import PCB
from classes.osPcb import OsPcb
from classes.mixedPcb import MixedPcb
from classes.interactivePcb import InteractivePcb
from classes.cpuBoundPcb import CpuPcb


class TestPcb(unittest.TestCase):
    
    def setUp(self):
        self.p1 = PCB(1, 500)
        self.p2 = PCB(2, 230)

    def test_childrenPCB(self):
        tempPCB = OsPcb(3, 10)
        self.assertEqual(tempPCB.getType(), "os")
        tempPCB = MixedPcb(3, 10)
        self.assertEqual(tempPCB.getType(), "mixed")
        tempPCB = InteractivePcb(3, 10)
        self.assertEqual(tempPCB.getType(), "interactive")
        tempPCB = CpuPcb(3, 10)
        self.assertEqual(tempPCB.getType(), "cpu")

    def test_pid(self):
        self.assertEqual(self.p1.getPid(), 1)
        self.assertEqual(self.p2.getPid(), 2)

        with self.assertRaises(AttributeError):
            x = self.p2.__pid

    def test_memory(self):
        self.assertEqual(self.p1.getMemory(), 500)
        self.assertEqual(self.p2.getMemory(), 230)

        with self.assertRaises(AttributeError):
            y = self.p1.__memory

    def test_wt(self):
        with self.assertRaises(ValueError):
            self.p1.addWt("10")  # type: ignore
            self.p2.addWt(1.2) # type: ignore

        self.p1.addWt(10)
        self.p2.addWt(20)
        self.assertEqual(self.p1.getWt(), 10)
        self.assertEqual(self.p2.getWt(), 20)

        self.p1.addWt(10)
        self.p2.addWt(20)
        self.assertEqual(self.p1.getWt(), 20)
        self.assertEqual(self.p2.getWt(), 40)

    def test_cpuBurst(self):
        with self.assertRaises(ValueError):
            self.p1.setCpuBurst(9.88) # type: ignore
            self.p2.setCpuBurst("1") # type: ignore

        self.p1.setCpuBurst(10)
        self.assertEqual(self.p1.getCpuBurst(), 10)
        self.p2.setCpuBurst(20)
        self.assertEqual(self.p2.getCpuBurst(), 20)

        self.p1.setCpuBurst(100)
        self.assertEqual(self.p1.getCpuBurst(), 100)
        self.p2.setCpuBurst(200)
        self.assertEqual(self.p2.getCpuBurst(), 200)

    def test_bt(self):
        with self.assertRaises(ValueError):
            self.p1.setBt("10")  # type: ignore
            self.p2.setBt(2.3) # type: ignore

        self.p1.setBt(10)
        self.p2.setBt(20)
        self.assertEqual(self.p1.getBt(), 10)
        self.assertEqual(self.p2.getBt(), 20)

        self.p1.setBt(100)
        self.p2.setBt(200)
        self.assertEqual(self.p1.getBt(), 100)
        self.assertEqual(self.p2.getBt(), 200)

    def test_iot(self):
        with self.assertRaises(ValueError):
            self.p1.setIot("10") # type: ignore
            self.p2.setIot(2.3) # type: ignore

        self.p1.setIot(10)
        self.p2.setIot(20)
        self.assertEqual(self.p1.getIot(), 10)
        self.assertEqual(self.p2.getIot(), 20)

        self.p1.setIot(100)
        self.p2.setIot(200)
        self.assertEqual(self.p1.getIot(), 100)
        self.assertEqual(self.p2.getIot(), 200)


if __name__ == "__main__":
    unittest.main()
