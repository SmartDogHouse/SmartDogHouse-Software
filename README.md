# SmartDogHouse-Software

### Run Tests
inside project folder <br> 
#### without coverage
```bash
python -m src.test.python.test_water_sensor #single test
```
```bash
python -m unittest discover -s ./src/test/ #all tests
```
#### with coverage:
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
