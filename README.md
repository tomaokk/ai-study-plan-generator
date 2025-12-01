# ai-study-plan-generator
AI Study Plan Generator

This is a small Python project that builds a personalized study schedule based on the number of days you have, how many hours you can study per day, and the topics you want to cover.
It uses a simple weighted system (difficulty + priority) to split your study time in a way that actually makes sense.
There’s also an optional AI summary feature if you connect an OpenAI API key.



What this project does
	•	Asks you for your study timeframe
	•	Lets you enter topics with difficulty and priority
	•	Calculates how your daily study hours should be divided
	•	Gives short guidance notes for each topic
	•	Can generate a more natural summary using a real LLM if you enable it

It runs in the terminal and prints a full plan for each day.
