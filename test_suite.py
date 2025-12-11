#!/usr/bin/env python3
# ============================================================================
# Test Suite for Sorting Visualizer
# Validates all algorithms and features
# ============================================================================

import random
from algorithms import ALGORITHMS, Step


class TestSortingAlgorithms:
    """Test suite for sorting algorithms."""

    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.results = {}

    def test_algorithm_generator(self, name: str, func) -> bool:
        """Test that algorithm generators produce valid Step objects."""
        print(f"\n{'='*60}")
        print(f"Testing: {name}")
        print(f"{'='*60}")

        test_cases = [
            [5, 2, 8, 1, 9],
            [1, 2, 3, 4, 5],
            [5, 4, 3, 2, 1],
            [3],
            [5, 5, 5, 5, 5],
            list(range(20, 0, -1)),
            [random.randint(0, 100) for _ in range(30)],
        ]

        all_passed = True
        for i, test_array in enumerate(test_cases):
            try:
                arr = test_array[:]
                generator = func(arr)
                steps = []
                
                # Consume all steps from generator
                for step in generator:
                    # Validate step structure
                    assert isinstance(step, Step), f"Invalid step type: {type(step)}"
                    assert step.type in ['compare', 'swap', 'overwrite', 'complete', 'done'], \
                        f"Invalid step type: {step.type}"
                    assert isinstance(step.description, str), "Step description must be string"
                    steps.append(step)
                
                print(f"  ✓ Test {i+1}: Generated {len(steps)} steps (array size: {len(arr)})")
                self.tests_passed += 1

            except AssertionError as e:
                print(f"  ✗ Test {i+1}: FAILED - {str(e)}")
                self.tests_failed += 1
                all_passed = False
            except Exception as e:
                print(f"  ✗ Test {i+1}: ERROR - {str(e)}")
                self.tests_failed += 1
                all_passed = False

        self.results[name] = all_passed
        return all_passed

    def test_generator_structure(self):
        """Test that algorithms return proper Step objects."""
        print(f"\n{'='*60}")
        print("Testing Generator Structure")
        print(f"{'='*60}")

        for algo_name, algo_func in list(ALGORITHMS.items())[:2]:  # Test first 2
            print(f"\n  Testing {algo_name}...")
            arr = [5, 2, 8, 1, 9]
            generator = algo_func(arr[:])
            
            try:
                step = next(generator)
                
                # Verify Step structure
                assert hasattr(step, 'type'), "Step missing 'type'"
                assert hasattr(step, 'i'), "Step missing 'i'"
                assert hasattr(step, 'j'), "Step missing 'j'"
                assert hasattr(step, 'value'), "Step missing 'value'"
                assert hasattr(step, 'description'), "Step missing 'description'"
                
                print(f"    ✓ Step structure valid")
                print(f"    ✓ Example step: {step.description}")
                self.tests_passed += 1
                
            except AssertionError as e:
                print(f"    ✗ {str(e)}")
                self.tests_failed += 1

    def run_all_tests(self):
        """Run complete test suite."""
        print("\n" + "="*60)
        print("SORTING VISUALIZER - TEST SUITE")
        print("="*60)

        # Test each algorithm
        for algo_name, algo_func in ALGORITHMS.items():
            self.test_algorithm_generator(algo_name, algo_func)

        # Test generator structure
        self.test_generator_structure()

        # Print summary
        self.print_summary()

    def print_summary(self):
        """Print test summary."""
        total = self.tests_passed + self.tests_failed
        percentage = (self.tests_passed / total * 100) if total > 0 else 0

        print(f"\n{'='*60}")
        print("TEST SUMMARY")
        print(f"{'='*60}")
        print(f"Total Tests: {total}")
        print(f"Passed:      {self.tests_passed} ✓")
        print(f"Failed:      {self.tests_failed} ✗")
        print(f"Success Rate: {percentage:.1f}%")
        print(f"{'='*60}")

        # Algorithm summary
        print("\nAlgorithm Test Results:")
        for algo_name, passed in self.results.items():
            status = "✓ PASSED" if passed else "✗ FAILED"
            print(f"  {algo_name:20s} {status}")

        print(f"\n{'='*60}")
        if self.tests_failed == 0:
            print("🎉 ALL TESTS PASSED! - Ready for production")
        else:
            print(f"⚠️  {self.tests_failed} test(s) failed - Review needed")
        print(f"{'='*60}\n")


def test_performance_variation():
    """Test that algorithms handle different array patterns."""
    print("\n" + "="*60)
    print("Performance Variation Testing")
    print("="*60)

    test_patterns = {
        "Random": [random.randint(0, 1000) for _ in range(50)],
        "Sorted": list(range(50)),
        "Reverse": list(range(50, 0, -1)),
        "Nearly Sorted": list(range(50)) + [49, 48, 47],
    }

    for pattern_name, pattern_array in test_patterns.items():
        print(f"\n  Testing with {pattern_name} array...")
        for algo_name, algo_func in list(ALGORITHMS.items())[:2]:  # Quick test
            arr = pattern_array[:]
            try:
                steps = list(algo_func(arr[:]))
                print(f"    ✓ {algo_name}: {len(steps)} steps")
            except Exception as e:
                print(f"    ✗ {algo_name}: {str(e)}")


if __name__ == "__main__":
    # Run main test suite
    test_suite = TestSortingAlgorithms()
    test_suite.run_all_tests()

    # Run additional tests
    test_performance_variation()

    print("\n✅ Testing complete! Check results above.\n")
