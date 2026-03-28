import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random

---------------- TITLE ----------------

st.title("Fake News Spread Modelling")

st.markdown("""
This simulation shows how fake news spreads in a social network using
Believer, Skeptic and Fact-checker model.
""")

---------------- THEORY ----------------

with st.expander("Project Theory"):
st.write("""
S = Skeptic (does not believe fake news)

B = Believer (believes fake news)

F = Fact-checker (stops fake news)

Fake news spreads with probability (beta)
Fact-checking converts believers with probability (gamma)
""")

---------------- USER INPUT ----------------

st.sidebar.header("Simulation Parameters")

N = st.sidebar.number_input("Number of Users", 10, 500, 100)
prob = st.sidebar.number_input("Connection Probability", 0.0, 1.0, 0.05)
beta = st.sidebar.number_input("Spread Rate (beta)", 0.0, 1.0, 0.4)
gamma = st.sidebar.number_input("Fact-check Rate (gamma)", 0.0, 1.0, 0.2)
time_steps = st.sidebar.number_input("Time Steps", 5, 100, 30)

---------------- BUTTON ----------------

run_simulation = st.sidebar.button("Run Simulation")

---------------- SIMULATION ----------------

if run_simulation:

G = nx.erdos_renyi_graph(N, prob)  

states = {node: 'S' for node in G.nodes()}  

initial_believers = random.sample(list(G.nodes()), min(5, N))  

for node in initial_believers:  
    states[node] = 'B'  

believers = []  
skeptics = []  
fact_checkers = []  

for t in range(time_steps):  

    new_states = states.copy()  

    for node in G.nodes():  

        if states[node] == 'B':  

            for neighbor in G.neighbors(node):  

                if states[neighbor] == 'S' and random.random() < beta:  
                    new_states[neighbor] = 'B'  

            if random.random() < gamma:  
                new_states[node] = 'F'  

    states = new_states  

    believers.append(list(states.values()).count('B'))  
    skeptics.append(list(states.values()).count('S'))  
    fact_checkers.append(list(states.values()).count('F'))  

# ---------------- GRAPH ----------------  

st.subheader("Fake News Spread Graph")  

fig, ax = plt.subplots()  

ax.plot(believers, marker='o', linestyle='-', label="Believers")  
ax.plot(skeptics, marker='s', linestyle='--', label="Skeptics")  
ax.plot(fact_checkers, marker='^', linestyle='-.', label="Fact-checkers")  

ax.set_xlabel("Time Steps")  
ax.set_ylabel("Number of Users")  
ax.set_title("Fake News Spread Modelling")  

ax.legend()  
ax.grid(True)  

st.pyplot(fig)  

# ---------------- FINAL OUTPUT ----------------  

st.subheader("Final Statistics")  

st.write("Believers:", believers[-1])  
st.write("Skeptics:", skeptics[-1])  
st.write("Fact-checkers:", fact_checkers[-1])  

# ---------------- TABLE ----------------  

st.subheader("Detailed Data")  

import pandas as pd  

df = pd.DataFrame({  
    "Time": list(range(time_steps)),  
    "Believers": believers,  
    "Skeptics": skeptics,  
    "Fact-checkers": fact_checkers  
})  

st.dataframe(df)

