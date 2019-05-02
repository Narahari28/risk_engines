Narahari Bharawdwaj
Supervised learning and Reinforcement Learning Agents for the Game of Risk

Supervised learning Java framework built by Yura Mamyrin

Reinforcement learning Python framework built by Surag Nair, inspired by Deepmind's AlphaGo Zero paper

Files modified:

supervised_agent/test_hard_model.py
supervised_agent/hard_model.py
supervised_agent/hard_server.py
supervised_agenthard_request.py (These files are entirely my own and expose the API for the supervised learning agent that can then be queried from the Java Domination environment)

src/src_swing/net/yura/domination/ui/commandline/CommandText.java (Repurposed to simulate games between any two chosen agents)

src/src/net/yura/domination/engine/core/RiskGame.java
src/src/net/yura/domination/engine/ai/AIManager.java (These files were repurposed to write game states and decisions made to files)

src/src/net/yura/domination/engine/ai/AIEmulator.java (Entirely my own, the actual logic for the supervised learning agent)

reinforcement_agent/risk/RiskGame.py
reinforcement_agent/risk/RiskLogic.py
reinforcement_agent/risk/RiskPlayers.py (These files are basically entirely my own and contain the logic for the game of Risk, serving as a game API)

reinforcement_agent/risk/pytorch/RiskNNet.py (Contains my neural network architecture)

reinforcement_agent/MCTS.py (Modified significantly from Surag Nair to accommodate MCTS for Risk)

reinforcement_agent/Coach.py
reinforcement_agent/main.py (These files were slightly modified from Surag Nair to train my Risk RL agent)
