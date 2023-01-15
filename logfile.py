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
    fs.mkdir("/dir1/dir1-3")

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

def test_create_log_file_simple_good(file_system):
    file_system.create_log_file("/dir", "logfile.log")
    assert file_system.ls("/dir") == ['logfile.log']

def test_create_log_file_dirs_missing_good(file_system):
    file_system.create_log_file("/dir/dir1/dir2", "logfile.log")
    assert file_system.ls("/dir/dir1/dir2") == ['logfile.log']

def test_create_log_file_no_directory_bad():
    fs = FileSystem(5, 5)
    assert fs.create_log_file("/", "logfile.log") == False

def test_create_log_file_incorrect_extencion_bad(file_system):
    assert file_system.create_log_file("/dir", "smth.lo") == False

def test_create_log_file_dir_is_full_bad(file_system_dir_overflow):
    assert file_system_dir_overflow.create_log_file("/dir1", "smth.log") == False

def test_create_log_file_already_exists_bad(file_system_with_files):
    assert file_system_with_files.create_log_file("/dir1/dir1-1", "logfile.log") == False

def test_create_log_file_impossible_path(file_system):
    assert file_system.create_log_file("/dir/dir.log", "smth.log") == False

#---------------------------------------------------------------------------------------------

def test_delete_log_file_simple_good(file_system_with_files):
    file_system_with_files.delete_log_file("/dir1/dir1-1/logfile.log")
    assert file_system_with_files.ls("/dir1/dir1-1") == ['binfile.bin']

def test_delete_log_file_doesnt_exist(file_system):
    assert file_system.delete_log_file("/dir/log.log") == False

#---------------------------------------------------------------------------------------------

def test_read_log_file_and_append_text_simple_good(file_system_with_files):
    file_system_with_files.append_text("/dir1/dir1-1/logfile.log", "some text")
    assert file_system_with_files.read_log_file("/dir1/dir1-1/logfile.log") == "some text"

def test_read_log_file_doesnt_exist_bad(file_system):
    assert file_system.read_log_file("/dir/log.log") == None

def test_read_log_file_several_lines_good(file_system_with_files):
    file_system_with_files.append_text("/dir1/dir1-1/logfile.log", "some text")
    file_system_with_files.append_text("/dir1/dir1-1/logfile.log", "another text")
    assert file_system_with_files.read_log_file("/dir1/dir1-1/logfile.log") == "some text\n\ranother text"

#---------------------------------------------------------------------------------------------

def test_append_text_several_lines(file_system_with_files):
    file_system_with_files.append_text("/dir1/dir1-1/logfile.log", "some text\n\ranother text\n\rsome more text here")
    assert file_system_with_files.read_log_file("/dir1/dir1-1/logfile.log") == "some text\n\ranother text\n\rsome more text here"

def test_append_text_file_doesnt_exist_good(file_system):
    file_system.append_text("/dir/log.log", "some text")
    assert file_system.read_log_file("/dir/log.log") == "some text"

#---------------------------------------------------------------------------------------------

def test_move_log_file_simple_good_1(file_system_with_files):
    file_system_with_files.move_log_file("/dir1/dir1-1/logfile.log", "/dir1/dir1-3")
    assert file_system_with_files.ls("/dir1/dir1-1") == ['binfile.bin']

def test_move_log_file_simple_good_2(file_system_with_files):
    file_system_with_files.move_log_file("/dir1/dir1-1/logfile.log", "/dir1/dir1-3")
    assert file_system_with_files.ls("/dir1/dir1-3") == ['logfile.log']

def test_move_binary_file_doesnt_exist(file_system_with_files):
    assert file_system_with_files.move_binary_file("/dir1/dir1-2/binfile.bin", "/dir1/dir1-1") == False
    
def test_move_binary_file_overflow(file_system_dir_overflow):
    file_system_dir_overflow.create_binary_file("/dir2", "binfile.bin")
    assert file_system_dir_overflow.move_binary_file("/dir2/binfile.bin", "/dir1") == False
    

def test_move_binary_file_such_name_already_exists(file_system_with_files):
    file_system_with_files.create_binary_file("/dir1/dir1-2", "binfile.bin")
    assert file_system_with_files.move_binary_file("/dir1/dir1-1/binfile.bin", "/dir1/dir1-2") == False


