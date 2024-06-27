#!/usr/bin/env python3
# -*- coding: utf-8 -*-



ling_and_seman = """Linguistic Structure and Semantics Analysis:
Conduct a detailed examination of the text's linguistic structure and semantic content. Focus on the following elements:

Syntactic Analysis:

Identify passive constructions. Explain their frequency and potential effects on clarity and agency attribution.
Analyze sentence structure variations (simple, compound, complex). Comment on how these affect readability and emphasis.


Semantic Analysis:

Detect instances of ambiguity. Explain how multiple interpretations could affect the text's meaning.
Highlight vague language or undefined terms. Discuss their impact on precision and understanding.
Identify presuppositions or unstated assumptions in the text.


Rhetorical Devices:

Spot uses of inflated language. How does it potentially elevate ordinary concepts?
Identify double speak. Explain how it might obscure or distort meaning.
Detect circumlocutions. Analyze their possible purposes (e.g., evasion, politeness).


Hedging and Qualifiers:

Identify hedging language (e.g., "sort of", "kind of", "possibly").
Spot qualifiers that limit assertions (e.g., "sometimes", "in some cases").
Discuss how these devices affect the perceived certainty or commitment of statements.


Imprecision and Tautologies:

Highlight areas of imprecise language or lack of specific detail.
Identify tautologies or redundant statements.
Analyze the potential effects of imprecision and tautologies on the text's informativeness.
"""

logic_and_arg = """Logical and Argumentative Analysis:
Conduct a thorough examination of the given text, focusing on the logical structure, argumentation, and evidence presentation. Your analysis should address the following aspects:
1. Trustworthiness Assessment:
    * Evaluate the overall credibility of the text based on the quality of evidence presented, internal consistency of arguments, and reliability of sources.
    * Assess the author's expertise or authority on the subject matter.
2. Logical Fallacies Identification:
    * Identify and explain any logical fallacies present in the text. These may include, but are not limited to:
        * Ad hominem arguments
        * Straw man fallacies
        * False dilemmas
        * Slippery slope arguments
        * Circular reasoning
        * Appeal to authority
        * Post hoc ergo propter hoc
    * For each fallacy identified, explain how it weakens the argument or misleads the reader.
3. Credibility and Evidence Evaluation:
    * Assess the quality, relevance, and sufficiency of evidence provided to support claims.
    * Evaluate the credibility of sources cited. Consider factors such as expertise, potential bias, and recency of information.
    * Identify any claims made without supporting evidence and discuss their impact on the overall argument.
4. Coherence and Cohesion Analysis:
    * Examine the logical flow of ideas throughout the text. Are arguments presented in a clear, sequential manner?
    * Assess the strength of connections between different parts of the argument.
    * Identify any logical gaps or unexplained leaps in reasoning.
5. Data Interpretation:
    * If statistical data or research findings are presented, evaluate the appropriateness and accuracy of their interpretation.
    * Check for any potential misuse or misrepresentation of data.
    * Assess whether conclusions drawn from the data are justified and proportionate to the evidence presented.
For each element of your analysis, provide specific examples from the text. Explain how these elements contribute to or detract from the overall strength and persuasiveness of the argument.
"""
prag_and_disct = """Pragmatic and Discourse-level Analysis:
Conduct an in-depth analysis of the given text, focusing on its pragmatic features, discourse structure, and rhetorical strategies. Your analysis should address the following aspects:
1. Pragmatic Analysis:
    * Implicature: Identify and explain instances where the text conveys meaning beyond its literal interpretation. What is implied but not explicitly stated?
    * Speech Acts: Analyze the types of speech acts used (e.g., assertives, directives, commissives, expressives, declaratives) and their functions within the text.
    * Contextual Relevance: Evaluate how well the language and content align with the context in which the text is presented. Consider the assumed audience, purpose, and setting.
2. Discourse-level Analysis:
    * Coherence: Assess the logical flow and connectivity between ideas throughout the text. How well does the text maintain a clear and understandable progression of thoughts?
    * Thematic Progression: Analyze how central themes or topics are introduced, developed, and maintained across the text.
    * Intertextuality: Identify and explain references or allusions to other texts, discourses, or cultural knowledge. How do these contribute to the text's meaning and effectiveness?
3. Metadiscourse Analysis:
    * Examine the use of discourse markers, transitions, and other metadiscursive elements that guide the reader through the text.
    * Analyze how the author refers to their own text or arguments (e.g., "As mentioned earlier," "In conclusion").
    * Identify instances of hedging (e.g., "perhaps," "may") or boosting (e.g., "clearly," "undoubtedly") and their effects on the perceived strength of claims.
4. Tone and Register Analysis:
    * Evaluate the overall tone of the text (e.g., formal, informal, persuasive, informative).
    * Assess the consistency of register throughout the text and its appropriateness for the intended audience and purpose.
    * Analyze how shifts in tone or register, if any, contribute to the text's effectiveness or impact.
5. Persuasive Techniques:
    * Identify and analyze the use of rhetorical appeals (ethos, pathos, logos).
    * Examine the employment of rhetorical devices such as rhetorical questions, repetition, analogy, or metaphor.
    * Assess the effectiveness of these persuasive techniques in the context of the text's goals.
"""

