from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import QuestionUG, QuestionPG
from exam_results.models import  ResultNotAttempt,ResultAnswer
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max
from datetime import datetime
import json
import random
from dotenv import load_dotenv
import os
load_dotenv()




@login_required
def exam_view(request):
    exam_type = request.GET.get('exam_type')
    subject = request.GET.get('subject')
    language = request.GET.get('language', 'english')

    if not exam_type or not subject:
        return redirect('home')

    # 👉 Always set exam_time regardless of session reuse
    question_count = int(os.getenv('UG', 10)) if exam_type.lower() == 'ug' else int(os.getenv('PG', 75))
    exam_time = int(os.getenv('UG_TIME', 600)) if exam_type.lower() == 'ug' else int(os.getenv('PG_TIME', 5400))
    # print(int(os.getenv('UG_TIME', 600)) , exam_time ,'  ---    ',int(os.getenv('PG_TIME', 5400)))
    # exam_time = 600

    # print(question_count, exam_time,subject,language, exam_type)
    try:
        if not request.session['question_indices']:
            request.session.pop('selected_questions', None)
            request.session.pop('question_indices', None)
            request.session.pop('cached_subject', None)
            request.session.pop('cached_exam_type', None)
    except:
        print("Error")


    if 'selected_questions' in request.session and 'question_indices' in request.session:
        selected_questions = request.session['selected_questions']
        question_indices = request.session['question_indices']
        
    else:
        Question = QuestionUG if exam_type.lower() == 'ug' else QuestionPG

        all_questions = list(Question.objects.filter(subject=subject).values(
            'id', 'question', 'option_a', 'option_b', 'option_c', 'option_d'
        ))
        # print("..............")
        # print(all_questions)

        correct_answers = ResultAnswer.objects.filter(
            user=request.user,
            exam_name=subject,
            ug_or_pg=exam_type.upper(),
            is_correct=True
        ).values_list('question_id', flat=True)

        available_questions = [q for q in all_questions if q['id'] not in correct_answers]

        if len(available_questions) < question_count:
            remaining_count = question_count - len(available_questions)
            answered_questions = [q for q in all_questions if q['id'] in correct_answers]
            available_questions.extend(random.sample(answered_questions, min(remaining_count, len(answered_questions))))

        selected_questions = random.sample(available_questions, min(question_count, len(available_questions)))

        question_indices = {str(idx): q['id'] for idx, q in enumerate(selected_questions)}

        request.session['selected_questions'] = selected_questions
        request.session['question_indices'] = question_indices



    # 🔄 Sort the questions as per index order
    sorted_questions = [None] * len(question_indices)
    for index, qid in question_indices.items():
        for question in selected_questions:
            if question['id'] == qid:
                sorted_questions[int(index)] = question
                break

    first_name = request.user.first_name or request.user.username
    last_name = request.user.last_name or ''

    def get_exam_names(table, user, subject):
        return table.objects.filter(user=user, subject=subject).values_list('exam_name', flat=True).distinct()

    def get_all_exam_names(user, subject):
        answers = get_exam_names(ResultAnswer, user, subject)
        not_attempts = get_exam_names(ResultNotAttempt, user, subject)
        all_exam_names = set(answers) | set(not_attempts)  # Union of both sets
        return list(all_exam_names)
    

    Exam_name_list = sorted(get_all_exam_names(user=request.user , subject=subject), key=lambda x: int(x.split('_')[1]))

    # Exam_name = str(subject)+'_'+str(int(Exam_name_list[-1].split('_')[-1])+1)
    if Exam_name_list:
        last_number = int(Exam_name_list[-1].split('_')[-1])
        Exam_name = f"{subject}_{last_number + 1}"
    else:
        Exam_name = f"{subject}_1"  # First exam for this subject




    # print(json.dumps(sorted_questions))
    # print(question_indices)
    context = {
        'Exam_name': Exam_name,
        'question_indices': question_indices,
        'exam_type': exam_type.upper(),
        'subject': subject,
        'language': language,
        'questions': json.dumps(sorted_questions),
        'question_count': len(sorted_questions),
        'user': request.user,
        'first_name': first_name,
        'last_name': last_name,
        'Exam_Time' : exam_time
    }
    # print(context)
    return render(request, 'exam/exam.html', context=context)



