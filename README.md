How to Use the Program
Follow these steps to run the NFA converter:

1. Run the Script
Open your terminal or command prompt and run the file using: python main.py

2. Enter the NFA Components
When the program starts, it will ask you to input the following:

States: Enter all states separated by a space (e.g., q0 q1 q2).

Alphabet: Enter the input symbols (e.g., 0 1). Note: You don't need to enter 'e' or 'epsilon' here.

Start State: Type the name of the initial state (e.g., q0).

Final States: Enter the original final states (e.g., q2).

3. Define Transitions
The program will ask for transitions one by one. Use the format: SourceState Symbol DestinationState

For Epsilon: Use the letter e as the symbol (e.g., q0 e q1).

For Regular Symbols: Use the symbols from your alphabet (e.g., q1 0 q2).

To Finish: Type done when you have entered all transitions.

4. View the Output
The program will automatically process the data and display:

Epsilon Closures: A list showing which states are reachable via epsilon for every state.

New Transition Table: The final NFA table without any epsilon transitions.

New Final States: The updated list of final states for the new NFA.
Team:
BOUFROUKH DJEMANA
GADDA MAYA LINA
BENZID OUMEIMA
