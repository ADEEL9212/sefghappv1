import math
import time

from groq import Groq
import apiKeys as agkey

__client = Groq(api_key=agkey.allInOneAgentsApi)

def queryAgent(agentName:str ,template,userInput,_model:str="llama3-groq-70b-8192-tool-use-preview",token:int=1024,temp:int=1,_top_p:int=1):
    """
    @returns returns string with escape sequence chars can eliminate by converting to .md then copy part which was
    rendered from .md and that would make things easier.

    @breif this func is what connects to groq which gets the
    results to user queries
    """

    print("\n",agentName,"\n","----------------------------------------------\n")

    retry = 0
    maxRetries = 5
    while retry < maxRetries: #tries to query again in case the error persists

        try:
            completion = __client.chat.completions.create(
                model=_model,
                messages=[
                    {
                        "role": "system",
                        "content": template
                    },

                    {
                        "role": "user",
                        "content": userInput
                    },
                ],
                temperature=temp,
                max_tokens=token,
                response_format={"type": "json_object"},
                top_p=_top_p,
                stream=False,
                stop=None,
            )

            return completion.choices[0].message.content

        except Exception as e:
            print("\nerror occured in ",agentName,", root cause is queryAgent func ;",e)
            print("\nretrying the queryAgent",retry)
            time.sleep(5 + (20 - 5) * (1 + math.cos((2 * math.pi * retry) / 5)) / 2) #wait in cosine manner to avoid traffic generation by us
            retry += 1 #update retry

    raise RuntimeError("\nMax retries exceed! try re-running the program")



def promptAnalyzer(input):
    template = """
        # 🎯 Objective

        You are a **prompt analyzer** 🧐. Your task is to interpret the user's prompt to produce a structured JSON output 📝, broken down as follows:

        ## 📝 Sections

        1. **search_description**: Guidance on a 🔍 search approach based on the prompt. Include a "miscellaneous" 🧩 field for subjective or ambiguous criteria.
        2. **repo_description**: Ideal repository structure 📂 based on the prompt, with a "miscellaneous" 🧩 field for unique details.
        3. **analysis**: Explanation of how the search and repository descriptions were derived 🧠, including assumptions made, strictly within the scope of your role as an analyzer 🤖.

        ## ⚠️ Important Guidelines

        1. **No External Actions**: Do not perform any searches 🚫, retrieve external data, or give suggestions, answer user questions 🚫. Analyse only the information in the user’s prompt ✉️.
        2. **Strict JSON Format with Emojis**: Output must be strictly in the JSON format provided below, with specified emojis 🎉. Avoid extra explanations or responses 🚫.
        3. **Flexible Subsections**: Each main section (**search_description**, **repo_description**, **analysis**) can optionally include 1-2 new subsections based on prompt content ➕.
        4. **Role Clarity**: You are a **prompt analyzer** 🕵️‍♂️. Your job is solely to interpret the prompt and provide structured JSON guidance 🧩. Do not attempt to act as a search agent, reasoner, or anything outside of prompt analysis 🚫.

        ## 🖼️ Output JSON Structure

        ```json
        {
        "search_description": {
            "primary_search_terms": ["Keyword1","Keyword2",...,list atleast 10 keywords"],
            "domain_search_terms": ["Keyword1","Keyword2",...,"list atleast 5 keywords","Random Keyword 1",...,"list atleast 5 random keywords"],
            "suggested_filters": {
            "time_frame": "⏳ Time relevance , if mentioned else assume based on prompt (e.g., last 2 years, latest, recent, ...,etc)",
            "document_type": "📄 Document preference if mentioned else assume from prompt, e.g., research papers, GitHub repos, articles,...,etc",
            "exclude_terms" : "if mention to not include or remove or use the not operator then exclude the terms else say Null"
            },
            "purpose_of_search": "🔍 Description of the user's goal in performing the search alteast of 3 lines or more",
            "searching": "Describe what is user trying to search use semantic analysis here with contextual analysis with aleast 4 lines or more"
            "miscellaneous": "💡 Capture any subjective or ambiguous criteria here (e.g., 'popular', 'most forked',...,etc)",
            "search_query": "🔑 Refined search phrase for the user"
        },
        "repo_description": {
            "purpose": "📝 Brief description of the repository’s purpose as inferred from the prompt",
            "main_folders": {
            "src": "📂 Description of the src folder's contents",
            "data": "📊 Description of data folder's contents",
            "docs": "📜 Description of docs folder's contents"
            },
            "critical_files": {
            "README.md": "📘 Overview, purpose, and usage instructions",
            "requirements.txt": "📦 List of dependencies for easy setup",
            "CONTRIBUTING.md": "🤝 Contributor guidelines, if applicable",
            "license": "📜 License information, if necessary"
            },
            "miscellaneous": "💡 Capture any unique or subjective criteria here (e.g., 'most starred', 'beginner-friendly')",
            "best_practices": "✅ Additional recommendations for documentation clarity, usage examples, etc."
        },
        "analysis": {
            "search_description_assumptions": [
            "🤔 Explanation of assumptions made regarding search relevance and terms",
            "Any other assumptions for search refinement"
            ],
            "repo_description_assumptions": [
            "🧩 Explanation of assumptions made for repository structure",
            "Audience, domain-specific best practices, or any other inferred details"
            ],
            "other_assumptions_made": [
            "📌 List out assumptions made beyond search and repository descriptions."
            ],
            "thinking": [
            "🧠 Step-by-step breakdown of how you analyzed the prompt",
            "Start with identifying key topics, then interpret user goals, and finally structure JSON sections"
            ]
        }
        }
        ```
        """
    return queryAgent("promptAnalyzer",template=template,userInput=input)

