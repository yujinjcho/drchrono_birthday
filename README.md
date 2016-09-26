# Birthday Reminder
Tool for reminding doctors of upcoming patient birthdays and contact information using drchrono's API

Collects patient data and finds patients who have upcoming birthdays (60 days) or whose birthdays have recently passed (14 days). 

When a greeting is sent via phone or email (not supported currently), the doctor can signify that a greeting has been sent. This greeting will be saved in the database and will show which patient received a greeting. Signifiers are based on recency so will be reset when the patients' birthdays come around next year.

![alt tag](http://i.imgur.com/SAGSViU.png)

# Patient Kiosk
Digital solution to replace pen/paper check-in process for doctor visits.
Leverages drchrono API to search for patients and appointment information.
Existing patient information is prefilled and can be updated by patients.
Allergies can also be updated or added.

# Config
Create `drchrono_config.py` in birthday\reminder folder. 

```
CLIENT_ID = 'CLIENT_ID'
CLIENT_SECRET = 'CLIENT_SECRET'
REDIRECT_URI = 'REDIRECT_URI'
```

Database configurations are also required in the project's `settings.py`.


