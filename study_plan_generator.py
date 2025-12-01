"""
AI Study Plan Generator
Author: toma okumagba

This script creates a simple personalized study plan based on:
- number of days
- hours available per day
- topics with difficulty and priority

There is also a stub where you can plug in a real LLM
to generate a more natural summary (Generative AI + prompt engineering).
"""

from typing import List, Dict


# Set this to True later if you connect to a real LLM API
USE_LLM = False


def collect_user_input() -> Dict:
    print("🧠 AI Study Plan Generator")
    print("--------------------------")

    while True:
        try:
            days = int(input("How many days do you have to study? "))
            if days <= 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a positive whole number for days.")

    while True:
        try:
            hours_per_day = float(input("How many hours per day can you study on average? "))
            if hours_per_day <= 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a positive number for hours per day.")

    while True:
        try:
            num_topics = int(input("How many topics or courses do you want to study? "))
            if num_topics <= 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a positive whole number for number of topics.")

    topics: List[Dict] = []
    print("\nNow enter your topics with difficulty and priority (1 = low, 5 = high).")
    for i in range(num_topics):
        print(f"\nTopic {i + 1}:")
        name = input("  Name of topic (e.g., MATH2030 Chapter 3): ").strip()
        while True:
            try:
                difficulty = int(input("  Difficulty (1-5): "))
                if difficulty < 1 or difficulty > 5:
                    raise ValueError
                break
            except ValueError:
                print("  Please enter a whole number from 1 to 5.")
        while True:
            try:
                priority = int(input("  Priority (1-5): "))
                if priority < 1 or priority > 5:
                    raise ValueError
                break
            except ValueError:
                print("  Please enter a whole number from 1 to 5.")

        topics.append(
            {
                "name": name if name else f"Topic {i + 1}",
                "difficulty": difficulty,
                "priority": priority,
            }
        )

    return {
        "days": days,
        "hours_per_day": hours_per_day,
        "topics": topics,
    }


def calculate_weights(topics: List[Dict]) -> List[Dict]:
    """
    Simple scoring:
    weight = difficulty + priority

    You could tweak this formula to change how aggressive the plan is.
    """
    for t in topics:
        t["weight"] = t["difficulty"] + t["priority"]
    total_weight = sum(t["weight"] for t in topics)
    if total_weight == 0:
        total_weight = 1  # avoid divide by zero
    for t in topics:
        t["proportion"] = t["weight"] / total_weight
    return topics


def generate_daily_plan(days: int, hours_per_day: float, topics: List[Dict]) -> Dict[int, List[Dict]]:
    """
    Returns a dict:
      day_index -> list of {name, hours}
    The schedule is the same pattern each day, which keeps this fast and simple.
    """
    plan: Dict[int, List[Dict]] = {}
    for day in range(1, days + 1):
        day_plan: List[Dict] = []
        for t in topics:
            topic_hours = round(hours_per_day * t["proportion"], 2)
            if topic_hours < 0.25:
                # tiny clean up: ignore extremely small slices
                continue
            day_plan.append(
                {
                    "name": t["name"],
                    "hours": topic_hours,
                }
            )
        plan[day] = day_plan
    return plan


def simple_ai_tip(topic_name: str, difficulty: int, priority: int) -> str:
    """
    Tiny "AI style" tips without any external API.
    Later you can replace this with a real LLM call.
    """
    if difficulty >= 4 and priority >= 4:
        return f"Start your session with {topic_name} while your focus is strongest. Break it into small chunks."
    if difficulty >= 4:
        return f"{topic_name} is challenging. Try active recall and short review blocks instead of long passive reading."
    if priority >= 4:
        return f"{topic_name} matters a lot. Make sure you review it briefly at the end of the day."
    return f"Keep {topic_name} steady and consistent. A little progress each day will stack up."


def build_raw_plan_text(plan: Dict[int, List[Dict]], meta: Dict) -> str:
    """
    Build a plain text version of the plan for optional LLM summarization.
    """
    lines = []
    lines.append(
        f"Study plan for {meta['days']} days, about {meta['hours_per_day']} hours per day."
    )
    for day, sessions in plan.items():
        lines.append(f"\nDay {day}:")
        if not sessions:
            lines.append("  (No sessions)")
        for s in sessions:
            lines.append(f"  - {s['name']}: {s['hours']} hours")
    return "\n".join(lines)


def llm_generate_summary(raw_plan_text: str) -> str:
    """
    Placeholder for Generative AI call.

    This is where you would:
    - send raw_plan_text and your instructions to an LLM
    - use your favorite provider's Python SDK
    - design a good system prompt and user prompt (prompt engineering)

    For now, it just returns a simple fallback summary.
    """
    if not USE_LLM:
        # Fallback summary when no API is connected
        return (
            "This plan balances your topics across the available days based on "
            "difficulty and priority. Start with the hardest or most important "
            "topics each day, and use short review blocks in the evening to lock things in."
        )

    # Pseudocode example (you would replace this with real API calls):
    #
    # prompt = f"""
    # You are a friendly study coach.
    # Here is a raw study plan:
    # {raw_plan_text}
    #
    # Write a short, encouraging summary (4-6 sentences) explaining how to use this plan.
    # """
    #
    # response = call_llm_api(prompt)
    # return response
    #
    # For now, we keep using the fallback above.
    return "LLM summary would appear here."


def print_plan(plan: Dict[int, List[Dict]], topics: List[Dict], meta: Dict) -> None:
    print("\n==============================")
    print("📚 Your AI Generated Study Plan")
    print("==============================\n")

    for day, sessions in plan.items():
        print(f"Day {day}:")
        if not sessions:
            print("  (No sessions)")
        for s in sessions:
            # find topic info for tips
            match = next((t for t in topics if t["name"] == s["name"]), None)
            if match:
                tip = simple_ai_tip(match["name"], match["difficulty"], match["priority"])
            else:
                tip = ""
            print(f"  - {s['name']}: {s['hours']} hours")
            if tip:
                print(f"    Tip: {tip}")
        print()

    raw_text = build_raw_plan_text(plan, meta)
    summary = llm_generate_summary(raw_text)

    print("Overall AI style summary:")
    print(summary)
    print("\nGood luck, you got this ✨")


def main():
    meta = collect_user_input()
    topics = calculate_weights(meta["topics"])
    plan = generate_daily_plan(meta["days"], meta["hours_per_day"], topics)
    print_plan(plan, topics, meta)


if __name__ == "__main__":
    main()