# papers/fetch_papers.py
import urllib

class CustomHTTPHandler(urllib.request.HTTPHandler):
    def http_open(self, req):
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')
        return super().http_open(req)

opener = urllib.request.build_opener(CustomHTTPHandler)
urllib.request.install_opener(opener)
import csv
from typing import List, Dict
from Bio import Entrez

Entrez.email = "keerthipolepalli570@gmail.com"
Entrez.tool = "get-papers-list"


def fetch_papers(query: str, max_results: int = 100) -> List[Dict]:
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    handle.close()
    id_list = record["IdList"]

    results = []
    for pmid in id_list:
        handle = Entrez.efetch(db="pubmed", id=pmid, retmode="xml")
        paper = Entrez.read(handle)
        handle.close()

        try:
            article = paper["PubmedArticle"][0]["MedlineCitation"]["Article"]
            authors = article.get("AuthorList", [])
            affiliations = []
            non_academic = []
            company_emails = []

            for author in authors:
                affil = author.get("AffiliationInfo", [{}])[0].get("Affiliation", "")
                affiliations.append(affil)
                if any(keyword in affil.lower() for keyword in ["pharma", "biotech", "inc", "ltd", "corp", "gmbh"]):
                    non_academic.append(author.get("LastName", ""))
                if "@" in affil:
                    company_emails.append(affil)

            title = article.get("ArticleTitle", "")
            pub_date = paper["PubmedArticle"][0]["MedlineCitation"]["Article"].get("Journal", {}).get("JournalIssue", {}).get("PubDate", {}).get("Year", "")

            results.append({
                "PubmedID": pmid,
                "Title": title,
                "Publication Date": pub_date,
                "NonAcademic Authors": "; ".join(non_academic),
                "Company Affiliations": "; ".join(affiliations),
                "Corresponding Author Email": "; ".join(company_emails)
            })
        except Exception as e:
            print(f"Error parsing paper {pmid}: {e}")
            continue

    return results


def save_to_csv(results: List[Dict], filename: str):
    if not results:
        print("No results to save.")
        return
    keys = results[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)
