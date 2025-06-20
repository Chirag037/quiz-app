import json
import time
import threading

# Global variable to store if time is up
time_up = False

def countdown(t):
    global time_up
    while t > 0:
        mins, secs = divmod(t, 60)
        print(f"\r⏳ Time Left: {mins:02d}:{secs:02d}", end="")
        time.sleep(1)
        t -= 1
    time_up = True
    print("\n⏰ Time's up!")

def ask_question(question_obj, question_num, total_questions, time_limit=15):
    global time_up
    time_up = False
    print(f"\nQuestion {question_num}/{total_questions}: {question_obj['question']}")
    for idx, option in enumerate(question_obj['options']):
        print(f"{idx + 1}. {option}")
    
    # Start countdown timer in a separate thread
    timer_thread = threading.Thread(target=countdown, args=(time_limit,))
    timer_thread.start()

    try:
        answer = None
        while not time_up and answer is None:
            user_input = input("\nEnter your choice (1-4): ")
            if user_input.isdigit():
                answer = int(user_input) - 1
    except Exception as e:
        print("Error:", e)
        answer = None

    timer_thread.join()
    return answer == question_obj['answer'] if answer is not None else False

def load_questions(filename="questions.json"):
    with open(filename, "r") as file:
        return json.load(file)

def main():
    print("🎮 Welcome to the Python Quiz Game!\n")
    questions = load_questions()
    total = len(questions)
    score = 0

    for idx, q in enumerate(questions):
        correct = ask_question(q, idx + 1, total)
        if correct:
            print("✅ Correct!\n")
            score += 1
        else:
            print(f"❌ Wrong! Correct answer: {q['options'][q['answer']]}\n")
        time.sleep(1)

    print(f"\n🏁 Quiz Completed! Your Score: {score}/{total}")

if __name__ == "__main__":
    main()
