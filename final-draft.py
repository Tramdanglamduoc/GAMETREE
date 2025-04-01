# Import Kivy modules for UI 
import kivy
from kivy.app import App # Base class for Kivy
from kivy.uix.button import Button #For buttons
from kivy.uix.textinput import TextInput #For user inputs
from kivy.core.window import Window #(Our case is Window size of the app)
from kivy.uix.label import Label #For displaying the results (the texts)
from kivy.uix.gridlayout import GridLayout #Layout 
from kivy.uix.boxlayout import BoxLayout #Layout cols or rows - look like table
from kivy.core.text import LabelBase #Specify custom fonts
from kivy.clock import Clock # Allows scheduling functions -- Coi lại cái này để ghi lại
import time #To measure execution time of AI moves

LabelBase.register(name="EmojiFont", fn_regular="seguiemj.ttf") #Use seguiemj.ttf - this font to also display the emojies

#window size for the application (width x height)
Window.size = (500, 500)


class TeamGameApp(App): # Main application class - Object-Oriented Programming
    def __init__(self, **kwargs): 
        super().__init__(**kwargs)

        # Initial player and game state variables
        self.score_P1 = 0
        self.score_P2 = 0
        self.bank = 0
        self.current_game_value = None # Current value of the game (the number being multiplied)
        self.current_player = 1 # Indicates whose turn it is (1 = player, 2 = AI)
        self.use_alpha_beta = True # Determine whether to use Alpha-Beta pruning or plain Minimax

        #AI search statistics
                 # Nodes in best path (AI only)
                 
        self.total_nodes_explored = 0        # Total number of nodes evaluated by the AI (AI only)
             # Temporary counter
        self.alpha_cuts = 0                 # ALL alpha cuts (both turns) - for both sides
        self.beta_cuts = 0                  # ALL beta cuts (both turns) - for both sides
        

    # Apply game-specific rules based on the current game value and whose turn it is
    def apply_rules(self, current_game_value, player, score_p1, score_p2, bank):

        # Rule 1: If the multiplication result is even, the current player loses 1 point
        if current_game_value % 2 == 0:
            if player == 1:
                score_p1 -= 1
            else:
                score_p2 -= 1
        
        # Rule 2: If the multiplication result is odd, the current player gains 1 point
        else:
            if player == 1:
                score_p1 += 1
            else:
                score_p2 += 1

        # Rule 3: If the multiplication result ends in 0 or 5, 1 point is added to the bank
        if current_game_value % 10 == 0 or current_game_value % 10 == 5:
            bank += 1

        # Return the updated scores and bank value
        return score_p1, score_p2, bank 
    



    # Evaluate the game state to return a score from AI's perspective -- Khúc này bắt đầu không hiểu lắm rồi á
    def evaluate(self, current_game_value, score_p1, score_p2, bank, is_ia_turn):
        # If the game ends (the condition a number greater than or equal to 1200 is reached), consider bank points depending on who finishes
        if current_game_value >= 1200:
            return score_p2 + bank - score_p1 if is_ia_turn else score_p2 - (score_p1 + bank)
        
        # Otherwise, return simple difference in scores
        return score_p2 - score_p1


    # Minimax algorithm 
    def minimax_no_ab(self, current_game_value, score_p1, score_p2, bank, depth, maximizing):
        #Count total nodes explored only when it's AI's actual turn
        if self.current_player == 2: 
            self.total_nodes_explored += 1
            
        # Base case: if game is over or depth limit reached, return evaluation function - above
        if current_game_value >= 1200 or depth == 0:
            return self.evaluate(current_game_value, score_p1, score_p2, bank, maximizing)


        if maximizing:
            max_eval = float('-inf')
            for move in self.get_valid_moves():
                new_val = current_game_value * move
                p1, p2, b = self.apply_rules(new_val, 2, score_p1, score_p2, bank)
                eval = self.minimax_no_ab(new_val, p1, p2, b, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_valid_moves():
                new_val = current_game_value * move
                p1, p2, b = self.apply_rules(new_val, 1, score_p1, score_p2, bank)
                eval = self.minimax_no_ab(new_val, p1, p2, b, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

    def minimax(self, current_game_value, score_p1, score_p2, bank, depth, alpha, beta, maximizing):
        # Only count nodes during AI's turn
        if self.current_player == 2:
            self.total_nodes_explored += 1
            

        if current_game_value >= 1200 or depth == 0:
            return self.evaluate(current_game_value, score_p1, score_p2, bank, maximizing)

        if maximizing:
            max_eval = float('-inf')
            for move in self.get_valid_moves():
                new_val = current_game_value * move
                p1, p2, b = self.apply_rules(new_val, 2, score_p1, score_p2, bank)
                eval = self.minimax(new_val, p1, p2, b, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)

                if beta <= alpha:
                    self.alpha_cuts += 1  # Always count alpha cuts
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_valid_moves():
                new_val = current_game_value * move
                p1, p2, b = self.apply_rules(new_val, 1, score_p1, score_p2, bank)
                eval = self.minimax(new_val, p1, p2, b, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)

                if beta <= alpha:
                    self.beta_cuts += 1  # Always count beta cuts
                    break
            return min_eval

    def get_valid_moves(self):
        return [2, 3, 4]

    def ai_move(self):
        
        
        # Don't reset alpha/beta cuts here!

        best_score = float('-inf')
        best_move = None
        move_time = 0

        for move in self.get_valid_moves():
            new_val = self.current_game_value * move
            p1, p2, b = self.apply_rules(new_val, 2, self.score_P1, self.score_P2, self.bank)

            
            start = time.perf_counter()

            if self.use_alpha_beta:
                eval_score = self.minimax(new_val, p1, p2, b, 5, float('-inf'), float('inf'), False)
            else:
                eval_score = self.minimax_no_ab(new_val, p1, p2, b, 5, False)

            end = time.perf_counter()
            duration = end - start

            if eval_score > best_score:
                best_score = eval_score
                best_move = move
                
                move_time = duration

        return best_move, move_time

    def play_turn(self, multiplier):
        self.current_game_value *= multiplier
        self.score_P1, self.score_P2, self.bank = self.apply_rules(
            self.current_game_value, self.current_player, self.score_P1, self.score_P2, self.bank
        )

        if self.current_game_value >= 1200:
            if self.current_player == 1:
                self.score_P1 += self.bank
            else:
                self.score_P2 += self.bank
            return True
        self.current_player = 2 if self.current_player == 1 else 1
        return False

    def build(self):
        self.window = GridLayout(cols=1, padding=10, spacing=10)

        self.greetings = Label(
            text="🎮 Welcome!\nChoose algorithm then who starts.",
            font_size=18, font_name="EmojiFont",
            halign="center", valign="middle",
            size_hint=(1, 1), text_size=(Window.width * 0.9, None))
        
        self.initial_text_input = TextInput(text="", font_size=20, size_hint_y=None, height=50, multiline=False)

        self.algorithm_choice_buttons = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        self.minimax_button = Button(text="🧠 Minimax", font_name="EmojiFont")
        self.alpha_beta_button = Button(text="⚡ Alpha-Beta", font_name="EmojiFont")
        self.minimax_button.bind(on_press=self.choose_minimax)
        self.alpha_beta_button.bind(on_press=self.choose_alpha_beta)
        self.algorithm_choice_buttons.add_widget(self.minimax_button)
        self.algorithm_choice_buttons.add_widget(self.alpha_beta_button)

        self.player_choice_buttons = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        self.human_start_button = Button(text="🙋 You Start", font_name="EmojiFont")
        self.ai_start_button = Button(text="🤖 AI Starts", font_name="EmojiFont")
        self.human_start_button.bind(on_press=self.choose_human_start)
        self.ai_start_button.bind(on_press=self.choose_ai_start)
        self.player_choice_buttons.add_widget(self.human_start_button)
        self.player_choice_buttons.add_widget(self.ai_start_button)

        self.multiplier_buttons = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        self.multiplier_widgets = []
        for i in [2, 3, 4]:
            btn = Button(text=f"×{i}", font_size=20)
            btn.bind(on_press=self.on_multiplier_chosen)
            btn.disabled = True
            self.multiplier_buttons.add_widget(btn)
            self.multiplier_widgets.append(btn)

        self.retry_button = Button(text="🔄 Retry", size_hint_y=None, height=50, font_name="EmojiFont")
        self.retry_button.bind(on_press=self.reset_game)
        self.retry_button.opacity = 0
        self.retry_button.disabled = True

        self.window.add_widget(self.greetings)
        self.window.add_widget(self.initial_text_input)
        self.window.add_widget(self.algorithm_choice_buttons)
        self.window.add_widget(self.player_choice_buttons)
        self.window.add_widget(self.retry_button)
        self.window.add_widget(self.multiplier_buttons)

        return self.window

    def choose_minimax(self, instance):
        self.use_alpha_beta = False
        self.greetings.text = "ℹ️ Minimax selected. Choose who starts."

    def choose_alpha_beta(self, instance):
        self.use_alpha_beta = True
        self.greetings.text = "ℹ️ Alpha-Beta selected. Choose who starts."

    def choose_human_start(self, instance):
        self.current_player = 1
        self.start_game()

    def choose_ai_start(self, instance):
        self.current_player = 2
        self.start_game()

    def start_game(self):
        try:
            value = int(self.initial_text_input.text.strip())
            if 8 <= value <= 18:
                self.current_game_value = value
                self.player_choice_buttons.opacity = 0
                self.player_choice_buttons.disabled = True
                self.algorithm_choice_buttons.opacity = 0
                self.algorithm_choice_buttons.disabled = True

                if self.current_player == 1:
                    self.greetings.text = f"✔️ Starting with {value}. Your turn!"
                    for btn in self.multiplier_widgets:
                        btn.disabled = False
                else:
                    self.greetings.text = f"✔️ Starting with {value}. AI is thinking..."
                    Clock.schedule_once(lambda dt: self.ai_starts_playing(), 1)
            else:
                self.greetings.text = "❌ Enter a number between 8 and 18."
        except ValueError:
            self.greetings.text = "❌ Invalid input."

    def ai_starts_playing(self):
        ai_multiplier, move_time = self.ai_move()
        game_over = self.play_turn(ai_multiplier)

        msg = f"🤖 AI chose ×{ai_multiplier} → {self.current_game_value}\n" \
            f"⏱ Thinking Time: {move_time:.4f} sec\n" \
            f"P1: {self.score_P1}, P2: {self.score_P2}, Bank: {self.bank}"

        if game_over:
            msg += f"\n🏁 Game Over!\n{self.get_winner_message()}"
            self.greetings.text = msg
            self.disable_buttons()
        else:
            self.greetings.text = msg + "\nYour turn!"
            for btn in self.multiplier_widgets:
                btn.disabled = False

        self.retry_button.opacity = 1
        self.retry_button.disabled = False

    def on_multiplier_chosen(self, instance):
        try:
            multiplier = int(instance.text.replace("×", ""))
            game_over = self.play_turn(multiplier)
            msg = f"You chose ×{multiplier} → {self.current_game_value}\n"\
                    f"P1: {self.score_P1} (Your Score), P2: {self.score_P2} (AI Score), Bank: {self.bank}\n"\
                    f"\n---------------------------------------------------------------\n"

            if game_over:
                msg += f"\n🏁 Game Over!\n{self.get_winner_message()}"
                self.greetings.text = msg
                self.disable_buttons()
                return

            ai_multiplier, move_time = self.ai_move()
            game_over = self.play_turn(ai_multiplier)

            msg += f"\n🤖 AI chose ×{ai_multiplier} → {self.current_game_value}\n" \
                    f"⏱ Thinking Time: {move_time:.4f} sec\n" \
                    f"P1: {self.score_P1} (Your Score), P2: {self.score_P2} (AI Score), Bank: {self.bank}\n" \
                    f"\n---------------------------------------------------------------\n"

            if game_over:
                msg += f"\n🏁 Game Over!\n{self.get_winner_message()}"
                self.greetings.text = msg
                self.disable_buttons()
            else:
                self.greetings.text = msg + "\nYour turn!"

            self.retry_button.opacity = 1
            self.retry_button.disabled = False

        except Exception as e:
            self.greetings.text = f"⚠️ Error: {e}"

    def get_winner_message(self):
        if self.score_P1 > self.score_P2:
            winner = "🎉 You win!"
        elif self.score_P2 > self.score_P1:
            winner = "🤖 AI wins!"
        else:
            winner = "🤝 It's a tie!"

        stats = f"\n\n---------------------------------------------------------------\n" \
                f"\n📊 Stats:" \
                 \
                f"\n• Total Nodes Explored: {self.total_nodes_explored}"

        if self.use_alpha_beta:
            stats += f"\n• Alpha Cuts: {self.alpha_cuts}" \
                     f"\n• Beta Cuts: {self.beta_cuts}"

        return f"{winner}{stats}"

    def disable_buttons(self):
        for btn in self.multiplier_widgets:
            btn.disabled = True

    def reset_game(self, instance):
        self.score_P1 = 0
        self.score_P2 = 0
        self.bank = 0
        self.current_game_value = None
        self.current_player = 1
        
        self.total_nodes_explored = 0
        self.alpha_cuts = 0
        self.beta_cuts = 0

        self.greetings.text = "🎮 Welcome!\nChoose algorithm then who starts."
        self.initial_text_input.text = ""
        for btn in self.multiplier_widgets:
            btn.disabled = True

        self.retry_button.opacity = 0
        self.retry_button.disabled = True
        self.player_choice_buttons.opacity = 1
        self.player_choice_buttons.disabled = False
        self.algorithm_choice_buttons.opacity = 1
        self.algorithm_choice_buttons.disabled = False

if __name__ == "__main__":
    Game = TeamGameApp()
    Game.run()