@csrf_exempt
@login_required
def submit_exam(request):
    if request.method == 'POST':
        try:
            print("Received exam submission request")
            data = json.loads(request.body)
            answers = data.get('answers', {})
            exam_name = data.get('exam_name')
            subject = data.get('subject')
            ug_or_pg = data.get('exam_type')
            question_indices = data.get('question_indices', {})
            # print(data)
            
            print(f"Submission data: exam_name={exam_name}, subject={subject}, ug_or_pg={ug_or_pg}")
            print(f"Answers count: {len(answers)}, Question indices count: {len(question_indices)}")
            
            if not subject or not ug_or_pg:
                print("Missing required data")
                return JsonResponse({'status': 'error', 'message': 'Missing required data'}, status=400)

            # Get all questions for this exam
            Question = QuestionUG if ug_or_pg.upper() == 'UG' else QuestionPG
            
            # Instead of getting all questions, filter by the question IDs in question_indices
            question_ids = list(map(int, question_indices.keys()))
            exam_questions = Question.objects.filter(id__in=question_ids, subject=subject)
            print(f"Found {len(exam_questions)} questions for this exam from {subject} ({ug_or_pg})")

            correct_count = 0
            incorrect_count = 0
            questions_data = []
            not_attempted_dict = {}
            mark = 0

            

            # Process each question in the exam
            for question in exam_questions:
                try:
                    question_id = str(question.id)
                    selected_option = answers.get(question_id)
                    
                    # Get the index from question_indices
                    question_index = -1
                    if question_id in question_indices:
                        try:
                            question_index = int(question_indices.get(question_id))
                        except (ValueError, TypeError):
                            print(f"Invalid question index for question {question_id}: {question_indices.get(question_id)}")
                    
                    is_correct = False
                    
                    # If no answer was selected, it's not attempted
                    if selected_option is None or selected_option == "none":
                        # Add to not_attempted_dict if we have a valid index
                        if question_index >= 0:
                            not_attempted_dict[question_id] = question_index
                    else:
                        # For attempted questions, check if correct and save to ResultAnswer
                        is_correct = selected_option == question.correct_option
                        if is_correct:
                            correct_count += 1
                            marks = int(os.getenv('UG_CORRECT', 5)) if ug_or_pg.lower() == 'ug' else int(os.getenv('PG_CORRECT', 4))
                            
                        else:
                            incorrect_count += 1
                            marks = int(os.getenv('UG_WRONG', -1)) if ug_or_pg.lower() == 'ug' else int(os.getenv('PG_WRONG', -1))

                        mark += marks
                        
                        # Save to ResultAnswer table for attempted questions
                        ResultAnswer.objects.create(
                            question_id=question.id,
                            index=question_index,
                            exam_name=exam_name,
                            subject=subject,
                            ug_or_pg=ug_or_pg.upper(),
                            user=request.user,
                            is_correct=is_correct,
                            selected_option=selected_option,
                            created_at = datetime.now(),
                            marks = marks
                        )
                        print(f"Saved attempted question {question_id}, option: {selected_option}, index: {question_index} , masks  : {marks}")

                    questions_data.append({
                        'text': question.question,
                        'attempted': selected_option is not None and selected_option != "none",
                        'selected_answer': selected_option if selected_option and selected_option != "none" else None,
                        'correct_answer': question.correct_option,
                        'is_correct': is_correct,
                        'question_index': question_index,
                        'option_a_value': question.option_a,
                        'option_b_value': question.option_b,
                        'option_c_value': question.option_c,
                        'option_d_value': question.option_d
                    })
                except Exception as question_error:
                    print(f"Error processing question {question.id}: {str(question_error)}")
                    continue

            # Save not attempted questions to ResultNotAttempt table
            if not_attempted_dict:
                not_attempted = ResultNotAttempt(
                    exam_name=exam_name,
                    subject=subject,
                    ug_or_pg=ug_or_pg.upper(),
                    user=request.user,
                    created_at = datetime.now(),
                    marks = mark

                )
                not_attempted.set_question_indices(not_attempted_dict)
                not_attempted.save()
                print(f"Saved not attempted questions: {len(not_attempted_dict)}")

            total_questions = len(exam_questions)
            attempted = correct_count + incorrect_count
            not_attempted_count = len(not_attempted_dict)
            score = (correct_count / total_questions) * 100 if total_questions > 0 else 0
            print(f"Exam results: attempted={attempted}, correct={correct_count}, score={score}")
            
            # Sort questions_data by question_index to display in the same order as the exam
            questions_data.sort(key=lambda q: q['question_index'])
            request.session.pop('selected_questions', None)
            request.session.pop('question_indices', None)
            request.session.pop('cached_subject', None)
            request.session.pop('cached_exam_type', None)
            
            # Render the results template
            context = {
                'subject': subject,
                'exam_name' : exam_name,
                'exam_type': ug_or_pg,
                'attempted': attempted,
                'correct': correct_count,
                'wrong': attempted - correct_count,
                'not_attempted': not_attempted_count,
                'total_questions': total_questions,
                # 'score': round(score, 2),
                'questions': questions_data,
                'score' : mark
            }
            
            # print('...........................................exam\n',context)
            return render(request, 'exam_results/results.html', context)
            return render(request, 'exam/results.html', context)

        except json.JSONDecodeError as e:
            print(f"JSON decode error: {str(e)}")
            return JsonResponse({'status': 'error', 'message': f'Invalid JSON format: {str(e)}'}, status=400)
        except Exception as e:
            import traceback
            print(f"Exception in submit_exam: {str(e)}")
            print(traceback.format_exc())
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
