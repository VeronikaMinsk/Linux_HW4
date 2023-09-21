import paramiko


def upload_file(host, user, passwd, local_path, remote_path, port=22):
    print(f"Upload file {local_path} in {remote_path}")
    transport = paramiko.Transport((host, port))
    transport.connect(None, username=user, password=passwd)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(local_path, remote_path)
    if sftp:
        sftp.close()
    if transport:
        transport.close()


def download_file(host, user, passwd, local_path, remote_path, port=22):
    print(f"Download file {remote_path} in {local_path}")
    transport = paramiko.Transport((host, port))
    transport.connect(None, username=user, password=passwd)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.get(remote_path, local_path)
    if sftp:
        sftp.close()
    if transport:
        transport.close()