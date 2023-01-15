from file_system import FileSystem
import pytest

@pytest.fixture
def file_system():
    fs = FileSystem(5, 5)
    fs.mkdir("/dir")
    return fs

@pytest.fixture
def file_system_with_files():
    fs = FileSystem(5, 5)
    fs.mkdir("/dir1")
    fs.mkdir("/dir1/dir1-1")
    fs.mkdir("/dir1/dir1-2")

    fs.create_binary_file("/dir1/dir1-1", "binfile.bin")
    fs.create_log_file("/dir1/dir1-1", "logfile.log")
    fs.create_buf_file("/dir1/dir1-2", "buffile.buf")
    fs.create_log_file("/dir1/dir1-2", "logfile.log")
    return fs

@pytest.fixture
def file_system_dir_overflow():
    fs = FileSystem(5, 5)
    fs.mkdir("/dir1")
    fs.create_binary_file("/dir1", "1.bin")
    fs.create_binary_file("/dir1", "2.bin")
    fs.create_binary_file("/dir1", "3.bin")
    fs.create_binary_file("/dir1", "4.bin")
    fs.create_binary_file("/dir1", "5.bin")
    return fs
#-------------------------------------------------------------------------------------
def test_ls_1(file_system_with_files):
    assert file_system_with_files.ls("/dir1/dir1-1") == ['binfile.bin', 'logfile.log']

def test_ls_2(file_system_with_files):
    assert file_system_with_files.ls("/dir1/dir1-2") == ['buffile.buf', 'logfile.log']

def test_ls_3(file_system_with_files):
    assert file_system_with_files.ls("/") == ['dir1']
    
#-------------------------------------------------------------------------------------

def test_mkdir_simple_good(file_system):
    file_system.mkdir("/dir")
    assert file_system.ls("/") == ['dir']

def test_mkdir_nested_good(file_system_with_files):
    file_system_with_files.mkdir("/dir1/dir1-3")
    assert file_system_with_files.ls("/dir1") == ['dir1-1', 'dir1-2', 'dir1-3']

def test_mkdir_some_dirs_missing(file_system):
    file_system.mkdir("/dir1/dir2")
    assert file_system.ls("/dir1") == ['dir2']

def test_mkdir_overflow_bad(file_system_dir_overflow):
    assert file_system_dir_overflow.mkdir("/dir1/dir2") == False

def test_mkdir_incorrect_path_bad(file_system):
    assert file_system.mkdir("/baddir.log") == False

#---------------------------------------------------------------------------------------
