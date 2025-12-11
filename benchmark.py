# ============================================================================
# Sorting Algorithm Benchmark
# Performance comparison of different sorting algorithms
# ============================================================================

import time
import random
from algorithms import ALGORITHMS


class SortingBenchmark:
    """Benchmark sorting algorithms and generate performance report."""

    def __init__(self):
        self.results = {}

    def benchmark(self, array_size: int = 1000, runs: int = 5):
        """
        Benchmark all sorting algorithms.
        
        Args:
            array_size: Size of array to sort
            runs: Number of runs for averaging
        """
        print(f"\n{'='*70}")
        print(f"SORTING ALGORITHM BENCHMARK")
        print(f"Array Size: {array_size} | Runs: {runs}")
        print(f"{'='*70}\n")

        for algo_name, algo_func in ALGORITHMS.items():
            times = []
            
            for run in range(runs):
                # Generate random data
                data = [random.randint(0, array_size) for _ in range(array_size)]
                
                # Measure time
                start = time.perf_counter()
                
                # Run algorithm (consume all generator steps)
                for _ in algo_func(data):
                    pass
                
                end = time.perf_counter()
                times.append((end - start) * 1000)  # Convert to milliseconds

            # Calculate statistics
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)

            self.results[algo_name] = {
                "average": avg_time,
                "min": min_time,
                "max": max_time,
                "runs": runs
            }

            print(f"{algo_name:20s} | Avg: {avg_time:8.2f}ms | Min: {min_time:8.2f}ms | Max: {max_time:8.2f}ms")

        print(f"\n{'='*70}\n")

    def print_summary(self):
        """Print summary of benchmark results."""
        if not self.results:
            print("No benchmark results available. Run benchmark() first.")
            return

        print(f"\n{'SUMMARY':-^70}")
        
        # Find fastest algorithm
        fastest = min(self.results.items(), key=lambda x: x[1]["average"])
        print(f"\n✓ Fastest Algorithm: {fastest[0]} ({fastest[1]['average']:.2f}ms average)")

        # Find slowest algorithm
        slowest = max(self.results.items(), key=lambda x: x[1]["average"])
        print(f"✗ Slowest Algorithm: {slowest[0]} ({slowest[1]['average']:.2f}ms average)")

        # Performance ratio
        ratio = slowest[1]["average"] / fastest[1]["average"]
        print(f"\n➜ Performance Ratio: {ratio:.2f}x")
        print(f"\n{'='*70}\n")


def main():
    """Run benchmark with different array sizes."""
    benchmark = SortingBenchmark()
    
    # Test with different sizes
    for size in [100, 500, 1000]:
        benchmark.benchmark(array_size=size, runs=3)
    
    benchmark.print_summary()


if __name__ == "__main__":
    main()
