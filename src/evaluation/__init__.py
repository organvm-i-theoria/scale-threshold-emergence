#!/usr/bin/env python3
"""
Evaluation Harness
===================
Runs benchmarks and validates system quality.

Features:
- Benchmark runner
- Gold fixture validation
- Report generation
- Trend tracking
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Optional


@dataclass
class BenchmarkResult:
    """Result of a benchmark run."""

    name: str
    score: float
    duration_ms: float
    passed: bool
    details: dict = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class ValidationResult:
    """Result of validation against gold fixtures."""

    test_name: str
    passed: bool
    expected: Any
    actual: Any
    diff: Optional[dict] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class EvaluationReport:
    """Complete evaluation report."""

    id: str
    benchmarks: list = field(default_factory=list)
    validations: list = field(default_factory=list)
    summary: dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


class EvaluationHarness:
    """Runs benchmarks and validates system quality."""

    def __init__(self, output_dir: str = "./data/evaluation"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.benchmarks: dict[str, Callable] = {}
        self.gold_fixtures: dict[str, Any] = {}
        self.history: list[EvaluationReport] = []

    def register_benchmark(self, name: str, benchmark_fn: Callable):
        """Register a benchmark function."""
        self.benchmarks[name] = benchmark_fn

    def register_gold_fixture(self, name: str, expected: Any):
        """Register a gold fixture for validation."""
        self.gold_fixtures[name] = expected

    def run_benchmark(self, name: str, **kwargs) -> BenchmarkResult:
        """
        Run a benchmark.

        Args:
            name: Benchmark name
            **kwargs: Arguments to pass to benchmark

        Returns:
            BenchmarkResult
        """
        if name not in self.benchmarks:
            raise ValueError(f"Benchmark not found: {name}")

        import time

        start = time.time()

        try:
            result = self.benchmarks[name](**kwargs)
            passed = True
            details = {"result": result}
        except Exception as e:
            passed = False
            result = 0.0
            details = {"error": str(e)}

        duration_ms = (time.time() - start) * 1000

        return BenchmarkResult(
            name=name,
            score=result,
            duration_ms=duration_ms,
            passed=passed,
            details=details,
        )

    def run_all_benchmarks(self, **kwargs) -> list[BenchmarkResult]:
        """Run all registered benchmarks."""
        results = []
        for name in self.benchmarks:
            result = self.run_benchmark(name, **kwargs)
            results.append(result)
        return results

    def validate(self, test_name: str, actual: Any) -> ValidationResult:
        """
        Validate against gold fixture.

        Args:
            test_name: Test/fixture name
            actual: Actual result

        Returns:
            ValidationResult
        """
        if test_name not in self.gold_fixtures:
            return ValidationResult(
                test_name=test_name,
                passed=False,
                expected=None,
                actual=actual,
                diff={"error": "Gold fixture not found"},
            )

        expected = self.gold_fixtures[test_name]

        if isinstance(expected, dict) and isinstance(actual, dict):
            diff = {}
            for key in expected:
                if key not in actual:
                    diff[key] = {"expected": expected[key], "actual": None}
                elif expected[key] != actual[key]:
                    diff[key] = {"expected": expected[key], "actual": actual[key]}

            for key in actual:
                if key not in expected:
                    diff[key] = {"expected": None, "actual": actual[key]}

            passed = len(diff) == 0
        else:
            passed = expected == actual
            diff = None

        return ValidationResult(
            test_name=test_name,
            passed=passed,
            expected=expected,
            actual=actual,
            diff=diff,
        )

    def run_validation_suite(
        self, test_results: dict[str, Any]
    ) -> list[ValidationResult]:
        """
        Run validation suite.

        Args:
            test_results: Dictionary of test_name -> actual result

        Returns:
            List of ValidationResults
        """
        results = []
        for test_name, actual in test_results.items():
            result = self.validate(test_name, actual)
            results.append(result)
        return results

    def generate_report(
        self,
        benchmarks: Optional[list[BenchmarkResult]] = None,
        validations: Optional[list[ValidationResult]] = None,
    ) -> EvaluationReport:
        """
        Generate evaluation report.

        Args:
            benchmarks: Optional benchmark results
            validations: Optional validation results

        Returns:
            EvaluationReport
        """
        report_id = f"eval_{len(self.history)}"

        benchmarks = benchmarks or []
        validations = validations or []

        passed_benchmarks = sum(1 for b in benchmarks if b.passed)
        passed_validations = sum(1 for v in validations if v.passed)

        summary = {
            "total_benchmarks": len(benchmarks),
            "passed_benchmarks": passed_benchmarks,
            "benchmark_pass_rate": passed_benchmarks / len(benchmarks)
            if benchmarks
            else 0,
            "total_validations": len(validations),
            "passed_validations": passed_validations,
            "validation_pass_rate": passed_validations / len(validations)
            if validations
            else 0,
            "avg_benchmark_duration_ms": sum(b.duration_ms for b in benchmarks)
            / len(benchmarks)
            if benchmarks
            else 0,
        }

        report = EvaluationReport(
            id=report_id,
            benchmarks=benchmarks,
            validations=validations,
            summary=summary,
        )

        self.history.append(report)
        return report

    def save_report(self, report: EvaluationReport) -> str:
        """Save report to file."""
        output_path = self.output_dir / f"{report.id}.json"

        data = {
            "id": report.id,
            "benchmarks": [
                {
                    "name": b.name,
                    "score": b.score,
                    "duration_ms": b.duration_ms,
                    "passed": b.passed,
                    "details": b.details,
                    "timestamp": b.timestamp,
                }
                for b in report.benchmarks
            ],
            "validations": [
                {
                    "test_name": v.test_name,
                    "passed": v.passed,
                    "expected": v.expected,
                    "actual": v.actual,
                    "diff": v.diff,
                    "timestamp": v.timestamp,
                }
                for v in report.validations
            ],
            "summary": report.summary,
            "created_at": report.created_at,
        }

        output_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return str(output_path)

    def get_history(self, limit: int = 10) -> list[EvaluationReport]:
        """Get evaluation history."""
        return self.history[-limit:]

    def get_trends(self, metric: str) -> list[dict]:
        """Get trends for a metric."""
        trends = []
        for report in self.history:
            if metric in report.summary:
                trends.append(
                    {"timestamp": report.created_at, "value": report.summary[metric]}
                )
        return trends

    def get_stats(self) -> dict:
        """Get evaluation statistics."""
        return {
            "total_benchmarks": len(self.benchmarks),
            "gold_fixtures": len(self.gold_fixtures),
            "total_reports": len(self.history),
        }
