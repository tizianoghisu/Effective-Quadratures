#!/usr/bin/env python
from unittest import TestCase
import unittest
import effective_quadratures.qr as qr
from effective_quadratures.utils import error_function
import numpy as np

class TestIntegrals(TestCase):
    
    def test_householder_vector(self):
        x = [4., 2., 1., -2., 4., 1.]
        x = np.mat(x)
        v, beta = qr.house(x.T)

        # Know solution
        real_v = [1.0000, -0.80621082,  -0.4031054,  0.80621082, -1.61242164,-0.4031054]
        real_v = np.mat(real_v)
        real_v = real_v.T

        if np.linalg.norm(real_v - v, 2) < 1e-07:
            print 'Success!'
        else:
            error_function('ERROR: Householder vector incorrect!')
    
    def test_qr_factorization(self):
        A =  [ [0.8147,    0.0975,    0.1576,    0.1419], [0.9058,    0.2785,    0.9706,    0.4218], [0.1270,    0.5469 ,   0.9572 ,   0.9157], [0.9134  ,  0.9575 ,   0.4854   , 0.7922], [0.6324 ,   0.9649,    0.8003 ,   0.9595]]
        Q, R = qr.qr_Householder(A)
        Q1, R1 = qr.qr_Householder(A,1)
        if np.linalg.norm(A - ( Q * R), 2) < 1e-15 and np.linalg.norm(A - ( Q1 * R1), 2) < 1e-15 :
            print 'Success!'
        else:
            error_function('ERROR: QR Householder not working!')
    
    def test_qr_factorization_fat_matrix(self):
        A = [[ 0.549723608291140 ,  0.380445846975357 ,  0.779167230102011 ,  0.011902069501241 ,  0.528533135506213 ,  0.689214503140008 ,  0.913337361501670 ,  0.078175528753184   ,0.774910464711502], 
        [0.917193663829810  , 0.567821640725221  , 0.934010684229183  , 0.337122644398882  , 0.165648729499781  , 0.748151592823709  , 0.152378018969223  , 0.442678269775446  , 0.817303220653433],
        [ 0.285839018820374 ,  0.075854289563064 ,  0.129906208473730 ,  0.162182308193243 ,  0.601981941401637 ,  0.450541598502498 ,  0.825816977489547 ,  0.106652770180584 ,  0.868694705363510],
        [0.757200229110721  , 0.053950118666607  , 0.568823660872193  , 0.794284540683907  , 0.262971284540144  , 0.083821377996933  , 0.538342435260057  , 0.961898080855054  , 0.084435845510910],
        [ 0.753729094278495 ,  0.530797553008973 ,  0.469390641058206 ,  0.311215042044805 ,  0.654079098476782 ,  0.228976968716819 ,  0.996134716626885 ,  0.004634224134067 ,  0.399782649098896]]

        Q, R = qr.qr_Householder(A)
        Q1, R1 = qr.qr_Householder(A, 1)
        if np.linalg.norm(A - ( Q * R), 2) < 2e-15 and np.linalg.norm(A - ( Q1 * R1), 2) < 2e-15 :
            print 'Success!'
        else:
            error_function('ERROR: QR Householder not working!')
    
    def test_least_squares(self):
        A = [[   0.129783563321146 ,  0.693035803160460 ,  0.542987352374312],
        [0.971602452337381  , 0.702475484644310 ,  0.540162073918995],
        [0.940153258292462  , 0.371312184808707 ,  0.786284036629558],
        [0.933119647195370  , 0.064105941014906 ,  0.601409398329654],
        [0.983758270635912  , 0.443451755787831,   0.947013554266040] ]
        b = [ 0.631218455441575 ,  0.878837482885143 ,  0.122686301726737  , 0.813548224731922  , 0.977604352516636]
        b = np.mat(b)
        b = b.T
        x = qr.solveLSQ(A, b)
        x_MATLAB = [ 0.356346872539370 ,  0.515012358852366 ,  0.221551548589301]
        x_MATLAB = np.mat(x_MATLAB)
        x_MATLAB = x_MATLAB.T
        residual = x - x_MATLAB
        if np.linalg.norm(residual, 2) < 4e-15 :
            print 'Success!'
        else:
            error_function('ERROR: Least squares routine not working!')

    def test_constrained_least_squares(self):
        A = [ [0.8147 ,   0.0975 ,   0.1576],
        [0.9058  ,  0.2785  ,  0.9706],
        [0.1270  ,  0.5469  ,  0.9572],
        [0.9134  ,  0.9575  ,  0.4854],
        [0.6324  ,  0.9649  ,  0.8003]]
        b = [0.1419 ,   0.4218  ,  0.9157 ,   0.7922  ,  0.9595]
        b = np.mat(b)
        b = b.T
        C = [ [0.7060 ,   0.0462 ,   0.6948],
        [0.0318,    0.0971,    0.3171],
        [0.2769,   0.8235,    0.9502] ]
        d = [0.0344,    0.4387,    0.3816]
        d = np.mat(d)
        d = d.T
        x = qr.solve_constrainedLSQ(A, b, C, d)
        x_MATLAB = [-1.7588,   -1.1531,    1.9134]
        x_MATLAB = np.mat(x_MATLAB)
        x_MATLAB = x_MATLAB.T
        residual = x - x_MATLAB
        if np.linalg.norm(residual, 2) < 2e-3 :
            print 'Success!'
        else:
            error_function('ERROR: Least squares routine not working!')

if __name__ == '__main__':
    unittest.main()
