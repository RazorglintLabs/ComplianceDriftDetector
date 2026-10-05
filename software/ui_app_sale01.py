"""Compliance Drift Detector — Sale 01 desktop UI semantics correction.

This launcher subclasses the frozen local UI and corrects presentation-level
ambiguities found during the owner walkthrough:

- policy-claim UNDECLARED state is kept separate from undeclared behavior refs;
- current state/current alignment are labeled explicitly;
- first_drift_time is presented as First threshold breach;
- a full-history RECOVERED label is shown when the latest checkpoint is aligned
  again after an earlier threshold breach;
- the engine's raw first-to-last trend remains visible in Evidence Detail.

No detector classification, evidence, report-seal, or verifier logic is changed.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from ui_app import (
    BG,
    FONT,
    FONT_BOLD,
    FONT_SMALL,
    FONT_TITLE,
    MUTED,
    PANEL,
    STATE_COLORS,
    TEXT,
    DriftUI,
)
from ui_semantics import CLAIM_STATES, history_status, result_counts


class Sale01DriftUI(DriftUI):
    """Frozen Sale 01 UI with clarified current-vs-history semantics."""

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
            text=(
                "Current policy-claim states are counted separately from unmatched behaviour references. "
                "Open any result to inspect its complete checkpoint history."
            ),
            bg=BG,
            fg=MUTED,
            font=FONT,
        ).pack(anchor="w", pady=(6, 18))

        cards = tk.Frame(content, bg=BG)
        cards.pack(fill="x")
        self.result_cards = {}
        display_labels = {
            "ALIGNED": "ALIGNED",
            "DRIFTING": "DRIFTING",
            "VIOLATED": "VIOLATED",
            "UNDECLARED": "UNDECLARED (NO EVIDENCE)",
        }
        for idx, state in enumerate(CLAIM_STATES):
            card = tk.Frame(cards, bg=PANEL, highlightthickness=1, highlightbackground=STATE_COLORS[state])
            card.grid(row=0, column=idx, sticky="nsew", padx=(0 if idx == 0 else 7, 0 if idx == 3 else 7))
            cards.grid_columnconfigure(idx, weight=1)
            count = tk.Label(card, text="0", bg=PANEL, fg=TEXT, font=("Segoe UI Semibold", 22))
            count.pack(anchor="w", padx=16, pady=(12, 0))
            tk.Label(
                card,
                text=display_labels[state],
                bg=PANEL,
                fg=STATE_COLORS[state],
                font=FONT_BOLD,
            ).pack(anchor="w", padx=16, pady=(0, 12))
            self.result_cards[state] = count

        undeclared_panel = tk.Frame(
            content,
            bg=PANEL,
            highlightthickness=1,
            highlightbackground=STATE_COLORS["UNDECLARED"],
        )
        undeclared_panel.pack(fill="x", pady=(12, 0))
        self.undeclared_behavior_count = tk.Label(
            undeclared_panel,
            text="0 undeclared behaviour findings",
            bg=PANEL,
            fg=TEXT,
            font=FONT_BOLD,
        )
        self.undeclared_behavior_count.pack(side="left", padx=(16, 12), pady=9)
        tk.Label(
            undeclared_panel,
            text="Unmatched UNDECLARED-* evidence references; these are findings, not policy-claim states.",
            bg=PANEL,
            fg=MUTED,
            font=FONT_SMALL,
        ).pack(side="left", padx=(0, 16), pady=9)

        table_panel = self._panel(content)
        table_panel.pack(fill="both", expand=True, pady=(14, 12))
        columns = ("claim", "state", "alignment", "history", "first_breach")
        self.results_tree = ttk.Treeview(table_panel, columns=columns, show="headings", style="Drift.Treeview")
        headings = {
            "claim": "Policy claim",
            "state": "Current state",
            "alignment": "Current alignment",
            "history": "History status",
            "first_breach": "First threshold breach",
        }
        widths = {"claim": 450, "state": 125, "alignment": 125, "history": 135, "first_breach": 175}
        for col in columns:
            self.results_tree.heading(col, text=headings[col])
            self.results_tree.column(col, width=widths[col], anchor="w")
        self.results_tree.pack(fill="both", expand=True, padx=1, pady=1)
        self.results_tree.bind("<Double-1>", self.open_selected_result)

        bottom = tk.Frame(content, bg=BG)
        bottom.pack(fill="x")
        tk.Label(
            bottom,
            text=(
                "RECOVERED = latest checkpoint is aligned after an earlier threshold breach. "
                "The raw first-to-last trend remains visible in Evidence Detail."
            ),
            bg=BG,
            fg=MUTED,
            font=FONT_SMALL,
        ).pack(side="left")
        self._button(bottom, "Open selected", self.open_selected_result).pack(side="right")

    def refresh_results(self) -> None:
        if self.report is None:
            return

        claim_counts, undeclared_behavior_count = result_counts(self.report)
        for state, label in self.result_cards.items():
            label.configure(text=str(claim_counts.get(state, 0)))

        noun = "finding" if undeclared_behavior_count == 1 else "findings"
        self.undeclared_behavior_count.configure(
            text=f"{undeclared_behavior_count} undeclared behaviour {noun}"
        )

        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        alignment_threshold = self.report.summary.get("thresholds", {}).get("alignment", 0.95)
        for analysis in self.report.analyses:
            state = analysis.state.value
            alignment = f"{analysis.current_alignment:.0%}"
            history = history_status(analysis, alignment_threshold=alignment_threshold)
            self.results_tree.insert(
                "",
                "end",
                iid=analysis.claim_id,
                values=(
                    analysis.claim_description,
                    state,
                    alignment,
                    history,
                    analysis.first_drift_time or "—",
                ),
                tags=(state,),
            )

        for state in STATE_COLORS:
            self.results_tree.tag_configure(state, foreground=TEXT)

    def refresh_evidence_page(self, analysis) -> None:
        state = analysis.state.value
        alignment_threshold = 0.95
        if self.report is not None:
            alignment_threshold = self.report.summary.get("thresholds", {}).get("alignment", 0.95)
        history = history_status(analysis, alignment_threshold=alignment_threshold)

        self.evidence_title.configure(text=analysis.claim_description)
        self.evidence_state.configure(
            text=f"Current state: {state}  •  {analysis.current_alignment:.0%} current alignment",
            fg=STATE_COLORS.get(state, TEXT),
        )
        self.evidence_reason.configure(text=analysis.reason)
        self.evidence_meta.configure(
            text=(
                f"History status: {history}   •   First-to-last trend: {analysis.trend}   •   "
                f"First threshold breach: {analysis.first_drift_time or '—'}   •   "
                f"Violation checkpoints: {analysis.violation_count}"
            ),
            wraplength=1040,
            justify="left",
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


def main() -> None:
    try:
        app = Sale01DriftUI()
        app.mainloop()
    except tk.TclError as exc:
        print("Unable to start the Sale 01 desktop UI.")
        print("The deterministic CLI remains available with: python software/run_scan.py")
        print(f"Tk error: {exc}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
