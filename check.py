import kivy
from kivy.app import App
from kivy.graphics import Rectangle, Color
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

Window.size = (400, 500)

class TeamGameApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.score_P1 = 0
        self.score_P2 = 0
        self.bank = 0
        self.current_game_value = None
        self.current_player = 1

    def apply_rules(self, current_game_value, player, score_p1, score_p2, bank):
        if current_game_value % 2 == 0:
            if player == 1:
                score_p1 -= 1
            else:
                score_p2 -= 1
        else:
            if player == 1:
                score_p1 += 1
            else:
                score_p2 += 1

        if current_game_value % 10 == 0 or current_game_value % 10 == 5:
            bank += 1

        return score_p1, score_p2, bank

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
            return True  # Game over

        self.current_player = 2 if self.current_player == 1 else 1
        return False  # Game continues

    def get_valid_moves(self):
        return [2, 3, 4]

    def evaluate(self, current_game_value, score_p1, score_p2, bank, is_ia_turn):
        if current_game_value >= 1200:
            if is_ia_turn:
                return score_p2 + bank - score_p1
            else:
                return score_p2 - (score_p1 + bank)
        return score_p2 - score_p1

    def minimax(self, current_game_value, score_p1, score_p2, bank, depth, alpha, beta, maximizing):
        if current_game_value >= 1200 or depth == 0:
            return self.evaluate(current_game_value, score_p1, score_p2, bank, maximizing)

        if maximizing:
            max_eval = float('-inf')
            for move in self.get_valid_moves():
                new_game_value = current_game_value * move
                new_score_p1, new_score_p2, new_bank = self.apply_rules(new_game_value, 2, score_p1, score_p2, bank)
                eval = self.minimax(new_game_value, new_score_p1, new_score_p2, new_bank, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_valid_moves():
                new_game_value = current_game_value * move
                new_score_p1, new_score_p2, new_bank = self.apply_rules(new_game_value, 1, score_p1, score_p2, bank)
                eval = self.minimax(new_game_value, new_score_p1, new_score_p2, new_bank, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def ai_move(self):
        best_move = None
        best_score = float('-inf')

        for move in self.get_valid_moves():
            new_game_value = self.current_game_value * move
            new_score_P1, new_score_P2, new_bank = self.apply_rules(new_game_value, 2, self.score_P1, self.score_P2, self.bank)
            eval_score = self.minimax(new_game_value, new_score_P1, new_score_P2, new_bank, 5, float('-inf'), float('inf'), False)

            if eval_score > best_score:
                best_score = eval_score
                best_move = move

        return best_move

    def build(self):
        self.window = GridLayout(cols=1, padding=10, spacing=10)

        self.greetings = Label(text="🎮 Welcome to Team Game!\nEnter starting value (8–18):", font_size=18)
        self.initial_text_input = TextInput(text="", font_size=20, size_hint_y=None, height=50, multiline=False)

        self.enter_button = Button(text="Start Game", size_hint_y=None, height=50)
        self.enter_button.bind(on_press=self.set_initial_value)

        self.window.add_widget(self.greetings)
        self.window.add_widget(self.initial_text_input)
        self.window.add_widget(self.enter_button)

        self.multiplier_buttons = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        self.multiplier_widgets = []
        for i in [2, 3, 4]:
            btn = Button(text=f"×{i}", font_size=20)
            btn.bind(on_press=self.on_multiplier_chosen)
            btn.disabled = True  # Ban đầu tắt
            self.multiplier_buttons.add_widget(btn)
            self.multiplier_widgets.append(btn)

        self.window.add_widget(self.multiplier_buttons)

        return self.window

    def set_initial_value(self, instance):
        try:
            value = int(self.initial_text_input.text.strip())
            if 8 <= value <= 18:
                self.current_game_value = value
                self.greetings.text = f"✔️ Game starts with value {value}.\nNow it's Player 1's turn!"
                for btn in self.multiplier_widgets:
                    btn.disabled = False
            else:
                self.greetings.text = "❌ Please enter a number between 8 and 18."
        except ValueError:
            self.greetings.text = "❌ Invalid input. Please enter a number."

    def on_multiplier_chosen(self, instance):
        if self.current_game_value is None:
            self.greetings.text = "⚠️ Please start the game first."
            return

        try:
            multiplier = int(instance.text.replace("×", ""))
            game_over = self.play_turn(multiplier)  # Player 1's move
            msg = f"🔹 P1 chose ×{multiplier} → Value: {self.current_game_value}\nScores – P1: {self.score_P1} | P2: {self.score_P2} | Bank: {self.bank}"

            if game_over:
                msg += "\n🏁 Game Over!"
                self.greetings.text = msg
                self.disable_buttons()
                return

            # AI move
            ai_multiplier = self.ai_move()
            game_over = self.play_turn(ai_multiplier)
            msg += f"\n🤖 AI chose ×{ai_multiplier} → Value: {self.current_game_value}\nScores – P1: {self.score_P1} | P2: {self.score_P2} | Bank: {self.bank}"

            if game_over:
                msg += "\n🏁 Game Over!"
                self.disable_buttons()

            self.greetings.text = msg
        except Exception as e:
            self.greetings.text = f"⚠️ Error: {e}"

    def disable_buttons(self):
        for btn in self.multiplier_widgets:
            btn.disabled = True

# Run the app
if __name__ == "__main__":
    TeamGameApp().run()
