import sys
import os
import pathlib
import py7zr
from ftplib import FTP

# pathnames should not contain trailing slash!
# 3rd param is e.g. F:\\Games\\Ford Racing 2
def upload_dir(ftp, localdir, ftpdir):
    try:
        if (ftp.pwd() == '/'):
            ftp.cwd(os.path.dirname(ftpdir)) # runs initially to cd into e.g. F:\\Games
        ftp.mkd(os.path.basename(ftpdir))
        ftp.cwd(os.path.basename(ftpdir)) # .cwd() expects relative path
    except Exception as e:
        print(e)
        raise

    localdir = os.path.join(localdir, '') # append slash at the end if not already there
    ftpdir = os.path.join(ftpdir, '')     # append slash at the end if not already there

    for fname in os.listdir(localdir):
        if os.path.isdir(localdir + fname):      
            upload_dir(ftp, localdir + fname, ftpdir + fname)
        else:
            print('STOR ' + ftpdir + fname)
            with open(localdir + fname, 'rb') as f:
                try:
                    ftp.storbinary('STOR ' + fname, f)
                except Exception as e:
                    print(e)
                    pass



f = 'Ford Racing 2 [!].7z'

if pathlib.Path(f).suffix == '.7z':
    with py7zr.SevenZipFile(f, mode='r') as z:
        try:
            z.extractall('_tmp')
        except Exception as e:
            pass
        for root, dirs, files in os.walk('_tmp'):
            if 'default.xbe' in files:
                break
        print("root is %s" % (root))

src = "C:\\Users\\malfunction\\repo\\PythonPractice"
path = pathlib.Path("_tmp\\Ford Racing 2").resolve()
fullpath = os.path.join(src, path)

ftp = FTP("192.168.1.123")
ftp.login("xbox", "xbox")

dst = "F:\\Games\\"
root = "_tmp\\Ford Racing 2"
ftpdir = os.path.join(dst, os.path.basename(root))

upload_dir(ftp, fullpath, ftpdir)
