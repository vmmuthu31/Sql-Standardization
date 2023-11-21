## Problem Statement:
- Consider there’s 1 table which contains 8 columns.

### Input Table:
Out of 8, I want 2 columns to perform standardisation.

### Output Table:
- We should have 10 columns, 2 columns with standardised value <br/> 
Ex: <br/>
Degree Column <br/>
B. Sc <br/>
B.Sc <br/>
Bachelor of Science <br/>
Bachelor of science <br/>
Bachelor of Science. <br/>
<br/>
All these values are corresponding to same value, which is Bachelor of Science<br/>

Now to over come this, we should create a mapping table which contains old entries and standardise entires which should look for the standardize data. <br/> 

Overall we should use 3 tables <br/>

Input table <br/>
Lookup table (2 table) <br/>
Output table <br/>

## Database Schema

The project utilizes three main tables:

1. **`input_table`**: Contains original data with multiple columns, including those that require standardization.
2. **`lookup_table`**: Stores the mapping from non-standard to standard values for specific columns.
3. **`output_table`**: Holds the standardized data along with the original data from the `input_table`.

## SQL Queries

### 1. Creating Tables

#### `input_table`

```sql
CREATE TABLE input_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    degree VARCHAR(255),
    field_of_study VARCHAR(255),
    -- Additional columns as required
);
```

#### `lookup_table`

```sql
CREATE TABLE lookup_table (
    original_value VARCHAR(255),
    standardized_value VARCHAR(255),
    column_name VARCHAR(255)
);
```

#### `output_table`

Initially created as a clone of the `input_table` with additional columns for standardized data.

```sql
CREATE TABLE IF NOT EXISTS output_table LIKE input_table;
ALTER TABLE output_table
ADD COLUMN standardized_degree VARCHAR(255),
ADD COLUMN standardized_field_of_study VARCHAR(255);
```

### 2. Populating `lookup_table`

Insert mappings for standardization.

```sql
INSERT INTO lookup_table (original_value, standardized_value, column_name) VALUES
('B. Sc', 'Bachelor of Science', 'degree'),
('B.Sc', 'Bachelor of Science', 'degree'),
-- Additional mappings as required
```

### 3. Data Copy and Standardization

Copy data from `input_table` to `output_table` and update with standardized values.

```sql
INSERT INTO output_table (id, degree, field_of_study /*, other columns*/)
SELECT id, degree, field_of_study /*, other columns*/ FROM input_table;

UPDATE output_table ot
INNER JOIN lookup_table lt ON ot.degree = lt.original_value AND lt.column_name = 'degree'
SET ot.standardized_degree = lt.standardized_value;

UPDATE output_table ot
INNER JOIN lookup_table lt ON ot.field_of_study = lt.original_value AND lt.column_name = 'field_of_study'
SET ot.standardized_field_of_study = lt.standardized_value;
```

## Usage Guidelines

- Ensure that the MySQL server is running before executing these queries.
- Use a database management tool like phpMyAdmin or MySQL Workbench for query execution.
- Backup your database before running these scripts in a production environment.

## Notes

- Modify the column names and types as per your actual data requirements.
- The `lookup_table` should be regularly updated with new mappings as needed.

