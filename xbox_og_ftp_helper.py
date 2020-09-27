import os
import argparse
import operator
import pathlib
import py7zr
from ftplib import FTP

# pip install py7zr


def humanize_bytes(bytes, precision=1):
    """Return a humanized string representation of a number of bytes.
    >>> humanize_bytes(1024*12342)
    '12.1 MB'
    """

    abbrevs = (
        (1<<50, 'PB'),
        (1<<40, 'TB'),
        (1<<30, 'GB'),
        (1<<20, 'MB'),
        (1<<10, 'kB'),
        (1, 'b')
    )
    if bytes == 1:
        return '1b'
    for factor, suffix in abbrevs:
        if bytes >= factor:
            break
    return '%.*f%s' % (precision, bytes / factor, suffix)


def get_dir_size(path):
    dirSize = 0
    for dirName, subdirList, fileList in os.walk(path):
        try:
            dirSize += sum(os.path.getsize(os.path.join(dirName, name)) for name in fileList)
        except OSError:
            pass
    return dirSize


def myftp_connect(addr, user, passwd, dest):
    try:
        ftp = FTP("192.168.1.123")
        ftp.login("xbox", "xbox")
        ftp.cwd(dest)
        return ftp
    except Exception as e:
        print(e)
        return None


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--addr", help="XBOX IPv4 address", required=True)
    parser.add_argument("--user", default="xbox", help="ftp user (default: xbox)")
    parser.add_argument("--pass", dest='passwd', default="xbox", help="ftp password (default: xbox)")
    parser.add_argument("--list", help="list games currently present on XBOX", action="store_true")
    parser.add_argument("--dryrun", help="dry run without actually transferring files", action="store_true")
    parser.add_argument("--path", dest='src', default=".", help="path to source directory (default: current directory)")
    parser.add_argument("--dest", dest='dst', default="F:\\Games\\", help="destination path (default: F:\\Games)")
    args = parser.parse_args()

    path = pathlib.Path(args.src).resolve()
    print("ftp credentials..: %s %s/%s\nsource...........: %s\ndestination......: %s\n" % (args.addr, args.user, args.passwd, path, args.dst))

    if not args.dryrun:
        ftp = myftp_connect(args.addr, args.user, args.passwd, args.dst)
        if ftp is None:
            exit(1)

    if args.list and not args.dryrun:
        print("[listing] %s" % args.dst)
        ftp.dir()
        ftp.quit()
        exit(0)

    for f in os.listdir(path):
        fullpath = os.path.join(path, f)
        if os.path.isdir(fullpath):
            print("[transferring] %s | %9s" % (fullpath, humanize_bytes(get_dir_size(fullpath))))
            if not args.dryrun:
                upload_dir(ftp, fullpath, os.path.join(args.dst, f))
        elif os.path.isfile(fullpath):
            if pathlib.Path(fullpath).suffix == '.7z':
                with py7zr.SevenZipFile(fullpath, mode='r') as z:
                    print("[extracting] %s | %9s" % (fullpath, os.path.getsize(fullpath)))
                    if not args.dryrun:
                        try:
                            z.extractall('_tmp')
                        except Exception as e:
                            pass
                        for root, dirs, files in os.walk('_tmp'):
                            if 'default.xbe' in files:
                                break
                        print("root of extracted .7z game is: %s" % (root))
                        upload_dir(ftp, os.path.join(os.path.dirname(fullpath), root), os.path.join(args.dst, f))
        else:
            pass
            #print("%s %s" % (f, 'not a directory or .7z file'))
    ftp.quit()