bias_and_sub ="""Bias, Subjectivity, and Author Intent Analysis:
Conduct a comprehensive analysis of the given text, focusing on identifying and evaluating aspects of bias, subjectivity, and the author's underlying intentions. Your analysis should address the following aspects:
1. Bias and Subjectivity Detection:
    * Identify instances of explicit or implicit bias in the text. This may include ideological, cultural, or personal biases.
    * Distinguish between objective statements and subjective opinions.
    * Analyze how the author's perspective might influence the presentation of information or arguments.
2. Author Positioning and Self-referential Language:
    * Examine how the author positions themselves within the text (e.g., as an expert, neutral observer, or passionate advocate).
    * Identify and analyze the use of self-referential language (e.g., "I believe," "in my experience").
    * Evaluate how the author's self-positioning affects the perceived credibility and persuasiveness of the text.
3. Omissions and Imbalances in Perspective:
    * Identify significant information or viewpoints that are absent from the text but relevant to the topic.
    * Assess whether the text presents a balanced view of the subject or favors certain perspectives over others.
    * Analyze how these omissions or imbalances might impact the reader's understanding of the topic.
4. Intended Function of Utterances:
    * Determine the primary intended functions of different parts of the text (e.g., to inform, persuade, entertain, or provoke).
    * Analyze how these functions align with or diverge from the stated purpose of the text.
    * Identify any hidden or secondary intentions that may be present in the text.
5. Emotional Loading of Language:
    * Identify words, phrases, or rhetorical devices that carry strong emotional connotations.
    * Analyze how emotional language is used to influence the reader's perceptions or reactions.
    * Evaluate the balance between emotional appeals and logical arguments in the text.
Your analysis should provide a nuanced understanding of the subtle ways in which bias, subjectivity, and author intent shape the text's message and potential impact.
"""


