# Save all train, test, val dataset
import os
import shutil
import time
from zipfile import ZipFile 
import requests
import tarfile
#root_dir = '/content/gdrive/' + 'parking_dataset_a/'
#dataset_dir = root_dir + 'CNR-EXT-Patches-150x150/'

root_dir = 'D:/'
dataset_dir = root_dir + 'CNR-EXT-Patches-150x150/'


def download_zip(save_d):
    # download the dataset
    if not os.path.exists(save_d):
        os.makedirs(save_d)
    url = 'http://cnrpark.it/dataset/CNR-EXT-Patches-150x150.zip'
    myfile = requests.get(url)
    fn = save_d + 'CNR-EXT-Patches-150x150.zip'
    open(fn, 'wb').write(myfile.content)

    # opening the zip file in READ mode 
    with ZipFile(fn, 'r') as zip: 
        # printing all the contents of the zip file 
        zip.printdir() 
        # extracting all the files 
        print('Extracting all the files now...') 
        zip.extractall(save_d) 
        print('Done!') 

def download_tar(save_d):
    # download the dataset
    if not os.path.exists(save_d):
        os.makedirs(save_d)
    url = 'http://cnrpark.it/dataset/CNR-EXT_FULL_IMAGE_1000x750.tar'
    myfile = requests.get(url)
    file_dir = save_d + 'full_image_and_csv.tar'
    print('Downloading all the files now...') 
    open(file_dir, 'wb').write(myfile.content)
    print('Done!')
    print('Extracting all the files now...') 
    tar = tarfile.open(file_dir)
    tar.extractall(save_d)
    tar.close()
    print('Done!\n')

def create_save_path(save_dir):
    if not os.path.exists(save_dir + 'train/busy'):
        os.makedirs(save_dir + 'train/busy')
    if not os.path.exists(save_dir + 'train/free'):
        os.makedirs(save_dir + 'train/free')
    if not os.path.exists(save_dir + 'test/busy'):
        os.makedirs(save_dir + 'test/busy')
    if not os.path.exists(save_dir + 'test/free'):
        os.makedirs(save_dir + 'test/free')
    if not os.path.exists(save_dir + 'val/busy'):
        os.makedirs(save_dir + 'val/busy')
    if not os.path.exists(save_dir + 'val/free'):
        os.makedirs(save_dir + 'val/free')

def create_parking_dataset(save_dir):
    create_save_path(save_dir)
    download_zip(root_dir)
    download_tar(root_dir)
    f_n = root_dir + 'LABELS/'
    fn = f_n + 'train.txt'
    train_path = [line for line in open(f_n + 'train.txt')]
    test_path = [line for line in open(f_n + 'test.txt')]
    val_path = [line for line in open(f_n + 'val.txt')]    
    #print(val_path)
    
    count = 0
    nb = 0
    nf = 0
    for li in train_path:
        count += 1
        source_n = li.split(' ')[0]
        source_n = root_dir + 'PATCHES/' + source_n
        print('\r',str(count),' ',source_n,end='')
        bl = int(li.split(' ')[1])
        if bl == 1:
            sname = save_dir + 'train/busy/' + li.split(' ')[0].split('/')[-1]
            nb += 1
        else:
            sname = save_dir + 'train/free/' + li.split(' ')[0].split('/')[-1]
            nf += 1
        print('\r',str(count),' ',sname,end='')
        shutil.copy(source_n, sname)

    print('\nCNR-EXT train dataset\nBusy image:%d\nFree image:%d'%(nb, nf))
    print('Total image in train dataset:%d\n'%(nb+nf))

    nb_before = nb
    nf_before = nf
    count = 0
    for li in test_path:
        count += 1  
        source_n = li.split(' ')[0]
        source_n = root_dir + 'PATCHES/' + source_n
        #print('\r',str(count),' ',source_n,end='')
        bl = int(li.split(' ')[1])
        if bl == 1:
            sname = save_dir + 'test/busy/' + li.split(' ')[0].split('/')[-1]
            nb += 1
        else:
            sname = save_dir + 'test/free/' + li.split(' ')[0].split('/')[-1]
            nf += 1
        print('\r',str(count),' ',source_n,end='')
        shutil.copy(source_n, sname)

    print('\nCNR-EXT test dataset\nBusy image:%d\nFree image:%d'%(nb-nb_before, nf-nf_before))
    print('Total image in test dataset:%d\n'%(nb+nf-nb_before-nf_before))

    nb_before = nb
    nf_before = nf
    count = 0
    for li in val_path:
        count += 1
        source_n = li.split(' ')[0]
        source_n = root_dir + 'PATCHES/' + source_n
        
        bl = int(li.split(' ')[1])
        if bl == 1:
            sname = save_dir + 'val/busy/' + li.split(' ')[0].split('/')[-1]
            nb += 1
        else:
            sname = save_dir + 'val/free/' + li.split(' ')[0].split('/')[-1]
            nf += 1
        print('\r',str(count),' ',source_n,end='')
        shutil.copy(source_n, sname)
    print('\nCNR-EXT val dataset\nBusy image:%d\nFree image:%d'%(nb-nb_before, nf-nf_before))
    print('Total image in val dataset:%d\n'%(nb+nf-nb_before-nf_before))

    print('\n\n>>>CNR-EXT database\nBusy image:%d\nFree image:%d'%(nb-nb_before, nf-nf_before))
    print('Total image in CNR-EXT database:%d\n'%(nb+nf-nb_before-nf_before))

