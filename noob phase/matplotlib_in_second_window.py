import os
from kivy.lang import Builder


import multiprocessing
import matplotlib.pyplot as plt

KV = '''
MDScreen:
    MDButton:
        pos_hint: {"center_x": .5}
        on_release: app.show_plot()

        MDButtonText:
            text: 'Press me'
'''


def plot_data(data):
    """Subprocess function to generate and display the plot."""
    # Create the plot
    x, y = data
    plt.plot(x, y)
    plt.title("Generated Plot")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.show()


if __name__ == '__main__':
    from kivymd.app import MDApp

    class Example(MDApp):
        def build(self):
            self.screen = Builder.load_string(KV)
            return self.screen

        def show_plot(self):
            x = [1, 2, 3, 4, 5]
            y = [i ** 2 for i in x]
            data = (x, y)
            plot_process = multiprocessing.Process(target=plot_data, args=(data,))
            plot_process.start()

    os.environ["KIVY_NO_WINDOW"] = "1"
    multiprocessing.set_start_method("spawn")
    Example().run()
