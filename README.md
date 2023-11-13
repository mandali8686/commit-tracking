# Large Language Model Analysis Toolkit

## Overview

This toolkit consists of two Python scripts (drivers) designed for analyzing software repositories using Large Language Models (LLMs). These drivers interact with the OpenAI API to process commit data from code repositories and evaluate the capabilities of LLMs in understanding code changes and dependencies.

## Research Questions
• RQ1: Assessing LLMs’ ability to identify changed files in a repository based on commit messages.

• RQ2: Evaluating whether LLMs can accurately identify affected components in a repository from commit modifications.


• RQ3: Comparing the effectiveness of LLMs in identifying files and components based on commit messages versus commit
modifications.
– RQ3.1: Examining potential discrepancies between these two methods and the scenarios where they occur.

• RQ4: Probing LLMs’ ability to recognize file dependencies across different commit messages or modifications.

## Scripts Description

1. **Driver for Commit Analysis (`commit_analysis_driver.py`):** This script processes commit messages and file modifications. It sends these data points to the OpenAI API and retrieves LLM's responses. The results are categorized into two types: message results and mods results.

2. **Driver for Dependency Analysis (`dependency_analysis_driver.py`):** This script focuses on analyzing dependencies within the software commits. It queries the LLM to understand file dependencies and stores the results separately.

## Prerequisites

- Python 3.x
- `openai` Python package
- Internet connection for API calls
- An active OpenAI API key

## Preparation

Before running the scripts, make sure to generate the prompts using `prompt.py`. This script will create `prompts.json` that acts as the input for the other two drivers.

## Running the Scripts

### Driver for Commit Analysis

1. Navigate to the script's directory.
2. Run the script with the following command:

   ```bash
   python commit_analysis_driver.py --API <your_api_key> --model <model_name>

Replace <your_api_key> with your actual API key and <model_name> with the desired model (e.g., 'gpt-3.5-turbo').

The script will output two files:
1. message_results.json: Contains results related to commit messages.
2. mods_results.json: Contains results related to file modifications.

**Evaluation Metrics**

Two evaluation metrics are employed to assess the accuracy of LLMs in understanding code repositories:

1. Type Evaluator: This evaluates the accuracy of the LLM in determining the change type of a commit.
2. File Evaluator: This assesses how accurately the LLM can match the changed files in a commit.

Both evaluators provide insights into the efficacy of LLMs in software repository analysis.

