from checkout import ssh_checkout_negative
from conftest import data


#
def test_step8():
    # test1
    assert ssh_checkout_negative(data["host"], data["user"], data["password"],
                                 "cd {}; 7z e badarx.7z -o{} -y".format(data['folder_out'], data['folder_ext']),
                                 "ERROR"), "Test8 Fail"


def test_step9():
    # test2
    assert ssh_checkout_negative(data["host"], data["user"], data["password"],
                                 "cd {}; 7z t bad_arx.7z".format(data['folder_out']), "ERROR"), "Test9 Fail"