def create_small_parking_dataset(save_dir):
    if not os.path.exists(save_dir + 'train_samll/busy'):
        os.makedirs(save_dir + 'train_samll/busy')
    if not os.path.exists(save_dir + 'train_samll/free'):
        os.makedirs(save_dir + 'train_samll/free')
    if not os.path.exists(save_dir + 'test_small/busy'):
        os.makedirs(save_dir + 'test_small/busy')
    if not os.path.exists(save_dir + 'test_small/free'):
        os.makedirs(save_dir + 'test_small/free')
    if not os.path.exists(save_dir + 'val_small/busy'):
        os.makedirs(save_dir + 'val_small/busy')
    if not os.path.exists(save_dir + 'val_small/free'):
        os.makedirs(save_dir + 'val_small/free')
    f_n = root_dir + 'LABELS/'
    fn = f_n + 'train.txt'
    train_path = [line for line in open(f_n + 'train.txt')]
    test_path = [line for line in open(f_n + 'test.txt')]
    val_path = [line for line in open(f_n + 'val.txt')]    
    #print(val_path)
    
    count = 0
    for li in train_path:
        if count == 5000:
            break
        count += 1
        source_n = li.split(' ')[0]
        source_n = root_dir + 'PATCHES/' + source_n
        print('\r',str(count),' ',source_n,end='')
        bl = int(li.split(' ')[1])
        if bl == 1:
            sname = save_dir + 'train_samll/busy/' + li.split(' ')[0].split('/')[-1]
        else:
            sname = save_dir + 'train_small/free/' + li.split(' ')[0].split('/')[-1]
        print('\r',str(count),' ',sname,end='')
        shutil.copy(source_n, sname)
    
    count = 0
    for li in test_path:
        if count == 1500:
            break
        count += 1  
        source_n = li.split(' ')[0]
        source_n = root_dir + 'PATCHES/' + source_n
        #print('\r',str(count),' ',source_n,end='')
        bl = int(li.split(' ')[1])
        if bl == 1:
            sname = save_dir + 'test_small/busy/' + li.split(' ')[0].split('/')[-1]
        else:
            sname = save_dir + 'test_small/free/' + li.split(' ')[0].split('/')[-1]
        print('\r',str(count),' ',source_n,end='')
        shutil.copy(source_n, sname)

    count = 0
    for li in val_path:
        if count == 1500:
            break
        count += 1
        source_n = li.split(' ')[0]
        source_n = root_dir + 'PATCHES/' + source_n
        
        bl = int(li.split(' ')[1])
        if bl == 1:
            sname = save_dir + 'val_small/busy/' + li.split(' ')[0].split('/')[-1]
        else:
            sname = save_dir + 'val_small/free/' + li.split(' ')[0].split('/')[-1]
        print('\r',str(count),' ',source_n,end='')
        shutil.copy(source_n, sname)

# main part
if __name__ == '__main__':
    create_parking_dataset(dataset_dir)
    create_small_parking_dataset(dataset_dir)
    print('\nFinish created CNR-EXT dataset!\n')