# M604 Data Visualization Dashboard

Social welfare states such as Deutschland pride upon their ability to service its people and continuously strive to uplift its people and community. A renowned presence not only in the European Union, but also across the world in providing extra-ordinary measures in the benefits, amenities and opportunities for all people regardless of ethnicity, age, religion or gender. However, even in the defined age of AI, data-driven decision making and data-reach on a global scale, majority of public records and performances are hidden from the public while it’s disclosure is at the discretion of news agencies, political campaigns and global event of scale.

Social Benefits are critical component of Germany’s welfare system portfolio. The overall Welfare system portfolio was approximately 33.6% of the GDP - it is then an area where multiple opportunities may arise that optimizes the social subsidy that the country offers and further areas can also benefit from the reduce contribution towards social benefits. 

### 🌍 GENESIS - Online Datenbank
The Genesis-online datenbank is the public repository for reports of public sector performance across all spheres. however as all data is defined within table views, it does not provide a more accurate representation of the process. Therefore, a web-based GUI was developed using the [STREAMLIT](https://streamlit.io/) library.

### 🚀 [HEAD DIRECTLY THERE!](https://social-benefits.streamlit.app/)

##### Or follow the link:
https://social-benefits.streamlit.app/

### Application Instructions

##### Python Version
```python
python 3.12.3
```
##### Clone Repository

```bash
git clone https://github.com/SHA-15/M602-Carbon-Footprint-Monitoring-Tool.git
```

##### Create python Virtual Environment

Firstly Navigate to the root directory of the project, then:
```bash
python3 venv venv
```
##### Activate the Virtual Environment
```bash
source venv/bin/activate
```

##### Install dependencies using requirements.txt
```bash
pip install -r requirements.txt
```

##### Run using the Terminal, while in the project root directory
```bash
streamlit run main.py
```

## UNIT TESTING
To perform unit tests on the program found in `unittests` directory enter the following command:
```bash
python -m unittest discover -s unittests -p "my_test_*.py" -v
```