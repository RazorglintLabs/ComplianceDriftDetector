"""
Compliance Drift Detector — Local Desktop UI

Thin Tkinter shell around the existing deterministic engine, renderers, CSV
loaders, and verifier. No network calls. No duplicated classification logic.

Run:
    python software/ui_app.py
"""

from __future__ import annotations

import contextlib
import io
import json
import os
import subprocess
import sys
import webbrowser
from pathlib import Path

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

_software_dir = str(Path(__file__).parent)
if _software_dir not in sys.path:
    sys.path.insert(0, _software_dir)

from compliance_drift_detector import ComplianceDriftDetector
from render_html_report import render_html_report
from report_renderer import render_json_report, render_markdown_report
from run_scan import load_evidence, load_policies
from verify import verify_drift_evidence, verify_drift_report


BG = "#252629"
HEADER = "#23272F"
PANEL = "#282C34"
PANEL_ALT = "#252A31"
TEXT = "#E2D3B7"
MUTED = "#B8AC99"
BORDER = "#C8A66A"
GREEN = "#176B4F"
ALIGNED = "#2E7D5B"
DRIFTING = "#A96E18"
VIOLATED = "#934A4A"
UNDECLARED = "#675D83"

STATE_COLORS = {
    "ALIGNED": ALIGNED,
    "DRIFTING": DRIFTING,
    "VIOLATED": VIOLATED,
    "UNDECLARED": UNDECLARED,
}

FONT = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI Semibold", 10)
FONT_TITLE = ("Segoe UI Semibold", 24)
FONT_SECTION = ("Segoe UI Semibold", 15)
FONT_SMALL = ("Segoe UI", 9)


class DriftUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Compliance Drift Detector")
        self.geometry("1220x780")
        self.minsize(1020, 680)
        self.configure(bg=BG)

        self.root_dir = Path(__file__).parent.parent
        self.output_dir = self.root_dir / "output"

        self.policy_path = tk.StringVar()
        self.evidence_path = tk.StringVar()
        self.header_section = tk.StringVar(value="New Scan")
        self.report = None
        self.detector = None
        self.analysis_by_claim = {}
        self.selected_claim_id: str | None = None

        self._build_styles()
        self._build_shell()
        self._build_new_scan_page()
        self._build_results_page()
        self._build_evidence_page()
        self._build_export_page()
        self.show_page("scan")

    def _build_styles(self) -> None:
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Drift.Treeview",
            background=PANEL,
            fieldbackground=PANEL,
            foreground=TEXT,
            bordercolor="#454A52",
            rowheight=30,
            font=FONT,
        )
        style.configure(
            "Drift.Treeview.Heading",
            background=HEADER,
            foreground=TEXT,
            relief="flat",
            font=FONT_BOLD,
        )
        style.map(
            "Drift.Treeview",
            background=[("selected", GREEN)],
            foreground=[("selected", "#F5F0E7")],
        )

    def _build_shell(self) -> None:
        header = tk.Frame(self, bg=HEADER, height=78, highlightthickness=1, highlightbackground=BORDER)
        header.pack(fill="x")
        header.pack_propagate(False)

        left = tk.Frame(header, bg=HEADER)
        left.pack(side="left", padx=28, pady=15)
        tk.Label(left, text="Compliance Drift Detector", bg=HEADER, fg=TEXT, font=("Segoe UI Semibold", 17)).pack(anchor="w")
        tk.Label(left, textvariable=self.header_section, bg=HEADER, fg=TEXT, font=FONT_SMALL).pack(anchor="w", pady=(2, 0))

        tk.Label(
            header,
            text="LOCAL-FIRST  •  No data uploaded",
            bg=HEADER,
            fg=TEXT,
            font=FONT_SMALL,
        ).pack(side="right", padx=28)

        self.body = tk.Frame(self, bg=BG)
        self.body.pack(fill="both", expand=True)

        self.pages: dict[str, tk.Frame] = {}

    def _page(self, name: str) -> tk.Frame:
        page = tk.Frame(self.body, bg=BG)
        page.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.pages[name] = page
        return page

    def _button(self, parent, text: str, command, *, primary: bool = False, width: int | None = None) -> tk.Button:
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=GREEN if primary else "#21222A",
            fg="#F5F0E7" if primary else TEXT,
            activebackground="#1D5C46" if primary else "#30333B",
            activeforeground="#F5F0E7",
            relief="flat",
            bd=0,
            padx=16,
            pady=10,
            cursor="hand2",
            font=FONT_BOLD,
            width=width,
        )

    def _panel(self, parent, *, border: str = "#454A52") -> tk.Frame:
        return tk.Frame(parent, bg=PANEL, highlightthickness=1, highlightbackground=border)

    def _entry_row(self, parent, label: str, variable: tk.StringVar, button_text: str, command) -> None:
        tk.Label(parent, text=label, bg=PANEL, fg=TEXT, font=FONT_BOLD).pack(anchor="w")
        row = tk.Frame(parent, bg=PANEL)
        row.pack(fill="x", pady=(8, 18))
        entry = tk.Entry(
            row,
            textvariable=variable,
            bg="#202329",
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            bd=0,
            font=FONT,
        )
        entry.pack(side="left", fill="x", expand=True, ipady=9)
        self._button(row, button_text, command, width=18).pack(side="left", padx=(10, 0))

    def _build_new_scan_page(self) -> None:
        page = self._page("scan")
        content = tk.Frame(page, bg=BG)
        content.pack(fill="both", expand=True, padx=54, pady=38)

        tk.Label(
            content,
            text="Are your systems still doing what your policies say they do?",
            bg=BG,
            fg=TEXT,
            font=FONT_TITLE,
        ).pack(anchor="w")
        tk.Label(
            content,
            text="Load two evidence files, run the deterministic checkpoint comparison, then inspect exactly where policy and behaviour diverge.",
            bg=BG,
            fg=TEXT,
            font=FONT,
            wraplength=940,
            justify="left",
        ).pack(anchor="w", pady=(8, 22))

        trust = self._panel(content, border=BORDER)
        trust.pack(fill="x", pady=(0, 22))
        tk.Label(
            trust,
            text="Runs locally  •  No cloud  •  Deterministic engine  •  Independent verifier",
            bg=PANEL,
            fg=TEXT,
            font=FONT_BOLD,
        ).pack(anchor="w", padx=18, pady=12)

        cards = tk.Frame(content, bg=BG)
        cards.pack(fill="x")
        cards.grid_columnconfigure(0, weight=1)
        cards.grid_columnconfigure(1, weight=1)

        p1 = self._panel(cards)
        p1.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        tk.Label(p1, text="1. Policy claims", bg=PANEL, fg=TEXT, font=FONT_SECTION).pack(anchor="w", padx=20, pady=(20, 4))
        tk.Label(p1, text="What your organisation says should be true.", bg=PANEL, fg=MUTED, font=FONT, wraplength=430, justify="left").pack(anchor="w", padx=20)
        inner1 = tk.Frame(p1, bg=PANEL)
        inner1.pack(fill="x", padx=20, pady=(20, 8))
        self._entry_row(inner1, "policy_claims.csv", self.policy_path, "Choose policy CSV", self.choose_policy)

        p2 = self._panel(cards)
        p2.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        tk.Label(p2, text="2. Behaviour evidence", bg=PANEL, fg=TEXT, font=FONT_SECTION).pack(anchor="w", padx=20, pady=(20, 4))
        tk.Label(p2, text="Observed records showing what actually happened.", bg=PANEL, fg=MUTED, font=FONT, wraplength=430, justify="left").pack(anchor="w", padx=20)
        inner2 = tk.Frame(p2, bg=PANEL)
        inner2.pack(fill="x", padx=20, pady=(20, 8))
        self._entry_row(inner2, "behavior_evidence.csv", self.evidence_path, "Choose evidence CSV", self.choose_evidence)

        flow = tk.Label(
            content,
            text="1 Load policy   →   2 Load evidence   →   3 Run scan   →   4 Review drift   →   5 Export / verify",
            bg=BG,
            fg=TEXT,
            font=FONT_SMALL,
        )
        flow.pack(anchor="w", pady=(26, 16))

        actions = tk.Frame(content, bg=BG)
        actions.pack(fill="x")
        self._button(actions, "Load example", self.load_example).pack(side="left")
        self._button(actions, "Run Compliance Drift Scan", self.run_scan, primary=True).pack(side="right")

        tk.Label(
            content,
            text="Checkpoint-based analysis only. This tool detects policy-behaviour drift; it does not certify compliance.",
            bg=BG,
            fg=MUTED,
            font=FONT_SMALL,
        ).pack(anchor="w", pady=(24, 0))

    def _build_results_page(self) -> None:
        page = self._page("results")
        content = tk.Frame(page, bg=BG)
        content.pack(fill="both", expand=True, padx=44, pady=30)

        top = tk.Frame(content, bg=BG)
        top.pack(fill="x")
        tk.Label(top, text="Scan results", bg=BG, fg=TEXT, font=FONT_TITLE).pack(side="left")
        nav = tk.Frame(top, bg=BG)
        nav.pack(side="right")
        self._button(nav, "New scan", lambda: self.show_page("scan")).pack(side="left", padx=(0, 8))
        self._button(nav, "Export & verify", lambda: self.show_page("export"), primary=True).pack(side="left")

        tk.Label(
            content,
            text="Four policy-behaviour states are visible at a glance. Open any result to inspect checkpoints and supporting evidence.",
            bg=BG,
            fg=MUTED,
            font=FONT,
        ).pack(anchor="w", pady=(6, 18))

        cards = tk.Frame(content, bg=BG)
        cards.pack(fill="x")
        self.result_cards = {}
        for idx, state in enumerate(("ALIGNED", "DRIFTING", "VIOLATED", "UNDECLARED")):
            card = tk.Frame(cards, bg=PANEL, highlightthickness=1, highlightbackground=STATE_COLORS[state])
            card.grid(row=0, column=idx, sticky="nsew", padx=(0 if idx == 0 else 7, 0 if idx == 3 else 7))
            cards.grid_columnconfigure(idx, weight=1)
            count = tk.Label(card, text="0", bg=PANEL, fg=TEXT, font=("Segoe UI Semibold", 22))
            count.pack(anchor="w", padx=16, pady=(12, 0))
            tk.Label(card, text=state, bg=PANEL, fg=STATE_COLORS[state], font=FONT_BOLD).pack(anchor="w", padx=16, pady=(0, 12))
            self.result_cards[state] = count

        table_panel = self._panel(content)
        table_panel.pack(fill="both", expand=True, pady=(18, 14))
        columns = ("claim", "state", "alignment", "trend", "first_drift")
        self.results_tree = ttk.Treeview(table_panel, columns=columns, show="headings", style="Drift.Treeview")
        headings = {
            "claim": "Policy claim",
            "state": "State",
            "alignment": "Alignment",
            "trend": "Trend",
            "first_drift": "Earliest observed drift",
        }
        widths = {"claim": 470, "state": 120, "alignment": 110, "trend": 120, "first_drift": 170}
        for col in columns:
            self.results_tree.heading(col, text=headings[col])
            self.results_tree.column(col, width=widths[col], anchor="w")
        self.results_tree.pack(fill="both", expand=True, padx=1, pady=1)
        self.results_tree.bind("<Double-1>", self.open_selected_result)

        bottom = tk.Frame(content, bg=BG)
        bottom.pack(fill="x")
        tk.Label(bottom, text="Double-click a result to inspect its evidence trail.", bg=BG, fg=MUTED, font=FONT_SMALL).pack(side="left")
        self._button(bottom, "Open selected", self.open_selected_result).pack(side="right")

    def _build_evidence_page(self) -> None:
        page = self._page("evidence")
        content = tk.Frame(page, bg=BG)
        content.pack(fill="both", expand=True, padx=44, pady=30)

        top = tk.Frame(content, bg=BG)
        top.pack(fill="x")
        self.evidence_title = tk.Label(top, text="Evidence detail", bg=BG, fg=TEXT, font=FONT_TITLE)
        self.evidence_title.pack(side="left")
        self._button(top, "Back to results", lambda: self.show_page("results")).pack(side="right")

        self.evidence_summary = self._panel(content, border=BORDER)
        self.evidence_summary.pack(fill="x", pady=(18, 16))
        self.evidence_state = tk.Label(self.evidence_summary, text="", bg=PANEL, fg=TEXT, font=FONT_SECTION)
        self.evidence_state.pack(anchor="w", padx=18, pady=(16, 4))
        self.evidence_reason = tk.Label(self.evidence_summary, text="", bg=PANEL, fg=TEXT, font=FONT, wraplength=1040, justify="left")
        self.evidence_reason.pack(anchor="w", padx=18)
        self.evidence_meta = tk.Label(self.evidence_summary, text="", bg=PANEL, fg=MUTED, font=FONT_SMALL)
        self.evidence_meta.pack(anchor="w", padx=18, pady=(8, 16))

        tk.Label(content, text="Checkpoint trail", bg=BG, fg=TEXT, font=FONT_SECTION).pack(anchor="w", pady=(0, 8))
        panel = self._panel(content)
        panel.pack(fill="both", expand=True)
        cols = ("time", "evidence", "compliant", "alignment", "hash")
        self.checkpoint_tree = ttk.Treeview(panel, columns=cols, show="headings", style="Drift.Treeview")
        for col, title, width in (
            ("time", "Checkpoint", 160),
            ("evidence", "Evidence", 100),
            ("compliant", "Compliant", 100),
            ("alignment", "Alignment", 110),
            ("hash", "Evidence hash", 520),
        ):
            self.checkpoint_tree.heading(col, text=title)
            self.checkpoint_tree.column(col, width=width, anchor="w")
        self.checkpoint_tree.pack(fill="both", expand=True, padx=1, pady=1)

    def _build_export_page(self) -> None:
        page = self._page("export")
        content = tk.Frame(page, bg=BG)
        content.pack(fill="both", expand=True, padx=44, pady=30)

        top = tk.Frame(content, bg=BG)
        top.pack(fill="x")
        tk.Label(top, text="Export & verify", bg=BG, fg=TEXT, font=FONT_TITLE).pack(side="left")
        self._button(top, "Back to results", lambda: self.show_page("results")).pack(side="right")

        tk.Label(
            content,
            text="Use the existing report formats, then independently verify the generated artifacts before handoff.",
            bg=BG,
            fg=MUTED,
            font=FONT,
        ).pack(anchor="w", pady=(6, 18))

        columns = tk.Frame(content, bg=BG)
        columns.pack(fill="both", expand=True)
        columns.grid_columnconfigure(0, weight=1)
        columns.grid_columnconfigure(1, weight=1)
        columns.grid_rowconfigure(0, weight=1)

        package = self._panel(columns)
        package.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        tk.Label(package, text="Report package", bg=PANEL, fg=TEXT, font=FONT_SECTION).pack(anchor="w", padx=20, pady=(18, 12))
        for filename, meaning in (
            ("drift_report.html", "Browser-viewable executive report"),
            ("drift_report.md", "Human-readable Markdown report"),
            ("drift_report.json", "Machine-readable drift analysis"),
            ("drift_evidence.json", "Evidence export with hashes"),
        ):
            row = tk.Frame(package, bg=PANEL_ALT, highlightthickness=1, highlightbackground="#454A52")
            row.pack(fill="x", padx=20, pady=5)
            tk.Label(row, text=filename, bg=PANEL_ALT, fg=TEXT, font=FONT_BOLD).pack(anchor="w", padx=12, pady=(8, 0))
            tk.Label(row, text=meaning, bg=PANEL_ALT, fg=MUTED, font=FONT_SMALL).pack(anchor="w", padx=12, pady=(0, 8))

        pkg_actions = tk.Frame(package, bg=PANEL)
        pkg_actions.pack(fill="x", padx=20, pady=18)
        self._button(pkg_actions, "Open HTML", self.open_html).pack(side="left")
        self._button(pkg_actions, "Open output folder", self.open_output_folder).pack(side="left", padx=(8, 0))

        verify = tk.Frame(columns, bg=GREEN, highlightthickness=1, highlightbackground="#2C7C61")
        verify.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        tk.Label(verify, text="Independent verification", bg=GREEN, fg="#F5F0E7", font=FONT_SECTION).pack(anchor="w", padx=20, pady=(18, 6))
        tk.Label(
            verify,
            text="The verifier recalculates expected structure or hashes from the generated artifacts and returns PASS or FAIL.",
            bg=GREEN,
            fg="#F5F0E7",
            font=FONT,
            wraplength=500,
            justify="left",
        ).pack(anchor="w", padx=20)

        verify_actions = tk.Frame(verify, bg=GREEN)
        verify_actions.pack(fill="x", padx=20, pady=(20, 10))
        self._button(verify_actions, "Verify report", self.verify_report).pack(side="left")
        self._button(verify_actions, "Verify evidence", self.verify_evidence).pack(side="left", padx=(8, 0))

        self.verify_result = tk.Label(
            verify,
            text="Run a scan first, then verify the generated package.",
            bg="#145E46",
            fg="#F5F0E7",
            font=FONT_BOLD,
            wraplength=500,
            justify="left",
            padx=14,
            pady=14,
        )
        self.verify_result.pack(fill="x", padx=20, pady=(10, 14))

        self.export_hash = tk.Label(verify, text="", bg=GREEN, fg="#F5F0E7", font=FONT_SMALL, wraplength=500, justify="left")
        self.export_hash.pack(anchor="w", padx=20)
        tk.Label(
            verify,
            text="Verification checks artifact integrity. It does not certify regulatory compliance or audit acceptance.",
            bg=GREEN,
            fg="#E5EEE9",
            font=FONT_SMALL,
            wraplength=500,
            justify="left",
        ).pack(anchor="w", padx=20, pady=(18, 18))

    def show_page(self, name: str) -> None:
        sections = {
            "scan": "New Scan",
            "results": "Results",
            "evidence": "Evidence Detail",
            "export": "Export & Verify",
        }
        self.header_section.set(sections[name])
        self.pages[name].tkraise()
        if name == "export":
            self.refresh_export_page()

    def choose_policy(self) -> None:
        path = filedialog.askopenfilename(title="Choose policy claims CSV", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if path:
            self.policy_path.set(path)

    def choose_evidence(self) -> None:
        path = filedialog.askopenfilename(title="Choose behaviour evidence CSV", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if path:
            self.evidence_path.set(path)

    def load_example(self) -> None:
        pack = self.root_dir / "examples" / "template_packs" / "deployment_approval"
        self.policy_path.set(str(pack / "policy_claims.csv"))
        self.evidence_path.set(str(pack / "behavior_evidence.csv"))

    def run_scan(self) -> None:
        policy = Path(self.policy_path.get().strip())
        evidence = Path(self.evidence_path.get().strip())
        if not policy.is_file() or not evidence.is_file():
            messagebox.showerror("Input required", "Choose both a policy CSV and a behaviour evidence CSV.")
            return

        capture = io.StringIO()
        try:
            with contextlib.redirect_stdout(capture):
                policies = load_policies(policy)
                evidence_rows = load_evidence(evidence)
        except SystemExit:
            detail = capture.getvalue().strip() or "The selected CSV files did not pass input validation."
            messagebox.showerror("Input validation failed", detail)
            return
        except Exception as exc:
            messagebox.showerror("Input error", str(exc))
            return

        detector = ComplianceDriftDetector()
        detector.load_policies(policies)
        detector.load_behavior(evidence_rows)
        report = detector.detect_drift()

        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "drift_report.json").write_text(render_json_report(report), encoding="utf-8")
        (self.output_dir / "drift_report.md").write_text(render_markdown_report(report), encoding="utf-8")
        (self.output_dir / "drift_report.html").write_text(render_html_report(report), encoding="utf-8")
        (self.output_dir / "drift_evidence.json").write_text(json.dumps(detector.export_evidence(), indent=2), encoding="utf-8")

        self.report = report
        self.detector = detector
        self.analysis_by_claim = {a.claim_id: a for a in report.analyses}
        self.refresh_results()
        self.show_page("results")

    def refresh_results(self) -> None:
        if self.report is None:
            return

        counts = dict(self.report.summary.get("state_counts", {}))
        counts["UNDECLARED"] = len(self.report.undeclared_behaviors)
        for state, label in self.result_cards.items():
            label.configure(text=str(counts.get(state, 0)))

        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        for analysis in self.report.analyses:
            state = analysis.state.value
            alignment = f"{analysis.current_alignment:.0%}"
            self.results_tree.insert(
                "",
                "end",
                iid=analysis.claim_id,
                values=(analysis.claim_description, state, alignment, analysis.trend, analysis.first_drift_time or "—"),
                tags=(state,),
            )

        for state, color in STATE_COLORS.items():
            self.results_tree.tag_configure(state, foreground=TEXT)

    def open_selected_result(self, event=None) -> None:
        selection = self.results_tree.selection()
        if not selection:
            messagebox.showinfo("Select a result", "Select a policy result first.")
            return
        claim_id = selection[0]
        analysis = self.analysis_by_claim.get(claim_id)
        if analysis is None:
            return
        self.selected_claim_id = claim_id
        self.refresh_evidence_page(analysis)
        self.show_page("evidence")

    def refresh_evidence_page(self, analysis) -> None:
        state = analysis.state.value
        self.evidence_title.configure(text=analysis.claim_description)
        self.evidence_state.configure(text=f"{state}  •  {analysis.current_alignment:.0%} alignment", fg=STATE_COLORS.get(state, TEXT))
        self.evidence_reason.configure(text=analysis.reason)
        self.evidence_meta.configure(
            text=f"Trend: {analysis.trend}   •   Earliest observed drift: {analysis.first_drift_time or '—'}   •   Violation checkpoints: {analysis.violation_count}"
        )

        for item in self.checkpoint_tree.get_children():
            self.checkpoint_tree.delete(item)
        for cp in analysis.checkpoints:
            self.checkpoint_tree.insert(
                "",
                "end",
                values=(
                    cp.checkpoint_time,
                    cp.evidence_count,
                    cp.compliant_count,
                    f"{cp.alignment_score:.0%}",
                    cp.evidence_hash,
                ),
            )

    def refresh_export_page(self) -> None:
        if self.report is None:
            self.export_hash.configure(text="")
            return
        self.export_hash.configure(text=f"Report hash: {self.report.report_hash}")

    def _verify_json_file(self, filename: str, verifier) -> None:
        path = self.output_dir / filename
        if not path.exists():
            self.verify_result.configure(text=f"FAIL — {filename} not found. Run a scan first.", bg=VIOLATED)
            return
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            valid, message = verifier(data)
        except Exception as exc:
            self.verify_result.configure(text=f"FAIL — {exc}", bg=VIOLATED)
            return
        if valid:
            self.verify_result.configure(text=f"PASS — {message}", bg="#145E46")
        else:
            self.verify_result.configure(text=f"FAIL — {message}", bg=VIOLATED)

    def verify_report(self) -> None:
        self._verify_json_file("drift_report.json", verify_drift_report)

    def verify_evidence(self) -> None:
        self._verify_json_file("drift_evidence.json", verify_drift_evidence)

    def open_html(self) -> None:
        path = self.output_dir / "drift_report.html"
        if not path.exists():
            messagebox.showinfo("No report yet", "Run a scan first.")
            return
        webbrowser.open(path.resolve().as_uri())

    def open_output_folder(self) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        path = str(self.output_dir.resolve())
        try:
            if sys.platform.startswith("win"):
                os.startfile(path)  # type: ignore[attr-defined]
            elif sys.platform == "darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path])
        except Exception as exc:
            messagebox.showerror("Could not open folder", str(exc))


def main() -> None:
    try:
        app = DriftUI()
        app.mainloop()
    except tk.TclError as exc:
        print("Unable to start the desktop UI.")
        print("The deterministic CLI remains available with: python software/run_scan.py")
        print(f"Tk error: {exc}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
