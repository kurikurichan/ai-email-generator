import csv

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from ..utils.generate_texts import final_email

router = APIRouter()


@router.get("/api/emails")
def get_emails():
    """
    Reads data from a CSV file containing information about individuals. 
    Constructs an email message based on the individual's information. 

    Args:
        None

    Returns:
        JSON List of dictionaries: Containing csv data and formatted email data


    Raises:
        HTTPException: If an error occurs during data retrieval or the CSV
                       file is empty, a 500 status code error is returned.
    """

    # load csv file
    csv_file_path = 'api/csvs/leads.csv'
    # Initialize an empty list to store the data for a NEW csv file
    data = []
    # Save length of data titles to make sure we only send the data
    # if we actually received data
    original_row_length = len(data)
    # Reading from CSV file
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        # Iterate over each row in the CSV file
        row_index = 0
        for row in csv_reader:
            row_index += 1
            # give each item in the row variable names
            name, job_role, email, company = row[:4]
            # add the "Message" header to 1st row since it wasn't in the original csv
            if row_index == 1:
                message = "Message"
            # else, the row is not headers and we can calculate the row's email message
            else:
                message = final_email(company, name, job_role)

            # Constructing a dictionary for this row's data
            row_data = {
                "name": name,
                "jobRole": job_role,
                "email": email,
                "company": company,
                "message": message
            }
            # add this dictionary to the data to return later
            data.append(row_data)
    # confirm there is new data before sending to the front end as JSON
    if len(data) > original_row_length:
        return JSONResponse(content=data, status_code=status.HTTP_200_OK)
    # if no new data then send back a 500 status code error
    else:
        raise HTTPException(
            status_code=500, detail="An error occurred when generating your request or the CSV file is empty.")
