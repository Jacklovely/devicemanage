import os
from datetime import datetime
from devicemanage.settings import BASE_LOG_DIR
f=open(r'/Users/christbella/work/workspace/python/devicemanage/log/test.txt','a+')
f.seek(0)
res1=len(f.readlines())

if res1 <6:
    f.write('fghfgjfgj\n')
    if res1 == 2:
        f.close()
        old_filename=BASE_LOG_DIR+"/test.txt"
        new_filename=old_filename+"."+datetime.now().strftime("%Y%m%d%H%M")
        print(old_filename)
        os.rename(old_filename,new_filename)
        f=open(old_filename,'a+')
        f.close()
# else:
#     f.seek(0)
#     f.truncate()
#     f.write('sdfsdg\n')

f.close()