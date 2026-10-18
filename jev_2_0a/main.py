from __future__ import annotations
import argparse
from config import DEFAULT_STOCKS
from jev.ai import analyze_all_with_jev
from jev.data import fetch_all_states
from jev.report import fmt,pctile,choice_value,score_value,confidence_value,noul_value,probability,print_table, print_report
from jev.research import build_peer_context

def main():
    parser = argparse.ArgumentParser(description="JEV 2.0A Quant Research Engine")
    parser.add_argument("--stocks", nargs="+", default=DEFAULT_STOCKS)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()
    print("\nFetching stock research data...\n")
    states = fetch_all_states(args.stocks)
    if not states: raise SystemExit("No stocks could be processed.")
    peer_context = build_peer_context(states)
    print("\nRunning JEV analyses...\n")
    results = analyze_all_with_jev(states)
    print_report(states, results, peer_context)
    if args.output: export_json(args.output, states, results, peer_context)

if __name__ == "__main__": main()
