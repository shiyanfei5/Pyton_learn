class User(object):
    def get_user(self):
        pass
    def insert_user(self):
        pass

class MysqlUser(User):
    def get_user(self):
        print("get mysql user")

    def insert_user(self):
        print("insert mysql user")

class OracleUser(User):
    def get_user(self):
        print("get oracle user")

    def insert_user(self):
        print("insert oracle user")


class Department(object):
    def get_department(self):
        pass

    def insert_department(self):
        pass

class MysqlDepartment(object):
    def get_department(self):
        print("get mysql department")

    def insert_department(self):
        print("insert mysql department")

class OracleDepartment(object):
    def get_department(self):
        print("get oracle department")

    def insert_department(self):
        print("insert oracle department")


class AbstractFactory(object):
    def create_user(self):
        pass

    def create_department(self):
        pass


class MysqlFactory(AbstractFactory):
    def create_user(self):
        return MysqlUser()

    def create_department(self):
        return MysqlDepartment()


class OracleFactory(AbstractFactory):
    def create_user(self):
        return OracleUser()

    def create_department(self):
        return OracleDepartment()

def func( AbstractFactory):
    return AbstractFactory.create_department(),AbstractFactory.create_user()

b = MysqlFactory()
func(b)[0].get_department()