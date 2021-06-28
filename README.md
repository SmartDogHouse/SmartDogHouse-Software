# SmartDogHouse-Software

CodeFactor: [![CodeFactor](https://www.codefactor.io/repository/github/smartdoghouse/smartdoghouse-software/badge)](https://www.codefactor.io/repository/github/smartdoghouse/smartdoghouse-software)

Codacy: [![Codacy Badge](https://app.codacy.com/project/badge/Grade/2b0b479212d047058a885b6f4ee8602e)](https://www.codacy.com/gh/SmartDogHouse/SmartDogHouse-Software/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=SmartDogHouse/SmartDogHouse-Software&amp;utm_campaign=Badge_Grade)

SonarCloud: [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=SmartDogHouse_SmartDogHouse-Software&metric=alert_status)](https://sonarcloud.io/dashboard?id=SmartDogHouse_SmartDogHouse-Software)

## Run Tests
inside project folder <br> 
### without coverage
```bash
python -m src.test.python.test_water_sensor #single test
```
```bash
python -m unittest discover -s ./src/test/ #all tests
```
### with coverage
```bash
pip install coverage
```
all tests:
```bash
coverage run -m unittest discover -s ./src/test/
```
create report:
```bash
coverage report #report in shell
coverage html #report website, open index.html in htmlcov folder
```
