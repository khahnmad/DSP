import All_Functions as af
import time

fake_list = [0,1,2,2,3,4,5,2,4,7]

try:
    test = af.import_csv('does_not_exist.csv')
except FileNotFoundError:
    af.export_list('does_not_exist.csv', fake_list)
    time.sleep(10)
    test = af.import_csv('does_not_exist.csv')