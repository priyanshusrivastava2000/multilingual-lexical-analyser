#!/bin/bash

# Kill existing session if it exists
tmux kill-session -t demo 2>/dev/null

# Create new detached session
tmux new-session -d -s demo -n 'tokenise'

# Window 1: Tokenisation example
tmux send-keys -t demo:tokenise 'mll --inspect "if x > 0 then return y end" --source english'

# Window 2: Translation example (with conflict)
tmux new-window -t demo -n 'translate'
tmux send-keys -t demo:translate 'mll --translate "if x > 0 then return y end" --source english --target spanish'

# Window 3: Interactive REPL
tmux new-window -t demo -n 'repl'
tmux send-keys -t demo:repl 'mll'

# Attach to the session
tmux attach -t demo
