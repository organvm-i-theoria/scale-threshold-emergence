#!/usr/bin/env python3
"""
Operations
==========
System monitoring and operations tooling.

Features:
- Health monitoring
- Metrics collection
- Alerting
- Runbook execution
"""

import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


@dataclass
class HealthStatus:
    """Represents health status."""

    component: str
    status: str  # healthy, degraded, unhealthy
    message: str = ""
    last_check: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: dict = field(default_factory=dict)


@dataclass
class Metric:
    """Represents a metric."""

    name: str
    value: float
    unit: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    tags: dict = field(default_factory=dict)


@dataclass
class Alert:
    """Represents an alert."""

    id: str
    severity: str  # info, warning, error, critical
    message: str
    component: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    acknowledged: bool = False


class Operations:
    """System monitoring and operations tooling."""

    def __init__(self):
        self.health_checks: dict[str, callable] = {}
        self.metrics: list[Metric] = []
        self.alerts: list[Alert] = {}
        self.runbooks: dict[str, callable] = {}
        self._start_time = time.time()

    def register_health_check(self, component: str, check_fn: callable):
        """Register a health check function."""
        self.health_checks[component] = check_fn

    def check_health(self, component: Optional[str] = None) -> dict[str, HealthStatus]:
        """
        Run health checks.

        Args:
            component: Optional specific component to check

        Returns:
            Dictionary of component -> HealthStatus
        """
        results = {}

        if component:
            if component in self.health_checks:
                try:
                    status = self.health_checks[component]()
                    results[component] = status
                except Exception as e:
                    results[component] = HealthStatus(
                        component=component, status="unhealthy", message=str(e)
                    )
        else:
            for comp, check_fn in self.health_checks.items():
                try:
                    status = check_fn()
                    results[comp] = status
                except Exception as e:
                    results[comp] = HealthStatus(
                        component=comp, status="unhealthy", message=str(e)
                    )

        return results

    def record_metric(
        self, name: str, value: float, unit: str = "", tags: Optional[dict] = None
    ):
        """Record a metric."""
        metric = Metric(name=name, value=value, unit=unit, tags=tags or {})
        self.metrics.append(metric)

    def get_metrics(self, name: Optional[str] = None, limit: int = 100) -> list[Metric]:
        """Get recorded metrics."""
        metrics = self.metrics

        if name:
            metrics = [m for m in metrics if m.name == name]

        return metrics[-limit:]

    def get_latest_metric(self, name: str) -> Optional[Metric]:
        """Get the latest metric by name."""
        for metric in reversed(self.metrics):
            if metric.name == name:
                return metric
        return None

    def create_alert(self, severity: str, message: str, component: str) -> Alert:
        """Create an alert."""
        alert_id = f"alert_{len(self.alerts)}"

        alert = Alert(
            id=alert_id, severity=severity, message=message, component=component
        )

        self.alerts[alert_id] = alert
        return alert

    def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge an alert."""
        if alert_id in self.alerts:
            self.alerts[alert_id].acknowledged = True
            return True
        return False

    def get_active_alerts(self, severity: Optional[str] = None) -> list[Alert]:
        """Get active alerts."""
        alerts = [a for a in self.alerts.values() if not a.acknowledged]

        if severity:
            alerts = [a for a in alerts if a.severity == severity]

        return alerts

    def get_alert_history(self, limit: int = 100) -> list[Alert]:
        """Get alert history."""
        return list(self.alerts.values())[-limit:]

    def register_runbook(self, name: str, runbook_fn: callable):
        """Register a runbook."""
        self.runbooks[name] = runbook_fn

    def execute_runbook(self, name: str, **kwargs) -> Any:
        """Execute a runbook."""
        if name not in self.runbooks:
            raise ValueError(f"Runbook not found: {name}")

        return self.runbooks[name](**kwargs)

    def get_uptime(self) -> float:
        """Get system uptime in seconds."""
        return time.time() - self._start_time

    def get_stats(self) -> dict:
        """Get operations statistics."""
        return {
            "health_checks": len(self.health_checks),
            "metrics_recorded": len(self.metrics),
            "active_alerts": len(self.get_active_alerts()),
            "runbooks": len(self.runbooks),
            "uptime_seconds": self.get_uptime(),
        }


def default_health_check(component: str) -> HealthStatus:
    """Default health check that returns healthy."""
    return HealthStatus(component=component, status="healthy", message="OK")
