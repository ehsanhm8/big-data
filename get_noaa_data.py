from google.cloud import bigquery
from google.oauth2 import service_account

key_path = "service-account-key.json"  # Your uploaded file name
credentials = service_account.Credentials.from_service_account_file(
    key_path,
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

client = bigquery.Client(credentials=credentials, project=credentials.project_id)

def get_county_events():
    query = """
    SELECT
        EXTRACT(YEAR FROM event_begin_time) as year,
        state,
        state_fips_code,
        cz_fips_code,
        cz_name as county,
        event_type,
        COUNT(event_id) as event_count
    FROM
        `bigquery-public-data.noaa_historic_severe_storms.storms_*`
    GROUP BY
        year, state, state_fips_code, cz_fips_code, county, event_type
    ORDER BY
        year, state, county, event_type
    """
    df = client.query(query).to_dataframe()
    df.to_csv('county_events.csv', index=False)
    return df

events_df = get_county_events()
print(events_df.head())
