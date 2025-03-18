import sys
from collections import defaultdict
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, 
    QLineEdit, QTabWidget, QHBoxLayout, QStackedWidget, QSizePolicy, 
    QScrollArea, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QTextEdit, QComboBox, QAbstractItemView
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QIcon
from Graph import read_graph_from_files, Graph
from Modified_BDA import k_shortest_paths
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from Output import draw_graph_with_path, draw_full_graph
from Diversity_Metric_Test import test_diversity_metrics

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MBDA Diverse Pathfinder")
        self.setFixedSize(1366, 768)
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Welcome Section
        self.welcome_widget = self.create_welcome_widget()
        self.stacked_widget.addWidget(self.welcome_widget)

        # Graph Selection Section
        self.graph_selection_widget = self.create_graph_selection_widget()
        self.stacked_widget.addWidget(self.graph_selection_widget)

        # Input Selection Section
        self.input_selection_widget = self.create_input_selection_widget()
        self.stacked_widget.addWidget(self.input_selection_widget)

        # Output Section with Tab Widget
        self.output_widget = self.create_output_widget()
        self.stacked_widget.addWidget(self.output_widget)

        # Initialize graph and position variables
        self.graph = None
        self.pos = {}

        # Initialize input fields for graph and coordinates
        self.graph_input = QLineEdit()  # For graph file path
        self.coord_input = QLineEdit()   # For coordinates file path

    def create_welcome_widget(self):
        # Create the main layout as an HBoxLayout (to have left and right sections)
        main_layout = QHBoxLayout()

        # Create the welcome layout (left side)
        welcome_layout = QVBoxLayout()
        welcome_label = QLabel("<font color='#0E4751'>MBDA</font> Diverse <br>Pathfinder")
        welcome_label.setAlignment(Qt.AlignLeft)  # Align text to the left
        welcome_label.setStyleSheet("font-size: 70px; font-weight: bold")  # Increase font size, make it bold
        welcome_layout.addWidget(welcome_label, alignment=Qt.AlignTop | Qt.AlignLeft)  # Add alignment for spacing
        welcome_layout.setContentsMargins(60, 125, 60, 60)  # Set larger margins for more space between text and window edge

        # Add the new text below the welcome label
        description_label = QLabel("\n            The K-shortest pathfinding tool that offers diverse and efficient \nroute options for pedestrian navigation, ensuring variety and flexibility \nin selecting the best paths through urban environments using Modified \nBidirectional Dijkstra's Algorithm.")
        description_label.setAlignment(Qt.AlignJustify)  # Align text to the left
        description_label.setStyleSheet("font-size: 20px;")  # Set font size for the description
        welcome_layout.addWidget(description_label, alignment=Qt.AlignTop | Qt.AlignLeft)  # Add the description label

        # Proceed button
        proceed_button = QPushButton("Start")
        proceed_button.clicked.connect(self.show_graph_selection)
        proceed_button.setStyleSheet("font-size: 20px; margin-bottom: 20px; background-color: #0E4751; font-weight: bold;")  # Changed button color
        proceed_button.setFixedWidth(150)
        proceed_button.setMinimumHeight(75)
        proceed_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Allow the button to expand
        welcome_layout.addWidget(proceed_button, alignment=Qt.AlignTop | Qt.AlignLeft)  # Align the button to the top left

        # Create a label for the image (right side)
        image_label = QLabel()
        image_label.setPixmap(QPixmap("Resources/GUI_img.png").scaled(500, 500, Qt.KeepAspectRatio))  # Adjust path and size
        image_label.setAlignment(Qt.AlignRight)  # Align the image to the right

        # Create a vertical layout for the right side to center the image
        right_layout = QVBoxLayout()
        right_layout.addStretch()  # Add stretchable space before the image
        right_layout.addWidget(image_label, alignment=Qt.AlignRight)  # Add the image label to the layout
        right_layout.addStretch()  # Add stretchable space after the image
        right_layout.setContentsMargins(0, 0, 70, 0)  # Add 20 pixels of padding to the right

        # Add welcome_layout (left) and right_layout (with image) to the main layout
        main_layout.addLayout(welcome_layout)  # Add the welcome layout to the left
        main_layout.addLayout(right_layout)  # Add the right layout to the right

        # Create the main widget with the main_layout
        welcome_widget = QWidget()
        welcome_widget.setLayout(main_layout)
        return welcome_widget

    def show_graph_selection(self):
        # Switch to the graph selection section
        self.stacked_widget.setCurrentWidget(self.graph_selection_widget)

    def create_graph_selection_widget(self):
        # Create the main vertical layout
        main_layout = QVBoxLayout()
        
        # Create and style the heading
        layout_label = QLabel("Choose your location")
        layout_label.setAlignment(Qt.AlignCenter)
        layout_label.setStyleSheet("font-size: 40px; font-weight: bold; text-align: center;")
        layout_label.setContentsMargins(0, 20, 0, 20)  # Add some vertical spacing
        main_layout.addWidget(layout_label)

        # Create horizontal layout for buttons
        button_layout = QHBoxLayout()
        
        # MOA button (existing code)
        moa_button = QPushButton()
        moa_button.setFixedSize(600, 400)
        moa_button.setStyleSheet("text-align: center;")
        
        # Create a vertical layout for the MOA button
        moa_layout = QVBoxLayout(moa_button)
        icon_label = QLabel()
        icon_label.setPixmap(QIcon("Resources/moa-bg.png").pixmap(QSize(550, 350)))
        icon_label.setAlignment(Qt.AlignCenter)
        moa_layout.addWidget(icon_label)
        
        text_label = QLabel("MOA Complex")
        text_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        text_label.setAlignment(Qt.AlignCenter)
        moa_layout.addWidget(text_label)
        
        moa_button.clicked.connect(self.load_moa_graph)
        button_layout.addWidget(moa_button)

        # Araneta button (existing code)
        araneta_button = QPushButton()
        araneta_button.setFixedSize(600, 400)
        araneta_button.setStyleSheet("text-align: center;")
        
        araneta_layout = QVBoxLayout(araneta_button)
        araneta_icon_label = QLabel()
        araneta_icon_label.setPixmap(QIcon("Resources/araneta-bg.png").pixmap(QSize(550, 350)))
        araneta_icon_label.setAlignment(Qt.AlignCenter)
        araneta_layout.addWidget(araneta_icon_label)
        
        araneta_text_label = QLabel("Araneta City")
        araneta_text_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        araneta_text_label.setAlignment(Qt.AlignCenter)
        araneta_layout.addWidget(araneta_text_label)
        
        araneta_button.clicked.connect(self.load_araneta_graph)
        button_layout.addWidget(araneta_button)

        # Add button layout to main layout
        main_layout.addLayout(button_layout)

        # Create the widget
        graph_selection_widget = QWidget()
        graph_selection_widget.setLayout(main_layout)
        return graph_selection_widget

    def load_moa_graph(self):
        # Load MOA graph and coordinates
        self.graph_input.setText("Graphs/moa-graph1.txt")
        self.coord_input.setText("Graphs/moa-coordinates1.txt")
        self.read_graph_from_files()  # Ensure the graph is loaded
        self.display_graph("Resources/moa-bg.png")  # Pass the background image for MOA graph
        self.populate_node_dropdowns()  # Populate dropdowns with nodes
        self.show_input_selection()  # Navigate to input selection after loading

    def load_araneta_graph(self):
        # Load Araneta graph and coordinates
        self.graph_input.setText("Graphs/araneta-graph1.txt")
        self.coord_input.setText("Graphs/araneta-coordinates1.txt")
        self.read_graph_from_files()  # Ensure the graph is loaded
        self.display_graph("Resources/araneta-bg.png")  # Pass the background image for Araneta graph
        self.populate_node_dropdowns()  # Populate dropdowns with nodes
        self.show_input_selection()  # Navigate to input selection after loading

    def populate_node_dropdowns(self):
        # Clear existing items in the dropdowns
        self.start_node_input.clear()
        self.end_node_input.clear()

        # Populate the dropdowns with nodes from the graph
        if self.graph is not None:
            nodes = sorted(list(self.graph.nodes))  # Sort the list of nodes alphabetically
            self.start_node_input.addItems(nodes)  # Add nodes to the start node dropdown
            self.end_node_input.addItems(nodes)    # Add nodes to the end node dropdown

    def display_graph(self, background_image):
        # Draw the entire graph and get the figure
        graph_image = draw_full_graph(self.graph, self.pos, background_image)  # Call the function to draw the full graph
        
        # Create a FigureCanvas from the figure
        canvas = FigureCanvas(graph_image)
        canvas.setFixedSize(1000, 600)  # Set a fixed size for the canvas

        # Clear any previous graph display
        if hasattr(self, 'graph_canvas'):
            self.graph_display.layout().removeWidget(self.graph_canvas)
            self.graph_canvas.deleteLater()  # Remove the previous canvas

        # Add the new canvas to the graph display area
        self.graph_display.layout().addWidget(canvas)
        self.graph_canvas = canvas  # Store a reference to the canvas for later removal

    def create_input_selection_widget(self):
        # Create the input selection layout
        input_layout = QVBoxLayout()
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(5)

        # Create a widget for the graph display
        self.graph_display = QWidget()
        self.graph_display.setLayout(QVBoxLayout())
        self.graph_display.layout().setContentsMargins(50, 50, 50, 50)
        self.graph_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Add the back button to the layout first to position it at the top
        back_button = QPushButton("Back")
        back_button.setStyleSheet("font-size: 16px; height: 30px;")
        back_button.setFixedWidth(100)
        back_button.clicked.connect(self.show_graph_selection)
        input_layout.addWidget(back_button, alignment=Qt.AlignLeft)

        # Add the graph display widget
        input_layout.addWidget(self.graph_display, alignment=Qt.AlignCenter | Qt.AlignTop)

        # Create a horizontal layout for the input fields
        input_fields_layout = QHBoxLayout()

        # Start Node Dropdown
        self.start_node_input = QComboBox()
        self.start_node_input.setStyleSheet("font-size: 16px; height: 30px;")
        self.start_node_input.setFixedWidth(300)

        # End Node Dropdown
        self.end_node_input = QComboBox()
        self.end_node_input.setStyleSheet("font-size: 16px; height: 30px;")
        self.end_node_input.setFixedWidth(300)

        # K Value Dropdown (1-10)
        self.k_value_input = QComboBox()
        self.k_value_input.setStyleSheet("font-size: 16px; height: 30px;")
        self.k_value_input.setFixedWidth(300)

                # Create vertical layouts for each input group
        start_node_group = QVBoxLayout()
        end_node_group = QVBoxLayout()
        k_value_group = QVBoxLayout()

        # Create labels
        start_label = QLabel("Starting Location:")
        start_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        end_label = QLabel("Target Location:")
        end_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        k_label = QLabel("Number of Routes:")
        k_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        # Populate the k_value_input with values from 1 to 10
        self.k_value_input.addItems([str(i) for i in range(1, 11)])

        # Add labels and dropdowns to their respective groups
        start_node_group.addWidget(start_label)
        start_node_group.addWidget(self.start_node_input)
        
        end_node_group.addWidget(end_label)
        end_node_group.addWidget(self.end_node_input)
        
        k_value_group.addWidget(k_label)
        k_value_group.addWidget(self.k_value_input)

        # Add the groups to the input fields layout
        input_fields_layout.addLayout(start_node_group)
        input_fields_layout.addLayout(end_node_group)
        input_fields_layout.addLayout(k_value_group)

        # Add the input fields layout to the main layout
        input_layout.addLayout(input_fields_layout)

        # Find Paths Button
        find_paths_button = QPushButton("Find K-Shortest Paths")
        find_paths_button.setStyleSheet("font-size: 16px; height: 30px; background-color: #0E4751; font-weight: bold;")
        find_paths_button.setFixedWidth(300)
        find_paths_button.clicked.connect(self.process_k_shortest_paths)

        # Add the button below the input fields
        input_layout.addWidget(find_paths_button, alignment=Qt.AlignTop | Qt.AlignCenter)

        input_widget = QWidget()
        input_widget.setLayout(input_layout)
        return input_widget

    def create_output_widget(self):
        # Create the output layout with a tab widget
        output_layout = QVBoxLayout()
        self.tabs = QTabWidget()

        # Create a back button
        back_button = QPushButton("Back")
        back_button.setStyleSheet("font-size: 16px; margin-bottom: 10px;")
        back_button.clicked.connect(self.show_input_selection)

        # Tab 1: Path and Graph
        self.path_widget = QWidget()
        self.path_layout = QVBoxLayout()

        # Create a scroll area for Tab 1
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_content = QWidget()
        self.scroll_area_layout = QVBoxLayout(self.scroll_area_content)
        self.scroll_area.setWidget(self.scroll_area_content)
        self.path_layout.addWidget(self.scroll_area)
        self.path_widget.setLayout(self.path_layout)
        self.tabs.addTab(self.path_widget, "Paths and Graph")

        # Tab 2: Diversity Metrics
        self.diversity_table = QTableWidget()
        self.diversity_table.setColumnCount(5)
        self.diversity_table.setHorizontalHeaderLabels([
            "Paths Compared", 
            "Distance Absolute Difference", 
            "Travel Time Absolute Difference",
            "Detour Factor",
            "Path Overlap"
        ])
        self.diversity_table.horizontalHeader().setStretchLastSection(True)
        self.diversity_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.diversity_table.verticalHeader().setVisible(False)
        self.diversity_table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Set to read-only

        # Create a layout for Tab 2
        tab2_layout = QVBoxLayout()
        
        # Legend button for Tab 2
        legend_button_tab2 = QPushButton("Diversity metrics")
        legend_button_tab2.setFixedWidth(100)
        legend_button_tab2.clicked.connect(lambda: self.show_legend("Diversity Metrics", 
            "<span style='font-size:18px; font-weight:bold;'>Important Note!</span><br>"
            "<span style='font-size:14px;'>    The Diversity Metrics are not available in single path searches as it is obtained by comparing the alternative paths to the shortest path.</span><br><br>"
            "<span style='font-size:20px; font-weight:bold;'>Absolute Difference</span><br>"
            "<span style='font-size:14px;'>    Measures the difference between two paths for both the distance and the travel time.</span><br><br>"
            "<span style='font-size:20px; font-weight:bold;'>Path Overlap</span><br>"
            "<span style='font-size:14px;'>    Measures the degree to which different k-shortest paths discovered by the search algorithm share the same edges in the graph.</span><br><br>"
            "<span style='font-size:20px; font-weight:bold;'>Detour Factor</span><br>"
            "<span style='font-size:14px;'>    Measures the trade-off between finding the shortest paths and achieving path diversity.</span><br>"))

        # Add the legend button to Tab 2 layout
        tab2_layout.addWidget(legend_button_tab2, alignment=Qt.AlignRight)
        tab2_layout.addWidget(self.diversity_table)  # Add the diversity table to Tab 2 layout

        # Set the layout for Tab 2
        tab2_widget = QWidget()
        tab2_widget.setLayout(tab2_layout)
        self.tabs.addTab(tab2_widget, "Diversity Metrics")

        # Tab 3: Average Metrics
        self.average_metrics_table = QTableWidget()
        self.average_metrics_table.setColumnCount(5)
        self.average_metrics_table.setHorizontalHeaderLabels([
            "Path", 
            "Avg Cost Absolute Difference", 
            "Avg Travel Time Absolute Difference",
            "Avg Detour Factor",
            "Avg Path Overlap"
        ])
        self.average_metrics_table.horizontalHeader().setStretchLastSection(True)
        self.average_metrics_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)  # Resize columns to fit content
        self.average_metrics_table.verticalHeader().setVisible(False)
        self.average_metrics_table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Set to read-only
        self.average_metrics_table.setFixedHeight(200)
        self.average_metrics_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Create a layout for Tab 3
        tab3_layout = QVBoxLayout()
        
        # Create a label for the narrative
        self.narrative_label = QLabel()  # Create a narrative label
        self.narrative_label.setStyleSheet("font-size: 16px; margin-top: 10px;")  # Optional styling
        
        # Create a scroll area for Tab 3
        self.tab3_scroll_area = QScrollArea()
        self.tab3_scroll_area.setWidgetResizable(True)
        tab3_content = QWidget()
        tab3_content_layout = QVBoxLayout(tab3_content)
        
        # Add the average metrics table and narrative label to the content layout
        tab3_content_layout.addWidget(self.average_metrics_table)  # Add the average metrics table to Tab 3 layout
        tab3_content_layout.addWidget(self.narrative_label)  # Add the narrative label to Tab 3 layout
        
        # Set the scroll area widget
        self.tab3_scroll_area.setWidget(tab3_content)
        tab3_layout.addWidget(self.tab3_scroll_area)  # Add the scroll area to Tab 3 layout

        # Set the layout for Tab 3
        tab3_widget = QWidget()
        tab3_widget.setLayout(tab3_layout)
        self.tabs.addTab(tab3_widget, "Average Metrics")  # Add Tab 3 to the tab widget

        back_button.setFixedWidth(100)
        output_layout.addWidget(back_button)
        output_layout.addWidget(self.tabs)  

        output_widget = QWidget()
        output_widget.setLayout(output_layout)
        return output_widget

    def show_input_selection(self):
        # Switch to the input selection section
        self.stacked_widget.setCurrentWidget(self.input_selection_widget)

    def read_graph_from_files(self):
        nodes_filename = self.coord_input.text()
        edges_filename = self.graph_input.text()

        if not nodes_filename or not edges_filename:
            QMessageBox.warning(self, "Input Error", "Please provide both graph and coordinates file paths.")
            return

        graph_dict, travel_times, self.pos = read_graph_from_files(nodes_filename, edges_filename)  # Unpack all three values
        self.graph = Graph(graph_dict, travel_times, self.pos)  # Create an instance of Graph with travel_times
        print("Graph and positions loaded successfully.")
    
    def process_k_shortest_paths(self):
        # Read the graph data first
        self.read_graph_from_files()  # Ensure the graph is loaded before proceeding

        # Get the start, end nodes, and k value
        start_node = self.start_node_input.currentText()  # Use currentText() instead of text()
        end_node = self.end_node_input.currentText()      # Use currentText() instead of text()
        
        # Check if k value is a valid number
        if not self.k_value_input.currentText().isdigit():  # Use currentText() instead of text()
            QMessageBox.warning(self, "Input Error", "Please enter a valid number for K.")
            return  # Exit the method if k is invalid
        
        k = int(self.k_value_input.currentText())  # Convert k to an integer

        # Check if the graph has been loaded
        if self.graph is None:
            QMessageBox.warning(self, "Input Error", "Graph data has not been loaded. Please load the graph first.")
            return  # Exit the method if the graph is not loaded

        # Validate nodes
        if start_node not in self.graph.nodes or end_node not in self.graph.nodes:
            QMessageBox.warning(self, "Input Error", "Please provide valid start and end nodes that exist in the graph.")
            return  # Exit the method if nodes are invalid

        # Switch to the output widget after validating inputs
        self.stacked_widget.setCurrentWidget(self.output_widget)  # Assuming output_widget is your output section

        print("Processing K-Shortest Paths...")  # Debugging line

        # Call the k_shortest_paths function
        if start_node and end_node:
            paths, paths_with_costs = k_shortest_paths(self.graph, start_node, end_node, k, self.pos)  # Now returns both
            
            # Determine the background image based on the loaded graph
            background_image = "Resources/moa-bg.png" if "moa" in self.graph_input.text() else "Resources/araneta-bg.png"
            
            # Pass the necessary variables including the background image
            self.display_paths(paths, start_node, end_node, paths_with_costs, background_image)  
            
            # Call the diversity metrics function and display results
            self.display_diversity_metrics(paths)  # Existing method to display diversity metrics
            self.display_average_metrics(paths)  # New method to display average metrics

    def display_paths(self, paths, start_node, end_node, paths_with_costs, background_image):
        # Clear previous output
        for i in reversed(range(self.scroll_area_layout.count())): 
            widget = self.scroll_area_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()  # Remove previous output widgets

        # Get the number of paths requested
        requested_paths_count = int(self.k_value_input.currentText()) if self.k_value_input.currentText().isdigit() else 1

        if paths:
            for i, path in enumerate(paths):
                # Initialize cumulative values
                cumulative_weight = 0
                cumulative_travel_time = 0

                # Create a new widget to hold the path text and graph
                output_widget = QWidget()
                output_layout = QVBoxLayout(output_widget)
                self.scroll_area_layout.addWidget(output_widget)

                # Create a table for segment details
                segment_table = QTableWidget()
                segment_table.setColumnCount(5)
                segment_table.setHorizontalHeaderLabels(["Segment", "Weight (Distance)", "Cumulative Weight", "Travel Time", "Cumulative Travel Time"])
                segment_table.setRowCount(len(path) - 1)  # Number of segments is one less than the number of nodes
                segment_table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Set to read-only

                # Fill the table with segment details
                for j in range(len(path) - 1):
                    segment = f"{path[j]} to {path[j + 1]}"
                    weight = self.graph.edges[path[j]][path[j + 1]]
                    travel_time = self.graph.travel_times[path[j]][path[j + 1]]

                    # Update cumulative values
                    cumulative_weight += weight
                    cumulative_travel_time += travel_time

                    # Insert data into the table
                    segment_table.setItem(j, 0, QTableWidgetItem(segment))
                    segment_table.setItem(j, 1, QTableWidgetItem(f"{weight} meters"))
                    segment_table.setItem(j, 2, QTableWidgetItem(f"{cumulative_weight} meters"))
                    segment_table.setItem(j, 3, QTableWidgetItem(f"{travel_time:.2f} seconds"))
                    segment_table.setItem(j, 4, QTableWidgetItem(f"{cumulative_travel_time:.2f} seconds"))

                # Set the table to resize to fit the content
                segment_table.resizeColumnsToContents()
                segment_table.resizeRowsToContents()

                # Disable scrollbars
                segment_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                segment_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                
                # Adjust the table to fit its contents fully
                buffer_width = 15  # Set a smaller buffer width to extend the table size
                segment_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
                segment_table.setFixedSize(
                    segment_table.horizontalHeader().length() + segment_table.verticalHeader().width() + buffer_width,
                    segment_table.verticalHeader().length() + segment_table.horizontalHeader().height()
                )

                # Create the path text label before the table
                path_text = QTextEdit(f"Path {i + 1}: {' ➜ '.join(path)} <br>(Distance: {cumulative_weight} meters, Travel Time: {cumulative_travel_time:.2f} seconds)")
                path_text.setStyleSheet("font-size: 16px; margin-bottom: 10px;")
                path_text.setReadOnly(True)  # Make it read-only to prevent editing
                output_layout.addWidget(path_text)  # Add the path text label to the output layout

                # Add the segment table to the output layout
                output_layout.addWidget(segment_table)

                # Draw the graph and get the figure
                fig = draw_graph_with_path(self.graph, path, i + 1, self.pos, start_node, end_node, cumulative_weight, background_image)
                canvas = FigureCanvas(fig)
                canvas.setFixedSize(1000, 600)  # Set a fixed size for the canvas to prevent squeezing
                output_layout.addWidget(canvas, alignment=Qt.AlignCenter)

            # Check if the number of produced paths is less than requested
            if len(paths) < requested_paths_count:
                no_more_paths_label = QLabel(f"No more paths found. Only {len(paths)} path(s) produced.")
                no_more_paths_label.setStyleSheet("font-size: 16px; margin-top: 10px;")
                self.scroll_area_layout.addWidget(no_more_paths_label)  # Add the message to the layout
        else:
            no_paths_label = QLabel("No paths found.")
            no_paths_label.setStyleSheet("font-size: 16px;")
            self.scroll_area_layout.addWidget(no_paths_label)

    def display_diversity_metrics(self, paths):
        # Clear previous table data
        self.diversity_table.setRowCount(0)

        # Capture the output of the test_diversity_metrics function
        results = test_diversity_metrics(paths, self.graph)

        # Only display the pairwise comparisons, excluding the averages
        for result in results:
            # Check if the result is an average
            if "Averages" in result[0]:
                continue

            # Unpack the result tuple (now includes detour factor)
            path_comparison, cd, po, tt_ab, df = result  # Added df to unpacking
            row_position = self.diversity_table.rowCount()
            self.diversity_table.insertRow(row_position)
            self.diversity_table.setItem(row_position, 0, QTableWidgetItem(path_comparison))
            self.diversity_table.setItem(row_position, 1, QTableWidgetItem(f"{cd:.2f}%"))
            self.diversity_table.setItem(row_position, 2, QTableWidgetItem(f"{tt_ab:.2f}%"))
            self.diversity_table.setItem(row_position, 3, QTableWidgetItem(f"{df:.2f}%"))
            self.diversity_table.setItem(row_position, 4, QTableWidgetItem(f"{po:.2f}%"))  # Rearranged order

        self.diversity_table.setStyleSheet("font-size: 18px;")

    def display_average_metrics(self, paths):
        # Clear previous table data
        self.average_metrics_table.setRowCount(0)
        
        # Capture the output of the test_diversity_metrics function
        results = test_diversity_metrics(paths, self.graph)

        # Define thresholds
        distance_threshold = 20
        overlap_threshold_high = 70
        overlap_threshold_low = 30
        travel_time_threshold = 15
        detour_threshold = 1.50  # New threshold for detour factor (50% longer than original)

        # Prepare narrative
        narrative_text = ""

        # Extract average metrics for each path
        for result in results:
            if "Averages" in result[0]:
                path_label, avg_cd, avg_po, avg_tt_ab, avg_df = result  # Added avg_df to unpacking
                row_position = self.average_metrics_table.rowCount()
                self.average_metrics_table.insertRow(row_position)
                self.average_metrics_table.setItem(row_position, 0, QTableWidgetItem(path_label))
                self.average_metrics_table.setItem(row_position, 1, QTableWidgetItem(f"{avg_cd:.2f}%"))
                self.average_metrics_table.setItem(row_position, 2, QTableWidgetItem(f"{avg_tt_ab:.2f}%"))
                self.average_metrics_table.setItem(row_position, 3, QTableWidgetItem(f"{avg_df:.2f}%"))
                self.average_metrics_table.setItem(row_position, 4, QTableWidgetItem(f"{avg_po:.2f}%"))  # Rearranged order

                # Add to narrative based on thresholds
                narrative_text += f"<br><b>**{path_label}**:</b><br>"

                # Evaluate cost difference
                if avg_cd >= distance_threshold:
                    narrative_text += f"- The absolute difference in distance is <b>{avg_cd:.2f}%</b>, indicating significant variation among paths.<br>"
                else:
                    narrative_text += f"- The absolute difference in distance is <b>{avg_cd:.2f}%</b>, suggesting paths are relatively similar in distance.<br>"

                # Evaluate path overlap
                if avg_po >= overlap_threshold_high:
                    narrative_text += f"- The path overlap is <b>{avg_po:.2f}%</b>, indicating that the paths are very similar and may not provide diverse routing options.<br>"
                elif avg_po <= overlap_threshold_low:
                    narrative_text += f"- The path overlap is <b>{avg_po:.2f}%</b>, indicating a high level of diversity among the paths, which can enhance navigation options.<br>"
                else:
                    narrative_text += f"- The path overlap is <b>{avg_po:.2f}%</b>, suggesting moderate similarity among the paths, which may limit diversity.<br>"

                # Evaluate travel time difference
                if avg_tt_ab >= travel_time_threshold:
                    narrative_text += f"- The travel time difference is <b>{avg_tt_ab:.2f}%</b>, suggesting that some paths may take significantly longer than others.<br>"
                else:
                    narrative_text += f"- The travel time difference is <b>{avg_tt_ab:.2f}%</b>, indicating that the paths are relatively consistent in travel time.<br>"

                # Add detour factor analysis to narrative
                narrative_text += f"- The detour factor is <b>{avg_df:.2f}%</b>, "
                if avg_df >= detour_threshold:
                    narrative_text += "indicating that alternative paths are significantly longer than the main path.<br>"
                else:
                    narrative_text += "suggesting that alternative paths maintain reasonable lengths compared to the main path.<br>"

        # Update narrative label text
        self.narrative_label.setText(narrative_text)
        self.average_metrics_table.setStyleSheet("font-size: 18px;")

    def show_legend(self, title, content):
        """Show a legend in a pop-up window."""
        QMessageBox.information(self, title, content, QMessageBox.Ok)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
