#!/usr/bin/env python3

import argparse
from papers.fetch_papers import fetch_papers, save_to_csv

def main():
    parser = argparse.ArgumentParser(description="Fetch papers from PubMed.")
    parser.add_argument("query", help="PubMed query")
    parser.add_argument("-o", "--output", help="Output CSV file", default="papers.csv")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    if args.debug:
        print(f"Fetching papers with query: {args.query}")

    papers = fetch_papers(args.query)

    if args.debug:
        print(f"Fetched {len(papers)} papers")

    save_to_csv(papers, args.output)

if __name__ == "__main__":
    main()
