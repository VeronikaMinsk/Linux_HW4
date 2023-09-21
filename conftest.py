import random
import string
import subprocess
from datetime import datetime
import pytest
import yaml
from checkout import  ssh_checkout

with open('config.yaml') as f:
    data = yaml.safe_load(f)


# or from conftest import data


@pytest.fixture()
def make_folders():
    # create all path in dir
    return ssh_checkout(data["host"], data["user"], data["password"],
                        "mkdir {} {} {} {} {}".format(data['folder_in'], data['folder_out'], data['folder_ext'],
                                                      data['folder_bad_arx'],
                                                      data['folder_ext2']), "")


@pytest.fixture()
def clear_folders():
    # remove all in dir /* all contains
    return ssh_checkout(data["host"], data["user"], data["password"],
                        "rm -rf {}/* {}/* {}/* {}/* {}/*".format(data['folder_in'], data['folder_out'],
                                                                 data['folder_ext'],
                                                                 data['folder_bad_arx'],
                                                                 data['folder_ext2']), "")


@pytest.fixture()
def make_files():
    # create random named(letters and numbers, length k =5) files which return as list
    list_off_files = []
    for i in range(data['count']):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout(data["host"], data["user"], data["password"],
                        "cd {}; dd if=/dev/urandom of={} bs={}M count=1 iflag=fullblock".format(data['folder_in'],
                                                                                                filename,
                                                                                                data['size_of_file']),
                        ""):
            list_off_files.append(filename)
    return list_off_files


# bs={}M size from config

@pytest.fixture()
def make_subfolder():
    # create random named(letters and numbers, length k =5) files and folders which return as list
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not ssh_checkout(data["host"], data["user"], data["password"],
                        "cd {}; mkdir {}".format(data['folder_in'], subfoldername), ""):
        return None, None
    if not ssh_checkout(data["host"], data["user"], data["password"],
                        "cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data['folder_in'],
                                                                                                  subfoldername,
                                                                                                  testfilename), ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture()
def make_bad_arx(make_folders, clear_folders, make_files):
    ssh_checkout(data["host"], data["user"], data["password"],
                 "cd {}; 7z a {}/arx1.7z".format(data['folder_in'], data['folder_bad_arx']),
                 "Everything is Ok"), "Test bad Fail"
    return ssh_checkout(data["host"], data["user"], data["password"],
                        "truncate -s {}/bad_arx.7z".format(data['folder_bad_arx']), ""), "test FAIL"


# fixture start time in format journalctl
@pytest.fixture()
def start_time():
    return datetime.now().strftime("%Y %m %d #H:%M:%S")


def func_test(cmd):
    return subprocess.run(f'{cmd}', shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout


def save_log(start_time, name=data['path_journal']):
    with open(name, 'w') as f:
        f.write(func_test(f'sudo journalctl --since {start_time}'))