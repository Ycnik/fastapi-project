# Copyright (C) 2023 - present Juergen Zimmermann, Hochschule Karlsruhe

# Aufruf:   uv run extras/dependency-check.py

"""Python-Script, um OWASP Dependency Check aufzurufen."""

import subprocess  # noqa: S404
from pathlib import Path
from sysconfig import get_platform

nvd_api_key = "47fbc0a4-9240-4fda-9a26-d7d5624c16bf"
project = "FastAPI"

base_script = "dependency-check"
betriebssystem = get_platform()
if betriebssystem in {"win-amd64", "win-arm64", "win32"}:
    base_exec_path = Path("C:/") / "Zimmermann"
    extension = "bat"
    base_script += ".bat"
    base_data_path = Path("C:\\") / "Zimmermann"
else:
    base_exec_path = Path("Zimmermann")
    base_data_path = Path("Zimmermann")

script = base_exec_path / "dependency-check" / "bin" / base_script
print(f"script={script}")

data_path = base_data_path / "dependency-check-data"
pyproject_path = Path("..")
report_path = "."

options = " ".join([
    f"--nvdApiKey {nvd_api_key} --project {project} --scan {pyproject_path}",
    f"--suppression extras/suppression.xml --out {report_path} --data {data_path}",
    # dependency-check.bat --advancedHelp
    "--disableArchive",
    "--disableAssembly",
    "--disableAutoconf",
    "--disableBundleAudit",
    "--disableCarthageAnalyzer",
    "--disableCentral",
    "--disableCentralCache",
    "--disableCmake",
    "--disableCocoapodsAnalyzer",
    "--disableComposer",
    "--disableCpan",
    "--disableDart",
    "--disableGolangDep",
    "--disableGolangMod",
    "--disableJar",
    "--disableMavenInstall",
    "--disableMixAudit",
    "--disableMSBuild",
    "--disableNodeAudit",
    "--disableNodeAuditCache",
    "--disableNodeJS",
    "--disableNugetconf",
    "--disableNuspec",
    "--disableOssIndex",
    "--disablePipfile",
    "--disablePnpmAudit",
    "--disableRubygems",
    "--disableSwiftPackageManagerAnalyzer",
    "--disableSwiftPackageResolvedAnalyzer",
    "--disableYarnAudit",
])
print(f"options={options}")
print()

subprocess.run(f"{script} {options}", shell=True)  # noqa: PLW1510, S602
