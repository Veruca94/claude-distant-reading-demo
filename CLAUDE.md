# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository is a distant reading demonstration project using Shakespeare plays as a corpus. "Distant reading" is a computational approach to literary analysis that examines large collections of texts through quantitative methods, as opposed to traditional close reading of individual works.

## Corpus Contents

The repository contains five Shakespeare plays from Project Gutenberg:

- `pg1513.txt` - Romeo and Juliet
- `pg1514.txt` - A Midsummer Night's Dream
- `pg1519.txt` - Much Ado about Nothing
- `pg1524.txt` - Hamlet
- `pg1533.txt` - Macbeth

All texts are in plain text format with Project Gutenberg headers and formatting intact.

## Architecture

This is currently a data-only repository containing the source texts for analysis. Analysis tools, scripts, or applications can be built on top of this corpus to perform distant reading operations such as:

- Word frequency analysis
- Character network analysis
- Sentiment analysis across plays
- Stylometric comparisons
- Topic modeling
- N-gram analysis

When developing analysis tools:
- Preserve the original text files unchanged - they serve as the canonical source data
- Text processing should account for Project Gutenberg headers (lines before "*** START OF THE PROJECT GUTENBERG EBOOK ***")
- Consider creating separate output directories for analysis results
- Document any text preprocessing steps (lowercasing, punctuation removal, stopword filtering, etc.)
