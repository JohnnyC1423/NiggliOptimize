"""
Tests The functions in PGComp/Matrixtools.py
"""
import pytest
import numpy
import os
from spHNF_manip.matrix_tools import *

def test_create_nxn_matrices():
    assert 3 == len(create_nxn_matrices(1))
    assert 81 == len(create_nxn_matrices(2))

def test_det_is_n():
    assert 1 == det_is_n(1, [[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    assert 0 == det_is_n(2, [[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    assert 1 == det_is_n(2, [[2, 0, 0], [0, 1, 0], [0, 0, 1]])

def test_edit_struct_enum():
    edit_struct_enum("tests/struct_enum.in", [[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    with open('tests/test_output/IdentityTestStruct_enum.in', 'r') as struct_enum:
        expected_struct_data1 = struct_enum.readlines()
    with open('tests/struct_enum.in', 'r') as struct_enum:
        struct_data1 = struct_enum.readlines()
    assert struct_data1 == expected_struct_data1

    edit_struct_enum("tests/struct_enum.in", [[1.1, 1.1, 1], [1.1, 1, 1], [1.1, 1, 1]])
    with open('tests/test_output/TestStruct_enum1.in', 'r') as struct_enum:
        expected_struct_data2 = struct_enum.readlines()
    with open('tests/struct_enum.in', 'r') as struct_enum:
        struct_data2 = struct_enum.readlines()
    assert struct_data2 == expected_struct_data2


def test_read_pg_out():
    data1 = read_pg_out("tests/test_output/pgx_outTest1.txt")
    expected_data1 = [[[-1, 0, 0], [0, 0, -1], [0, -1, 0]], [[0, 0, 1], [-1, 0, 0], [0, 1, 0]]]
    assert expected_data1 == data1
    data2 = read_pg_out("tests/test_output/pgx_outTest2.txt")
    expected_data2 = [[[-1, 0, 0], [-1, 0, 1], [-1, 1, 0]], [[-1, 0, 1], [-1, 0, 0], [-1, 1, 0]],
                     [[-1, 0, 0], [0, -1, 0], [0, 0, -1]]]
    assert expected_data2 == data2


def test_calculate_transform():
    identity = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    m1 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    transform1 = [[0, 0, 1], [0, 1, 0], [1, 0, 0]]
    transform2 = [[1, 1, 5], [1, 1, 0], [1, 5, 1]]
    assert numpy.array_equal(identity, calculate_transform(identity, identity))
    assert numpy.array_equal(m1, calculate_transform(m1, identity))
    assert numpy.array_equal(m1, calculate_transform(identity, m1))
    assert numpy.array_equal([[7, 8, 9], [4, 5, 6], [1, 2, 3]], calculate_transform(transform1, m1))
    assert numpy.array_equal([[40, 47, 54], [5, 7, 9], [28, 35, 42]], calculate_transform(transform2, m1))


def test_create_matrix():
    identity = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    m1 = [[1.1, 0, 0], [0, -.1, 0], [0, 0, -0]]
    assert numpy.array_equal(identity, create_matrix("1   0   0", "0   1   0", "0   0   1"))
    assert numpy.array_equal(m1, create_matrix("1.1   0   0", "0   -0.1   0", "0   0   0"))


def test_save_matrix():
    identity = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    save_matrix(identity, "tests/test_output/saveMatrixTest1.txt")
    with open('tests/test_output/saveMatrixTest1.txt', 'r') as Data:
        data1 = Data.readlines()
    with open("tests/test_output/saveMatrixExpected1.txt", 'r') as Data:
        expected_data1 = Data.readlines()
    assert data1 == expected_data1
    m1 = [[1.1111111, 0, 0], [0, 1, 0], [0, 0, 1]]
    save_matrix(m1, "tests/test_output/saveMatrixTest2.txt")
    with open('tests/test_output/saveMatrixTest2.txt', 'r') as Data:
        data2 = Data.readlines()
    with open("tests/test_output/saveMatrixExpected2.txt", 'r') as Data:
        expected_data2 = Data.readlines()
    assert data2 == expected_data2


def test_matrix_float_to_int():
    identity = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    assert numpy.array_equal(identity, matrix_float_to_int(identity))
    m1 = [[1.01, 0.00001, 0], [0, .9999999, 0], [0, 0.000005, 1]]
    assert numpy.array_equal(identity, matrix_float_to_int(m1))


def test_check_similarities():
    identity = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    assert 2 == check_similarities([identity, identity], [identity, identity])


def test_find_equivalent_basis():
    basis = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
def test_get_URT():
    pg_identity = [[[1, 0, 0], [0, 1, 0], [0, 0, 1]],[[1, 0, 0], [0, 1, 0], [0, 0, 1]]]
    assert 1 == get_URT(pg_identity)
    pg1 = [[[1, 0, 1], [0, 1, 0], [0, 0, 1]],[[1, 0, 0], [0, 1, 0], [0, 0, 1]]]
    assert 0 == get_URT(pg1)
    pg2 = [[[0, 0, 0], [0, 0, 0], [0, 0, 0]],[[0, 0, 0], [0, 0, 0], [0, 0, 0]]]
    assert 1 == get_URT(pg2)
    pg3 = [[[1, 0, 0], [0, 1, 0], [0, 0, 1]],[[1, 0, 0], [0, 1, 1], [0, 0, 1]]]    
    assert 0 == get_URT(pg3)
def test_is_one():
    pg_identity = [[[1, 0, 0], [0, 1, 0], [0, 0, 1]],[[1, 0, 0], [0, 1, 0], [0, 0, 1]]]
    assert 1 == is_one(pg_identity)
    pg1 = [[[1, 0, 1], [0, 1, 0], [0, 0, 1]],[[1, 0, 0], [0, 1, 0], [0, 0, 1]]]
    assert 1 == is_one(pg1)
    pg2 = [[[0, 0, 0], [0, 0, 0], [0, 0, 0]],[[0, 0, 0], [0, 0, 0], [0, 0, 3]]]
    assert 0 == is_one(pg2)
    pg3 = [[[1, 0, 0], [0, 2, 0], [0, 0, 1]],[[1, 0, 0], [0, 1, 1], [0, 0, 1]]]    
    assert 0 == is_one(pg3)
