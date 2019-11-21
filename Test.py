import inspect
import Test2

if __name__=='__main__':
    for key,data in inspect.getmembers(Test2,inspect.isclass):
        print(data.a)