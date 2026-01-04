import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

conn = snowflake.connector.connect(
    user=os.getenv('SNOWFLAKE_USER'),
    password=os.getenv('SNOWFLAKE_PASSWORD'),
    account=os.getenv('SNOWFLAKE_ACCOUNT'),
    warehouse='FINANCE_WH',
    database='FINANCE_DB',
    schema='RAW',
    role='ACCOUNTADMIN'
)

query = "SELECT * FROM FINANCE_DB.RAW.FCT_CUSTOMER_BEHAVIOR"
df = pd.read_sql(query, conn)
df.columns = [col.upper() for col in df.columns]

features = ['TOTAL_ORDERS', 'TOTAL_SPENT', 'AVG_SPENT']
X = df[features]
y = df['TARGET_CHURN']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = LogisticRegression(class_weight='balanced', random_state=42)
model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)
print(f"Logistic Regression Accuracy: {accuracy_score(y_test, y_pred):.2f}")
print(classification_report(y_test, y_pred))

results_df = X_test.copy()
results_df['ACTUAL_CHURN'] = y_test.values
results_df['PREDICTED_CHURN'] = y_pred
results_df['PREDICTION_DATE'] = datetime.now()
results_df.columns = [col.upper() for col in results_df.columns]

try:
    success, nchunks, nrows, _ = write_pandas(
        conn=conn,
        df=results_df,
        table_name='CHURN_PREDICTIONS',
        database='FINANCE_DB',
        schema='RAW',
        auto_create_table=True,
        overwrite=True
    )
    if success:
        print(f"Successfully uploaded {nrows} rows to CHURN_PREDICTIONS table in Snowflake!")
except Exception as e:
    print(f"Error while uploading to Snowflake: {e}")

conn.close()