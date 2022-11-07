# Pssp

    Errors:

- ran into an error when trying to deploy via GCP received:

  - **  **File "app.py", line 17, in `<module>`

  **    **app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://' + GCP_MYSQL_USER+ ':' + GCP_MYSQL_PASSWORD + '@' + GCP_MYSQL_HOSTNAME + ':3306/patient_portal'

  TypeError: must be str, not NoneType