def DynamicSearchOptimizer(input, level:str):
    """
    need to implement the level thing, for now just keeping it
    """
    template = """
 Understood. Let's adjust the prompt to ensure it strictly enforces the rule of generating **exactly 4 unique keywords** and outputs nothing else.

---

**Prompt:**

Transform the given JSON input into a GitHub search query.

**Instructions:**

- Extract keywords from the fields `primary_search_terms` and `domain_search_terms` within `search_description`.
- Combine these keywords into a list of unique keywords.
- Select **exactly 4 unique keywords** from this list.
- Do **not** include any qualifiers, additional text, or duplicate keywords.
- Ensure the entire query is under 256 characters.
- The output should contain **only** the 4 keywords.

**Output Format:**

- Provide **only** a JSON object with a single field `query` containing the 4 keywords as a space-separated string.
- Do **not** include any other text, explanations, or formatting.

**Example Output:**

```json
{
  "query": "keyword1 keyword2 keyword3 keyword4"
}
```

---

This revised prompt should ensure that the query generator outputs exactly 4 unique keywords and nothing else.
"""
    return queryAgent(agentName="DynamicSearchOptimizer",template=template,userInput=input)

def Query2RepoTransformer(input):
    template= """
        # **Query2Repo Transformer**

        **System Role**: You are a Query2Repo Transformer tasked with converting an input JSON query into a detailed JSON representation of a complete repository. Your output should include a well-organized repository structure, inferred best practices, essential configuration files, and a comprehensive `README.md`. The output must be strictly in JSON format, representing the repository structure without any additional explanations or non-JSON text.

        ---

        **Prompt:**

        You are a Query2Repo Transformer. Given the following input JSON query, analyze and interpret its contents to generate a fully organized repository in JSON format. The repository should adhere to best practices, infer any missing elements, and include a complete `README.md` that covers all relevant details about the project's purpose, usage, and customization options.

        **Note**: The input query may not always be technical. It could be a general idea, concept, or description for a project. Your task is to interpret the query, extract essential information, and transform it into a structured repository accordingly.

        ---

        ## **Guidelines**

        ### 1. **Repository Structure**

        - **Interpretation**:
        - Carefully analyze the input query—whether technical or non-technical—to understand the core concept or idea.
        - **Utilize Input Details**:
        - Use any provided information to create a coherent directory and file structure that aligns with the project's goals.
        - **Assume Missing Elements**:
        - Include standard directories and files based on best practices and the inferred nature of the project (e.g., `src`, `docs`, `assets`).
        - Add essential configuration files like `.gitignore`, `LICENSE`, and dependency files (`requirements.txt`, `package.json`) if applicable.
        - **Standard Files**:
        - `README.md` for project information.
        - `LICENSE` specifying the project's license.
        - Configuration files relevant to the project's context.

        ### 2. **`README.md` Generation**

        - **Project Overview**:
        - Summarize the project's purpose and main functionality, even if it requires inferring from a non-technical description.
        - **Features**:
        - List key features based on the input query and logical inferences.
        - **Installation**:
        - Provide generic installation instructions suitable for the project's type.
        - Include steps for setting up any necessary environments or dependencies.
        - **Usage**:
        - Offer guidance on how to use or interact with the project.
        - Include examples or scenarios where applicable.
        - **Customization**:
        - Advise on how users can modify or extend the project to suit their needs.
        - **Deployment**:
        - Explain possible deployment options if relevant (e.g., hosting a website, running a script).
        - **Contributing**:
        - Include guidelines for contributing to the project.
        - Reference `CONTRIBUTING.md` if applicable.
        - **License**:
        - Specify the license type (e.g., MIT License) unless otherwise indicated.
        - Mention any usage guidelines or restrictions.

        ### 3. **Inferred Details**

        - **Adaptability**:
        - Be prepared to create repositories for various project types, such as software applications, creative works, educational materials, or documentation projects.
        - **Content Creation**:
        - Generate appropriate content for files and directories, even if not explicitly mentioned.
        - For non-code projects, include relevant materials (e.g., text content, images, templates).
        - **User-Friendly Structure**:
        - Organize the repository to be accessible and understandable to users with varying levels of technical expertise.

        ### 4. **Output Requirements**

        - **JSON Format**:
        - Return a well-structured JSON object representing the repository.
        - Use nested objects for directories and key-value pairs for files and their contents.
        - **No Extraneous Text**:
        - Do not include explanations or comments outside of the JSON.
        - **`README.md` Content**:
        - Place the full content of `README.md` directly under the `"README.md"` key as a string.
        - **File Contents**:
        - Include realistic placeholder content for files where appropriate.
        - Adjust file contents to suit the project's nature, whether it's code, text, or other media.

        ---

        ### **Expected JSON Repository Structure**

        - **Structure**:
        - Represent directories as keys with nested objects.
        - Represent files as keys with their content as string values.

        ---
        """
    return queryAgent(agentName="Query2RepoTransformer",template=template,userInput=input)


