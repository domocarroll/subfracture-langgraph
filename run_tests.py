#!/usr/bin/env python3
"""
SUBFRACTURE Test Runner

Comprehensive test execution script for SUBFRACTURE LangGraph system.
Supports various testing modes including unit tests, integration tests,
performance testing, and continuous integration.

Usage:
    python run_tests.py --all                    # Run all tests
    python run_tests.py --unit                   # Unit tests only
    python run_tests.py --integration            # Integration tests only
    python run_tests.py --performance            # Performance tests only
    python run_tests.py --brief ai               # Test specific brief
    python run_tests.py --coverage               # Run with coverage
    python run_tests.py --parallel               # Parallel execution
"""

import argparse
import asyncio
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Dict, Any
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

class SubfractureTestRunner:
    """
    Comprehensive test runner for SUBFRACTURE LangGraph system
    """
    
    def __init__(self):
        self.test_dir = Path(__file__).parent / "tests"
        self.results = {}
        
    def run_pytest_command(self, args: List[str]) -> Dict[str, Any]:
        """Run pytest with specified arguments"""
        
        cmd = ["python", "-m", "pytest"] + args
        print(f"🔧 Running: {' '.join(cmd)}")
        
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(__file__).parent)
        duration = time.time() - start_time
        
        return {
            "command": ' '.join(cmd),
            "returncode": result.returncode,
            "duration": duration,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.returncode == 0
        }
    
    def run_unit_tests(self) -> Dict[str, Any]:
        """Run unit tests for individual components"""
        
        print("\n🧪 Running Unit Tests")
        print("=" * 40)
        
        args = [
            str(self.test_dir / "test_comprehensive_workflow.py::TestIndividualAgents"),
            "-v",
            "--tb=short"
        ]
        
        result = self.run_pytest_command(args)
        self.results["unit_tests"] = result
        
        if result["success"]:
            print("✅ Unit tests passed")
        else:
            print("❌ Unit tests failed")
            print(result["stderr"])
        
        return result
    
    def run_integration_tests(self) -> Dict[str, Any]:
        """Run integration tests for complete workflows"""
        
        print("\n🔗 Running Integration Tests")
        print("=" * 40)
        
        args = [
            str(self.test_dir / "test_comprehensive_workflow.py::TestCompleteWorkflows"),
            "-v",
            "--tb=short"
        ]
        
        result = self.run_pytest_command(args)
        self.results["integration_tests"] = result
        
        if result["success"]:
            print("✅ Integration tests passed")
        else:
            print("❌ Integration tests failed")
            print(result["stderr"])
        
        return result
    
    def run_validation_tests(self) -> Dict[str, Any]:
        """Run validation module tests"""
        
        print("\n💝 Running Validation Tests")
        print("=" * 40)
        
        args = [
            str(self.test_dir / "test_comprehensive_workflow.py::TestValidationModules"),
            "-v",
            "--tb=short"
        ]
        
        result = self.run_pytest_command(args)
        self.results["validation_tests"] = result
        
        if result["success"]:
            print("✅ Validation tests passed")
        else:
            print("❌ Validation tests failed")
            print(result["stderr"])
        
        return result
    
    def run_synthesis_tests(self) -> Dict[str, Any]:
        """Run synthesis module tests"""
        
        print("\n🔮 Running Synthesis Tests")
        print("=" * 40)
        
        args = [
            str(self.test_dir / "test_comprehensive_workflow.py::TestSynthesisModules"),
            "-v",
            "--tb=short"
        ]
        
        result = self.run_pytest_command(args)
        self.results["synthesis_tests"] = result
        
        if result["success"]:
            print("✅ Synthesis tests passed")
        else:
            print("❌ Synthesis tests failed")
            print(result["stderr"])
        
        return result
    
    def run_performance_tests(self) -> Dict[str, Any]:
        """Run performance and metrics tests"""
        
        print("\n⚡ Running Performance Tests")
        print("=" * 40)
        
        args = [
            str(self.test_dir / "test_comprehensive_workflow.py::TestMetrics"),
            "-v",
            "--tb=short",
            "--benchmark-only"  # If pytest-benchmark is available
        ]
        
        result = self.run_pytest_command(args)
        self.results["performance_tests"] = result
        
        if result["success"]:
            print("✅ Performance tests passed")
        else:
            print("❌ Performance tests failed")
            print(result["stderr"])
        
        return result
    
    def run_edge_case_tests(self) -> Dict[str, Any]:
        """Run edge case and error handling tests"""
        
        print("\n🛡️  Running Edge Case Tests")
        print("=" * 40)
        
        args = [
            str(self.test_dir / "test_comprehensive_workflow.py::TestPerformanceAndEdgeCases"),
            "-v",
            "--tb=short"
        ]
        
        result = self.run_pytest_command(args)
        self.results["edge_case_tests"] = result
        
        if result["success"]:
            print("✅ Edge case tests passed")
        else:
            print("❌ Edge case tests failed")
            print(result["stderr"])
        
        return result
    
    def run_specific_brief_test(self, brief_type: str) -> Dict[str, Any]:
        """Run test for specific brand brief type"""
        
        print(f"\n📋 Running {brief_type.upper()} Brief Test")
        print("=" * 40)
        
        brief_method_map = {
            "ai": "test_ai_consultancy_workflow",
            "fashion": "test_sustainable_fashion_workflow", 
            "fintech": "test_fintech_workflow",
            "saas": "test_b2b_saas_workflow"
        }
        
        if brief_type not in brief_method_map:
            print(f"❌ Unknown brief type: {brief_type}")
            return {"success": False, "error": f"Unknown brief type: {brief_type}"}
        
        test_method = brief_method_map[brief_type]
        args = [
            f"{self.test_dir}/test_comprehensive_workflow.py::TestCompleteWorkflows::{test_method}",
            "-v",
            "--tb=short"
        ]
        
        result = self.run_pytest_command(args)
        self.results[f"{brief_type}_brief_test"] = result
        
        if result["success"]:
            print(f"✅ {brief_type.upper()} brief test passed")
        else:
            print(f"❌ {brief_type.upper()} brief test failed")
            print(result["stderr"])
        
        return result
    
    def run_coverage_analysis(self) -> Dict[str, Any]:
        """Run tests with coverage analysis"""
        
        print("\n📊 Running Coverage Analysis")
        print("=" * 40)
        
        args = [
            str(self.test_dir),
            "--cov=src",
            "--cov-report=html",
            "--cov-report=term-missing",
            "-v"
        ]
        
        result = self.run_pytest_command(args)
        self.results["coverage_analysis"] = result
        
        if result["success"]:
            print("✅ Coverage analysis completed")
            print("📁 HTML coverage report generated in htmlcov/")
        else:
            print("❌ Coverage analysis failed")
            print(result["stderr"])
        
        return result
    
    def run_parallel_tests(self) -> Dict[str, Any]:
        """Run tests in parallel for speed"""
        
        print("\n🚀 Running Parallel Tests")
        print("=" * 40)
        
        args = [
            str(self.test_dir),
            "-n", "auto",  # Automatic CPU detection
            "-v",
            "--tb=short"
        ]
        
        result = self.run_pytest_command(args)
        self.results["parallel_tests"] = result
        
        if result["success"]:
            print("✅ Parallel tests passed")
        else:
            print("❌ Parallel tests failed")
            print(result["stderr"])
        
        return result
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run complete test suite"""
        
        print("\n🎯 Running Complete SUBFRACTURE Test Suite")
        print("=" * 50)
        
        test_results = {}
        
        # Run all test categories
        test_results["unit"] = self.run_unit_tests()
        test_results["validation"] = self.run_validation_tests()
        test_results["synthesis"] = self.run_synthesis_tests()
        test_results["integration"] = self.run_integration_tests()
        test_results["edge_cases"] = self.run_edge_case_tests()
        test_results["performance"] = self.run_performance_tests()
        
        # Calculate overall results
        all_passed = all(result.get("success", False) for result in test_results.values())
        total_duration = sum(result.get("duration", 0) for result in test_results.values())
        
        print(f"\n🏁 Test Suite Summary")
        print("=" * 30)
        print(f"⏰ Total Duration: {total_duration:.2f} seconds")
        print(f"📊 Test Categories: {len(test_results)}")
        
        for category, result in test_results.items():
            status = "✅" if result.get("success") else "❌"
            duration = result.get("duration", 0)
            print(f"   {status} {category}: {duration:.2f}s")
        
        if all_passed:
            print("\n🎉 All tests passed!")
        else:
            print("\n⚠️  Some tests failed - check individual results")
        
        self.results["all_tests"] = {
            "success": all_passed,
            "duration": total_duration,
            "categories": test_results
        }
        
        return self.results["all_tests"]
    
    def generate_test_report(self, output_file: str = "test_report.json"):
        """Generate comprehensive test report"""
        
        report = {
            "timestamp": time.time(),
            "test_results": self.results,
            "summary": {
                "total_categories": len(self.results),
                "passed_categories": sum(1 for r in self.results.values() if r.get("success")),
                "total_duration": sum(r.get("duration", 0) for r in self.results.values()),
                "overall_success": all(r.get("success", False) for r in self.results.values())
            }
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Test report saved to: {output_file}")
        return report


def main():
    """Main test runner execution"""
    
    parser = argparse.ArgumentParser(description="SUBFRACTURE Test Runner")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--integration", action="store_true", help="Run integration tests only")
    parser.add_argument("--validation", action="store_true", help="Run validation tests only")
    parser.add_argument("--synthesis", action="store_true", help="Run synthesis tests only")
    parser.add_argument("--performance", action="store_true", help="Run performance tests only")
    parser.add_argument("--edge-cases", action="store_true", help="Run edge case tests only")
    parser.add_argument("--brief", choices=["ai", "fashion", "fintech", "saas"], 
                       help="Test specific brief type")
    parser.add_argument("--coverage", action="store_true", help="Run with coverage analysis")
    parser.add_argument("--parallel", action="store_true", help="Run tests in parallel")
    parser.add_argument("--report", help="Generate test report to file")
    
    args = parser.parse_args()
    
    runner = SubfractureTestRunner()
    
    print("🔮 SUBFRACTURE LangGraph Test Runner")
    print("Physics-Based Brand Intelligence Testing")
    print("=" * 40)
    
    try:
        # Execute requested tests
        if args.all:
            runner.run_all_tests()
        elif args.unit:
            runner.run_unit_tests()
        elif args.integration:
            runner.run_integration_tests()
        elif args.validation:
            runner.run_validation_tests()
        elif args.synthesis:
            runner.run_synthesis_tests()
        elif args.performance:
            runner.run_performance_tests()
        elif args.edge_cases:
            runner.run_edge_case_tests()
        elif args.brief:
            runner.run_specific_brief_test(args.brief)
        elif args.coverage:
            runner.run_coverage_analysis()
        elif args.parallel:
            runner.run_parallel_tests()
        else:
            print("❓ No test type specified. Use --help for options.")
            print("💡 Try: python run_tests.py --all")
            return 1
        
        # Generate report if requested
        if args.report:
            runner.generate_test_report(args.report)
        
        # Return appropriate exit code
        if runner.results:
            all_successful = all(r.get("success", False) for r in runner.results.values())
            return 0 if all_successful else 1
        
        return 0
        
    except KeyboardInterrupt:
        print("\n⏸️  Tests interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Test runner failed: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)