# 🗄️ MySQL CLI & Dynamic CSV Ingestion Tool

A custom Command-Line Interface (CLI) application built in Python to interactively manage MySQL databases. This tool goes beyond basic CRUD operations by offering dynamic CSV data ingestion, automated schema generation with on-the-fly data type deduction, and safe SQL transaction management.

## 🚀 Key Features

* **Intelligent Data Ingestion (`timport`):** Parses raw CSV files and dynamically generates `CREATE TABLE` queries by deducing the optimal SQL data types (`INT`, `FLOAT`, `VARCHAR`) from the dataset's first row.
* **Standard Ingestion (`import`):** Quickly creates tables with default `VARCHAR(100)` types for rapid prototyping and imports all CSV records.
* **Metadata Exploration:** Directly queries the `information_schema` to search for specific tables based on column names or data types.
* **Transaction-Based Cleanup (`drop all`):** Safely drops all tables within the current database using batched SQL transactions and rollback mechanisms.
* **Interactive CLI Shell:** Provides a continuous loop shell to execute commands, read data, and inspect table structures.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Database:** MySQL
* **Dependencies:** `mysql-connector-python`

## 📁 Project Structure

Ensure your directory is structured as follows before running the tool:

```text
├── db2026_project1.py     # Main CLI application script
├── README.md              # Project documentation
└── csv_files/             # Directory containing raw data files
    ├── hospital.csv
    ├── professor.csv
    └── fruits.csv
```
## ⚙️ Setup & Installation

1. Clone this repository.
2. Install the required Python MySQL connector:
   ```bash
   pip install mysql-connector-python
   ```
3. Update the database connection credentials (host, user, password, database) in the `db2026_project1.py` file to match your local MySQL server.
4. Run the script:
   ```bash
   python db2026_project1.py
   ```

## 💻 Available Commands

Once the CLI is running (indicated by the `>` prompt), you can use the following commands:

| Command | Description |
| :--- | :--- |
| `show tables` | Lists all tables currently existing in the database. |
| `desc <table_name>` | Displays the schema (column names and data types) of a specific table. |
| `read <table_name>` | Fetches and displays all records from a specific table. |
| `import <file_path> <table_name>` | Creates a table using `VARCHAR(100)` for all columns and imports data from the specified CSV file. |
| `timport <file_path> <table_name>` | **[Advanced]** Deduces data types (`INT`, `FLOAT`, `VARCHAR`) from the CSV content, creates the optimized table, and imports the data. |
| `drop all` | Safely executes a transaction to drop all tables in the database. |
| `find tables column=<name>` | Searches the `information_schema` for all tables containing a specific column name. |
| `find tables col_type=<type>` | Searches the `information_schema` for all tables containing a specific data type (e.g., `INT`, `FLOAT`, `VARCHAR`). |
| `exit` | Closes the database connection and exits the CLI. |

## 📸 Demonstration

*(Showcasing the intelligent type deduction and schema generation)*

**1. Creating a table with type guessing (`timport`):**
> ![timport command](Captured_results\2_professor_timport.png) 


**2. Searching tables by data type:**
> ![find tables command](Captured_results\5_find_tables_col_type.png)

**3. Safely dropping all tables:**
> ![drop all command](Captured_results\6_final_drop_and_show.png)