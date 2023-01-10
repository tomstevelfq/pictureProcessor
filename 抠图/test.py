import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
from rembg.bg import remove
import numpy as np
import io
from PIL import Image
import time
import shutil
from PIL import ImageFile
from PIL import Image
ImageFile.LOAD_TRUNCATED_IMAGES = True
imgs=dict()
i=1
j=1
model_name='u2net_human'

def findAllFile(base):
    files=[]
    for root, ds, fs in os.walk(base):
        for f in fs:
          fullname = os.path.join(root, f)
          files.append(fullname)
    return files

def genimg(imgpath):
    img_alpha=np.load(imgs[imgpath])
    img_array=np.array(Image.open(imgpath).convert('RGBA'))
    img_array[:,:,3]=img_alpha*img_array[:,:,3]
    img_array[:,:,2]=img_alpha*img_array[:,:,2]
    img_array[:,:,1]=img_alpha*img_array[:,:,1]
    img_array[:,:,0]=img_alpha*img_array[:,:,0]

    img=Image.fromarray(img_array)
    global i
    img.save('./抠图/'+str(i)+'.png')
    print('导出第',i,'张')
    i+=1
def koutu(input_path,output_path):
    # Uncomment the following line if working with trucated image formats (ex. JPEG / JPG)
    # ImageFile.LOAD_TRUNCATED_IMAGES = True
    img=Image.open(input_path)
    f=np.array(img)
    result = remove(f,alpha_matting=True)
    array_file_name='./2/'+str(time.time())
    np.save(array_file_name,result[:,:,3]>150)
    imgs[input_path]=array_file_name+'.npy'
    global j
    print('第',j,'张完成')
    j+=1

def start():
    print('准备中...')
    if not os.path.exists('2'):
        os.mkdir('2')
    filenames=findAllFile('./图片')
    for it in filenames:
        it='/'.join(it.split('\\'))
        ss=it.split('/')[:-1]
        it=it.split('/')[-1]
        ss[1]='抠图'
        if not(os.path.exists('/'.join(ss))):
            os.mkdir('/'.join(ss))
        try:
            koutu('./图片/'+it,'./3/'+it.split('.')[0]+'fsfd.png')
        except Exception as e:
            print('Error',e)
    for it in imgs:
        try:
            genimg(it)
        except Exception as e:
            print('Error',e)
    shutil.rmtree('2')
    
if __name__ =='__main__':
    start()
