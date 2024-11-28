# Firefly Assignment (Eitan Paran)

### _requirements_
- python 3.12
- pip3
- docker

### Installation
- Clone the repo to a folder on your machine
- Navigate to the root folder (/firefly_assignment)
- run the requirements.txt file
  ```sh
  pip3 install -r requirements.txt
  ```

### Installing Allure and running allure service (For reporting)

- Pull allure service docker container from docker hub: https://hub.docker.com/r/frankescobar/allure-docker-service/
- run the container: 
  ```sh
  docker run -p 5050:5050 -e CHECK_RESULTS_EVERY_SECONDS=3 -e KEEP_HISTORY=1 \
                 -v ${PWD}/allure-results:/app/allure-results \
                 -v ${PWD}/allure-reports:/app/default-reports \
                 frankescobar/allure-docker-service
  ```

### Running the tests

- Make sure you are running the tests from the project's root directory (/firefly_assignment)
- execute the following pytest command to run all suites:
  ```sh
  pytest -vs tests/sanity/tests_sanity.py tests/stress/tests_stress.py --alluredir=tests/allure-results
  ```
- When the run completes you will see on the console a link to the report, click it


### Tests Plan
> Note 1: `The following is a list of tests to be implemented for testing the feature (There could be many more, but this is a list representing a good place to start`
> Note 2: `I've implemented some of them but implementing the rest is more of the same, technically wise, so i assumed the 2 suites and the infrastructure i've implemented will be enough for the home assignment`.

A. Sanity - Integrations:
- 1. Create Integration
- 2. Delete Integration
- 3. Update Integration
- 4. Get Integration
- 5. Get All Integrations

B. Sanity - Assets:
- 1. Create Asset
- 2. Delete Asset
- 3. Update Asset
- 4. List Assets by integration id
- 5. Get Asset By Id


C. Sanity - Negative Usage:

- 1. Validate for deleting integrations - all assets are deleted as well
- 2.  Try to create an asset with empty integration_id / description / name
- 3. Try to create an integration with empty name / type
- 4. Try to list asset without specifying integration id / specifying invalid integration_id
- 5. Try to update asset without specifying integration_id / name / description
- 6. Try to get asset with invalid asset id
- 7. Try to delete a non existing asset / invalid asset_id / empty asset_id
- 8. Try to update an integration and send invalid integration id / send empty name / send the same existing name
- 9. Try to create integration with empty name / type
- 10. Try to get integration and send empty integration_id / invalid integration_id
- 11. Try to delete integration and send empty / invalid integration_id


D. Functional:

- 1. Try to create 2 assets with the same name under the same integration and under 2 separated integration
- 2. Try to create 2 integrations with the same name under the same tenant and under different tenants
- 3. Try to create an asset in integration which exist on tenant1 but while you are logged to tenant2
- 4. Try to create an integration on tenant1 while you are logged to tenant2
- 5. Try to update an integration to have the same name as other integration
- 6. Try to update an asset to have the same name as other asset
- 7. Delete an integration from one tenant and recreate it on the other tenant
- 8. Delete an asset from one integration and recreate it on another integration
- 9. Delete an asset from one integration on one tenant and recreate it on another tenant
- 10. Integrations segregations (Create asset on each tenant, make sure assets are attached to corresponding - tenants)
- 11. Tenants segregation (Create Integration with assets on each tenant, make sure tenants are segregated)
- 12. Tenants segregations: try to update an asset from tenant1 on tenant2
- 13. Tenants segregation: try to update integration from tenant1 on tenant 2


D. Stress:

- 1. Execute 1000 parallel get calls and validate it is not exceeding a 1 minute timeout
- 2. Execute 1000 parallel post calls and validate it is not exceeding a 1 minute timeout
- 3. Execute 1000 parallel put calls and validate it is not exceeding a 1 minute timeout
- 4. Execute 1000 parallel delete calls and validate it is not exceeding a 1 minute timeout
- 5. Execute 1000 parallel patch calls and validate it is not exceeding a 1 minute timeout
- 6. reach system overload by incrementally adding all possible elements. check overload point is meeting the KPIs

E. Performance:

- 1. Measure time for executing get command, make sure it meets KPIs
- 2. Measure time for executing post command, make sure it meets KPIs
- 3. Measure time for executing put command, make sure it meets KPIs
- 4. Measure time for executing delete command, make sure it meets KPIs
- 5. Measure time for executing patch command, make sure it meets KPIs
- 6. Measure Performance during load. In the background run high load on the system, and measure each rest time 

F. Endurance:

- 1. Reach critical point by overloading the system, then reduce 10%, run load in background for 5 hours. check stability
- 2. Load the system with repeating calls (write and delete), reach ~90% load. run for 5 hours, check stability

G. Peak:

- 1. iterate with load to find critical point. the repeatedly shock the system with critical point for N times.check stability
