from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ResultAnswer,ResultNotAttempt
from exam.models import QuestionPG,QuestionUG
from django.shortcuts import render
import json
from collections import defaultdict
from dotenv import load_dotenv
from markdown import markdown
from django.utils.safestring import mark_safe
import os
load_dotenv()


@login_required
def test_history_view(request):
    user = request.user

    # Group attempts by subject
    attempts_by_subject = defaultdict(list)
    total_attempts = 0

    # Fetch all answered questions by the user
    results = ResultAnswer.objects.filter(user=user).order_by('exam_name', 'index')

    not_attempted = ResultNotAttempt.objects.filter(user=user).order_by('exam_name')

    # Dictionary to hold highest index for each exam_name
    highest_not_attempted_by_exam = {}

    for entry in not_attempted:
        try:
            data_dict = json.loads(entry.question_indices or '{}')
            if data_dict:
                highest_value = max(data_dict.values())
                exam_name = entry.exam_name
                # Keep highest value if multiple entries exist for same exam_name
                if exam_name not in highest_not_attempted_by_exam or highest_value > highest_not_attempted_by_exam[exam_name]:
                    highest_not_attempted_by_exam[exam_name] = highest_value
        except Exception as e:
            print(f"Error parsing question_indices for {entry.exam_name}: {e}")


    # We'll use a dict to group each exam attempt by exam_name and subject
    grouped_attempts = {}
    for res in results:
        key = (res.exam_name, res.subject)
        # print(grouped_attempts[key])
        if key not in grouped_attempts:
            grouped_attempts[key] = {
                'questions': [],
                'correct': 0,
                'worng':0,
                'total': 0,
                'score': 0,
                'date': res.created_at,  # using id as fallback for ordering (assumes increasing over time)
                'ug_or_pg':res.ug_or_pg,

            }
        grouped_attempts[key]['questions'].append(res)
        

        if res.is_correct:
            grouped_attempts[key]['correct'] += 1
        else:
            grouped_attempts[key]['worng'] += 1
        grouped_attempts[key]['score'] += res.marks
        grouped_attempts[key]['total'] = max(highest_not_attempted_by_exam[res.exam_name],res.index)+1

    # Format the data for template
    attempt_number = 1
    for (exam_name, subject), data in grouped_attempts.items():
        # score = (data['correct'] / data['total']) * 100 if data['total'] > 0 else 0
        # date_attempted = ResultAnswer.objects.filter(user=user, exam_name=exam_name).order_by('id').first().id
        try:
            total = int(data.get('total', 0))
            correct = int(data.get('correct', 0))
            score = (correct / total) * 100 if total > 0 else 0
        except (ValueError, TypeError):
            score = 0
                
        attempts_by_subject[subject].append({
            'attempt_number': (str(exam_name).split('_')[-1]),
            'exam_name': exam_name,
            # 'subject':subject,
            'date_attempted': data['date'],  # optionally use actual date if available in model
            'score': data['score'],
            'correct_answers': data['correct'],
            'worng_answers': data['worng'],
            'total_questions': data['total'],
            'ug_or_pg':data['ug_or_pg'],
            'id': ResultAnswer.objects.filter(user=user, exam_name=exam_name).first().id  # use this ID for detail view
        })

        # print(attempts_by_subject)
        attempt_number += 1
        total_attempts += 1

    context = {
        'attempts_by_subject': dict(attempts_by_subject),
        'total_attempts': total_attempts,
    }

    # print(context)

    return render(request, 'exam_results/test_history.html', context)






