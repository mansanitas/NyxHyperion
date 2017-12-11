import os
import sys
from hashlib import md5
import math
import configparser
import shutil


config = configparser.ConfigParser()
config_file = os.path.join(os.path.dirname(__file__), 'settings.cfg')
config.read(config_file)
cfg_path = config['Server']['path']
cfg_limit = int(config['Server']['limit'])


class filesandfolders:
    def deletefiles(dir):
        if os.path.exists(dir):
            filelist = [f for f in os.listdir(dir)]
            for f in filelist:
                byebye = os.path.join(dir, f)
                if os.path.isfile(byebye):
                    os.remove(byebye)
                else:
                    print('ERROR: {d} is not a local path'.format(d=byebye))

    def deletefolder(dir):
        if os.path.exists(dir):
            os.rmdir(dir)
        else:
            print('ERROR: {d} is not a local path'.format(d=dir))

    def freespace(d):
        foldersize = int(math.floor(filesandfolders.getFolderSize(d) / 1024**3))
        if foldersize > (cfg_limit - 1):  # -1 to be sure to be under the limit
            r = 0
        else:
            r = 1
        return r

    def getFolderSize(d):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(d):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size

    def getFileSize(d):
        try:
            b = os.path.getsize(d)
            return b
        except:
            return 0

    # def getFileNamesFromFolder(d):
    #     fn = []
    #     for dirpath, dirnames, filenames in os.walk(d):
    #         for f in filenames:
    #             fn = fn + [f]
    #     return fn

    def md5sum(filename):  
        """ https://bitbucket.org/prologic/tools/src/tip/md5sum?fileviewer=file-view-default """
        hash = md5()
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(128 * hash.block_size), b""):
                hash.update(chunk)
        return hash.hexdigest()

    def listdirs(folder):
        """ https://stackoverflow.com/a/142368/1623867 """
        return [d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))]

    def copyDirAndFiles(root_src_dir, root_dst_dir):
        """ https://stackoverflow.com/a/7420617/1623867 """
        for src_dir, dirs, files in os.walk(root_src_dir):
            dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            counter = 0
            for file_ in files:
                counter += 1
                src_file = os.path.join(src_dir, file_)
                dst_file = os.path.join(dst_dir, file_)
                if os.path.exists(dst_file):
                    os.remove(dst_file)
                print('INFO: Copy file {c: >3}/{ttl} {s} to {d}'.format(
                    c=counter,
                    ttl=len(files),
                    s=file_,
                    d=dst_dir
                ))
                shutil.copy(src_file, dst_dir)

    def moveDirAndFiles(root_src_dir, root_dst_dir):
        """ https://stackoverflow.com/a/7420617/1623867 """
        for src_dir, dirs, files in os.walk(root_src_dir):
            dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            counter = 0
            for file_ in files:
                counter += 1
                src_file = os.path.join(src_dir, file_)
                dst_file = os.path.join(dst_dir, file_)
                if os.path.exists(dst_file):
                    os.remove(dst_file)
                print('INFO: Move file {c: >3}/{ttl} {s} to {d}'.format(
                    c=counter,
                    ttl=len(files),
                    s=file_,
                    d=dst_dir
                ))
                shutil.move(src_file, dst_dir)


class queries:
    def query_yes_no(question, default='yes'):
        """Ask a yes/no question via raw_input() and return their answer.

        "question" is a string that is presented to the user.
        "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

        The "answer" return value is one of "yes" or "no".
        """
        # from http://code.activestate.com/recipes/577058-query-yesno/
        valid = {
                'yes': 'yes',
                'y': 'yes',
                'ye': 'yes',
                'no': 'no',
                'n': 'no'
        }
        if default is None:
            prompt = ' [y/n] '
        elif default == 'yes':
            prompt = ' [Y/n] '
        elif default == 'no':
            prompt = ' [y/N] '
        else:
            raise ValueError('invalid default answer: {d}'.format(d=default))

        while 1:
            sys.stdout.write(question + prompt)
            choice = input().lower()
            if default is not None and choice == '':
                return default
            elif choice in valid.keys():
                return valid[choice]
            else:
                sys.stdout.write('Please respond with \'yes\' or \'no\' (or \'y\' or \'n\').')