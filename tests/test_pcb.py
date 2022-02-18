import unittest
from classes.pcb import PCB
from utils import currStatus


class TestPcb(unittest.TestCase):

    currMemory = currStatus["memory"]
    @classmethod
    def setUpClass(cls):
        currStatus["memory"] = 5000

    @classmethod
    def tearDownClass(cls):
        currStatus["memory"] = currMemory

    def setUp(self):
        self.p1 = PCB(1, 500)
        self.p2 = PCB(2, 230)

    def test_pid(self):
        self.assertEqual(self.p1.getPid(), 1)
        self.assertEqual(self.p2.getPid(), 2)

        with self.assertRaises(AttributeError):
            self.p1.__pid = 10
            self.p2.__pid = 10
    
    def test_memory(self):
        self.assertEqual(self.p1.getMemory(), 500)
        self.assertEqual(self.p2.getMemory(), 230)

        with self.assertRaises(AttributeError):
            self.p1.__memory = 20
            self.p2.__memory = 45

    def test_wt(self):
        with self.assertRaises(ValueError):
            self.p1.addWt("10")
            self.p2.addWt(1.2)

        self.p1.addWt(10)
        self.p2.addWt(20)
        self.assertEqual(self.p1.getWt(), 10)
        self.assertEqual(self.p2.getWt(), 20)

        self.p1.addWt(10)
        self.p2.addWt(20)
        self.assertEqual(self.p1.getWt(), 20)
        self.assertEqual(self.p2.getWt(), 40)
    
    def test_cpuT(self):
        with self.assertRaises(ValueError):
            self.p1.addCpuT(9.88)
            self.p2.addCpuT("1")

        self.p1.addCpuT(10)
        self.p2.addCpuT(20)
        self.assertEqual(self.p1.getCpuT(), 10)
        self.assertEqual(self.p2.getCpuT(), 20)

        self.p1.addCpuT(10)
        self.p2.addCpuT(20)
        self.assertEqual(self.p1.getCpuT(), 20)
        self.assertEqual(self.p2.getCpuT(), 40)
    
    def test_bt(self):
        with self.assertRaises(ValueError):
            self.p1.setBt("10")
            self.p2.setBt(2.3)

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
            self.p1.setIot("10")
            self.p2.setIot(2.3)

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