@login_required
def result_detail_view(request, exam_name, subject, ug_or_pg):
    print(exam_name,subject,ug_or_pg)
    try:
        user = request.user
        ug_or_pg = ug_or_pg.upper()

        # Get attempted questions
        attempted_qs = ResultAnswer.objects.filter(
            user=user,
            exam_name=exam_name,
            subject=subject,
            ug_or_pg=ug_or_pg
        )

        # Get not attempted record (there should be only one per exam)
        not_attempted_record = ResultNotAttempt.objects.filter(
            user=user,
            exam_name=exam_name,
            subject=subject,
            ug_or_pg=ug_or_pg
        ).first()

        total_questions = attempted_qs.count()
        correct_count = attempted_qs.filter(is_correct=True).count()
        attempted = total_questions
        not_attempted = 0
        mark = sum(a.marks for a in attempted_qs)

        if not_attempted_record:
            not_attempted_dict = not_attempted_record.get_question_indices() or {}
            not_attempted = len(not_attempted_dict)
            mark += not_attempted_record.marks or 0

        all_questions = []

        Question = QuestionUG if ug_or_pg == 'UG' else QuestionPG

        for ans in attempted_qs:
            try:
                question_obj = Question.objects.get(id=ans.question_id)
                # all_questions.append({
                #             'text': mark_safe(markdown(question_obj.question, extensions=['extra'])),
                #             'selected_answer': ans.selected_option,
                #             'attempted': True,
                #             'correct_answer': question_obj.correct_option,
                #             'is_correct': ans.is_correct,
                #             'question_index': ans.index,
                #             'option_a_value': mark_safe(markdown(question_obj.option_a, extensions=['extra'])),
                #             'option_b_value': mark_safe(markdown(question_obj.option_b, extensions=['extra'])),
                #             'option_c_value': mark_safe(markdown(question_obj.option_c, extensions=['extra'])),
                #             'option_d_value': mark_safe(markdown(question_obj.option_d, extensions=['extra'])),
                #             'marks': ans.marks
                #         })
                
                all_questions.append({
                    'text': mark_safe(markdown(question_obj.question, extensions=['extra'])),  # only question uses markdown
                    'selected_answer': ans.selected_option,
                    'attempted': True,
                    'correct_answer': question_obj.correct_option,
                    'is_correct': ans.is_correct,
                    'question_index': ans.index,
                    'option_a_value': mark_safe(question_obj.option_a),  # No markdown here
                    'option_b_value': mark_safe(question_obj.option_b),
                    'option_c_value': mark_safe(question_obj.option_c),
                    'option_d_value': mark_safe(question_obj.option_d),
                    'marks': ans.marks
                })

            except Question.DoesNotExist:
                print(f"Question not found for ID: {ans.question_id}")

        # Add placeholders for not attempted (optional)
        if not_attempted_record:
            Question = QuestionUG if ug_or_pg == 'UG' else QuestionPG
            question_ids = map(int, not_attempted_dict.keys())
            questions = Question.objects.filter(id__in=question_ids)

            for q in questions:
                index = not_attempted_dict.get(str(q.id), -1)
                all_questions.append({
                    'text': mark_safe(markdown(q.question, extensions=['extra'])),
                    'selected_answer': None,
                    'attempted': None,
                    'correct_answer': q.correct_option,
                    'is_correct': False,
                    'question_index': index,
                    'option_a_value': mark_safe(markdown(q.option_a, extensions=['extra'])),
                    'option_b_value': mark_safe(markdown(q.option_b, extensions=['extra'])),
                    'option_c_value': mark_safe(markdown(q.option_c, extensions=['extra'])),
                    'option_d_value': mark_safe(markdown(q.option_d, extensions=['extra'])),
                    'marks': 0
                })

        all_questions.sort(key=lambda x: x['question_index'])

        context = {
            'exam_name': exam_name,
            'subject': subject,
            'exam_type': ug_or_pg,
            'attempted': attempted,
            'correct': correct_count,
            'wrong': attempted - correct_count,
            'not_attempted': not_attempted,
            'total_questions': attempted + not_attempted,
            'score': mark,
            'questions': all_questions
        }
        # print('exam_results',context)
        return render(request, 'exam_results/results.html', context)

    except Exception as e:
        import traceback
        print("Error in result_detail_view:", e)
        print(traceback.format_exc())
        return render(request, 'exam_results/error.html', {'message': 'Something went wrong while fetching result details.'})
