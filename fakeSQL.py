class fakeSQL(object):
    def __init__(self, *args):
        pass
    def cursor(self, *args):
        return Cursor()
    def commit(self, *args):
        pass
    def disconnect (self,*args):
        pass
class Cursor():
    def __init__(self, *args):
        print("cursor class inited")
        pass

    def execute(self,*args):
        print("executed")
        pass

    def fetchone(self, *args):
        print("fetched")
        return [0,1]