class CustomKeyHandler:
    def __init__(self):
        self.pressed = {}         # Отслеживание удержания клавиш
        self.pressed_once = set()  # Для одиночных нажатий
        self.released = set()      # Для клавиш, которые только что отпустили

    def on_key_press(self, symbol, modifiers):
        """Вызывается при нажатии клавиши."""
        if not self.pressed.get(symbol, False):
            self.pressed_once.add(symbol)
        self.pressed[symbol] = True
        self.released.discard(symbol)

    def on_key_release(self, symbol, modifiers):
        """Вызывается при отпускании клавиши."""
        self.released.add(symbol)
        self.pressed[symbol] = False
        self.pressed_once.discard(symbol)

    def is_pressed(self, symbol):
        """Проверяет, удерживается ли клавиша."""
        return self.pressed.get(symbol, False)

    def is_pressed_once(self, symbol):
        """Проверяет, была ли клавиша нажата один раз, и убирает ее из набора."""
        if symbol in self.pressed_once:
            self.pressed_once.remove(symbol)
            return True
        return False

    def is_released(self, symbol):
        """Проверяет, была ли клавиша только что отпущена, и убирает ее из набора."""
        if symbol in self.released:
            self.released.remove(symbol)
            return True
        return False
