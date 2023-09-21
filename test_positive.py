from checkout import ssh_checkout
from conftest import data, save_log
from load import upload_file


def test_step0(start_time):
    res = []
    upload_file(data["host"], data["user"], data["password"], data["local_path"], data["remote_path"])
    res.append(ssh_checkout(data["host"], data["user"], data["password"],
                            f"echo {data['password']} | sudo -S dpkg -i {data['remote_path']}",
                            "Настраивается пакет"))
    res.append(ssh_checkout(data["host"], data["user"], data["password"],
                            f"echo {data['password']} | sudo -S dpkg -s {data['pkg_name']}",
                            "Status: install ok installed"))
    assert all(res), "Test Fail"


def test_step1(make_folders, clear_folders, make_files, start_time):
    res1 = ssh_checkout(data["host"], data["user"], data["password"],
                        "cd {}; 7z a {}/arx1.7z".format(data['folder_in'], data['folder_out']),
                        "Everything is Ok"), "Test1 Fail"
    res2 = ssh_checkout(data["host"], data["user"], data["password"], "ls {}".format(data['folder_out']),
                        "arx.7z"), "Test1 Fail"
    save_log(start_time)
    assert res1 and res2, "Test Fail"


def test_step2(clear_folders, make_files):
    res = []
    res.append(
        ssh_checkout(data["host"], data["user"], data["password"],
                     "cd {}; 7z a {}/arx1.7z".format(data['folder_in'], data['folder_out']),
                     "Everything is Ok")), "Test2 Fail"
    res.append(ssh_checkout(data["host"], data["user"], data["password"],
                            "cd {}; 7z e arx1.7z -o{} -y".format(data['folder_out'], data['folder_ext']),
                            "Everything is Ok"))
    for item in make_files:
        res.append(ssh_checkout(data["host"], data["user"], data["password"], "ls {}".format(data['folder_ext']), item))
    assert all(res)


def test_step3():
    assert ssh_checkout(data["host"], data["user"], data["password"],
                        "cd {}; 7z t {}/arx1.7z".format(data['folder_in'], data['folder_out']),
                        "Everything is Ok"), "Test3 Fail"


def test_step4(make_folders, clear_folders, make_files):
    assert ssh_checkout(data["host"], data["user"], data["password"],
                        "cd {}; 7z u {}/arx1.7z".format(data['folder_in'], data['folder_out']),
                        "Everything is Ok"), "Test4 Fail"


def test_step5(clear_folders, make_files):
    res = [ssh_checkout(data["host"], data["user"], data["password"],
                        "cd {}; 7z a {}/arx1.7z".format(data['folder_in'], data['folder_out']), "Everything is Ok")]
    for item in make_files:
        res.append(
            ssh_checkout(data["host"], data["user"], data["password"], "cd {}; 7z l arx1.7z".format(data['folder_out']),
                         item))
    assert all(res)


def test_step6(make_folders, clear_folders, make_files, make_subfolder):
    res = [ssh_checkout(data["host"], data["user"], data["password"],
                        "cd {}; 7z a {}/arx1.7z".format(data['folder_in'], data['folder_out']), "Everything is Ok"),
           ssh_checkout(data["host"], data["user"], data["password"],
                        "cd {}; 7z x arx1.7z -o{} -y".format(data['folder_out'], data['folder_ext2']),
                        "Everything is Ok")]
    for item in make_files:
        res.append(
            ssh_checkout(data["host"], data["user"], data["password"], "ls {};".format(data['folder_ext2']), item))

    res.append(ssh_checkout(data["host"], data["user"], data["password"], "ls {};".format(data['folder_ext2']),
                            make_subfolder[0]))
    res.append(ssh_checkout(data["host"], data["user"], data["password"],
                            "ls {}/{};".format(data['folder_ext2'], make_subfolder[0]),
                            make_subfolder[1]))  # fall in dir {}/{}
    assert all(res)


#
def test_step7():
    assert ssh_checkout(data["host"], data["user"], data["password"], "7z d {}/arx1.7z".format(data['folder_out']),
                        "Everything is Ok"), "Test7 Fail"


def test_step10():
    assert ssh_checkout(data["host"], data["user"], data["password"],
                        "7z t {}/{}".format(data['folder_out'], data['name_of_arch']),
                        "Everything is Ok"), "Test10 Fail"
