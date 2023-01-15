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

#--------------------------------------------------------------

def test_create_buf_file_simple_good(file_system):
    file_system.create_buf_file("/dir", "buffile.buf")
    assert file_system.ls("/dir") == ['buffile.buf']

def test_create_buf_file_dirs_missing_good(file_system):
    file_system.create_buf_file("/dir/dir1/dir2", "buffile.buf")
    assert file_system.ls("/dir/dir1/dir2") == ['buffile.buf']

def test_create_buf_file_no_directory_bad():
    fs = FileSystem(5, 5)
    assert fs.create_buf_file("/", "buffile.buf") == False

def test_create_buf_file_incorrect_extencion_bad(file_system):
    assert file_system.create_buf_file("/dir", "smth.bu") == False

def test_create_buf_file_dir_is_full_bad(file_system_dir_overflow):
    assert file_system_dir_overflow.create_buf_file("/dir1", "smth.buf") == False

def test_create_buf_file_already_exists_bad(file_system_with_files):
    assert file_system_with_files.create_buf_file("/dir1/dir1-2", "buffile.buf") == False

def test_create_buf_file_impossible_path(file_system):
    assert file_system.create_buf_file("/dir/dir.buf", "smth.buf") == False

#--------------------------------------------------------------------------------------------

def test_delete_buf_file_simple_good(file_system_with_files):
    file_system_with_files.delete_buf_file("/dir1/dir1-2/buffile.buf")
    assert file_system_with_files.ls("/dir1/dir1-2") == ['logfile.log']

def test_delete_buf_file_doesnt_exist(file_system):
    assert file_system.delete_buf_file("/dir/buf.buf") == False

#--------------------------------------------------------------------------------------------

def test_buf_file_simple_good(file_system_with_files):
    file_system_with_files.push_to_buf_file("/dir1/dir1-2/buffile.buf", "some element")
    assert file_system_with_files.consume_from_buf_file("/dir1/dir1-2/buffile.buf") == "some element"

def test_buf_file_several_elems(file_system_with_files):
    file_system_with_files.push_to_buf_file("/dir1/dir1-2/buffile.buf", "first elem")
    file_system_with_files.push_to_buf_file("/dir1/dir1-2/buffile.buf", "second elem")
    file_system_with_files.push_to_buf_file("/dir1/dir1-2/buffile.buf", "third elem")
    file_system_with_files.push_to_buf_file("/dir1/dir1-2/buffile.buf", "fourth elem")
    assert file_system_with_files.push_to_buf_file("/dir1/dir1-2/buffile.buf", "fifth elem") == True

def test_consume_several_elems(file_system_with_files):
    file_system_with_files.push_to_buf_file("/dir1/dir1-2/buffile.buf", "first elem")
    file_system_with_files.push_to_buf_file("/dir1/dir1-2/buffile.buf", "second elem")
    file_system_with_files.push_to_buf_file("/dir1/dir1-2/buffile.buf", "third elem")
    file_system_with_files.push_to_buf_file("/dir1/dir1-2/buffile.buf", "fourth elem")
    file_system_with_files.push_to_buf_file("/dir1/dir1-2/buffile.buf", "fifth elem")

    file_system_with_files.consume_from_buf_file("/dir1/dir1-2/buffile.buf")
    file_system_with_files.consume_from_buf_file("/dir1/dir1-2/buffile.buf")
    file_system_with_files.consume_from_buf_file("/dir1/dir1-2/buffile.buf")
    file_system_with_files.consume_from_buf_file("/dir1/dir1-2/buffile.buf")
    assert file_system_with_files.consume_from_buf_file("/dir1/dir1-2/buffile.buf") == "fifth elem"

def test_buf_file_overflow(file_system_with_files):
    file_system_with_files.push_to_buf_file("/dir1/dir1-2/buffile.buf", "first elem")
    file_system_with_files.push_to_buf_file("/dir1/dir1-2/buffile.buf", "second elem")
    file_system_with_files.push_to_buf_file("/dir1/dir1-2/buffile.buf", "third elem")
    file_system_with_files.push_to_buf_file("/dir1/dir1-2/buffile.buf", "fourth elem")
    file_system_with_files.push_to_buf_file("/dir1/dir1-2/buffile.buf", "fifth elem")
    assert file_system_with_files.push_to_buf_file("/dir1/dir1-2/buffile.buf", "error elem") == False

def test_buf_file_consume_empty_file(file_system_with_files):
    file_system_with_files.push_to_buf_file("/dir1/dir1-2/buffile.buf", "first elem")
    file_system_with_files.push_to_buf_file("/dir1/dir1-2/buffile.buf", "second elem")
    file_system_with_files.push_to_buf_file("/dir1/dir1-2/buffile.buf", "third elem")
    file_system_with_files.push_to_buf_file("/dir1/dir1-2/buffile.buf", "fourth elem")
    file_system_with_files.push_to_buf_file("/dir1/dir1-2/buffile.buf", "fifth elem")

    file_system_with_files.consume_from_buf_file("/dir1/dir1-2/buffile.buf")
    file_system_with_files.consume_from_buf_file("/dir1/dir1-2/buffile.buf")
    file_system_with_files.consume_from_buf_file("/dir1/dir1-2/buffile.buf")
    file_system_with_files.consume_from_buf_file("/dir1/dir1-2/buffile.buf")
    file_system_with_files.consume_from_buf_file("/dir1/dir1-2/buffile.buf")
    assert file_system_with_files.consume_from_buf_file("/dir1/dir1-2/buffile.buf") == False
    


    
    
    
    