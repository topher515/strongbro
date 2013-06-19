"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from lift.algorithms import Strongliftish

class StrongliftishAlgorithmTest(TestCase):

    def setUp(self):
        self.algo = Strongliftish()

    def assertZeroed(self, exer_data):
        for set_ in exer_data.sets:
            self.assertEqual(set_.completed_reps, 0)

    def assertNew(self, exer_data):
        self.assertTrue(exer_data.failed)
        self.assertZeroed(exer_data)

    def setSuccessData(self, exer_data):
        for set_ in exer_data.sets:
            set_.completed_reps = set_.assigned_reps
            set_.completed_weight = set_.assigned_weight


    def setFailureData(self, exer_data):
        self.setSuccessData(exer_data)
        for set_ in exer_data.sets:
            if set_.name == 'work':
                set_.completed_reps = 2
                break

    def test_uploading(self):

        exer_data_0 = self.algo.build_first_exercise_data()

        self.assertNew(exer_data_0)

        self.setSuccessData(exer_data_0)

        self.assertFalse(exer_data_0.failed)
        self.assertTrue(exer_data_0.succeeded)

        exer_data_1 = self.algo.build_next_exercise_data([exer_data_0])

        self.assertNew(exer_data_1)

        self.setSuccessData(exer_data_1)
        self.assertTrue(exer_data_1.succeeded)
        self.assertGreater(exer_data_1.work_weight, exer_data_0.work_weight)

        exer_data_2 = self.algo.build_next_exercise_data([exer_data_1, exer_data_0])

        self.assertNew(exer_data_2)

        self.setSuccessData(exer_data_2)
        self.assertTrue(exer_data_2.succeeded)
        self.assertGreater(exer_data_2.work_weight, exer_data_1.work_weight)

    def test_failures(self):

        exer_data_0 = self.algo.build_first_exercise_data()

        self.assertNew(exer_data_0)

        self.setSuccessData(exer_data_0)

        self.assertFalse(exer_data_0.failed)
        self.assertTrue(exer_data_0.succeeded)

        exer_data_1 = self.algo.build_next_exercise_data([exer_data_0])

        self.assertNew(exer_data_1)
        self.assertGreater(exer_data_1.work_weight, exer_data_0.work_weight)

        self.setFailureData(exer_data_1)
        self.assertTrue(exer_data_1.failed)

        exer_data_2 = self.algo.build_next_exercise_data([exer_data_1, exer_data_0])

        self.assertNew(exer_data_2)
        self.assertEqual(exer_data_2.work_weight, exer_data_1.work_weight)

        self.setFailureData(exer_data_2)

        exer_data_3 = self.algo.build_next_exercise_data([exer_data_2, 
                            exer_data_1, exer_data_0])

        self.assertNew(exer_data_3)
        self.assertEqual(exer_data_3.work_weight, exer_data_2.work_weight)

        self.setFailureData(exer_data_3)

        exer_data_4 = self.algo.build_next_exercise_data([exer_data_3, 
                            exer_data_2, exer_data_1, exer_data_0])

        self.assertNew(exer_data_4)
        self.assertLess(exer_data_4.work_weight, exer_data_3.work_weight)
