import streamlit as st
import pandas as pd
from page_format import default_pages_config
from utils import add_s_plural

default_pages_config()

st.title("QCM")

questions_df = pd.read_csv("questions.csv")
q_options_df = pd.read_csv("q_options.csv")

# questions_df = questions_df.head().copy()

total_num_question = questions_df.shape[0]

question_number = 1 if "question_number" not in st.session_state else st.session_state["question_number"]
total_answered_question = 1 if "total_answered_question" not in st.session_state \
    else st.session_state["total_answered_question"]

if "question_number" not in st.session_state:
    st.session_state["question_number"] = question_number
    st.session_state["total_answered_question"] = total_answered_question
    st.session_state["dict_count_right_answer"] = {}

dict_count_right_answer = st.session_state["dict_count_right_answer"]

options = [""]
_option = ["A. ", "B. ", "C. ", "D. ", "E. "]

are_all_questions_answered = question_number > questions_df.shape[0]

cols_row_form = st.columns(3)

if are_all_questions_answered:
    cols_row_form[1].write("Vous avez finis toutes les questions")
else:
    with cols_row_form[1].form(key="qcm_form"):
        q_options = q_options_df.loc[q_options_df["question_num"] == question_number]
        _option = [_[0] + _[1] for _ in zip(_option, q_options["options"].to_list())]
        options = options + _option

        question_text = questions_df.loc[questions_df['question_num'] == question_number, "text"].values[0]
        user_answer = st.radio(
            label=f"Question {total_answered_question}/{total_num_question}: {question_text}",
            options=options,
            key="user_answer"
        )

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            if user_answer == "":
                st.warning("Veuillez sélectionner une réponse.")
            else:
                user_answer = user_answer[3:]
                st.write(f"user_answer: {user_answer}")
                is_true_option = q_options_df.loc[(q_options_df["options"] == user_answer) &
                                                  (q_options_df["question_num"] == question_number),
                                                  "is_true_option"].values[0]
                dict_count_right_answer[question_number] = {
                    "question": question_text,
                    "user_answer": user_answer,
                    "is_true_option": is_true_option
                }
                question_number += 1
                total_answered_question += 1

                st.session_state["question_number"] = question_number
                st.session_state["total_answered_question"] = total_answered_question
                st.session_state["dict_count_right_answer"] = dict_count_right_answer
                st.rerun()

keys_correct_answers = [k for k in dict_count_right_answer.keys() if dict_count_right_answer[k]["is_true_option"]]
keys_incorrect_answers = [k for k in dict_count_right_answer.keys() if k not in keys_correct_answers]

if are_all_questions_answered:
    cols_row1_results = st.columns(3)

    score = round(100 * len(keys_correct_answers) / len(dict_count_right_answer.keys()), 2)
    score_color = "black"
    if score < 40:  # red
        score_color = "red"
    elif score < 50:  # orange
        score_color = "orange"
    elif score < 60:  # black
        pass
    elif score < 95:  # green
        score_color = "green"
    else:  # from 95 to 100: blue
        score_color = "blue"

    cols_row1_results[1].write("<h2 style='text-align: center;'>Score</h2>", unsafe_allow_html=True)
    cols_row1_results[1].write(f"<h2 style='color:{score_color}; text-align: center;'>{score}%</h2>",
                               unsafe_allow_html=True)
    if not len(keys_incorrect_answers):
        cols_row1_results[1].success("Bravo! Vous avez répondu correctement a toutes les questions.")

    cols_row2_results = st.columns(2)
    with cols_row2_results[0]:
        # Correct answers
        st.write(f"<h3 style='background-color: #FFFCE7; text-align: center'>{len(keys_incorrect_answers)} "
                 f"réponse{add_s_plural(len(keys_incorrect_answers))} "
                 f"incorrecte{add_s_plural(len(keys_incorrect_answers))}</h3>", unsafe_allow_html=True)
        questions_table = ""
        for current_question_key in keys_incorrect_answers:
            # current_question_key = keys_incorrect_answers[0]
            current_answer_dict = dict_count_right_answer[current_question_key]
            current_question_options = q_options_df.loc[q_options_df["question_num"] == current_question_key]
            current_question_correct_answer_df = current_question_options.loc[
                current_question_options["is_true_option"]]
            current_question_correct_answer_option = current_question_correct_answer_df["options"].values[0]
            current_question_correct_answer_details = current_question_correct_answer_df["details"].values[0]

            questions_table += f"""
            <h5>Question {current_question_key}: {current_answer_dict["question"]}</h5>
            <table style="width: 100%">
                <tr><th>Votre réponse</th> <th>Réponse correcte</th></tr>
                <tr>
                    <td style="background-color: #FFFCE7;">{current_answer_dict["user_answer"]}</td> 
                    <td>{current_question_correct_answer_option}</td>
                </tr>
            </table>
            <p>{current_question_correct_answer_details}</p>
            """

        st.write(questions_table, unsafe_allow_html=True)

    with cols_row2_results[1]:
        # Correct answers
        st.write(f"<h3 style='background-color: #E8F9EE; text-align: center'>{len(keys_correct_answers)} "
                 f"réponse{add_s_plural(len(keys_correct_answers))} "
                 f"correcte{add_s_plural(len(keys_correct_answers))}</h3>", unsafe_allow_html=True)

        questions_table = ""
        for current_question_key in keys_correct_answers:
            # current_question_key = keys_incorrect_answers[0]
            current_answer_dict = dict_count_right_answer[current_question_key]
            current_question_options = q_options_df.loc[q_options_df["question_num"] == current_question_key]
            current_question_correct_answer_df = current_question_options.loc[
                current_question_options["is_true_option"]]
            current_question_correct_answer_option = current_question_correct_answer_df["options"].values[0]
            current_question_correct_answer_details = current_question_correct_answer_df["details"].values[0]

            questions_table += f"""
                    <h5>Question {current_question_key}: {current_answer_dict["question"]}</h5>
                    <table style="width: 100%">
                        <tr><th>Votre réponse</th> <th>Réponse correcte</th></tr>
                        <tr>
                            <td style="background-color: #E8F9EE">{current_answer_dict["user_answer"]}</td> 
                            <td>{current_question_correct_answer_option}</td>
                        </tr>
                    </table>
                    <p>{current_question_correct_answer_details}</p>
                    """

        st.write(questions_table, unsafe_allow_html=True)


def retake():
    st.session_state["question_number"] = 1
    st.session_state["total_answered_question"] = 1
    st.session_state["dict_count_right_answer"] = {}
    # st.rerun()


st.button(label="Recommencer", on_click=retake, type="primary")