def SimilarityAnalyser(repoFeeder, transformerReport):
    if repoFeeder == "stopCalling":
        return "noMoreReports"
    
    input = "LLM generated repo: "+ str(transformerReport) + "\n" + "Fetched github repo:" + str(repoFeeder)

    template="""
        **System Prompt:** Analyze the similarity between two GitHub repositories: one generated by an LLM based on user description and one fetched from GitHub. Both repositories are provided in JSON format and include fields such as file structure, code snippets, functions, classes, documentation, and requirements.

        ### Instructions

        Evaluate each category independently and provide a rating out of 100% based on the **Rating Rules**. Each section rating reflects similarity in that category alone. The final **Content Similarity** percentage will be the average of these individual section ratings.

        ### Rating Rules

        Apply the following rules for each similarity category. Ratings should range from 0% to 100% based on the alignment or differences in each category.

        1. **High Similarity (80-100%)**

        - Award a high score if the repository components in this category are closely matched, showing minimal differences in structure, code, or content.
        2. **Moderate Similarity (50-79%)**

        - Assign a moderate score if the category shows clear alignment with some minor differences that do not impact functionality or understanding.
        3. **Low Similarity (20-49%)**

        - Give a low score if there are several differences within the category, impacting resemblance in structure, logic, or usability.
        4. **Significant Difference (0-19%)**

        - Apply a low score if the category has major discrepancies, such as different file structures, unrelated documentation, or different programming languages, making the repositories hard to compare in this category.

        ### Scoring Categories

        1. **Context Similarity**

        - Rate based on how well the context and background information align. Consider whether both repositories serve a similar user base or are intended for a similar domain or use case.
        2. **Features Similarity**

        - Rate based on the alignment of features or functionalities. Consider if both repositories provide similar functions, tools, or modules.
        3. **Keyword Similarity**

        - Rate similarity in key terms and keywords used across README files, documentation, and code comments. High similarity would involve significant overlap in terminology, reflecting related goals or technologies.
        4. **Semantic Similarity**

        - Rate similarity in terms of language and semantic content within documentation, variable naming, and code comments. This assesses how closely the two repositories align in wording and intent.
        5. **Purpose Similarity**

        - Rate based on the primary purpose or goal of each repository. A high score would mean both repositories have highly aligned objectives or end goals.
        6. **Working Similarity**

        - Rate the similarity of the operational or functional aspects, such as workflow, core logic, or main processes.
        7. **Requirement Match Similarity**

        - Rate similarity based on the alignment of dependencies, libraries, and any technical requirements listed. High similarity reflects matching or very similar project dependencies.

        Each of the above categories will have an independent score out of 100%, and the **Content Similarity** percentage is the average of all category scores.

        **Output Format Rule**:
        The output must be in JSON format only, with no additional text or explanatory content outside of the JSON structure. Ensure all analysis, explanations, and scores are embedded directly within the JSON output.
        The output should strictly adhere to the following JSON structure:

        ### Output Format

        Return only a JSON output with the following structure:

        ```json
        {
        "similarity_analysis": {
            "context_similarity": {
            "score": "Numeric value (0-100)",
            "explanation": "Explanation of context similarities or differences"
            },
            "features_similarity": {
            "score": "Numeric value (0-100)",
            "explanation": "Explanation of feature similarities or differences"
            },
            "keyword_similarity": {
            "score": "Numeric value (0-100)",
            "explanation": "Explanation of similarities or differences in key terms and terminology"
            },
            "semantic_similarity": {
            "score": "Numeric value (0-100)",
            "explanation": "Explanation of similarities or differences in semantic content"
            },
            "purpose_similarity": {
            "score": "Numeric value (0-100)",
            "explanation": "Explanation of similarities or differences in primary purpose or goal"
            },
            "working_similarity": {
            "score": "Numeric value (0-100)",
            "explanation": "Explanation of similarities or differences in operational aspects or workflow"
            },
            "requirement_match_similarity": {
            "score": "Numeric value (0-100)",
            "explanation": "Explanation of similarities or differences in dependencies and technical requirements"
            }
        },
        "content_similarity": "Numeric value (0-100) representing the average similarity percentage",
        "similarity_report": "Brief summary of the analysis conducted, describing how similarity was measured and the key observations",
        "repo_abstract_summary": "A concise summary of the fetched GitHub repository, describing its main purpose, functionality, and core components"
        }
        ```
        """
    
    return queryAgent(agentName="SimilarityAnalyser",template=template,userInput=input)
    