DENSE_PROMPT = """
Here is a prompt that estimates the semantic density of a text and provides a scale from "Dense" to "Not Dense at All":

Prompt:

Given the following text, estimate its semantic density. Semantic density refers to the richness and complexity of the information conveyed in the text. Consider factors such as the depth of ideas, the use of technical or specialized vocabulary, the level of abstraction, and the amount of information packed into each sentence.

Text:

arduino

Semantic Density Scale:

Dense: The text is rich with complex ideas, specialized vocabulary, and detailed information. Each sentence conveys a substantial amount of information, often requiring prior knowledge or significant cognitive effort to understand.

Somewhat Dense: The text contains a moderate level of complexity, with a mix of specialized and general vocabulary. The ideas are somewhat layered and require a reasonable level of understanding and cognitive effort.

Moderate: The text strikes a balance between complexity and simplicity. It conveys its ideas clearly without oversimplifying, using a mix of detailed and straightforward information.

Somewhat Simple: The text is relatively straightforward, using mostly general vocabulary and simpler ideas. It conveys information clearly but with less depth and fewer complexities.

Not Dense at All: The text is very simple, using basic vocabulary and straightforward ideas. It conveys information in a direct and easy-to-understand manner, with little to no complexity.

Instructions:

Read the provided text.
Evaluate the text based on the criteria described above.
Assign a semantic density rating from 1 to 5, with 1 being "Dense" and 5 being "Not Dense at All."
Justify your rating with a brief explanation.
text to evaluate: /n"""
PROMPT = """
Pragmatic and Discourse Analysis for Text Evaluation:

Trustworthiness Assessment:

Evaluate overall credibility based on evidence quality, internal consistency, and source reliability.
Analyze the coherence and cohesion of arguments presented.


Logical Fallacies Identification:

Detect common fallacies (e.g., ad hominem, straw man, false dilemmas, slippery slopes, circular reasoning).
Identify more subtle logical inconsistencies or faulty reasoning patterns.


Rhetorical Devices and Language Manipulation:

Inflated Language: Identify use of grandiose terms to elevate mundane concepts.
Double Speak: Detect deliberately euphemistic, ambiguous, or obscure language.
Circumlocutions: Recognize unnecessary verbosity or indirect expressions.
Hedging and Qualifiers: Identify language that reduces assertiveness or expresses uncertainty.
Imprecision: Highlight generalizations or lack of specific details.
Tautologies: Spot redundant or self-reinforcing statements.


Syntactic Analysis:

Passive Constructions: Identify use of passive voice to obscure agency or responsibility.
Sentence Structure: Analyze complexity, length, and variation in sentence construction.


Semantic Analysis:

Ambiguity: Detect terms or phrases with multiple possible interpretations.
Vagueness: Highlight undefined or poorly defined terms and concepts.
Presuppositions: Identify unstated assumptions embedded in the text.


Pragmatic Analysis:

Implicature: Recognize implied meanings beyond literal interpretations.
Speech Acts: Analyze the intended function of utterances (e.g., assertives, directives, commissives).
Contextual Relevance: Evaluate appropriateness of language use in given context.


Discourse-level Analysis:

Coherence: Assess logical flow and connectivity between ideas.
Thematic Progression: Analyze development and maintenance of central themes.
Intertextuality: Identify references or allusions to other texts or discourses.


Credibility and Evidence Evaluation:

Source Analysis: Assess credibility and potential biases of information sources.
Citation Quality: Evaluate the relevance, recency, and authority of cited sources.
Data Interpretation: Analyze how quantitative or qualitative data is presented and interpreted.


Bias and Subjectivity Detection:

Identify lexical choices that reveal ideological stances or personal opinions.
Recognize omissions or imbalances in perspective presentation.


Tone and Register Analysis:

Evaluate formality level and its consistency throughout the text.
Assess emotional loading of language and its appropriateness to the genre.


Persuasive Techniques:

Identify appeals to emotion, authority, or logic (ethos, pathos, logos).
Detect use of rhetorical questions, repetition, or other persuasive devices.


Metadiscourse Analysis:

Examine use of discourse markers, hedges, and boosters.
Analyze self-referential language and author positioning within the text.



This refactored prompt incorporates a more comprehensive approach to text analysis, integrating elements of pragmatics and discourse analysis. It provides a structured framework for evaluating various aspects of language use, from surface-level features to deeper semantic and pragmatic implications.
here is the text to evaluate:
"""

orwell_langauge = """ analyze and look for:
1. Staleness of imagery and lack of precision are common issues in modern writing, especially political writing.
2. Overuse of dying metaphors: Using clichéd metaphors that have lost their evocative power.
3. Operators or verbal false limbs: Using unnecessarily complex phrases instead of simple verbs.
4. Pretentious diction: Using overly formal or scientific-sounding words to appear more sophisticated or impartial.
5. Meaningless words: Using vague terms that lack clear definitions, especially in political contexts.
6. Excessive use of foreign phrases, scientific words, or jargon when everyday English equivalents exist.
7. Overreliance on passive voice and noun constructions instead of active verbs.
8. Use of euphemisms to obscure unpleasant truths or defend morally questionable actions.
9. Vague or cloudy language that obscures meaning, often used to defend political positions.
10. Inflated style: Using an abundance of long words to cover up a lack of substance.
11. Ready-made phrases: Stringing together pre-fabricated phrases rather than constructing original sentences.
12. Political orthodoxy tends to produce lifeless, imitative writing styles.
13. Insincerity often leads to unclear language and the use of long words to hide true intentions.
14. The gap between declared and real aims often results in the use of long words and exhausted idioms.
"""


