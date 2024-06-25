# PhonePe Pulse Data Visualization and Exploration

This repository contains a Streamlit application for visualizing and exploring PhonePe Pulse data. The app connects to a MySQL database to fetch data on transactions and users, and displays interactive visualizations to provide .

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Data Schema](#data-schema)
- [Features](#features)
- [Visualizations](#visualizations)
- [Insights](#insights)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your_username/phonepe_pulse_viz.git
    cd phonepe_pulse_viz
    ```

2. Set up a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Ensure that you have a MySQL database set up with the required schema. Update the database connection details in the script if necessary.

## Usage

1. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

2. Open your web browser and navigate to `http://localhost:8501` to access the app.

## Data Schema

The app uses data from six tables in the `phonepay_db` database:

1. `aggregated_transaction`
   - Columns: State, Year, Quarter, Transaction_type, Transaction_count, Transaction_amount

2. `aggregated_user`
   - Columns: State, Year, Quarter, Brand, Transaction_count, Percentage

3. `map_transaction`
   - Columns: State, Year, Quarter, District, Transaction_count, Transaction_amount

4. `map_user`
   - Columns: State, Year, Quarter, District, Registered_user, App_open

5. `top_transaction`
   - Columns: State, Year, Quarter, Entity_name, Transaction_count, Transaction_amount

6. `top_user`
   - Columns: State, Year, Quarter, District, Registered_user

## Features

- **Dataset Selection:** Users can select different datasets to explore, including aggregated transactions, aggregated users, map transactions, map users, top transactions, and top users.
- **Filtering:** Data can be filtered by year and quarter.
- **Visualization:** Interactive choropleth maps and bar charts to visualize the data.

## Visualizations

### Tab 1: Visualization

- **Aggregated Transactions:** Displays a choropleth map showing transaction amounts by state, along with top states and transaction categories.
- **Aggregated Users:** Shows the total registered users by state and top brands.
- **Map Transactions:** Visualizes transaction amounts and counts by district.
- **Map Users:** Displays registered users and app opens by district.
- **Top Transactions:** Shows top entities by transaction count and amount.
- **Top Users:** Displays top states and districts by registered users.

### Tab 2: Insights

1. **Increase in Merchant Payments:** Bar chart showing the total merchant payments by year.
2. **Growth in P2P Transactions:** Line chart showing the growth in peer-to-peer transactions by year.
3. **High Transaction Volume in Metropolitan Areas:** Bar chart showing the top 10 states by transaction count.
4. **Most Popular States for Digital Transactions:** Bar chart showing the top states for digital transactions for a selected year.
5. **Significant Increase in Registered Users:** Line chart showing the increase in registered users by year.
6. **Top Brands by Transaction Count:** Bar chart showing the top brands by transaction count.
7. **Transaction Trends by Quarter:** Line chart showing transaction trends by quarter.
8. **Increase in App Opens:** Line chart showing the increase in app opens by year.
9. **Top Entities by Transaction Amount:** Bar chart showing the top entities by transaction amount.
10. **Yearly Transaction Comparison:** Line chart showing yearly transaction comparison.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have any suggestions or improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