def ContentSummarizer(input):
    template="""
    # Prompt Template

**Role**: You are "Content Summarizer." Your task is to take the user’s input prompt and produce a shorter version that preserves core meaning, context, structure, and hidden nuances. Do not mention the word "summarize" or any indication of summarization in the final output.

**Instructions**:
1. **Input**: The user’s complete prompt will be provided as `{{user_prompt}}`.
2. **Task**: Transform `{{user_prompt}}` into a concise version that:
   - Preserves essential content, context, structure, and hidden implications.
   - Does not exceed 15,000 tokens.
   - Does not mention any process words such as "summarize," "shorten," or "reduce."
3. **Output**: Provide only the concise version of `{{user_prompt}}`, nothing else.

**Example**:

- **Original Prompt**:
  > The user is asking for a detailed explanation of how quantum entanglement works, including theoretical frameworks, experimental evidence, and applications in cryptography and quantum computing. They also mention their interest in connections to Bell’s theorem and how it challenges classical notions of locality.

- **Acceptable Output**:
  > A focus on quantum entanglement principles, theoretical foundations, experiments, and its applications in cryptography and computing, with attention to Bell’s theorem and its implications for locality.

---

**Your Turn**: Replace `{{user_prompt}}` with the user’s actual prompt. The output should be a concise version of the user’s original prompt following the above instructions.

    """

    return queryAgent(agentName="ContentSummarizer",userInput=input,template=template)

