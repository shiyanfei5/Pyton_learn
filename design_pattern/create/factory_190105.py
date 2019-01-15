
"""
简单工厂模式：工厂函数耦合了多种产品，耦合性较大
"""
class Operation(object):
    def __init__(self, num1 ,num2):
        self.opt1 = num1
        self.opt2 = num2

    def get_result(self):
        raise  Exception('No Implentation')


class OperationAdd(Operation):

    # 调用构造函数
    def get_result(self):
        return self.opt1 + self.opt2


class OperationSub(Operation):

    def get_result(self):
        return self.opt1 - self.opt2


class OperationMul(Operation):

    def get_result(self):
        return self.opt1 * self.opt2


class OperationDiv(Operation):

    def get_result(self):
        return self.opt1 / self.opt2



class Factory(object):

    def create_op(self,ch,num1,num2):
        if ch == '+':
            return OperationAdd(num1,num2)
        elif ch == '-':
            return OperationSub(num1,num2)
        elif ch == '*':
            return OperationMul(num1,num2)
        elif ch == '/':
            return OperationDiv(num1,num2)


fa = Factory()
obj = fa.create_op('+',1,3)
print(obj.get_result())



class LeiFeng(object):
    def buy_rice(self):
        pass

    def sweep(self):
        pass

class UnderGraduate(LeiFeng):
    def buy_rice(self):
        print("UnderGraduate buy rice ok")


    def sweep(self):
        print("UnderGraduate sweep ok ")


class Volunteer(LeiFeng):
    def buy_rice(self):
        print("Volunteer buy price")

    def sweep(self):
        print("Volunteer sweep ok")

class IFactory(object):
    def create(self):
        pass


class VolunteerFactory(IFactory):
    def create(self):
        return  Volunteer()

class UnderGraduateFactory(IFactory):
    def create(self):
        return  UnderGraduateFactory()

def func(factory):
    return factory.create()

volunteer = VolunteerFactory.create()
undergraduate = UnderGraduateFactory.create()

