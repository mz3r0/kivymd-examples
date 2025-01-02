from kivy.graphics import Color, Rectangle, RoundedRectangle


class LockBehavior:
    def __init__(self, w, enabled=False, radius=None):
        self.widget = w  # Composition over inheritance!
        self.enabled = enabled

        # Draw the semi-transparent overlay
        with w.canvas.after:
            Color(0.8, 0.8, 0.8, 0.5)
            if radius:
                self.overlay = RoundedRectangle(size=w.size, pos=w.pos, radius=radius)
            else:
                self.overlay = Rectangle(size=w.size, pos=w.pos)

        # Bind size and position updates
        w.bind(size=self.update_overlay, pos=self.update_overlay)

    def toggle_enabled(self):
        """ Method to enable or disable the widget. """
        self.enabled = not self.enabled
        self.overlay.opacity = 0 if self.enabled else 0.5  # Hide overlay if enabled

    def update_overlay(self, *args):
        """ Method to toggle the overlay opacity. """
        self.overlay.size = self.widget.size
        self.overlay.pos = self.widget.pos

    # Delegatee touch methods

    def on_touch_down(self, touch):
        if not self.enabled \
                and self.widget.collide_point(*touch.pos) \
                and not touch.is_mouse_scrolling:
            return True  # Block touch events
        return False  # Allow other handlers to process the event

    def on_touch_move(self, touch):
        if not self.enabled and self.widget.collide_point(*touch.pos):
            return True  # Block touch events
        return False  # Allow other handlers to process the event

    def on_touch_up(self, touch):
        if not self.enabled \
                and self.widget.collide_point(*touch.pos) \
                and not touch.is_mouse_scrolling:
            return True  # Block touch events
        return False  # Allow other handlers to process the event

# This behavior is incomplete because in some instances children's
    # on_touch_down is called while the parent's is not.
