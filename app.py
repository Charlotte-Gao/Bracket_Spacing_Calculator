import shiny
from shiny import App, reactive, render, ui
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Define the UI
app_ui = ui.page_fluid(
    ui.panel_title("Bracket Spacing Calculator"),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_numeric("brackets_length", "Length between brackets(meters)", value=14.879),
            ui.input_numeric("offset", "First/End Bracket Offset (mm)", value=200),
            ui.input_numeric("num_brackets", "Number of Brackets", value=19),
            ui.input_action_button("calculate", "Calculate"),
            ui.output_text_verbatim("spacing"),
            ui.output_plot("spacing_plot")
        )
    )
)

# Define the server logic
def server(input, output, session):
   
    @reactive.event(input.calculate)
    def calculate():
        brackets_length = input.brackets_length() * 1000  # Convert to mm
        offset = input.offset()
        num_brackets = input.num_brackets()
        spacing = round(brackets_length/num_brackets)

        # Return the calculated values
        return brackets_length, offset, num_brackets, spacing

    @output
    @render.text
    def spacing():
        brackets_length, offset, num_brackets, spacing = calculate()
        return f"Spacing: {spacing}mm"

   
    @output
    @render.plot
    def spacing_plot():
        brackets_length, offset, num_brackets, spacing = calculate()
        total_length = 2 * offset + brackets_length
        positions = [offset + i * spacing for i in range(num_brackets+1)]

        # Plot the roof-like line
        plt.plot([0, total_length], [0, 0], 'k-', lw=2)

        # Plot the bracket positions

        ## TODO: Postions need to be within the length between brackets.
        plt.plot(positions, [0] * len(positions), 'bo')

        # Annotate total length with an arrow
        plt.annotate(f'Length between brackets: {brackets_length / 1000:.3f} m',
                     xy=(brackets_length / 2, 0), xytext=(brackets_length / 2, 20),
                     arrowprops=dict(facecolor='blue', shrink=0.05),
                     ha='center', fontsize=10, color='blue')

        # Annotate start position of the first bracket with an arrow
        plt.annotate('1st Bracket',
                     xy=(offset, 0), xytext=(offset, 30),
                     arrowprops=dict(facecolor='purple', shrink=0.05),
                     ha='center', fontsize=6, color='purple')

        # Annotate end position of the last bracket with an arrow
        plt.annotate('Last Bracket',
                     xy=(total_length-2*offset, 0), xytext=(total_length-2*offset, 30),
                     arrowprops=dict(facecolor='purple', shrink=0.05),
                     ha='center', fontsize=6, color='purple')

        # Highlight total length with a double-headed arrow
        plt.annotate('', xy=(0, -10), xytext=(total_length, -10),
                     arrowprops=dict(arrowstyle='<->', color='blue', lw=1.5))
        plt.text(total_length / 2, -20, f'Total Length: {total_length:.1f} mm',
                 ha='center', fontsize=6, color='blue')

        # Highlight the offsets at the start and end
        plt.annotate('', xy=(0, -30), xytext=(offset, -30),
                     arrowprops=dict(arrowstyle='<->', color='purple', lw=1.5))
        plt.text(offset / 2, -40, '200 mm', ha='center', fontsize=10, color='purple')

        plt.annotate('', xy=(total_length - 2*offset, -30), xytext=(total_length, -30),
                     arrowprops=dict(arrowstyle='<->', color='purple', lw=1.5))
        plt.text(total_length - offset / 2, -40, '200 mm', ha='center', fontsize=10, color='purple')

        # Configure plot
        plt.xlabel("Position (mm)")
        plt.yticks([])
        plt.ylim(-50, 50)
        plt.title("Bracket Positions with Values")
        plt.grid(True)

app = App(app_ui, server)

# Run the app
if __name__ == "__main__":
    app.run()