import streamlit as st
import random
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
import os

# Growth mindset quotes
quotes = [
    "The only person you should try to be better than is the person you were yesterday.",
    "Mistakes are proof that you're trying.",
    "Everything is hard before it is easy.",
    "Success is not final, failure is not fatal: it is the courage to continue that counts.",
    "The expert in anything was once a beginner.",
    "Your potential is unlimited. Go do what you want to do.",
    "The more you practice, the better you get.",
    "I haven't failed. I've just found 10,000 ways that won't work."
]

def load_reflections():
    if os.path.exists('reflections.json'):
        with open('reflections.json', 'r') as f:
            return json.load(f)
    return []

def save_reflection(reflection_data):
    reflections = load_reflections()
    reflections.append(reflection_data)
    with open('reflections.json', 'w') as f:
        json.dump(reflections, f)

def main():
    st.set_page_config(page_title="Growth Mindset App", page_icon="🌱", layout="wide")
    
    st.title("🌱 Growth Mindset Journey")
    st.markdown("### Embrace the power of 'yet'!")

    # Tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Daily Reflection", "Progress Tracker", "Past Reflections"])

    with tab1:
        # Daily Quote
        st.subheader("Today's Inspiration")
        st.info(random.choice(quotes))

        # Self-reflection
        st.subheader("Daily Reflection")
        
        with st.form("reflection_form"):
            date = st.date_input("Date", datetime.now())
            mood = st.slider("How are you feeling today?", 1, 10, 5)
            today_learned = st.text_area("What did you learn today?")
            challenges = st.text_area("What challenges did you face?")
            growth_area = st.text_area("What would you like to improve?")
            
            # Growth Activities Checkboxes
            st.subheader("Today's Growth Activities")
            col1, col2 = st.columns(2)
            
            with col1:
                read_new = st.checkbox("Read something new")
                practiced = st.checkbox("Practiced a skill")
                feedback = st.checkbox("Asked for feedback")
                
            with col2:
                challenge = st.checkbox("Tried something difficult")
                helped = st.checkbox("Helped someone else")
                reflected = st.checkbox("Reflected on mistakes")

            submit_button = st.form_submit_button("Save Reflection")

            if submit_button:
                reflection_data = {
                    "date": date.strftime("%Y-%m-%d"),
                    "mood": mood,
                    "learned": today_learned,
                    "challenges": challenges,
                    "growth_area": growth_area,
                    "activities": {
                        "read_new": read_new,
                        "practiced": practiced,
                        "feedback": feedback,
                        "challenge": challenge,
                        "helped": helped,
                        "reflected": reflected
                    }
                }
                save_reflection(reflection_data)
                st.success("Reflection saved! Keep growing! 🌱")

    with tab2:
        st.subheader("Growth Progress")
        
        reflections = load_reflections()
        if reflections:
            df = pd.DataFrame(reflections)
            
            # Mood tracking over time
            fig_mood = px.line(df, x="date", y="mood", title="Mood Progress Over Time")
            st.plotly_chart(fig_mood)

            # Activities completion
            activities_data = pd.DataFrame([r["activities"] for r in reflections])
            activities_sum = activities_data.sum()
            fig_activities = px.bar(activities_sum, title="Completed Growth Activities")
            st.plotly_chart(fig_activities)
        else:
            st.info("Start logging your reflections to see your progress!")

    with tab3:
        st.subheader("Previous Reflections")
        reflections = load_reflections()
        if reflections:
            for reflection in reversed(reflections):
                with st.expander(f"Reflection from {reflection['date']}"):
                    st.write(f"**Mood:** {reflection['mood']}/10")
                    st.write(f"**Learned:** {reflection['learned']}")
                    st.write(f"**Challenges:** {reflection['challenges']}")
                    st.write(f"**Growth Areas:** {reflection['growth_area']}")
                    
                    st.write("**Completed Activities:**")
                    activities = reflection['activities']
                    for activity, done in activities.items():
                        st.write(f"- {activity.replace('_', ' ').title()}: {'✅' if done else '❌'}")
        else:
            st.info("No previous reflections found.")

if __name__ == "__main__":
    main() 