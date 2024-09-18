import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset from your local machine
file_path = r'C:\Users\IoannisZografakis-Re\Downloads\10-employees.csv'
employees_df = pd.read_csv(file_path)

# Step 1: Filter the Data
filtered_df = employees_df[
    (employees_df['PerformanceScore'].isin(['Exceeds', 'Fully Meets'])) &
    (employees_df['EmpStatusID'] == 1) &
    (employees_df['Salary'] > 60000) &
    (employees_df['EmpSatisfaction'] >= 4)
]

# Selecting specific columns
filtered_df = filtered_df[[
    'Employee_Name', 'EmpID', 'GenderID', 'Department', 'Salary',
    'PerformanceScore', 'EmpSatisfaction', 'EmpStatusID', 'Absences'
]]

# Step 2: Specify a valid output path on your system
output_file_path = r'C:\Users\IoannisZografakis-Re\Documents\filtered_employees.csv'

# Exporting the filtered data to CSV
filtered_df.to_csv(output_file_path, index=False)

# Step 3: Group and Aggregate by Department
department_group = filtered_df.groupby('Department').agg(
    mean_salary=pd.NamedAgg(column='Salary', aggfunc='mean'),
    mean_satisfaction=pd.NamedAgg(column='EmpSatisfaction', aggfunc='mean')
).reset_index()

# Step 4: Create Bar Chart and Line Plot with Dual Y-Axis
fig, ax1 = plt.subplots(figsize=(10, 6))

# Bar chart with different colors for each bar
colors = plt.get_cmap('tab10')(range(len(department_group)))
ax1.bar(department_group['Department'], department_group['mean_salary'], color=colors, label='Mean Salary')
ax1.set_xlabel('Department')
ax1.set_ylabel('Average Salary', color='skyblue')
ax1.tick_params(axis='y', labelcolor='skyblue')

# Line plot for satisfaction with dual axis
ax2 = ax1.twinx()
ax2.plot(department_group['Department'], department_group['mean_satisfaction'], color='green', marker='o', label='Mean Satisfaction')
ax2.set_ylabel('Average Satisfaction', color='green')
ax2.tick_params(axis='y', labelcolor='green')

# Adding title and legends
plt.title('Average Salary and Satisfaction by Department')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Step 5: Department Distribution and Salary Statistics
department_distribution = filtered_df['Department'].value_counts()

# Salary statistics by department
salary_stats = filtered_df.groupby('Department')['Salary'].describe()

# Display salary statistics (this part might not work without a custom viewer, so you can print it instead)
print(salary_stats)

# Pie chart for department distribution with unique colors
plt.figure(figsize=(8, 8))

colors = plt.get_cmap('tab20')(range(len(department_distribution)))
plt.pie(department_distribution, labels=department_distribution.index, autopct='%1.1f%%', colors=colors, startangle=90)
plt.title('Distribution of Employees Across Departments')
plt.show()

# Step 6: Group by Performance Score and Calculate Average Absences
performance_group = filtered_df.groupby('PerformanceScore').agg(
    mean_absences=pd.NamedAgg(column='Absences', aggfunc='mean')
).reset_index()

# Bar chart for average absences with different colors for each bar
plt.figure(figsize=(8, 6))
colors = sns.color_palette('viridis', len(performance_group))
sns.barplot(x='PerformanceScore', y='mean_absences', data=performance_group, palette=colors)

# Customizing the chart
plt.title('Average Number of Absences by Performance Score')
plt.xlabel('Performance Score')
plt.ylabel('Average Number of Absences')

# Remove legend for a cleaner look
plt.show()
