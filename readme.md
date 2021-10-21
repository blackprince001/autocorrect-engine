Autocorrect System
==========================================

An autocorrect system predicts that likelihood of a mispelled word to
the correct one.

Steps for Implementing an autocorrect system
----------------------------------------------------------------------------------------------

    1. Identify the mispelled word
    2. Find strings that are `n` edit distance away from the mispelled word
    3. Filter suggested candidates to retain only one found in the vocabulary
    4. Order filtered candidates based on word probabilities
    5. Predict the most likely candidate


In [ ]:

    sample_text = """Thsi is how it's going to make prediactions"""
    for i in sample_text.lower().split():
        best = correct_spelling(i, vocabs, word_probability)
        if best == 0:
            continue
        print(f'"{i}" can be replaced with "{best}"\n')

    "thsi" can be replaced with "[('phsi', 1.0392158492887607e-06), ('thei', 2.0784316985775213e-06), ('thi', 2.0784316985775213e-06), ('this', 0.003951098658995868)]"

    "it's" can be replaced with "[('its', 0.0011306668440261717), ('itus', 5.196079246443803e-06)]"

    "prediactions" can be replaced with "[('predictions', 2.0784316985775213e-06)]"
